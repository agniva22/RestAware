# Sleep Summary Generation with Large Language Models

This repository contains scripts to generate sleep summaries from posture and movement data using three different large language models (LLMs):

- **Falcon** (`falcon.py`) — [tiiuae/falcon-7b-instruct]
- **LLaMA** (`llama.py`) — [NousResearch/Llama-2-7b-chat-hf]
- **Mistral** (`mistral.py`) — [mistralai/Mistral-7B-Instruct-v0.1]

---

## Overview

Each script loads decoded sleep data, processes it, and generates natural language summaries describing sleep patterns, postures, and movements using a specific LLM.

---

## Scripts

### `falcon.py`

- Uses the Falcon 7B Instruct model for generating detailed sleep summaries.
- Leverages the instruction-tuned version for improved conversational quality.

### `llama.py`

- Uses LLaMA 2 7B Chat HF model.
- Designed for chat-based interactions and contextual summaries.

### `mistral.py`

- Uses Mistral 7B Instruct v0.1 model.
- Instruction-tuned for high-quality text generation on tasks like summarization.

---

## Usage

1. Ensure dependencies and model weights are correctly set up (e.g., via Hugging Face Transformers).
2. Prepare your decoded sleep data file (e.g., `decoded_sleep_data.csv`).
3. Run any of the scripts:

```bash
python falcon.py --input decoded_sleep_data.csv --output falcon_summary.txt
python llama.py --input decoded_sleep_data.csv --output llama_summary.txt
python mistral.py --input decoded_sleep_data.csv --output mistral_summary.txt

