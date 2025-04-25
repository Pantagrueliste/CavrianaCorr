# Digital Edition of Filippo Cavriana's Correspondence
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8224585.svg)]([https://doi.org/10.5281/zenodo.8224585](https://doi.org/10.5281/zenodo.14789457))
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by/4.0/)  

[![TEI Valid](https://github.com/Pantagrueliste/CavrianaCorr/actions/workflows/tei-validation.yml/badge.svg?branch=main)](https://github.com/Pantagrueliste/CavrianaCorr/actions/workflows/tei-validation.yml)
[![Frontend Build Status](https://github.com/Pantagrueliste/CavrianaCorr_FrontEnd/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/Pantagrueliste/CavrianaCorr_FrontEnd/actions/workflows/main.yml)


This project presents the first comprehensive digital edition of Filippo Cavriana's (1536-1606) correspondence, drawn from the *Mediceo del Principato* collection at the [State Archives of Florence](http://www.archiviodistato.firenze.it/), the *Archivio Gonzaga* in the [Archivio di Stato di Mantova](https://archiviodistatomantova.cultura.gov.it/), and the manuscript collection of the [Bibliothèque nationale de France](https://www.bnf.fr). 

As a physician at the court of France, and a spy for the grand dukes of Tuscany, Cavriana's letters provide crucial insights into the French Wars of Religion, the ideas, and the language of 16th-century European politics.

## Citation

This edition represents thousands of hours of archival research, transcription, and encoding work. If you use these materials in your research, please cite this digital edition:

```markdown
Clément Godbarge. ‘Pantagrueliste/cavrianacorr: V.0.1.0-alpha’. *Zenodo*, 2 February 2025. https://doi.org/10.5281/zenodo.14789457.
```

## Project Scope

The collection encompasses Cavriana's extensive correspondence network throughout Europe, providing crucial insights into late 16th-century diplomatic relations and the complex political landscape of Renaissance Italy and France.

## Technical Implementation

- Full TEI-XML encoding with semantic markup
- Named entity recognition and annotation
- Interactive data visualizations including correspondence heatmap
- Integration with Semantic Web standards
- Version-controlling and lifecylce management through GitHub
- Long-term storage on Zenodo

## Release Schedule

The project follows a phased release approach, with development and content publication spanning from late 2024 through early 2026.

```mermaid
gantt
    title Project Release Schedule
    dateFormat YYYY-MM
    axisFormat %Y-%m
    
    section Development
    Backend Development & Launch :2024-09, 2025-01
    
    section Content Release
    
    1st Batch (1566)         :2024-12, 2025-02
    2nd Batch (69-71)     :2025-01, 2025-04
    3rd Batch (72-77)      :2025-04, 2025-06
    4th Batch (77-87)     :2025-06, 2025-08
    5th Batch (87-89)      :2025-08, 2025-10
    6th Batch (89-06)      :2025-10, 2025-12
    
    section Review
    Peer Review & Final Edition  :2025-12, 2026-04
```

## Access and Licensing

This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/). While the content is freely available, proper attribution is required for any use or adaptation of these materials.

## Visualizations

The project includes several visualizations to help explore Cavriana's correspondence:

- **Letter Heatmap Calendar**: An interactive calendar heatmap showing Cavriana's letter-writing activity over time, with color intensity representing text volume (word count). See [heatmap_README.md](heatmap_README.md) for details.

## Contributing

To report issues or provide feedback, please submit an issue via GitHub or contact [Clément Godbarge](mailto:cag30@st-andrews.ac.uk) directly.

## Acknowledgments

This project has received support from the State Archives of Florence, the University of St Andrews, The Harvard University Center for Italian Renaissance Studies, and the Medici Archive Project.

---

**Note on Data Use**: This digital edition represents substantial scholarly work in transcription, annotation, and encoding. While we encourage its use for research, teaching, or data scraping, we ask that you acknowledge this contribution by citing the project appropriately in your work.
