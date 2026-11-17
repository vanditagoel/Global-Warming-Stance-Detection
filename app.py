import os
import joblib
import streamlit as st

MODEL_PATH = os.path.join(os.path.dirname(__file__), "climate_stance_model.pkl")

st.set_page_config(
    page_title="Indic Climate Stance Detector",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 Indic Climate Stance Detector")
st.write(
    "Enter a Hindi, Bengali, or code-mixed comment. "
    "The model predicts the stance toward the claim:"
)
st.info("“Climate change and global warming is a serious concern.”")

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)

model = load_model()

if model is None:
    st.error(
        "Model file not found. Place climate_stance_model.pkl "
        "in the same folder as app.py, then restart the app."
    )
    st.stop()

comment = st.text_area(
    "Enter a comment",
    placeholder="Example: जलवायु परिवर्तन सच में एक गंभीर समस्या है...",
    height=140
)

if st.button("Predict stance", type="primary", use_container_width=True):
    if not comment.strip():
        st.warning("Please enter a comment first.")
    else:
        prediction = model.predict([comment.strip()])[0]
        descriptions = {
            "Favour": "The comment supports the claim.",
            "Against": "The comment opposes the claim.",
            "None": "The comment is neutral, unrelated, or expresses no clear stance."
        }
        st.subheader(f"Predicted stance: {prediction}")
        st.success(descriptions.get(prediction, "Prediction completed."))

st.divider()
st.caption(
    "Academic prototype for CSET346. Predictions are model outputs, "
    "not verified facts. Evaluation is preliminary and the labelled dataset "
    "contains very few real-world examples."
)
