import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

print("🚀 Starting TrueFit AI Model Training...")

# Load dataset
df = pd.read_csv('model/dataset.csv')
print(f"✅ Dataset loaded: {len(df)} records, {df['career'].nunique()} careers")

# Combine features
df['combined'] = (
    df['technical_skills'] + ' ' +
    df['technical_skills'] + ' ' +
    df['soft_skills'] + ' ' +
    df['education'] + ' ' +
    df['experience'] + ' ' +
    df['career_interest'] + ' ' +
    df['career_interest']
)

X = df['combined']
y = df['career']

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.15, random_state=42
)

# Pipeline with RandomForest
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=2000,
        ngram_range=(1, 3),
        stop_words='english',
        sublinear_tf=True,
        min_df=1
    )),
    ('clf', RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        max_depth=15,
        min_samples_split=2
    ))
])

# Train
print("🔄 Training model...")
pipeline.fit(X_train, y_train)

# Accuracy
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model Accuracy: {accuracy * 100:.1f}%")

# Save
os.makedirs('model', exist_ok=True)
joblib.dump(pipeline, 'model/career_model.pkl')
joblib.dump(le, 'model/label_encoder.pkl')

print("✅ Model saved!")
print(f"✅ Careers covered: {len(le.classes_)}")
print("🎉 Training Complete!")