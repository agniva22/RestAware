# Sleep Data Visualization & Exploitory Analysis

This script processes the decoded sleep posture dataset (`decoded_sleep_data.csv`) to generate:

- Time-series scatter plots of sleep **Posture** and **Status**
- Line plots of **Movement Value** over time  
- Summary statistics per participant saved to `data_summary.txt`  
- All plots saved as EPS images in the `./Image` directory  

---

## How It Works

- Reads `decoded_sleep_data.csv` with columns like `Name`, `millis`, `Status`, `Posture`, and `Movement_Value`.
- Converts `millis` to timestamps relative to script runtime.
- Generates individual plots for each participant.
- Outputs a summary text file with counts and descriptive stats.

---

## Usage

1. Place `decoded_sleep_data.csv` in the script folder.
2. Run the script.
3. Check the `Image/` folder for plots.
4. Open `data_summary.txt` for the textual summary.

---

## Dependencies

- pandas
- matplotlib
- seaborn

Install with:

```bash
pip install pandas matplotlib seaborn

