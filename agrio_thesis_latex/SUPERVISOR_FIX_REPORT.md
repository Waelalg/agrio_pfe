# Supervisor Fix Report

Date: 2026-06-24

Backup branch created before edits:

- `backup-before-supervisor-fixes-20260624`

## Files Modified

- `main.tex`
- `preamble.tex`
- `README.md`
- `references.bib`
- `chapters/00_general_introduction.tex`
- `chapters/01_precision_agriculture.tex`
- `chapters/02_digital_twins_iot_ai.tex`
- `chapters/03_state_of_the_art.tex`
- `chapters/04_comparative_analysis.tex`
- `chapters/06_global_architecture.tex`
- `figures/research_papers/FIGURE_SOURCES.md`
- `figures/chapter_06/6.3.png`
- `figures/chapter_06/Figure 6.4 -- Internal backend architecture of the FastAPI-based Digital Twin platform.png`

Build-generated tracked files were also updated by the successful LaTeX build:

- `main.aux`
- `main.bbl`
- `main.blg`
- `main.lof`
- `main.log`
- `main.lot`
- `main.out`
- `main.pdf`
- `main.toc`

## Sections Rewritten

- General Introduction: removed detailed description of the implemented platform, architecture, stack, dashboard, ML model, database, actuator, pump-control implementation, and system name.
- Chapter 1: rewritten as theoretical background covering precision agriculture, smart irrigation, soil--plant--atmosphere variables, IoT, MQTT, ML decision support, Digital Twin concepts, and the progression from monitoring to control.
- Chapter 2: rewritten as related work/state of the art based only on original research papers and including the requested comparison table.
- Chapter 3: rewritten as research gap and scientific positioning, with implementation details postponed to later chapters.
- Chapter 4: rewritten as a concise comparative analysis using original research papers only.
- Chapter 6: updated the MQTT communication layer and backend layer with focused implementation views, real MQTT topics, and a simplified backend architecture that excludes non-implemented production services.

## Citations Added or Standardized

The early chapters now cite these original research papers:

- `kodali2017mqttirrigation`
- `balaceanu2019libelium`
- `bellvert2023vineyarddt`
- `millan2025tomatodt`
- `tancredi2025irrigationdt`
- `elhachimi2025collectiveirrigationdt`
- `kallenberg2025interoperabledt`
- `eddaoudi2024predictiveirrigation`
- `gupta2025iotirrigation`
- `liu2025cottondt`

## Figures Added

Three research-paper figures were extracted and inserted:

- `figures/research_papers/tancredi_ml_dt_irrigation.png` in Chapter 1, Machine learning for irrigation decision support.
- `figures/research_papers/bellvert_vineyard_dt.png` in Chapter 1, Digital Twin concepts in agriculture.
- `figures/research_papers/millan_tomato_dt.png` in Chapter 2, Digital Twin irrigation systems in vineyards and tomato farms.

The figure source log was updated at:

- `figures/research_papers/FIGURE_SOURCES.md`

Chapter 6 implementation figures updated:

- `figures/chapter_06/6.3.png` inserted as Figure 6.3 with label `fig:mqtt_communication_architecture`.
- `figures/chapter_06/Figure 6.4 -- Internal backend architecture of the FastAPI-based Digital Twin platform.png` inserted as Figure 6.4 with label `fig:backend_architecture`.
- `figures/chapter_06/Figure 6.5 -- Digital Twin processing architecture from live sensor data to simulation and recommendation.png` inserted as Figure 6.5 with label `fig:digital_twin_processing_workflow`.
- `figures/chapter_06/Figure 6.6 -- Docker Compose deployment architecture of the Agrio platform.png` inserted as Figure 6.6 with label `fig:docker_compose_deployment_architecture`.
- `figures/chapter_06/Figure 6.7 -- Detailed technical architecture of the implemented Digital Twin smart irrigation platform.png` inserted as Figure 6.7 with label `fig:simplified_technical_architecture`; the image content is the new simplified technical architecture.

The MQTT topics reference image was not inserted as a numbered figure because it contains an embedded "Figure 6.4" title. The MQTT topics are instead documented in Table `tab:mqtt_topics`.

Chapter 6 backend figure verification:

- The simplified backend figure was checked against the supervisor's excluded-service list; unsupported production services are not shown.

Chapter 6 Digital Twin workflow update:

- The Digital Twin layer was expanded to explain live data acquisition, MQTT ingestion and persistence, zone state update, AI prediction, what-if simulation, and recommendation with supervised action.
- The Machine learning, Recommendation and validation, and Actuator and feedback sections were shortened so they complement Figure 6.5 without repeating the full workflow explanation.
- Non-implemented components listed by the supervisor were not added to the Chapter 6 Digital Twin workflow text.

Chapter 6 deployment update:

- The deployment architecture section was expanded around Figure 6.6 with service-level explanations for the backend, PostgreSQL, ML service, frontend, scheduler, MQTT communication, and ngrok prototype access.
- Port mappings were documented as Table `tab:docker_compose_ports`.
- Runtime configuration categories were documented as Table `tab:runtime_configuration`.
- Persistent storage, environment configuration, and deployment operations were described as text instead of separate image blocks.
- No Docker Compose file was found in `C:\Users\lenovo\Desktop\pfe`, so the service ports were taken from existing thesis deployment documentation and should be verified against the final implementation package.
- The Figure 6.6 image still contains some visual labels that were not verified from a Compose file, such as reverse-proxy and external administration/monitoring wording. These labels are not described as implemented services in Chapter 6 text.

Chapter 6 simplified technical architecture update:

- Figure 6.7 was changed from the old dense technical architecture block to the simplified layered view.
- The text below Figure 6.7 now explains the field and edge layer, communication layer, backend platform, Digital Twin service, ML service, recommendation/control, scheduler, data layer, client interfaces, infrastructure/deployment, external integrations, and arrow semantics.
- Old Figure 6.7 labels were replaced with `fig:simplified_technical_architecture`.
- Non-implemented services listed by the supervisor were not added to the Chapter 6 text as implemented components. Optional visual items in the image, such as maps, ngrok, and optional MQTT worker, are described only as optional or conditional where mentioned.

Chapter 7 MQTT payload update:

- The old overloaded Figure 7.1 payload image was removed from the Chapter 7 source.
- Three focused cropped payload visuals were inserted as continued parts of Figure 7.1:
  - `figures/chapter_07/7.1.1_sensor_ingestion_payload_cropped.png`
  - `figures/chapter_07/7.1.2_wemos_status_payload_cropped.png`
  - `figures/chapter_07/7.1.3_actuator_command_payload_cropped.png`
- Final payload labels are `fig:mqtt_payload_sensor_ingestion`, `fig:mqtt_payload_wemos_status`, and `fig:mqtt_payload_actuator_command`.
- The WeMos command values table was added as `tab:wemos_command_values`.
- The original `7.1.1.png`, `7.1.2.png`, and `7.1.3.png` images contained embedded visible figure numbers; cropped copies were created to avoid conflicts with LaTeX numbering.

Chapter 8 dataset and ML workflow update:

- Figure 8.1 was updated to the simplified dataset adaptation and feature-engineering workflow image.
- The final Figure 8.1 label is `fig:dataset_feature_engineering_workflow`.
- The text around Figure 8.1 now explains dataset adaptation, cleaning, normalization, feature engineering, target separation, Random Forest training, evaluation, and metadata export.
- A feature-group table was added as `tab:ml_feature_groups`.
- The `need_irrigation` and `suggested_hour` model explanations were rewritten to avoid overclaiming the mathematical formulation of the second task.
- Training-time dataset preparation is now explicitly distinguished from runtime inference through the ML service.
- Unsupported feature-engineering elements such as VPD, rolling statistics, lag features, StandardScaler, online learning, drift detection, crop-growth modeling, yield prediction, and full optimization are not described as implemented training features.

Skipped figures:

- Balaceanu et al. Libelium monitoring figure: skipped because the local PDF states all rights reserved.
- Kodali and Sarjerao MQTT architecture figure: skipped because no reuse license is visible in the local IEEE PDF.

## Review Papers Excluded From Main Source Pool

The rewritten early chapters avoid using review, overview, systematic-review, bibliometric-review, and student-thesis sources as main citations. The bibliography was cleaned so only explicitly cited original research papers are printed.

Excluded from the rewritten early chapters as main sources:

- Subeesh and Chauhan review
- Zhang et al. review
- Gund et al. bibliometric review
- Awais et al. review
- Tsaousidis et al. AI-enabled Digital Twin overview/review source
- Ahsen et al. systematic review
- Garcia et al. IoT overview
- Obaideen et al. IoT overview
- Del-Coco et al. ML smart irrigation review
- Morchid et al. review/context source
- Jones et al. systematic Digital Twin review
- Yao et al. systematic Digital Twin review
- El Ouahabi Morocco water-security narrative/context paper
- Tlemcen student thesis

## TODOs Requiring Manual Verification

- Confirm with the supervisor whether the all-rights-reserved Balaceanu figure and unclear-license Kodali IEEE figure may be included under the institution's thesis policy.
- If four Chapter 1 figures are mandatory, use either supervisor-approved reproduction of those two figures or thesis-owned schematics adapted from the original papers.
- Visually review the wide landscape comparison table in Chapter 2 after printing/exporting.
- Later implementation chapters should split overloaded diagrams into smaller focused visuals.

## Build Status

Command run from `agrio_thesis_latex`:

```powershell
latexmk -xelatex -interaction=nonstopmode main.tex
```

Chapter 6 rebuild command:

```powershell
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

Result: successful. `main.pdf` was generated and the final `latexmk` pass reported all targets up to date.

Log check found no LaTeX errors, missing files, or undefined citations. Remaining warnings are typography/font/PDF-conversion warnings, including existing overfull lines in appendices and an Amiri ToUnicode warning.

## Structure and Validation Pass - 2026-06-25

Branch created before this pass:

- `fix-structure-validation-pass`

### Files Updated

- `chapters/03_state_of_the_art.tex`
- `chapters/04_comparative_analysis.tex`
- `chapters/06_global_architecture.tex`
- `chapters/07_backend_database_iot.tex`
- `chapters/08_digital_twin_ml.tex`
- `chapters/09_interfaces_control.tex`
- `chapters/10_deployment.tex`
- `chapters/11_results_validation.tex`
- `appendices/appendix_a_figures_checklist.tex`
- `appendices/appendix_h_literature_matrix.tex`
- `appendices/appendix_i_database_tables.tex`
- `appendices/appendix_j_api_services.tex`
- `appendices/appendix_m_defense_positioning.tex`
- regenerated build outputs including `main.pdf`, `main.lof`, `main.toc`, `main.aux`, and `main.log`

### Changes Applied

- Split the former continued Chapter 7 payload sequence into independent figures 7.1, 7.2, and 7.3.
- Removed the previously requested FastAPI OpenAPI and PostgreSQL placeholder text blocks.
- Kept figure captions without explicit source-attribution lines, following the latest formatting request.
- Rewrote Chapter 11 as scenario-based validation using only available Chapter 11 figures 11.1, 11.2, and 11.3.
- Removed Chapter 11 placeholder figure boxes for missing figures 11.4-11.9.
- Replaced Appendix A's draft insertion checklist with a final-status figure note.
- Reworked Appendix H so review papers are explicitly excluded as orientation sources and original research papers remain the main source pool.
- Strengthened conclusions in Chapters 6, 8, 9, and 10.
- Removed or softened unverified deployment-service wording and API-documentation screenshot expectations.

### Verification

Final build command:

```powershell
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

Result: successful. The generated PDF is:

- `main.pdf`
- size: 31,718,844 bytes
- timestamp: 2026-06-25 13:27:13

Final scans found:

- no LaTeX errors, missing files, fatal errors, undefined references, or undefined citations in `main.log`
- no remaining explicit source-caption text in thesis sources, `main.lof`, or `main.aux`
- no remaining draft figure-insertion placeholders or removed Figure 7.3/7.4 placeholder text
- no continued-caption or empty optional-caption pattern in Chapter 7
- List of Figures now contains separate Figure 7.1, 7.2, and 7.3 payload entries

Remaining manual visual TODO:

- Several Chapter 7 ERD/runtime screenshots still contain embedded old figure numbers inside the image pixels. LaTeX numbering is correct, but those images should be regenerated or cropped if exact visual numbering inside the screenshots is required.
