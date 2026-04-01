import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

base_dir = r"c:\Users\Hirumi Weerasooriya\Machine-Learning-project\Random Forest"
data_path = os.path.join(base_dir, "loan_dataset_20000.csv")

df = pd.read_csv(data_path)
target_col = "loan_paid_back"

categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
df_processed = df.copy()
label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df_processed[col] = le.fit_transform(df_processed[col].astype(str))
    label_encoders[col] = le

X = df_processed.drop(target_col, axis=1)
y = df_processed[target_col]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train_scaled, y_train)

joblib.dump(rf_model, os.path.join(base_dir, "random_forest_loan_model.pkl"))
joblib.dump(scaler, os.path.join(base_dir, "scaler.pkl"))
joblib.dump(label_encoders, os.path.join(base_dir, "label_encoders.pkl"))

print("Created files:")
print("- random_forest_loan_model.pkl")
print("- scaler.pkl")
print("- label_encoders.pkl")
