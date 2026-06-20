# Agrio Master LaTeX Project

Compile from this directory with:

```powershell
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

This project is the Master Diploma version of the Agrio work. It keeps the same cover-page style and research title as `agrio_thesis_latex`, but its PDF is organized around the scientific part of the work: background, state of the art, synthesis, and conclusion.

## Structure

- Front matter: dedication, acknowledgements, abstract, résumé, Arabic summary, abbreviations, lists.
- `chapters/00_general_introduction.tex`: context and problem statement, objectives, and thesis outline for the Master Diploma.
- `chapters/01_precision_agriculture.tex`: `Precision Agriculture and Smart Irrigation`.
- `chapters/02_digital_twins_iot_ai.tex`: `Digital Twins, IoT, and Artificial Intelligence`.
- `chapters/03_state_of_the_art.tex`: `Digital Twins in Agriculture and Irrigation: State of the Art`.
- `chapters/04_comparative_analysis.tex`: `Comparative Analysis and Scientific Positioning`.
- `chapters/12_general_conclusion.tex`: Master-focused general conclusion.
- `references.bib`: shared bibliography from the thesis project.

## Figures

The Master project includes the figures used by the selected scientific chapters:

- `figures/cover/`
- `figures/chapter_01/`
- `figures/chapter_02/`
- `figures/chapter_03/`
- `figures/chapter_04/`

## Notes

The project uses XeLaTeX because the document supports English, French, and Arabic text. The bibliography uses classic BibTeX with `IEEEtran.bst`.
