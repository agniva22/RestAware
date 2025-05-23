# Sleep Posture Classification with Neural Network

This script trains and evaluates a neural network model to classify sleep postures using data from `decoded_sleep_data.csv`.

---

## Features

- Encodes categorical label (`Status`) into numeric format.
- Uses features: `Movement_Value`, `Hour`, and `Minute`.
- Standardizes features and splits data into train/test sets (70/30).
- Implements a feedforward neural network with PyTorch.
- Trains the model for 1000 epochs with batch size 32.
- Evaluates performance with Accuracy, F1 Score, ROC, and classification report.

---

## Usage

1. Place `decoded_sleep_data.csv` in the working directory.
2. Run the script.
3. Review console output for training progress and evaluation metrics.

---

## Requirements

- pandas
- numpy
- matplotlib
- scikit-learn
- torch

Install dependencies using:

```bash
pip install pandas numpy matplotlib scikit-learn torch

