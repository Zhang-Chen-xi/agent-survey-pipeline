# Module 17: DOCX Delivery

> Generates a publication-ready Word document using docx-js (Node.js) with full academic formatting.

## Agent Instructions

You are producing a professional Word document. Use the docx-js library for maximum control over formatting.

### Pre-flight Check

- [ ] Node.js 18+ available
- [ ] `npm install docx` completed in working directory
- [ ] Manuscript content ready (from writing modules)
- [ ] Citation style determined

### Document Generation with docx-js

#### Basic Structure

```javascript
import { Document, Packer, Paragraph, TextRun, HeadingLevel, 
         AlignmentType, TabStopPosition, TabStopType,
         PageBreak, Table, TableRow, TableCell, WidthType,
         Header, Footer, PageNumber, NumberFormat } from 'docx';

// Chinese academic paper defaults
const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },  // A4 in DXA
        margin: {
          top: 1440,    // 2.54cm
          bottom: 1440,
          left: 1800,   // 3.17cm
          right: 1800,
        },
      },
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "{Paper Title}", font: "SimSun", size: 18 })],
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ children: [PageNumber.CURRENT], font: "Times New Roman", size: 20 })],
        })],
      }),
    },
    children: [/* paragraphs go here */],
  }],
});

const buffer = await Packer.toBuffer(doc);
fs.writeFileSync("_delivery/manuscript.docx", buffer);
```

#### Text Formatting Helpers

**Body paragraph (Chinese academic):**
```javascript
function bodyPara(text) {
  const runs = [];
  // Parse inline citations [1,2] as superscript
  text.split(/(\[\d+(?:[,\-]\d+)*\])/g).forEach(part => {
    if (/^\[\d+/.test(part)) {
      runs.push(new TextRun({ text: part, superScript: true, font: "Times New Roman", size: 24 }));
    } else if (part) {
      runs.push(new TextRun({ text: part, font: "SimSun", size: 24 }));
    }
  });
  return new Paragraph({
    children: runs,
    spacing: { line: 360 },  // 1.5x line spacing
    indent: { firstLine: 480 },  // 2-char indent
  });
}
```

**Heading:**
```javascript
function heading(text, level) {
  const fonts = { 1: "SimHei", 2: "SimHei", 3: "SimHei" };
  const sizes = { 1: 32, 2: 28, 3: 24 };  // 16pt, 14pt, 12pt
  return new Paragraph({
    children: [new TextRun({ text, font: fonts[level], size: sizes[level], bold: true })],
    spacing: { before: 240, after: 120 },
    heading: level === 1 ? HeadingLevel.HEADING_1 : level === 2 ? HeadingLevel.HEADING_2 : HeadingLevel.HEADING_3,
  });
}
```

**Reference entry:**
```javascript
function refEntry(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: "Times New Roman", size: 21 })],  // 五号 10.5pt
    spacing: { line: 240 },
    indent: { left: 420, hanging: 420 },  // Hanging indent
  });
}
```

### Document Sections

Generate in order:
1. **Title page** (if required by venue)
2. **Abstract** (Chinese + English for bilingual papers)
3. **Keywords**
4. **Table of Contents** (if >10 pages)
5. **Body sections** (per outline)
6. **References**
7. **Appendices** (if any)

### Verification

After generating the DOCX:

1. **Convert to PDF for visual check** (if LibreOffice available):
```bash
soffice --headless --convert-to pdf _delivery/manuscript.docx --outdir _delivery/
pdftoppm -jpeg -r 150 _delivery/manuscript.pdf _delivery/preview
```

2. **Inspect each preview image** for:
   - [ ] Chinese characters render correctly (宋体/黑体, no garbled text)
   - [ ] Superscript citations display correctly
   - [ ] Heading hierarchy visible
   - [ ] First-line indentation correct
   - [ ] Page margins correct
   - [ ] Tables formatted properly
   - [ ] References with hanging indent

3. **Check document structure** by reading back:
```bash
pandoc _delivery/manuscript.docx -t plain | head -100
```

### Output

Save to `_delivery/manuscript.docx`:

```
DOCX Delivery Complete:
📄 File: _delivery/manuscript.docx
📊 Sections: {N}
📦 Size: {X} KB
✅ Chinese formatting verified
✅ Citations as superscript
✅ References with hanging indent
✅ Visual inspection passed
```

### Error Recovery

| Error | Recovery |
|-------|----------|
| docx-js not installed | `npm install docx` |
| Chinese font missing | Ensure SimSun/SimHei available on system; fallback to system CJK font |
| Table width overflow | Use percentage widths, adjust column ratios |
| Large file size | Compress embedded images before insertion |
