import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

# Load ML-ready CSV
df = pd.read_csv("ml_matches.csv")

# Features and label
X = df[["tot_diff", "auto_diff", "teleop_diff", "endgame_diff"]]
y = df["label"]

# Split into train and test (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train logistic regression
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate performance
y_pred = model.predict(X_test)
print("=== Performance on Test Set ===")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the trained model
joblib.dump(model, "match_predictor.pkl")
print("Model trained and saved as 'match_predictor.pkl'")
