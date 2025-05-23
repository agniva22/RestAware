# RestAware

**RestAware** is a comprehensive framework for **smart, non-invasive sleep monitoring** using a 24GHz FMCW radar sensor. It integrates raw data collection, preprocessing, posture classification, exploratory analysis, and sleep summary generation using large language models (LLMs). This repository supports healthcare researchers and developers in building intelligent, privacy-preserving sleep monitoring systems.

---

## 📁 Repository Structure

### `Dataset/`

- **Description**: Contains all raw and decoded sleep data.
- **Contents**:
  - `raw_sleep_data.csv`: Unprocessed sleep monitoring data captured via radar sensors.
  - `decoded_sleep_data.csv`: Preprocessed and posture-labeled version of raw data for downstream analysis.

### `EDA/`

- **Exploratory Data Analysis** of decoded data.
- Generates:
  - Sleep posture and movement visualizations
  - Per-person statistical summaries (`data_summary.txt`)
  - Visual assets (EPS format)

### `Posture_classification/`

- **Goal**: Classify sleep postures using machine learning and neural networks.
- **Contents**:
  - `lazy_classification.py`: Compares multiple ML models using LazyPredict.
  - `neural_net_posture.py`: Uses a PyTorch neural network to classify sleep posture.
  - Output: performance reports, confusion matrix images, and best model insights.

### `sleep_summary_generation/`

- **Goal**: Automatically generate natural language sleep summaries from posture and movement data.
- **Models Used**:
  - `mistral.py`: [Mistral 7B Instruct](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1)
  - `llama.py`: [LLaMA-2 7B Chat](https://huggingface.co/NousResearch/Llama-2-7b-chat-hf)
  - `falcon.py`: [Falcon-7B-Instruct](https://huggingface.co/tiiuae/falcon-7b-instruct)
- Outputs high-level sleep summaries in plain English.

### `physical_parameters/`

- **Purpose**: Scripts to interface with and collect data using a **24GHz FMCW radar** sensor.
- Includes:
  - Radar initialization and configuration
  - Data capture logic
  - File generation for raw sleep data

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/RestAware.git
cd RestAware

