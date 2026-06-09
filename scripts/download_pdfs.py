#!/usr/bin/env python3
"""
Multi-source PDF downloader for the Agent Survey Pipeline.

Downloads PDFs for a list of references using a priority cascade:
arXiv → PubMed Central → Open Access → Semantic Scholar → Web Search

Usage:
    python download_pdfs.py --input references.json --output-dir _pdfs/ --mailto user@example.com
"""

import argparse
import json
import os
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional


def sanitize_filename(name: str, max_len: int = 80) -> str:
    """Create a safe filename from a paper reference."""
    name = name.lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'\s+', '_', name)
    name = name[:max_len]
    return name or "unnamed"


def is_safe_url(url: str) -> bool:
    """Check if a URL is safe for downloading."""
    if not url:
        return False
    if not url.startswith(("http://", "https://")):
        return False
    # Block private IPs
    for prefix in ["10.", "172.16.", "172.17.", "172.18.", "172.19.",
                    "172.20.", "172.21.", "172.22.", "172.23.", "172.24.",
                    "172.25.", "172.26.", "172.27.", "172.28.", "172.29.",
                    "172.30.", "172.31.", "192.168.", "127.", "localhost"]:
        if prefix in url:
            return False
    return True


def download_file(url: str, output_path: str, timeout: int = 30) -> bool:
    """Download a file from URL, verify it's a PDF."""
    if not is_safe_url(url):
        return False
    
    req = urllib.request.Request(url, headers={
        "User-Agent": "AgentSurveyPipeline/1.0"
    })
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return False
            content = resp.read()
            # Verify PDF magic bytes
            if content[:5] != b'%PDF-':
                return False
            # Check reasonable size (1KB - 200MB)
            if len(content) < 1024 or len(content) > 200 * 1024 * 1024:
                return False
            Path(output_path).write_bytes(content)
            return True
    except Exception:
        return False


def try_arxiv(arxiv_id: str, output_path: str) -> bool:
    """Try downloading from arXiv."""
    if not arxiv_id:
        return False
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    return download_file(url, output_path)


def try_pmc(pmc_id: str, output_path: str) -> bool:
    """Try downloading from PubMed Central."""
    if not pmc_id:
        return False
    url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/pdf/"
    return download_file(url, output_path)


def try_unpaywall(doi: str, mailto: str, output_path: str) -> bool:
    """Try finding OA PDF via Unpaywall."""
    if not doi or not mailto:
        return False
    
    url = f"https://api.unpaywall.org/v2/{doi}?email={mailto}"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            oa_url = None
            # Try best_oa_location first
            best = data.get("best_oa_location", {})
            if best and best.get("url_for_pdf"):
                oa_url = best["url_for_pdf"]
            elif best and best.get("url"):
                oa_url = best["url"]
            
            # Fallback to any oa_location with PDF
            if not oa_url:
                for loc in data.get("oa_locations", []):
                    if loc.get("url_for_pdf"):
                        oa_url = loc["url_for_pdf"]
                        break
            
            if oa_url:
                return download_file(oa_url, output_path)
    except Exception:
        pass
    return False


def try_semantic_scholar(title: str, output_path: str) -> bool:
    """Try finding PDF via Semantic Scholar."""
    if not title:
        return False
    
    params = urllib.parse.urlencode({
        "query": title,
        "limit": "1",
        "fields": "openAccessPdf"
    })
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?{params}"
    
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            results = data.get("data", [])
            if results:
                pdf_info = results[0].get("openAccessPdf", {})
                if pdf_info and pdf_info.get("url"):
                    return download_file(pdf_info["url"], output_path)
    except Exception:
        pass
    return False


def download_reference(ref: dict, output_dir: str, mailto: str = "") -> dict:
    """Attempt to download a PDF for a reference using the priority cascade."""
    ref_id = ref.get("ref_id", "unknown")
    title = ref.get("title", "")
    doi = ref.get("doi", "")
    
    # Construct filename
    first_author = ref.get("authors", ["unknown"])[0] if ref.get("authors") else "unknown"
    author_last = first_author.split(",")[0].split()[-1] if " " in first_author else first_author
    year = ref.get("year", "0000")
    first_word = title.split()[0].lower() if title else "untitled"
    filename = sanitize_filename(f"{author_last}_{year}_{first_word}")
    output_path = os.path.join(output_dir, f"{filename}.pdf")
    
    # Handle collision
    counter = 2
    while os.path.exists(output_path):
        output_path = os.path.join(output_dir, f"{filename}_{counter}.pdf")
        counter += 1
    
    result = {
        "ref_id": ref_id,
        "title": title,
        "filename": os.path.basename(output_path),
        "success": False,
        "source": None,
        "attempts": []
    }
    
    # Extract arXiv ID from various fields
    arxiv_id = ref.get("arxiv_id", "")
    if not arxiv_id and doi and "arxiv" in doi.lower():
        arxiv_id = doi.split("arxiv.")[-1] if "arxiv." in doi else ""
    
    # Extract PMC ID
    pmc_id = ref.get("pmc_id", "") or ref.get("enrichment", {}).get("pubmed_id", "")
    
    # Priority cascade
    sources = [
        ("arxiv", lambda: try_arxiv(arxiv_id, output_path)),
        ("pmc", lambda: try_pmc(pmc_id, output_path)),
        ("unpaywall", lambda: try_unpaywall(doi, mailto, output_path)),
        ("semantic_scholar", lambda: try_semantic_scholar(title, output_path)),
    ]
    
    for source_name, attempt_fn in sources:
        result["attempts"].append(source_name)
        if attempt_fn():
            result["success"] = True
            result["source"] = source_name
            break
        time.sleep(0.5)  # Courtesy delay between sources
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Download PDFs for references")
    parser.add_argument("--input", "-i", required=True, help="Path to references JSON")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory for PDFs")
    parser.add_argument("--mailto", "-m", default="", help="Email for Unpaywall/Crossref")
    parser.add_argument("--manifest", default="download_manifest.json", help="Output manifest")
    args = parser.parse_args()
    
    mailto = args.mailto or os.environ.get("CROSSREF_MAILTO", "")
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Load references
    with open(args.input, "r") as f:
        data = json.load(f)
    
    references = data if isinstance(data, list) else data.get("references", [])
    print(f"Loaded {len(references)} references")
    
    results = []
    for i, ref in enumerate(references):
        title_short = ref.get("title", "unknown")[:50]
        print(f"  [{i+1}/{len(references)}] {title_short}...")
        result = download_reference(ref, args.output_dir, mailto)
        results.append(result)
        time.sleep(0.5)
    
    # Summary
    downloaded = sum(1 for r in results if r["success"])
    failed = len(results) - downloaded
    
    manifest = {
        "total": len(results),
        "downloaded": downloaded,
        "failed": failed,
        "success_rate": f"{downloaded/max(len(results),1)*100:.1f}%",
        "downloads": [r for r in results if r["success"]],
        "failed_references": [r for r in results if not r["success"]]
    }
    
    Path(args.manifest).write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"\nDownload Complete: {downloaded}/{len(results)} ({manifest['success_rate']})")
    print(f"Manifest saved to {args.manifest}")


if __name__ == "__main__":
    main()
