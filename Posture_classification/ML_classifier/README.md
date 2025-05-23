# Sleep Posture Classification

This script performs sleep posture classification using sensor data from `decoded_sleep_data.csv`.

---

## Features

- Encodes sleep postures into numeric labels.
- Uses features: `Movement_Value`, `Hour`, and `Minute`.
- Standardizes features before training.
- Splits data into train/test sets (70/30).
- Runs multiple classifiers via `LazyClassifier`.
- Evaluates models using Accuracy, F1 Score, and ROC AUC.
- Selects the best performing model based on accuracy.
- Displays and saves the confusion matrix of the best model.

---

## Usage

1. Ensure `decoded_sleep_data.csv` is in the working directory.
2. Run the script.
3. View printed model comparison results.
4. Find the confusion matrix plot saved as `confusion_matrix.png`.

---

## Dependencies

- pandas
- numpy
- matplotlib
- scikit-learn
- lazypredict

Install with:

```bash
pip install pandas numpy matplotlib scikit-learn lazypredict

