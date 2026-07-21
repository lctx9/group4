# Interactive Terminal Execution Feedback for Repository-Level Test Generation: An Empirical Study on TestExplora

[![Paper](https://img.shields.io/badge/Paper-IEEE%20Format-blue.svg)](paper/output/paper_final.pdf)
[![Presentation](https://img.shields.io/badge/Slides-PDF%2FPPTX-orange.svg)](presentation/slides_final.pdf)
[![Benchmark](https://img.shields.io/badge/Benchmark-TestExplora-green.svg)](https://github.com/microsoft/TestExplora)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

**Group 4 — FPT University, Vietnam**  
* **Le Chi Tam** (SE190322) — Lead Author & Data Infrastructure
* **Le Tran Gia Huy** (SE193344) — Project Lead & Pipeline Integration
* **Nguyen Tien Phu** (SE190131) — LLM Runner & Agent Interfaces
* **Truong Van An** (SE194268) — Metrics & Statistical Analysis

---

## 📌 Project Overview

Automated software testing is central to software quality assurance, yet static language models used for test generation exhibit a **compliance bias** — passively accepting erroneous output rather than identifying underlying logic flaws. 

This repository contains the complete replication package for our empirical study evaluating a dual-agent, open-source system pairing **DeepSeek-V3** (operating via the SWE-agent CLI bash terminal) with **Llama-3.3-70B** on **1,552 Python tasks** from the **TestExplora** benchmark.

### 🌟 Key Empirical Results
* **Pass@1 Fail-to-Pass (F2P) Rate:** **35.05% ± 0.93%** (more than double the static Plain Context baseline of **16.60%**).
* **Pass@3 Cumulative F2P Rate:** **71.59% ± 45.10%** (median: 100.00%).
* **Statistical Significance:** Paired one-tailed Wilcoxon signed-rank test ($W = 239,987.5$, $p = 0.000000 < 0.05$; Cliff's $\delta = 0.3018$, medium effect size; Pass@3 Cliff's $\delta = 0.7412$, large effect size).
* **Execution Cost:** Total API execution cost for all 4,656 agent invocations was approximately **$10.00–$12.00 USD** via paid OpenRouter API endpoints.

---

## 📂 Repository Structure

```
.
├── data/                       # Dataset snapshots & pilot sampling
│   ├── raw/                    # Raw TestExplora parquet data & source README
│   └── pilot_sample.csv        # Stratified pilot dataset
├── figures/                    # 300 DPI high-resolution figures for paper
├── paper/                      # Complete LaTeX paper source & compiled PDF
│   ├── main.tex                # Primary IEEEtran paper entry point
│   ├── references.bib          # 28 peer-reviewed BibTeX references (with DOIs & URLs)
│   ├── output/paper_final.pdf  # Compiled final paper PDF
│   ├── quality/ai_checklog.md  # Quality assurance checklist
│   └── sections/               # 8 modular paper sections (00_abstract to 07_conclusion)
├── presentation/               # Final presentation slides
│   ├── slides_final.pdf        # PDF slide deck
│   └── slides_final.pptx       # PowerPoint presentation deck
├── results/                    # Raw outputs & statistical notebooks
│   ├── full_llm_output.csv     # Complete 4,656 agent execution results
│   ├── full_analysis.ipynb     # Jupyter notebook reproducing all statistical tests & p-values
│   └── summary.csv             # Per-task aggregated metrics
├── scripts/                    # Python automation & evaluation scripts
│   ├── run_full_experiment.py  # SWE-agent execution runner script
│   ├── analyze_full_experiment.py # Statistical test calculator (Wilcoxon & Cliff's delta)
│   └── generate_figures.py     # Matplotlib figure generation pipeline
├── .gitignore                  # Clean repository exclusion rules
└── README.md                   # Project documentation & replication guide
```

---

## 🚀 How to Reproduce the Experiment

### 1. Prerequisites & Environment Setup
Clone this repository and install Python dependencies:
```bash
git clone https://github.com/lctx9/group4.git
cd group4
pip install scipy pandas numpy matplotlib seaborn jupyter openpyxl
```

### 2. API Key Configuration
Set your OpenRouter API key environment variable (no API keys are hardcoded in this repository):
```powershell
# Windows PowerShell
$env:OPENROUTER_API_KEY="your_openrouter_api_key_here"
```
```bash
# Linux / macOS
export OPENROUTER_API_KEY="your_openrouter_api_key_here"
```

### 3. Running the Dual-Agent Execution Pipeline
To execute the interactive terminal exploration agent (`DeepSeek-V3`) and code fixer agent (`Llama-3.3-70B-Instruct`):
```bash
python scripts/run_full_experiment.py
```

### 4. Running Statistical Analysis & Generating Paper Figures
To recalculate Wilcoxon signed-rank tests, Cliff's delta effect sizes, and reproduce all figures:
```bash
# Run statistical analysis script
python scripts/analyze_full_experiment.py

# Generate high-resolution figures
python scripts/generate_figures.py
```

Or open `results/full_analysis.ipynb` in Jupyter Notebook to interactively verify all table figures and $p$-values.

---

## 📄 License & Citation

This project is licensed under the MIT License. If you use this codebase or benchmark results in your research, please cite:

```bibtex
@article{group4_testexplora_2026,
  author    = {Le Chi Tam and Le Tran Gia Huy and Nguyen Tien Phu and Truong Van An},
  title     = {Interactive Terminal Execution Feedback for Repository-Level Test Generation: An Empirical Study on TestExplora},
  journal   = {FPT University Technical Report},
  year      = {2026}
}
```
