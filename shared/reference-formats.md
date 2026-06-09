# Reference Format Specifications

> Cross-cutting protocol for citation formatting across GB/T 7714-2015, APA 7th, IEEE, and Chicago 17th.

## GB/T 7714-2015 (Chinese National Standard)

### In-text Citation
- Sequential numbers in square brackets, as superscript: `……取得了显著效果^[1]^`
- Multiple citations: `[1-3]` (range) or `[1,3,5]` (discrete)

### Reference List Entries

**Journal article [J]:**
```
[序号] 作者. 题名[J]. 刊名, 年, 卷(期): 起始页-终止页.
[1] 张三, 李四. 深度学习在自然语言处理中的应用[J]. 计算机学报, 2023, 46(3): 500-520.
```

**Conference paper [C]:**
```
[序号] 作者. 题名[C]//会议录名称. 出版地: 出版者, 年: 起始页-终止页.
[2] Smith J, Doe A. Attention mechanisms[C]//Proc of ICML. New York: ACM, 2022: 1234-1245.
```

**Book [M]:**
```
[序号] 作者. 书名[M]. 版次. 出版地: 出版者, 年.
```

**Thesis [D]:**
```
[序号] 作者. 题名[D]. 保存地: 保存单位, 年.
```

**Online resource [EB/OL]:**
```
[序号] 作者. 题名[EB/OL]. (发布日期)[引用日期]. URL.
```

**Patent [P]:**
```
[序号] 发明人. 专利名称: 专利号[P]. 公告日期.
```

### Author Name Rules
- 3 authors or fewer: list all
- More than 3: list first 3, then add ", 等" (Chinese) or ", et al." (English)
- Chinese names: 姓在前名在后, no comma between surname and given name
- English names: SURNAME First, e.g., "SMITH J A"

---

## APA 7th Edition

### In-text Citation
- Author-year format: (Smith, 2023) or Smith (2023)
- Multiple authors: (Smith & Doe, 2023), (Smith et al., 2023) for 3+
- Multiple works: (Smith, 2023; Doe, 2022) — alphabetical, semicolon-separated

### Reference List Entries

**Journal article:**
```
Smith, J. A., & Doe, B. C. (2023). Title of the article. Journal Name, 15(3), 123-145. https://doi.org/10.xxxx/xxxxx
```

**Conference paper:**
```
Smith, J. A. (2022). Title of the paper. In Proceedings of the Conference Name (pp. 123-134). Publisher. https://doi.org/10.xxxx/xxxxx
```

**Book:**
```
Smith, J. A. (2021). Title of the book (2nd ed.). Publisher.
```

---

## IEEE Style

### In-text Citation
- Sequential numbers in square brackets: [1], [2], [1, 3], [1]–[5]

### Reference List Entries

**Journal article:**
```
[1] J. A. Smith and B. C. Doe, "Title of the article," IEEE Trans. Pattern Anal. Mach. Intell., vol. 45, no. 3, pp. 1234-1245, Mar. 2023.
```

**Conference paper:**
```
[2] J. A. Smith, "Title of the paper," in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), 2022, pp. 1234-1245.
```

---

## Chicago 17th Edition (Notes-Bibliography)

### Footnote Citation
```
1. John A. Smith and B. C. Doe, "Title of the Article," Journal Name 15, no. 3 (2023): 123.
```

### Bibliography Entry
```
Smith, John A., and B. C. Doe. "Title of the Article." Journal Name 15, no. 3 (2023): 123-145.
```

---

## BibTeX Entry Types

| Entry Type | Use For | Required Fields |
|-----------|---------|----------------|
| `@article` | Journal articles | author, title, journal, year, volume |
| `@inproceedings` | Conference papers | author, title, booktitle, year |
| `@book` | Books | author/editor, title, publisher, year |
| `@phdthesis` | Doctoral theses | author, title, school, year |
| `@mastersthesis` | Master's theses | author, title, school, year |
| `@techreport` | Technical reports | author, title, institution, year |
| `@misc` | Web resources, preprints | author, title, howpublished, year |
| `@incollection` | Book chapters | author, title, booktitle, publisher, year |

### BibTeX Template

```bibtex
@article{bibkey,
  author    = {Last, First and Last2, First2},
  title     = {Title of the Article},
  journal   = {Journal Name},
  year      = {2023},
  volume    = {15},
  number    = {3},
  pages     = {123--145},
  doi       = {10.xxxx/xxxxx},
  language  = {en}
}
```

## Conversion Between Styles

When converting between citation styles:
1. The BibTeX file is the canonical source
2. Reformat in-text citations according to the target style
3. Regenerate the reference list from BibTeX using the target style
4. Verify no citations are lost in conversion
