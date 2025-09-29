# Benchmarking Expert Chatbot Personas

[![Project Status](https://img.shields.io/badge/status-in_progress-blue.svg)](./)
[![Language](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Made with](https://img.shields.io/badge/made%20with-OpenAI%20API-black.svg)](https://platform.openai.com/)
[![License](https://img.shields.io/badge/license-TBD-lightgrey.svg)](#license)

> **Repository URL:** https://github.com/abhigyak47/iphs391_fall2025_miniproject-1_benchmarking-expert-chatbot-personas

A compact, reproducible mini‑project for **IPHS 391 (Fall 2025)** that designs an expert chatbot persona, runs controlled conversations, and **benchmarks persona quality** using a transparent, weighted rubric. The project doubles as an academic portfolio artifact and a practical template for prompt‑engineering experiments.

---

## Table of Contents
- [Overview](#overview)
- [Methodology](#methodology)
  - [Persona Design](#persona-design)
  - [Evaluation Rubric](#evaluation-rubric)
  - [Experiment Protocol](#experiment-protocol)
- [Results](#results)
- [Files Description](#files-description)
- [Usage Instructions](#usage-instructions)
  - [Installation (with `uv`)](#installation-with-uv)
  - [Environment Variables](#environment-variables)
  - [Run the Chatbot Locally](#run-the-chatbot-locally)
  - [Reproducing the Benchmark](#reproducing-the-benchmark)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

This repository implements a **persona‑driven chatbot** and a **repeatable evaluation workflow** for benchmarking conversational quality. The core idea is to define a clear expert **persona prompt**, iterate on it, and score conversation samples with a **weighted rubric** spanning consistency, depth, authenticity, creativity, and engagement. The workflow is intentionally lightweight and file‑based to make audit and replication straightforward.

**Key goals**
- Create a rich persona that behaves consistently across prompts.
- Run comparable chat sessions and capture the interaction logs.
- Score performance using a documented rubric and report the findings.

> The repo currently includes rubric definitions, a system persona prompt, conversation logs, a runnable chatbot script, and a draft report document. See the **Files Description** section for details.

---

## Methodology

### Persona Design

The project centers on a domain persona defined in `prompt_persona.txt`. The prompt encodes:
- **Identity & Voice:** a specific background, tone, and style (e.g., warm, contextual, grounded in lived practice).
- **Behavioral Constraints:** must speak with character, avoid generic/boilerplate responses, and follow conversation norms.
- **Operational Rules:** currency/date guidance, travel/transport defaults, and fallback behaviors for missing context.
- **Mini “QA” Filters:** a pre‑answer self‑check to enforce persona fidelity (e.g., story/voice checks, currency sanity, etc.).

Design principles:
- **Persona-first prompting:** elevate identity, goals, and constraints into the *system* message.
- **Few‑shot positioning (optional):** short exemplars to anchor tone and behavior without overfitting.
- **Guardrails before cleverness:** hard requirements (what *must* be true) precede stylistic flourish (what’s *nice*).

### Evaluation Rubric

Performance is assessed as a weighted linear combination of independent factors (0–100 each):

- **Consistency (20%)** — stays in character; preserves constraints and knowledge boundaries.
- **Depth (10%)** — uses specialized knowledge and nuanced reasoning.
- **Authenticity (25%)** — responses feel real, context‑aware, and grounded in the persona’s background.
- **Creativity (15%)** — engaging, original turns without “persona drift.”
- **Engagement (30%)** — invites dialogue, asks good follow‑ups, and adapts to user cues.

> The canonical rubric and guidance live in `chat_rubric.txt`, with iterative notes in `chat_rubric_history.md`.

Scoring flow:
1. Generate or import multi‑turn conversations (see `chat_history.json`).
2. Apply the rubric per turn or per dialogue segment; average per factor.
3. Compute the weighted total score and summarize in the report.

### Experiment Protocol

1. **Seed** the chatbot with the persona (system message).
2. **Run** a fixed conversation script (or a small set of challenge prompts).
3. **Capture** conversations to `chat_history.json` for transparency.
4. **Score** with the rubric; log the rationale.
5. **Iterate** on the persona and meta‑prompt; repeat steps 2–4.
6. **Report**: synthesize findings in a short paper (see `mp1_chatbot_report.docx`).

---

## Results

- The repository documents rubric definitions and persona evolution. As of this snapshot, representative results and narratives are consolidated in **`mp1_chatbot_report.docx`** and the rubric files. The goal is to keep results **auditable** (chat logs) and **traceable** (prompt + rubric version notes).
- A concise “scorecard” can be maintained in `README.md` (this file) or a dedicated `results.md` as the project progresses.

> Tip: Add a small table summarizing your latest overall score and per‑factor averages when you finalize them.

---

## Files Description

| File | Purpose |
|---|---|
| `prompt_persona.txt` | System persona prompt defining identity, voice, constraints, and safety rails. |
| `run_chatbot.py` | Python script to run the persona‑conditioned chatbot locally (Gradio/OpenAI API). |
| `chat_history.json` | Saved conversation transcripts for scoring and audit. |
| `chat_rubric.txt` | Primary scoring rubric (weights, factor definitions, and scoring guidance). |
| `chat_rubric_history.md` | Iteration notes and changes to the rubric over time. |
| `metaprompt_history.txt` | Notes on meta‑prompting strategies and design decisions. |
| `mp1_chatbot_report.docx` | Mini‑project report combining method, experiments, and findings. |
| `.DS_Store` | System file (safe to ignore). |

> File list reflects the current public repo directory view.

---

## Usage Instructions

### Installation (with `uv`)

This project uses the fast Python package manager **[`uv`](https://docs.astral.sh/uv/)**.

```bash
# 0) Install uv (if not installed)
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell):
iwr https://astral.sh/uv/install.ps1 | iex

# 1) Create & activate a virtual environment
uv venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 2) Install dependencies into the uv environment
uv pip install openai==1.* gradio==4.* python-dotenv
```

### Environment Variables

Set your OpenAI credentials and (optionally) the model:

```bash
# Required: API key (either works)
export OPENAI_API_KEY="sk-..."      # or
export OPENAI_TOKEN="sk-..."

# Optional: override the model used by run_chatbot.py
# The script defaults to: gpt-4o-mini
export OPENAI_MODEL="gpt-4o-mini"
```

> If both `OPENAI_API_KEY` and `OPENAI_TOKEN` are present, the script will use either (API clients typically check `OPENAI_API_KEY` first). If `OPENAI_MODEL` is **not** set, the default **`gpt-4o-mini`** is used.

You may also place these in a `.env` file (loaded via `python-dotenv`):
```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

### Run the Chatbot Locally

```bash
python run_chatbot.py
```

**Common fixes**  
- Ensure `prompt_persona.txt` is in the same directory as `run_chatbot.py` (or update the path).  
- If you see *“model not found”*, set `export OPENAI_MODEL="gpt-4o-mini"` (default) **or** another available model (e.g., `gpt-4o`).  
- If you see *“messages format”* errors, confirm each message dict is of the form `{"role": "...", "content": "..."}` and the conversation list is passed to the API exactly as specified in the OpenAI Python SDK docs.

### Reproducing the Benchmark

1. Run a conversation and export/save to `chat_history.json` (the script can append or overwrite).  
2. Score the conversation using `chat_rubric.txt`. Start with per‑factor notes, then compute weighted scores:  
   \\(\text{Total} = 0.20\times C + 0.10\times D + 0.25\times A + 0.15\times Cr + 0.30\times E\\)  
3. Record deltas and insights in `chat_rubric_history.md` and `metaprompt_history.txt`.  
4. Update `mp1_chatbot_report.docx` with the new results summary.

---

## Contributing

Contributions are welcome. For small fixes (typos, doc polish), open a PR. For larger changes (new personas, rubric factors, or tooling), please open an issue first to discuss scope and alignment with the benchmarking goals.

Suggested improvements:
- Add automated scoring helpers (lightweight scripts) to compute factor averages from annotated logs.
- Provide a `requirements.txt` and `Makefile` for one‑command setup.
- Publish a `results.md` with a compact score table.

---

## License

_No license specified yet._ If you intend for others to reuse your code and materials, consider adding an OSI‑approved license (e.g., MIT) at the repository root as `LICENSE`.

---

## Acknowledgments

- Built for **IPHS 391 (Fall 2025)** mini‑project on persona benchmarking.
- Thanks to project guidance and prior conversations reflected in `metaprompt_history.txt` and rubric files.
- The persona prompt and evaluation framing are inspired by current best practices in prompt engineering and human‑centered evaluation.
