# LIVEWELL / Nadex-recommendation

This repository is part of the **LIVEWELL** initiative: building an ML-driven workflow for stock price prediction and Nadex binary option recommendations.

## Overview
- **Nadex-results** → stores and processes raw/extracted results data.
- **Nadex-recommendation** → generates daily trading recommendations.
- **Nadex-backtesting** → R&D notebooks for testing strategies and validating ideas.

**This is the Nadex-recommendation repository.**

- All runnable code lives in **`notebooks/`** (Jupyter).
- **Do not commit data or outputs.** Historical/results/reports live in **S3** (see `configs/s3.yaml`).
- Repo configuration lives in **`configs/`** (e.g., `s3.yaml`, `strategy.yaml`, `risk.yaml`, `anonymization.yaml`, `experiment.yaml`).

- The required notebooks/contracts.csv file lists the contracts that will be available for trading the next day
- Run the notebooks/nadex-recommendation.ipynb file
- Recommendations are provided and are pushed to an S3 bucket

## Quickstart
1) Clone and install
```bash
git clone https://github.com/ianfmc/<repo-name>
cd <repo-name>
pip install -r requirements.txt
```

2. Configure

- Set AWS creds via env/SSO
- Edit `configs/s3.yaml` (required)
- If this is **Nadex-recommendation**, also edit `configs/strategy.yaml` (and optional `risk.yaml`)

3. Run

- Open a notebook in `notebooks/` (e.g., `01_signals.ipynb`, `02_backtest.ipynb`, or repo-specific notebook)
- Artifacts (CSV/HTML/logs) will be written to **S3** prefixes from `configs/s3.yaml`


## License

MIT License

Copyright (c) 2025 Ian F. McCallum

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


