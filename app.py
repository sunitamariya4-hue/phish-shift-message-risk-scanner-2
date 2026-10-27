import os
import re
import joblib
import streamlit as st

st.set_page_config(
    page_title="PhishShift Risk Scanner",
    page_icon="🛡️",
    layout="centered"
)

st.caption(
    "Educational / Helpdesk Decision-Support Tool: "
    "Not a safety guarantee."
)

st.title("🛡️ PhishShift Message Risk Scanner")

st.write(
    "Scan emails and SMS for phishing tactics, "
    "suspicious links, and urgency cues."
)

# Load model files from the same folder as app.py
@st.cache_resource
def load_models():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    vectorizer_path = os.path.join(
        base_dir, "tfidf_vectorizer.pkl"
    )
    classifier_path = os.path.join(
        base_dir, "risk_classifier.pkl"
    )

    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(
            f"Missing file: {vectorizer_path}"
        )

    if not os.path.exists(classifier_path):
        raise FileNotFoundError(
            f"Missing file: {classifier_path}"
        )

    vectorizer = joblib.load(vectorizer_path)
    classifier = joblib.load(classifier_path)

    return vectorizer, classifier


try:
    vectorizer, classifier = load_models()
except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.info(
        "Check whether tfidf_vectorizer.pkl and "
        "risk_classifier.pkl exist in the GitHub "
        "repository's main folder."
    )
    st.stop()


user_text = st.text_area(
    "Enter Message Body / Subject Line:",
    placeholder=(
        "Example: Your payroll access is suspended. "
        "Verify your details at hxxp://example..."
    ),
    height=120
)

if st.button("Scan Message Risk"):

    if not user_text.strip():
        st.warning("Please enter a message to scan.")

    else:
        features = vectorizer.transform([user_text])
        classes = list(classifier.classes_)
        probabilities = classifier.predict_proba(features)[0]

        if "phishing" in classes:
            phish_idx = classes.index("phishing")
        else:
            st.error(
                "The model does not contain a "
                "'phishing' class. Check the training labels."
            )
            st.stop()

        phish_prob = float(probabilities[phish_idx])

        st.divider()

        if 0.40 <= phish_prob <= 0.60:
            st.info(
                f"⚠️ Classification: ABSTAIN / UNCERTAIN "
                f"(Risk Score: {phish_prob:.2f})"
            )
            st.write(
                "**Action:** Send the message to a human "
                "analyst for further checking."
            )

        elif phish_prob > 0.60:
            st.error(
                f"🚨 Classification: SUSPICIOUS / PHISHING "
                f"(Risk Score: {phish_prob:.2f})"
            )

        else:
            st.success(
                f"✅ Classification: BENIGN / LEGITIMATE "
                f"(Risk Score: {phish_prob:.2f})"
            )

        st.subheader("🔍 Suspicious Cues Analysis")

        cues_detected = []

        if re.search(
            r"(urgent|immediately|suspended|action required|final notice)",
            user_text,
            re.I
        ):
            cues_detected.append(
                "Artificial urgency or coercive language detected."
            )

        if re.search(
            r"(hxxp|\[\.\]|bit\.ly|tinyurl|\.cc|\.top)",
            user_text,
            re.I
        ):
            cues_detected.append(
                "Defanged URL or suspicious domain pattern detected."
            )

        if re.search(
            r"(password|bank|deposit|verify|payroll|code)",
            user_text,
            re.I
        ):
            cues_detected.append(
                "A request involving sensitive information detected."
            )

        if cues_detected:
            for cue in cues_detected:
                st.markdown(f"- ⚠️ {cue}")
        else:
            st.markdown(
                "- No common threat triggers were detected."
            )
