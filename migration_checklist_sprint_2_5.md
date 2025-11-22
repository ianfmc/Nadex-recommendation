# LIVEWELL / Nadex — Monorepo Migration Checklist (Sprint 2.5)

Use this checklist as you move from the multi-repo setup into the `livewell-nadex` monorepo.  
You can update this file as you go — check off items, add notes, or record small deviations.

---

## 1. Monorepo Bootstrap

- [ ] Create new repo: `livewell-nadex` on GitHub.
- [ ] Clone locally and create base folder structure:
  - [ ] `src/nadex_common/`
  - [ ] `notebooks/`
  - [ ] `configs/`
  - [ ] `sprints/`

- [ ] Add `pyproject.toml` to repo root.
- [ ] Add `requirements.txt` (copy from current primary repo or consolidate later).
- [ ] Add `.gitignore` tailored for Python + notebooks.

---

## 2. Shared Library (`nadex_common`)

- [ ] Copy `strategy_rsi.py` from existing `lib/` into `src/nadex_common/strategy_rsi.py`.
- [ ] Copy `utils_s3.py` from existing `lib/` into `src/nadex_common/utils_s3.py`.
- [ ] Create `src/nadex_common/__init__.py` that re-exports core functions:
  - [ ] `generate_rsi_signals`
  - [ ] `append_runlog_s3`
  - [ ] `save_dataframe_to_s3`, `save_text_to_s3` (if present)
- [ ] From repo root, run `pip install -e .` to enable imports:
  ```bash
  pip install -e .
  ```

---

## 3. Notebooks

- [ ] Copy `nadex-results.ipynb` into `notebooks/`.
- [ ] Copy `nadex-recommendation.ipynb` into `notebooks/`.
- [ ] Copy `nadex-backtesting.ipynb` into `notebooks/`.

- [ ] In each notebook, update imports to use `nadex_common` instead of local `lib/`:
  - [ ] Remove any `sys.path.append("../lib")` or similar.
  - [ ] Replace with:
    ```python
    from nadex_common import generate_rsi_signals, append_runlog_s3
    ```

---

## 4. Configuration

- [ ] Create `configs/` folder in the monorepo.
- [ ] Copy `s3.yaml` into `configs/s3.yaml`.
- [ ] Copy `strategy.yaml` into `configs/strategy.yaml`.
- [ ] Verify notebooks load config from `configs/*.yaml` using the existing loader.

---

## 5. Sprints & Documentation

- [ ] Create `sprints/` folder.
- [ ] Add existing sprint files:
  - [ ] `sprint_1.md`
  - [ ] `sprint_2.md`
  - [ ] `sprint_2_5.md`
  - [ ] `sprint_3.md`
- [ ] Add root `README.md` explaining the new structure (this file).

- [ ] Optional: update the LIVEWELL Canvas to reference the new monorepo structure and URL.

---

## 6. Validation

For each notebook:

- [ ] `notebooks/nadex-results.ipynb` runs end-to-end using `configs/s3.yaml`:
  - [ ] Reads PDFs / historical inputs.
  - [ ] Writes cleaned CSVs to the correct S3 prefixes.
  - [ ] Updates manifest and run log as before.

- [ ] `notebooks/nadex-recommendation.ipynb` runs end-to-end:
  - [ ] Reads cleaned history from S3.
  - [ ] Uses `nadex_common.generate_rsi_signals` correctly.
  - [ ] Writes recommendation artifacts and summary.
  - [ ] Appends to run log.

- [ ] `notebooks/nadex-backtesting.ipynb` runs correctly (once wired to shared lib in Sprint 3).

---

## 7. Legacy Repos

- [ ] In `Nadex-results` repo:
  - [ ] Update `README` to point to `livewell-nadex`.
  - [ ] Optionally mark the repo as archived in GitHub settings.

- [ ] In `Nadex-recommendation` repo:
  - [ ] Update `README` to point to `livewell-nadex`.
  - [ ] Optionally mark the repo as archived.

- [ ] In `Nadex-backtesting` repo:
  - [ ] Update `README` to point to `livewell-nadex`.
  - [ ] Optionally mark the repo as archived.

---

## Notes / Variations

Use this space to capture any deviations from the plan (for example, if you decide to keep one repo active as a staging area or you introduce additional shared modules):

- 
