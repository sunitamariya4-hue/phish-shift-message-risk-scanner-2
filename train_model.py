import os
import re
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. Load split datasets (Deduplicated and campaign-separated)
train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")

# Combine title and body text for feature extraction
X_train_text = train_df['subject_or_title'].fillna('') + " " + train_df['body_text'].fillna('')
y_train = train_df['label']

X_test_text = test_df['subject_or_title'].fillna('') + " " + test_df['body_text'].fillna('')
y_test = test_df['label']

# ---------------------------------------------------------
# Model 1: Rule-Based Classifier (Baseline)
# ---------------------------------------------------------
def rule_based_predict(text):
    text_lower = str(text).lower()
    suspicious_patterns = [
        r'urgent', r'immediately', r'suspended', r'verify',
        r'hxxp', r'bit\.ly', r'free', r'action required', r'payroll'
    ]
    for pattern in suspicious_patterns:
        if re.search(pattern, text_lower):
            return "phishing"
    return "legitimate"

rule_preds = [rule_based_predict(t) for t in X_test_text]
print("========================================")
print("1. Rule-Based Baseline Performance")
print("========================================")
print(f"Accuracy: {accuracy_score(y_test, rule_preds):.2f}\n")

# ---------------------------------------------------------
# Feature Extraction: TF-IDF
# ---------------------------------------------------------
vec = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
X_train_vec = vec.fit_transform(X_train_text)
X_test_vec = vec.transform(X_test_text)

# ---------------------------------------------------------
# Model 2: TF-IDF + Linear Classifier (Logistic Regression)
# ---------------------------------------------------------
linear_clf = LogisticRegression(class_weight='balanced')
linear_clf.fit(X_train_vec, y_train)
linear_preds = linear_clf.predict(X_test_vec)

print("========================================")
print("2. TF-IDF Linear Classifier Performance")
print("========================================")
print(f"Accuracy: {accuracy_score(y_test, linear_preds):.2f}\n")

# ---------------------------------------------------------
# Model 3: Random Forest Classifier (Third Model)
# ---------------------------------------------------------
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
rf_clf.fit(X_train_vec, y_train)
rf_preds = rf_clf.predict(X_test_vec)

print("========================================")
print("3. Random Forest (Third Model) Performance")
print("========================================")
print(f"Accuracy: {accuracy_score(y_test, rf_preds):.2f}\n")

# ---------------------------------------------------------
# Save artifacts for Render Streamlit UI Deployment
# ---------------------------------------------------------
os.makedirs("model", exist_ok=True)
joblib.dump(vec, "model/tfidf_vectorizer.pkl")
joblib.dump(linear_clf, "model/risk_classifier.pkl")

print("----------------------------------------")
print("Successfully saved vectorizer and classifier in 'model/' directory.")