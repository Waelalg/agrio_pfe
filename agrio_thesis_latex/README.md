# Agrio Engineering Thesis LaTeX Project

Compile from this directory with:

```powershell
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

This project is the Engineering Diploma version of the Agrio work. It keeps the shared background and state of the art, then focuses on the engineering contribution: requirements, conception, architecture, implementation, AI/Digital Twin pipeline, deployment, validation, and future perspectives.

The project uses XeLaTeX because the thesis contains English, French, and Arabic text. It uses classic BibTeX with `IEEEtran.bst` because `biber`/`biblatex-ieee` was not available in the local environment. If `biblatex-ieee` is installed later, the bibliography setup can be migrated to `biblatex`.

## Structure

- Front matter: dedication, acknowledgements, abstract, résumé, Arabic summary, abbreviations, lists.
- General Introduction: context and problem statement, objectives, and thesis outline for the Engineering Diploma.
- Background and state of the art: chapters 1 to 4.
- Contribution: conception and design: chapters 5 and 6.
- Implementation: chapters 7 to 9.
- Deployment, validation, and discussion: chapters 10 and 11.
- General Conclusion and Future Perspectives.
- Bibliography and appendices.

## Figures

All DOCX figure placeholders were converted into LaTeX `figure` environments with framed placeholder boxes. The commented `\includegraphics` line above each box shows the intended path. Put final images under `figures/cover/`, `figures/chapter_01/` through `figures/chapter_11/`, or `figures/appendix/`, then uncomment and adjust the corresponding `\includegraphics` line.

## Bibliography

The original numbered bibliography was converted into `references.bib`, and `main.tex` prints all entries with `\nocite{*}`. In-text references such as `[1]` were preserved because automatic citation-key replacement can corrupt meaning when several bracketed numbers occur in prose. Replace them manually with `\cite{...}` when the final source mapping is reviewed.

## Fonts

The main font is Latin Modern Roman. Arabic support uses Amiri if installed, then Noto Naskh Arabic, then Arial as a fallback. If XeLaTeX reports a missing Arabic font, install Amiri or Noto Naskh Arabic, or edit `preamble.tex` and replace the `\arabicfont` fallback with a font available on the machine.

## Manual cleanup checklist

- Replace every framed figure placeholder with the final image.
- Review in-text numeric references `[1]`, `[2]`, etc. and convert them to `\cite{...}`.
- Verify long tables visually after final compilation; some wide tables may need manual column-width tuning.
- Check the Arabic summary rendering on the target machine, especially if Arial is used as the fallback Arabic font.
- Add supervisor names on the cover page.
