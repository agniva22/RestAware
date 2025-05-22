import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, f1_score, 
    roc_auc_score, classification_report, ConfusionMatrixDisplay
)

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

df = pd.read_csv("./decoded_sleep_data.csv")
df['Time'] = pd.to_datetime(df['millis'], unit='ms')
df['Hour'] = df['Time'].dt.hour
df['Minute'] = df['Time'].dt.minute

le_posture = LabelEncoder()
le_status = LabelEncoder()
df['Posture_Encoded'] = le_posture.fit_transform(df['Posture'])
df['Status_Encoded'] = le_status.fit_transform(df['Status'])

features = ['Movement_Value', 'Hour', 'Minute']
X = StandardScaler().fit_transform(df[features])
y_posture = df['Posture_Encoded'].values

X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(X, y_posture, test_size=0.3, random_state=42)

X_train_tensor = torch.tensor(X_train_p, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train_p, dtype=torch.long)
X_test_tensor = torch.tensor(X_test_p, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test_p, dtype=torch.long)

train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

class PostureClassifier(nn.Module):
    def __init__(self, input_dim, num_classes):
        super(PostureClassifier, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        return self.net(x)

model = PostureClassifier(input_dim=X_train_p.shape[1], num_classes=len(np.unique(y_train_p))).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(1000):
    model.train()
    for batch_x, batch_y in train_loader:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)
        
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f"Epoch [{epoch+1}/1000], Loss: {loss.item():.4f}")

model.eval()
all_preds = []
all_labels = []

with torch.no_grad():
    for batch_x, batch_y in test_loader:
        batch_x = batch_x.to(device)
        outputs = model(batch_x)
        _, predicted = torch.max(outputs, 1)
        all_preds.extend(predicted.cpu().numpy())
        all_labels.extend(batch_y.numpy())

print("\nClassification Report:")
print(classification_report(all_labels, all_preds, target_names=le_posture.classes_))

accuracy = accuracy_score(all_labels, all_preds)
balanced_acc = balanced_accuracy_score(all_labels, all_preds)
f1 = f1_score(all_labels, all_preds, average='weighted')

with torch.no_grad():
    outputs = model(torch.tensor(X_test_p, dtype=torch.float32).to(device))
    probs = torch.softmax(outputs, dim=1).cpu().numpy()

try:
    y_test_cat = np.eye(len(np.unique(y_train_p)))[y_test_p]
    roc_auc = roc_auc_score(y_test_cat, probs, multi_class='ovr')
except:
    roc_auc = "N/A"

print("\nPosture Classification Results:")
print(f"{'Accuracy:':<20} {accuracy:.4f}")
print(f"{'Balanced Accuracy:':<20} {balanced_acc:.4f}")
print(f"{'F1 Score:':<20} {f1:.4f}")
print(f"{'ROC AUC:':<20} {roc_auc if roc_auc == 'N/A' else f'{roc_auc:.4f}'}")

with open("./performance_report.txt", "w") as f:
    f.write("Posture Classification Results (Neural Network):\n")
    f.write(f"Accuracy: {accuracy:.4f}\n")
    f.write(f"F1 Score: {f1:.4f}\n")
    f.write(f"ROC AUC: {roc_auc if roc_auc == 'N/A' else f'{roc_auc:.4f}'}\n\n")

plt.figure(figsize=(10, 10))
ConfusionMatrixDisplay.from_predictions(
    all_labels,
    all_preds,
    display_labels=le_posture.classes_,
    cmap="Blues"
)
plt.xticks(rotation=25)
plt.title("Posture - Neural Network")
plt.savefig('./confusion_matrix.png')
plt.clf()
