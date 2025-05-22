import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
    ConfusionMatrixDisplay,
)
from lazypredict.Supervised import LazyClassifier
from sklearn.base import clone
import time

df = pd.read_csv("./decoded_sleep_data.csv")
df['Time'] = pd.to_datetime(df['millis'], unit='ms')
df['Hour'] = df['Time'].dt.hour
df['Minute'] = df['Time'].dt.minute

le_posture = LabelEncoder()
df['Posture_Encoded'] = le_posture.fit_transform(df['Posture'])

features = ['Movement_Value', 'Hour', 'Minute']
X = StandardScaler().fit_transform(df[features])
y_posture = df['Posture_Encoded']

X_train, X_test, y_train, y_test = train_test_split(X, y_posture, test_size=0.3, random_state=42)

clf_posture = LazyClassifier(verbose=0, ignore_warnings=True)
models_posture, _ = clf_posture.fit(X_train, X_test, y_train, y_test)

results = []

for model_name in models_posture.index:
    model = clone(clf_posture.models[model_name])
    start_time = time.time()
    model.fit(X_train, y_train)
    time_taken = time.time() - start_time

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')

    try:
        roc = roc_auc_score(y_test, model.predict_proba(X_test), multi_class='ovr')
    except:
        roc = np.nan

    results.append({
        "Model": model_name,
        "Accuracy": round(acc, 4),
        "ROC": round(roc, 4) if not np.isnan(roc) else "N/A",
        "F1 Score": round(f1, 4),
        "Time Taken": round(time_taken, 2),
        "Model_Obj": model  
    })

results_df = pd.DataFrame(results).set_index("Model")
print("Posture Classification Results:")
print(results_df[["Accuracy", "ROC", "F1 Score", "Time Taken"]])

best_model_name = results_df["Accuracy"].idxmax()
best_model_row = results_df.loc[best_model_name]
best_model = best_model_row["Model_Obj"]

print("\nBest Model:", best_model_name)
print("Accuracy:", best_model_row["Accuracy"])
print("F1 Score:", best_model_row["F1 Score"])
print("ROC:", best_model_row["ROC"])

y_best_pred = best_model.predict(X_test)
plt.figure(figsize=(10, 10))
ConfusionMatrixDisplay.from_predictions(
    y_test, y_best_pred, display_labels=le_posture.classes_, cmap="Blues"
)
plt.xticks(rotation=25)
plt.title(f"Posture - Best Model: {best_model_name}")
plt.savefig('./confusion_matrix.png')
plt.clf()
