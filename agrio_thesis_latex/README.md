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

The early chapters now use explicit `\cite{...}` commands and `main.tex` prints only cited entries. Review, overview, systematic-review, bibliometric-review, and thesis sources should not be used as main sources for the background or related-work chapters unless the supervisor explicitly approves them for limited context.

## Fonts

The main font is Latin Modern Roman. Arabic support uses Amiri if installed, then Noto Naskh Arabic, then Arial as a fallback. If XeLaTeX reports a missing Arabic font, install Amiri or Noto Naskh Arabic, or edit `preamble.tex` and replace the `\arabicfont` fallback with a font available on the machine.

## Manual cleanup checklist

- Replace every framed figure placeholder with the final image.
- Review in-text numeric references `[1]`, `[2]`, etc. and convert them to `\cite{...}`.
- Verify long tables visually after final compilation; some wide tables may need manual column-width tuning.
- Check the Arabic summary rendering on the target machine, especially if Arial is used as the fallback Arabic font.
- Add supervisor names on the cover page.
