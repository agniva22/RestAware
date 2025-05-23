# Sleep Posture Data Processing Scripts

This repository contains Python scripts for processing raw sleep sensor data collected from 25 participants. The workflow includes:

1. **Merging** multiple raw data files into a single aggregated CSV.
2. **Decoding** raw sensor values into interpretable sleep posture labels.

---

## 📂 Scripts Overview

### `merge_data.py`

Merges individual raw CSV files (one per participant) into a single aggregated dataset.

#### ✅ Features
- Automatically assigns a unique participant ID
- Concatenates all data into one clean CSV

#### 🚀 Usage

```bash
python merge_data.py --input_dir path/to/raw_files --output_file raw_sleep_data.csv
python decode_data.py --input_file raw_sleep_data.csv --output_file decoded_sleep_data.csv
```
