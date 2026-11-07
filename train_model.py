import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

# Load dataset
df = pd.read_csv("heart.csv")

# Replace zero values used as invalid measurements
df["RestingBP"] = df["RestingBP"].replace(0, df.loc[df["RestingBP"] != 0, "RestingBP"].mean())
df["Cholesterol"] = df["Cholesterol"].replace(
    0, df.loc[df["Cholesterol"] != 0, "Cholesterol"].mean()
)

X = df.drop("HeartDisease", axis=1)
y = df["HeartDisease"]

numeric_features = [
    "Age", "RestingBP", "Cholesterol",
    "FastingBS", "MaxHR", "Oldpeak"
]

categorical_features = [
    "Sex", "ChestPainType",
    "RestingECG", "ExerciseAngina", "ST_Slope"
]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000))
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42
)

model.fit(X_train, y_train)

print("Test Accuracy:", model.score(X_test, y_test))

# Save complete pipeline
with open("heart_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model saved successfully!")