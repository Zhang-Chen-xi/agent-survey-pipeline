#!/usr/bin/env python3
"""
BibTeX Verification Script for the Agent Survey Pipeline.

Reads a .bib file and verifies each entry against Crossref and Semantic Scholar APIs.
Outputs a verification report in JSON and Markdown formats.

Usage:
    python verify_bib.py --input references.bib --output verification_report.json
    python verify_bib.py --input references.bib --mailto user@example.com

Environment:
    CROSSREF_MAILTO: Email for Crossref Polite Pool (alternative to --mailto)
"""

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional


def parse_bibtex(filepath: str) -> list[dict]:
    """Simple BibTeX parser — extracts entries from a .bib file."""
    entries = []
    text = Path(filepath).read_text(encoding="utf-8")
    
    # Match @type{key, ... }
    pattern = re.compile(r'@(\w+)\s*\{([^,]+),\s*(.*?)\n\}', re.DOTALL)
    
    for match in pattern.finditer(text):
        entry_type = match.group(1).lower()
        bibkey = match.group(2).strip()
        body = match.group(3)
        
        entry = {
            "bibkey": bibkey,
            "type": entry_type,
            "raw": match.group(0)
        }
        
        # Extract fields
        field_pattern = re.compile(r'(\w+)\s*=\s*\{([^}]*)\}', re.DOTALL)
        for fmatch in field_pattern.finditer(body):
            field_name = fmatch.group(1).lower()
            field_value = fmatch.group(2).strip()
            entry[field_name] = field_value
        
        entries.append(entry)
    
    return entries


def crossref_verify(doi: str, mailto: str = "") -> Optional[dict]:
    """Verify a DOI against Crossref API."""
    if not doi:
        return None
    
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='')}"
    headers = {
        "User-Agent": f"AgentSurveyPipeline/1.0 (mailto:{mailto})" if mailto 
                      else "AgentSurveyPipeline/1.0"
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get("message", {})
    except Exception as e:
        return {"error": str(e)}


def crossref_search_title(title: str, mailto: str = "") -> Optional[dict]:
    """Search Crossref by title."""
    if not title:
        return None
    
    params = urllib.parse.urlencode({
        "query.title": title,
        "select": "DOI,title,author,container-title,published-print,volume,page",
        "rows": "1"
    })
    url = f"https://api.crossref.org/works?{params}"
    headers = {
        "User-Agent": f"AgentSurveyPipeline/1.0 (mailto:{mailto})" if mailto
                      else "AgentSurveyPipeline/1.0"
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            items = data.get("message", {}).get("items", [])
            return items[0] if items else None
    except Exception as e:
        return {"error": str(e)}


def semantic_scholar_verify(title: str) -> Optional[dict]:
    """Verify a paper against Semantic Scholar API."""
    if not title:
        return None
    
    params = urllib.parse.urlencode({
        "query": title,
        "limit": "1",
        "fields": "title,authors,year,venue,externalIds,citationCount"
    })
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?{params}"
    
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            results = data.get("data", [])
            return results[0] if results else None
    except Exception as e:
        return {"error": str(e)}


def normalize_title(title: str) -> str:
    """Normalize a title for comparison."""
    if not title:
        return ""
    title = title.lower().strip()
    title = re.sub(r'[^\w\s]', '', title)
    title = re.sub(r'\s+', ' ', title)
    return title


def title_similarity(t1: str, t2: str) -> float:
    """Simple Jaccard similarity between two titles."""
    w1 = set(normalize_title(t1).split())
    w2 = set(normalize_title(t2).split())
    if not w1 or not w2:
        return 0.0
    intersection = w1 & w2
    union = w1 | w2
    return len(intersection) / len(union)


def verify_entry(entry: dict, mailto: str = "") -> dict:
    """Verify a single BibTeX entry."""
    result = {
        "bibkey": entry["bibkey"],
        "title": entry.get("title", "UNKNOWN"),
        "doi": entry.get("doi", ""),
        "status": "UNVERIFIED",
        "hallucination_type": None,
        "details": {}
    }
    
    doi = entry.get("doi", "")
    title = entry.get("title", "")
    
    # Step 1: DOI check
    if doi:
        cr = crossref_verify(doi, mailto)
        if cr and "error" not in cr:
            cr_title = " ".join(cr.get("title", []))
            sim = title_similarity(title, cr_title)
            
            if sim > 0.85:
                result["status"] = "VERIFIED"
                result["details"]["crossref"] = True
                result["details"]["title_match"] = sim
            else:
                result["status"] = "SUSPICIOUS"
                result["hallucination_type"] = "PH"
                result["details"]["crossref_title_mismatch"] = True
                result["details"]["crossref_title"] = cr_title
                result["details"]["similarity"] = sim
        elif cr and "error" in cr:
            result["details"]["crossref_error"] = cr["error"]
        time.sleep(0.2)  # Rate limit courtesy
    
    # Step 2: Title search (Crossref)
    if result["status"] == "UNVERIFIED" and title:
        cr_search = crossref_search_title(title, mailto)
        if cr_search and "error" not in cr_search:
            cr_title = " ".join(cr_search.get("title", []))
            sim = title_similarity(title, cr_title)
            if sim > 0.85:
                result["status"] = "VERIFIED"
                result["details"]["crossref_search"] = True
                result["details"]["found_doi"] = cr_search.get("DOI", "")
        time.sleep(0.2)
    
    # Step 3: Semantic Scholar check
    if title:
        s2 = semantic_scholar_verify(title)
        if s2 and "error" not in s2:
            s2_title = s2.get("title", "")
            sim = title_similarity(title, s2_title)
            if sim > 0.85:
                if result["status"] == "UNVERIFIED":
                    result["status"] = "VERIFIED"
                result["details"]["semantic_scholar"] = True
                result["details"]["s2_citations"] = s2.get("citationCount", 0)
            elif sim > 0.5:
                result["details"]["s2_partial_match"] = s2_title
        time.sleep(0.5)  # S2 rate limit
    
    # Classification
    if result["status"] == "UNVERIFIED":
        # Could be TF or just not indexed
        if not doi and not result["details"].get("semantic_scholar"):
            result["hallucination_type"] = "POSSIBLE_TF"
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Verify BibTeX entries against Crossref/S2")
    parser.add_argument("--input", "-i", required=True, help="Path to .bib file")
    parser.add_argument("--output", "-o", default="verification_report.json", help="Output JSON")
    parser.add_argument("--mailto", "-m", default="", help="Crossref Polite Pool email")
    parser.add_argument("--report", "-r", default="verification_report.md", help="Output Markdown report")
    args = parser.parse_args()
    
    mailto = args.mailto or __import__("os").environ.get("CROSSREF_MAILTO", "")
    
    entries = parse_bibtex(args.input)
    print(f"Parsed {len(entries)} BibTeX entries from {args.input}")
    
    results = []
    for i, entry in enumerate(entries):
        print(f"  [{i+1}/{len(entries)}] Verifying: {entry.get('title', entry['bibkey'])[:60]}...")
        result = verify_entry(entry, mailto)
        results.append(result)
    
    # Summary
    verified = sum(1 for r in results if r["status"] == "VERIFIED")
    suspicious = sum(1 for r in results if r["status"] == "SUSPICIOUS")
    unverified = sum(1 for r in results if r["status"] == "UNVERIFIED")
    
    summary = {
        "total": len(results),
        "verified": verified,
        "suspicious": suspicious,
        "unverified": unverified,
        "verified_pct": f"{verified/max(len(results),1)*100:.1f}%",
        "results": results
    }
    
    # Save JSON
    Path(args.output).write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\nJSON report saved to {args.output}")
    
    # Save Markdown
    md_lines = [
        "# Citation Verification Report\n",
        f"## Summary\n",
        f"- Total: {len(results)}",
        f"- Verified: {verified} ({summary['verified_pct']})",
        f"- Suspicious: {suspicious}",
        f"- Unverified: {unverified}\n",
        "## Results\n",
    ]
    for r in results:
        status_icon = {"VERIFIED": "✅", "SUSPICIOUS": "⚠️", "UNVERIFIED": "❌"}.get(r["status"], "?")
        md_lines.append(f"- {status_icon} [{r['bibkey']}] {r['title'][:80]} — {r['status']}")
        if r.get("hallucination_type"):
            md_lines.append(f"  - Hallucination type: {r['hallucination_type']}")
    
    Path(args.report).write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Markdown report saved to {args.report}")
    
    print(f"\nVerification Complete: {summary['verified_pct']} verified")


if __name__ == "__main__":
    main()
