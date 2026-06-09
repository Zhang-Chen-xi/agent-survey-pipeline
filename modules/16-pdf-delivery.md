# Module 16: PDF Delivery

> Generates the final paper as a publication-ready PDF document.

## Agent Instructions

You are producing the final PDF deliverable. The goal is a clean, professional document ready for submission or sharing.

### PDF Generation Methods (in priority order)

#### Method 1: LaTeX → PDF (Preferred for Academic Papers)

If the manuscript is in LaTeX format:

```bash
# Compile with pdflatex + bibtex
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex  # Second pass for references
```

Ensure:
- All citations resolved
- No overfull hbox warnings (adjust text or use `\sloppy` if needed)
- Bibliography generated correctly
- Figures included at appropriate resolution (300 DPI minimum)

#### Method 2: DOCX → PDF (via LibreOffice)

```bash
soffice --headless --convert-to pdf manuscript.docx --outdir _delivery/
```

For better results with Chinese text:
```bash
soffice --headless --convert-to pdf --infilter="Microsoft Word 2007-2019 XML" manuscript.docx
```

#### Method 3: Markdown → PDF (via pandoc)

```bash
pandoc manuscript.md -o manuscript.pdf \
  --pdf-engine=xelatex \
  --citeproc \
  --bibliography=_references/references.bib \
  -V geometry:margin=2.54cm \
  -V fontsize=12pt \
  -V lang=zh-CN  # for Chinese papers
```

#### Method 4: HTML → PDF (for complex layouts)

Generate styled HTML first, then convert:
```bash
# Using wkhtmltopdf
wkhtmltopdf --page-size A4 --margin-top 2.5cm manuscript.html manuscript.pdf

# Or using Playwright/Puppeteer for better CSS support
```

### Chinese Document Specifics

For Chinese papers, ensure:
- **Body text**: SimSun (宋体), 小四 (12pt)
- **Headings**: SimHei (黑体), bold
- **Line spacing**: 1.5x (360 twips in DOCX)
- **First line indent**: 2 characters (480 twips)
- **Page size**: A4
- **Margins**: Top/Bottom 2.54cm, Left/Right 3.17cm (or per journal spec)

### Post-Generation Verification

After PDF generation:

1. **Convert to images for visual inspection**:
```bash
pdftoppm -jpeg -r 150 manuscript.pdf _delivery/preview
```

2. **Check each page** for:
   - [ ] Text renders correctly (no garbled characters, no black blocks for Chinese)
   - [ ] Citations resolved (no `??` or `[?]` markers)
   - [ ] Figures display correctly
   - [ ] Page breaks are reasonable (no single lines at top/bottom of page)
   - [ ] Header/footer correct
   - [ ] Page numbers present and correct
   - [ ] Table of contents links work (if applicable)

3. **Verify PDF metadata**:
```python
from pypdf import PdfReader
reader = PdfReader("manuscript.pdf")
print(f"Pages: {len(reader.pages)}")
print(f"Title: {reader.metadata.title}")
print(f"Author: {reader.metadata.author}")
```

### Output

Save to `_delivery/manuscript.pdf` with:
- PDF metadata populated (title, author, creation date)
- File size reported
- Page count reported
- Preview images generated

```
PDF Delivery Complete:
📄 File: _delivery/manuscript.pdf
📊 Pages: {N}
📦 Size: {X} MB
✅ All citations resolved
✅ All figures rendered
✅ Visual inspection passed
```

### Error Recovery

| Error | Recovery |
|-------|----------|
| LaTeX compilation fails | Check log, fix errors, retry. If persistent, switch to DOCX→PDF |
| Chinese characters garbled | Use xelatex instead of pdflatex, ensure CJK fonts installed |
| LibreOffice hangs | Kill process, retry with `--norestore` flag |
| pandoc missing template | Install template or use default |
| PDF too large (>50MB) | Compress images: `gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dNOPAUSE -dBATCH -dPDFSETTINGS=/ebook` |
