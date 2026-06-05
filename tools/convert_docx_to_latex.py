from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Iterable

from docx import Document
from docx.document import Document as DocumentType
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph


ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / "Agrio_Combined_Thesis_Expanded_Full_No_Visuals.docx"
OUT = ROOT / "agrio_thesis_latex"


CHAPTER_FILES = {
    "General Introduction": "chapters/00_general_introduction.tex",
    "Chapter 1 - Precision Agriculture and Smart Irrigation": "chapters/01_precision_agriculture.tex",
    "Chapter 2 - Digital Twins, IoT, and Artificial Intelligence": "chapters/02_digital_twins_iot_ai.tex",
    "Chapter 3 - Digital Twins in Agriculture and Irrigation: State of the Art": "chapters/03_state_of_the_art.tex",
    "Chapter 4 - Comparative Analysis and Scientific Positioning": "chapters/04_comparative_analysis.tex",
    "Chapter 5 - Requirements Specification and Design": "chapters/05_requirements_design.tex",
    "Chapter 6 - Global Architecture of the Proposed Digital Twin": "chapters/06_global_architecture.tex",
    "Chapter 7 - Backend, Database, and IoT Data Ingestion": "chapters/07_backend_database_iot.tex",
    "Chapter 8 - Digital Twin and Machine Learning Layer": "chapters/08_digital_twin_ml.tex",
    "Chapter 9 - User Interfaces and Irrigation Control": "chapters/09_interfaces_control.tex",
    "Chapter 10 - Deployment Environment": "chapters/10_deployment.tex",
    "Chapter 11 - Results, Validation, and Discussion": "chapters/11_results_validation.tex",
    "General Conclusion": "chapters/12_general_conclusion.tex",
}

PART_BEFORE = {
    "Chapter 1 - Precision Agriculture and Smart Irrigation": "Theoretical Background",
    "Chapter 3 - Digital Twins in Agriculture and Irrigation: State of the Art": "State of the Art and Scientific Positioning",
    "Chapter 5 - Requirements Specification and Design": "Requirements and Architecture",
    "Chapter 7 - Backend, Database, and IoT Data Ingestion": "Implementation",
    "Chapter 10 - Deployment Environment": "Deployment, Validation, and Discussion",
}

APPENDIX_FILES = {
    "Appendix A - Figure Placement Checklist": "appendices/appendix_a_figures_checklist.tex",
    "Appendix B - Full Class Diagram": "appendices/appendix_b_class_diagram.tex",
    "Appendix C - Full Detailed Architecture": "appendices/appendix_c_architecture.tex",
    "Appendix D - Complete Database ERD": "appendices/appendix_d_erd.tex",
    "Appendix E - Example MQTT Payloads": "appendices/appendix_e_payloads.tex",
    "Appendix F - Missing Visual Capture Guide": "appendices/appendix_f_capture_guide.tex",
    "Appendix G - Thesis Expansion Notes for Final Editing": "appendices/appendix_g_expansion_notes.tex",
    "Appendix H - Detailed Paper-by-Paper Literature Matrix": "appendices/appendix_h_literature_matrix.tex",
    "Appendix I - Detailed Database Table Descriptions": "appendices/appendix_i_database_tables.tex",
    "Appendix J - Detailed API and Service Responsibilities": "appendices/appendix_j_api_services.tex",
    "Appendix K - Detailed Algorithms and Pseudocode": "appendices/appendix_k_algorithms.tex",
    "Appendix L - Expanded Chapter Text Blocks for Final Integration": "appendices/appendix_l_extra_text_blocks.tex",
    "Appendix M - Defense-Oriented Scientific Positioning": "appendices/appendix_m_defense_positioning.tex",
}


def iter_blocks(doc: DocumentType) -> Iterable[Paragraph | Table]:
    for child in doc.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, doc)
        elif isinstance(child, CT_Tbl):
            yield Table(child, doc)


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def has_arabic(text: str) -> bool:
    return any("\u0600" <= ch <= "\u06ff" for ch in text)


def para_latex(text: str) -> str:
    escaped = latex_escape(text)
    if has_arabic(text):
        return "\\begin{Arabic}\n" + escaped + "\n\\end{Arabic}\n"
    return escaped + "\n"


def slug(text: str) -> str:
    value = text.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value[:70] or "placeholder"


def title_without_prefix(text: str) -> str:
    text = re.sub(r"^Chapter\s+\d+\s*-\s*", "", text)
    text = re.sub(r"^Appendix\s+[A-Z]\s*-\s*", "", text)
    return text.strip()


def title_latex(text: str) -> str:
    escaped = latex_escape(text)
    if has_arabic(text):
        return f"\\texorpdfstring{{\\textarabic{{{escaped}}}}}{{Arabic summary}}"
    return escaped


def section_command(level: int, title: str, current_kind: str) -> str:
    title = title_latex(title_without_prefix(title))
    if current_kind == "front":
        return f"\\chapter*{{{title}}}\n\\addcontentsline{{toc}}{{chapter}}{{{title}}}\n"
    if current_kind == "intro" or title in {"General Introduction", "General Conclusion"}:
        return f"\\chapter*{{{title}}}\n\\addcontentsline{{toc}}{{chapter}}{{{title}}}\n"
    if current_kind == "appendix":
        return f"\\section{{{title}}}\n" if level > 1 else f"\\chapter{{{title}}}\n"
    if level == 1:
        return f"\\chapter{{{title}}}\n"
    if level == 2:
        return f"\\section{{{title}}}\n"
    return f"\\subsection{{{title}}}\n"


def parse_caption(text: str) -> str:
    return re.sub(r"^Table\s+[A-Za-z0-9.]+\s*[-–]\s*", "", text).strip()


def table_to_latex(table: Table, caption: str | None) -> str:
    rows = [[clean_text(cell.text) for cell in row.cells] for row in table.rows]
    if not rows:
        return ""
    ncols = max(len(row) for row in rows)
    width = max(0.09, min(0.28, 0.86 / max(ncols, 1)))
    spec = "@{}" + "".join([f">{{\\raggedright\\arraybackslash}}p{{{width:.2f}\\textwidth}}" for _ in range(ncols)]) + "@{}"
    out = ["\\begin{footnotesize}", "\\setlength{\\tabcolsep}{2pt}", f"\\begin{{longtable}}{{{spec}}}"]
    if caption:
        out.append(f"\\caption{{{latex_escape(parse_caption(caption))}}}\\\\")
    first = rows[0] + [""] * (ncols - len(rows[0]))
    out.append("\\toprule")
    out.append(" & ".join(latex_escape(cell) for cell in first) + r" \\")
    out.append("\\midrule")
    out.append("\\endfirsthead")
    out.append("\\toprule")
    out.append(" & ".join(latex_escape(cell) for cell in first) + r" \\")
    out.append("\\midrule")
    out.append("\\endhead")
    for row in rows[1:]:
        padded = row + [""] * (ncols - len(row))
        out.append(" & ".join(latex_escape(cell) for cell in padded) + r" \\")
    out.append("\\bottomrule")
    out.append("\\end{longtable}")
    out.append("\\end{footnotesize}\n")
    return "\n".join(out)


def figure_to_latex(text: str) -> str:
    match = re.match(r"Figure\s+([A-Za-z0-9.]+)\s*[-–]\s*(.*)", text)
    number = match.group(1) if match else "x"
    rest = match.group(2) if match else text
    source = "Authors"
    source_match = re.search(r"\[Source:\s*(.*?)\s*\]\.?$", rest)
    if source_match:
        source = source_match.group(1).rstrip(".")
        rest = rest[: source_match.start()].strip()
    caption = rest.rstrip(".")
    if number.startswith("A"):
        folder = "appendix"
    else:
        chapter = number.split(".")[0]
        folder = "cover" if chapter == "0" else f"chapter_{int(chapter):02d}" if chapter.isdigit() else "appendix"
    filename = f"fig_{slug(number)}_{slug(caption)[:45]}.png"
    label = f"fig:{slug(number + '-' + caption)}"
    return (
        "\\begin{figure}[H]\n"
        "    \\centering\n"
        f"    % \\includegraphics[width=0.9\\textwidth]{{figures/{folder}/{filename}}}\n"
        f"    \\fbox{{\\parbox{{0.85\\textwidth}}{{\\centering Insert Figure {latex_escape(number)} here: {latex_escape(caption)}.}}}}\n"
        f"    \\caption{{{latex_escape(caption)}. Source: {latex_escape(source)}.}}\n"
        f"    \\label{{{label}}}\n"
        "\\end{figure}\n"
    )


def listing_or_paragraph(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        return "\\begin{lstlisting}\n" + stripped + "\n\\end{lstlisting}\n"
    m = re.match(r"^(.*payload example:)\s*(\{.*\})$", stripped, flags=re.I)
    if m:
        return para_latex(m.group(1)) + "\\begin{lstlisting}\n" + m.group(2) + "\n\\end{lstlisting}\n"
    return para_latex(stripped)


class Writer:
    def __init__(self) -> None:
        self.files: dict[str, list[str]] = {}
        self.current_path = "chapters/00_front_matter.tex"
        self.current_kind = "front"
        self.list_kind: str | None = None
        self.pending_caption: str | None = None
        self.in_bibliography = False
        self.bibliography_lines: list[str] = []
        self.conversion_notes: list[str] = []
        self.files[self.current_path] = []

    def switch(self, path: str, kind: str) -> None:
        self.close_list()
        self.current_path = path
        self.current_kind = kind
        self.files.setdefault(path, [])

    def write(self, text: str) -> None:
        self.files[self.current_path].append(text)

    def close_list(self) -> None:
        if self.list_kind:
            self.write(f"\\end{{{self.list_kind}}}\n")
            self.list_kind = None

    def write_list_item(self, kind: str, text: str) -> None:
        env = "itemize" if kind == "List Bullet" else "enumerate"
        if self.list_kind != env:
            self.close_list()
            self.list_kind = env
            self.write(f"\\begin{{{env}}}\n")
        self.write(f"\\item {latex_escape(text)}\n")


def make_cover() -> str:
    return r"""\begin{titlepage}
\centering
\vspace*{0.5cm}
{\large People's Democratic Republic of Algeria\par}
{\large Ministry of Higher Education and Scientific Research\par}
\vspace{0.4cm}
{\Large \textbf{École Supérieure en Informatique}\par}
{\large -08 Mai 1945- Sidi Bel Abbès\par}
\vspace{0.8cm}
\fbox{\parbox{0.32\textwidth}{\centering Official ESI-SBA logo placeholder}}
\vspace{0.9cm}

{\Large \textbf{Final Year Thesis}\par}
\vspace{0.2cm}
{\large Combined Master 2 and Engineering Degree\par}
\vspace{0.9cm}

{\large\textbf{French Title}\par}
\vspace{0.2cm}
{\Large Conception et Déploiement d'un Jumeau Numérique pour l'Optimisation d'un Système d'Irrigation Intelligent en Agriculture de Précision\par}
\vspace{0.7cm}

{\large\textbf{English Title}\par}
\vspace{0.2cm}
{\Large Design and Deployment of a Digital Twin for the Optimization of an Intelligent Irrigation System in Precision Agriculture\par}
\vfill

\begin{flushleft}
\textbf{Presented by:}\\
Lebaili Mohamed Ouail -- Computer Systems Engineering (CIS)\\
Senhadji Mohamed Said -- Artificial Intelligence and Data Science (AIDS)\\[0.4cm]
\textbf{Supervised by:} [Insert supervisor names]\\[0.4cm]
\textbf{Academic year:} 2025--2026
\end{flushleft}
\end{titlepage}
\cleardoublepage
"""


def bib_entries() -> str:
    return r"""@article{subeesh2026agriculturaldt,
  author = {Subeesh, A. and Chauhan, N.},
  title = {Agricultural digital twin for smart farming: A review},
  journal = {Green Technologies and Sustainability},
  year = {2026}
}

@article{zhang2025agriculturedtreview,
  author = {Zhang, R. and Zhu, H. and Chang, Q. and Mao, Q.},
  title = {A Comprehensive Review of Digital Twins Technology in Agriculture},
  journal = {Agriculture},
  year = {2025}
}

@article{gund2025bibliometricdt,
  author = {Gund, R. and Badgujar, C. M. and Samiappan, S. and Jagadamma, S.},
  title = {Application of Digital Twin Technology in Smart Agriculture: A Bibliometric Review},
  journal = {Agriculture},
  year = {2025}
}

@article{awais2025precisiondt,
  author = {Awais, M. and Wang, X. and Hussain, S. and Aziz, F. and Mahmood, M. Q.},
  title = {Advancing Precision Agriculture Through Digital Twins and Smart Farming Technologies: A Review},
  journal = {AgriEngineering},
  year = {2025}
}

@article{tsaousidis2026aidt,
  author = {Tsaousidis, M. and Kalampokas, T. and Vrochidou, E. and Papakostas, G. A.},
  title = {AI-Enabled Digital Twins in Agriculture},
  journal = {AI},
  year = {2026}
}

@article{ahsen2025waterdt,
  author = {Ahsen, R. and others},
  title = {Harnessing Digital Twins for Sustainable Agricultural Water Management: A Systematic Review},
  journal = {Applied Sciences},
  year = {2025}
}

@article{garcia2020iotirrigation,
  author = {García, L. and Parra, L. and Jimenez, J. M. and Lloret, J. and Lorenz, P.},
  title = {IoT-Based Smart Irrigation Systems: An Overview on the Recent Trends on Sensors and IoT Systems for Irrigation in Precision Agriculture},
  journal = {Sensors},
  year = {2020}
}

@article{obaideen2022iotirrigation,
  author = {Obaideen, K. and others},
  title = {An overview of smart irrigation systems using IoT},
  journal = {Energy Nexus},
  year = {2022}
}

@article{delcoco2024mlirrigation,
  author = {Del-Coco, M. and Leo, M. and Carcagnì, P.},
  title = {Machine Learning for Smart Irrigation in Agriculture: How Far along Are We?},
  journal = {Information},
  year = {2024}
}

@article{morchid2026iotmlirrigation,
  author = {Morchid, A. and Said, Z. and Tairi, H.},
  title = {Innovative applications of internet of things and machine learning in sustainable agricultural irrigation management: Benefits and challenges},
  journal = {Smart Agricultural Technology},
  year = {2026}
}

@inproceedings{kodali2017mqttirrigation,
  author = {Kodali, R. K. and Sarjerao, B. S.},
  title = {A Low Cost Smart Irrigation System Using MQTT Protocol},
  booktitle = {IEEE Region 10 Symposium},
  year = {2017}
}

@article{balaceanu2019libelium,
  author = {Balaceanu, C. and Suciu, G. and Marcu, I.},
  title = {Libelium-based IoT Monitoring Solution for Precision Agriculture},
  journal = {Journal of E-Technology},
  year = {2019}
}

@article{millan2025tomatodt,
  author = {Millán, S. and Montesinos, C. and Casadesús, J. and Vadillo, J. M. and Campillo, C.},
  title = {Use of a Digital Twin for Water Efficient Management in a Processing Tomato Commercial Farm},
  journal = {Agronomy},
  year = {2025}
}

@article{bellvert2023sentinel,
  author = {Bellvert, J. and others},
  title = {Assimilation of Sentinel-2 Biophysical Variables into a Digital Twin for the Automated Irrigation Scheduling of a Vineyard},
  journal = {Water},
  year = {2023}
}

@article{manocha2024iotdtirrigation,
  author = {Manocha, H. and Sood, S. K. and Bhatia, M.},
  title = {IoT-digital twin-inspired smart irrigation approach for optimal water utilization},
  journal = {Sustainable Computing: Informatics and Systems},
  year = {2024}
}

@inproceedings{tancredi2025mldt,
  author = {Tancredi, F. and Preite, P. and Vignali, G.},
  title = {Digital twin enhanced with Machine Learning Algorithms for Irrigation Management Using Sensor Data},
  booktitle = {Procedia Computer Science},
  year = {2025}
}

@article{qin2025irrigationdrainagedt,
  author = {Qin and others},
  title = {Digital twin-enabled intelligent irrigation-drainage system for precision water-salt management in saline agroecosystems},
  journal = {Agricultural Water Management},
  year = {2025}
}

@article{liu2025cottondt,
  author = {Liu and others},
  title = {Digital twin technology for cotton canopy development: A water-stress perspective},
  journal = {Smart Agricultural Technology},
  year = {2025}
}

@article{elhachimi2025collectiveirrigation,
  author = {El Hachimi and others},
  title = {Towards collective intelligence in agriculture: Deep reinforcement learning and digital twins for efficient management of collective irrigation water distribution systems},
  journal = {Smart Agricultural Technology},
  year = {2025}
}

@book{montgomery2021linearregression,
  author = {Montgomery, D. C. and Peck, E. A. and Vining, G. G.},
  title = {Introduction to Linear Regression Analysis},
  publisher = {Wiley},
  year = {2021}
}

@article{breiman2001randomforest,
  author = {Breiman, L.},
  title = {Random Forests},
  journal = {Machine Learning},
  year = {2001}
}

@misc{fastapi2026docs,
  author = {{FastAPI Documentation}},
  title = {FastAPI framework and automatic OpenAPI documentation},
  year = {2026}
}

@misc{docker2026compose,
  author = {{Docker Documentation}},
  title = {Docker Compose overview},
  year = {2026}
}

@misc{hivemq2026mqtt,
  author = {{HiveMQ}},
  title = {MQTT Essentials and publish/subscribe messaging},
  year = {2026}
}

@misc{openmeteo2026api,
  author = {{Open-Meteo Documentation}},
  title = {Weather Forecast API},
  year = {2026}
}

@misc{libelium2017smartagriculture,
  author = {{Libelium}},
  title = {Smart Agriculture IoT vertical kit and Plug \& Sense sensing platform},
  year = {2017}
}
"""


def write_static_files() -> None:
    (OUT / "preamble.tex").write_text(
        r"""\usepackage[a4paper,top=2.5cm,bottom=2.5cm,inner=3.2cm,outer=2.5cm]{geometry}
\usepackage{fontspec}
\usepackage{polyglossia}
\setmainlanguage{english}
\setotherlanguage{french}
\setotherlanguage{arabic}
\setmainfont{Latin Modern Roman}
% Arabic font fallback: install Amiri or Noto Naskh Arabic if this fallback does not render correctly.
\IfFontExistsTF{Amiri}{\newfontfamily\arabicfont[Script=Arabic]{Amiri}}{%
  \IfFontExistsTF{Noto Naskh Arabic}{\newfontfamily\arabicfont[Script=Arabic]{Noto Naskh Arabic}}{%
    \newfontfamily\arabicfont[Script=Arabic]{Arial}}}
\usepackage{graphicx}
\usepackage{float}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{multirow}
\usepackage[table]{xcolor}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{amsmath}
\usepackage{setspace}
\usepackage{tocloft}
\usepackage{ragged2e}
\usepackage{listings}
\usepackage{hyperref}
\usepackage{cleveref}

\onehalfspacing
\justifying
\emergencystretch=2em
\setlength{\parindent}{1.2cm}
\setlength{\parskip}{0.2em}
\hypersetup{
  colorlinks=true,
  linkcolor=black,
  citecolor=black,
  urlcolor=blue,
  pdftitle={Agrio Digital Twin Smart Irrigation Thesis},
  pdfauthor={Lebaili Mohamed Ouail and Senhadji Mohamed Said}
}
\lstset{
  basicstyle=\ttfamily\small,
  breaklines=true,
  frame=single,
  columns=fullflexible,
  showstringspaces=false
}
""",
        encoding="utf-8",
    )
    (OUT / "main.tex").write_text(
        r"""\documentclass[12pt,a4paper,oneside]{report}
\input{preamble}

\begin{document}

\input{chapters/00_front_matter}

\cleardoublepage
\pagenumbering{arabic}

\input{chapters/00_general_introduction}
\input{chapters/01_precision_agriculture}
\input{chapters/02_digital_twins_iot_ai}
\input{chapters/03_state_of_the_art}
\input{chapters/04_comparative_analysis}
\input{chapters/05_requirements_design}
\input{chapters/06_global_architecture}
\input{chapters/07_backend_database_iot}
\input{chapters/08_digital_twin_ml}
\input{chapters/09_interfaces_control}
\input{chapters/10_deployment}
\input{chapters/11_results_validation}
\input{chapters/12_general_conclusion}

\cleardoublepage
\nocite{*}
\bibliographystyle{IEEEtran}
\bibliography{references}

\appendix
\input{appendices/appendix_a_figures_checklist}
\input{appendices/appendix_b_class_diagram}
\input{appendices/appendix_c_architecture}
\input{appendices/appendix_d_erd}
\input{appendices/appendix_e_payloads}
\input{appendices/appendix_f_capture_guide}
\input{appendices/appendix_g_expansion_notes}
\input{appendices/appendix_h_literature_matrix}
\input{appendices/appendix_i_database_tables}
\input{appendices/appendix_j_api_services}
\input{appendices/appendix_k_algorithms}
\input{appendices/appendix_l_extra_text_blocks}
\input{appendices/appendix_m_defense_positioning}

\end{document}
""",
        encoding="utf-8",
    )
    (OUT / "references.bib").write_text(bib_entries(), encoding="utf-8")
    (OUT / "README.md").write_text(
        """# Agrio Thesis LaTeX Project

Compile from this directory with:

```powershell
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

The project uses XeLaTeX because the thesis contains English, French, and Arabic text. It uses classic BibTeX with `IEEEtran.bst` because `biber`/`biblatex-ieee` was not available in the local environment. If `biblatex-ieee` is installed later, the bibliography setup can be migrated to `biblatex`.

## Figures

All DOCX figure placeholders were converted into LaTeX `figure` environments with framed placeholder boxes. The commented `\\includegraphics` line above each box shows the intended path. Put final images under `figures/cover/`, `figures/chapter_01/` through `figures/chapter_11/`, or `figures/appendix/`, then uncomment and adjust the corresponding `\\includegraphics` line.

## Bibliography

The original numbered bibliography was converted into `references.bib`, and `main.tex` prints all entries with `\\nocite{*}`. In-text references such as `[1]` were preserved because automatic citation-key replacement can corrupt meaning when several bracketed numbers occur in prose. Replace them manually with `\\cite{...}` when the final source mapping is reviewed.

## Fonts

The main font is Latin Modern Roman. Arabic support uses Amiri if installed, then Noto Naskh Arabic, then Arial as a fallback. If XeLaTeX reports a missing Arabic font, install Amiri or Noto Naskh Arabic, or edit `preamble.tex` and replace the `\\arabicfont` fallback with a font available on the machine.

## Manual cleanup checklist

- Replace every framed figure placeholder with the final image.
- Review in-text numeric references `[1]`, `[2]`, etc. and convert them to `\\cite{...}`.
- Verify long tables visually after final compilation; some wide tables may need manual column-width tuning.
- Check the Arabic summary rendering on the target machine, especially if Arial is used as the fallback Arabic font.
- Add supervisor names on the cover page.
""",
        encoding="utf-8",
    )


def convert() -> list[str]:
    if OUT.exists():
        shutil.rmtree(OUT)
    for rel in [
        "chapters",
        "appendices",
        "figures/cover",
        "figures/chapter_01",
        "figures/chapter_02",
        "figures/chapter_03",
        "figures/chapter_04",
        "figures/chapter_05",
        "figures/chapter_06",
        "figures/chapter_07",
        "figures/chapter_08",
        "figures/chapter_09",
        "figures/chapter_10",
        "figures/chapter_11",
        "figures/appendix",
    ]:
        (OUT / rel).mkdir(parents=True, exist_ok=True)

    write_static_files()
    writer = Writer()
    writer.write("\\pagenumbering{roman}\n")
    writer.write(make_cover())

    doc = Document(DOCX)
    skipping_cover = True
    skipping_toc_placeholder = False

    for block in iter_blocks(doc):
        if isinstance(block, Table):
            writer.close_list()
            writer.write(table_to_latex(block, writer.pending_caption))
            writer.pending_caption = None
            continue

        style = block.style.name
        text = clean_text(block.text)
        if not text:
            continue

        if skipping_cover:
            if text == "Dedication":
                skipping_cover = False
            else:
                continue

        if text == "Table of Contents":
            writer.close_list()
            skipping_toc_placeholder = True
            writer.write("\\cleardoublepage\n\\tableofcontents\n\\cleardoublepage\n\\listoffigures\n\\cleardoublepage\n\\listoftables\n\\cleardoublepage\n")
            continue
        if skipping_toc_placeholder:
            if text == "General Introduction" and style.startswith("Heading"):
                skipping_toc_placeholder = False
            else:
                continue

        if text == "Bibliography":
            writer.close_list()
            writer.in_bibliography = True
            writer.switch("chapters/12_general_conclusion.tex", "intro")
            continue
        if writer.in_bibliography:
            if text == "Appendices":
                writer.in_bibliography = False
                continue
            writer.bibliography_lines.append(text)
            continue

        if text in CHAPTER_FILES:
            kind = "intro" if text in {"General Introduction", "General Conclusion"} else "chapter"
            writer.switch(CHAPTER_FILES[text], kind)
            if text in PART_BEFORE:
                writer.write(f"\\part{{{latex_escape(PART_BEFORE[text])}}}\n")
            writer.write(section_command(1, text, kind))
            continue

        if text in APPENDIX_FILES:
            writer.switch(APPENDIX_FILES[text], "appendix")
            writer.write(section_command(1, text, "appendix"))
            continue

        if text.startswith("Part ") and " - " in text:
            continue

        if style == "Caption" and text.startswith("Table "):
            writer.close_list()
            writer.pending_caption = text
            continue

        if style == "Figure Placeholder" or text.startswith("Figure A.") and "[Source:" in text:
            writer.close_list()
            writer.write(figure_to_latex(text))
            continue

        if style in {"List Bullet", "List Number"}:
            writer.write_list_item(style, text)
            continue

        writer.close_list()
        if style.startswith("Heading"):
            level = int(re.search(r"\d+", style).group(0))
            writer.write(section_command(level, text, writer.current_kind))
        else:
            writer.write(listing_or_paragraph(text))

    writer.close_list()

    for path, chunks in writer.files.items():
        target = OUT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(chunks), encoding="utf-8")

    return writer.conversion_notes


if __name__ == "__main__":
    notes = convert()
    print(f"Generated {OUT}")
    if notes:
        print("\n".join(notes))
