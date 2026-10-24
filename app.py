import streamlit as st
import joblib
import re

# Page Configuration
st.set_page_config(
    page_title="PhishShift Risk Scanner",
    page_icon="🛡️",
    layout="centered"
)

# NFR-03: Mandatory Safety & Decision-Support Disclaimer
st.caption("Educational / Helpdesk Decision-Support Tool (NFR-03): Not a safety guarantee.")

st.title("🛡️ PhishShift Message Risk Scanner")
st.write("Scan emails and SMS for phishing tactics, defanged links, and urgency cues.")

# Load Model Artifacts
@st.cache_resource
def load_models():
    vec = joblib.load("model/tfidf_vectorizer.pkl")
    clf = joblib.load("model/risk_classifier.pkl")
    return vec, clf

try:
    vectorizer, classifier = load_models()
except Exception as e:
    st.error("Model files not found! Please run train_models.py first.")
    st.stop()

# User Input Box
user_text = st.text_area(
    "Enter Message Body / Subject Line:",
    placeholder="e.g., Your payroll access is suspended. Verify bank details at hxxp://...",
    height=120
)

# Inference Action
if st.button("Scan Message Risk"):
    if not user_text.strip():
        st.warning("Please enter a valid message to scan.")
    else:
        # Transform & Predict Probability
        features = vectorizer.transform([user_text])
        classes = list(classifier.classes_)
        phish_idx = classes.index("phishing") if "phishing" in classes else 1
        
        # Get probability score
        probs = classifier.predict_proba(features)[0]
        phish_prob = probs[phish_idx]

        st.divider()

        # FR-04: Abstain / Reject Logic (Threshold: 0.40 - 0.60)
        if 0.40 <= phish_prob <= 0.60:
            st.info(f"⚠️ Classification: **ABSTAIN / UNCERTAIN** (Risk Score: {phish_prob:.2f})")
            st.write("**Action:** Model confidence is borderline. Route message safely to a Human L2 Analyst.")
        elif phish_prob > 0.60:
            st.error(f"🚨 Classification: **SUSPICIOUS / PHISHING** (Risk Score: {phish_prob:.2f})")
        else:
            st.success(f"✅ Classification: **BENIGN / LEGITIMATE** (Risk Score: {phish_prob:.2f})")

        # FR-04: Safe Explanation of Risk Cues
        st.subheader("🔍 Suspicious Cues Analysis")
        cues_detected = []
        
        # Urgency cue check
        if re.search(r'(urgent|immediately|suspended|action required|final notice)', user_text, re.I):
            cues_detected.append("Artificial urgency or coercive language pattern.")
            
        # Defanged URL / Shortener check
        if re.search(r'(hxxp|\[\.\]|bit\.ly|tinyurl|\.cc|\.top)', user_text, re.I):
            cues_detected.append("Defanged URL or suspicious domain suffix spotted.")
            
        # Credential / Banking cue
        if re.search(r'(password|bank|deposit|verify|payroll|code)', user_text, re.I):
            cues_detected.append("Sensitive request targeting account credentials or financial data.")

        if cues_detected:
            for cue in cues_detected:
                st.markdown(f"- ⚠️ {cue}")
        else:
            st.markdown("- No common threat triggers or explicit urgency patterns found.")