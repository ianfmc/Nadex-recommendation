# LIVEWELL / Nadex — Sprints Overview

This folder tracks the incremental evolution of the LIVEWELL Nadex workflow (results, recommendation, and backtesting) in short, reviewable sprints.

## Files

- `sprint_1.md` — **Historical Results MVP**  
  Extract and normalize historical Nadex Daily Results PDFs in **Nadex-results**, write cleaned CSVs to S3, maintain a processed manifest and run log.

- `sprint_2.md` — **Configuration, Shared Library, and Recommendation Pipeline**  
  Align **Nadex-recommendation** with the Sprint 1 architecture: externalized configs, shared `lib/`, run logging, and guardrail parameters in `strategy.yaml`.

- `sprint_3.md` — **Bucket Guards + Backtesting Baseline (Planned)**  
  Add runtime S3 bucket guards in both repos and stand up the A-2 backtesting baseline (single source of truth via `lib/strategy_rsi.py`) to compare RSI modes/thresholds and pick daily defaults.

## Usage

- Each sprint file captures:
  - **Sprint goal**
  - **User stories targeted**
  - **Definition of done**
  - **End-of-sprint status & notes**
  - **(Optional) Retrospective**

- When starting a new sprint:
  1. Copy the previous `sprint_X.md` as a template.
  2. Update dates, goal, and stories targeted.
  3. At the end of the sprint, capture actuals and a brief retrospective.

This keeps the main README focused and lets the **sprints/** folder act as the project’s NATOPS logbook for how the system evolved over time.
