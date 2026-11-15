
import os

import requests
import streamlit as st

st.set_page_config(page_title="AuroraStay Q&A", page_icon="🏨")

BACKEND_URL = os.environ.get(
    "BACKEND_URL", "http://localhost:7860"
).rstrip("/")

st.title("AuroraStay Staff Q&A")
st.caption("Find answers from the hotel policy documents.")
st.info(
    "Internal POC: review the answer and sources before advising a guest. "
    "Live availability and reservation records are not connected."
)

with st.form("question_form"):
    question = st.text_area(
        "Your question",
        placeholder="Include the property and rate plan where relevant.",
        max_chars=4000
    )
    submitted = st.form_submit_button("Get answer")

if submitted:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Checking policy documents..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/answer",
                    json={"question": question.strip()},
                    timeout=180
                )
                response.raise_for_status()
                st.session_state["result"] = response.json()

            except (requests.RequestException, ValueError):
                st.session_state.pop("result", None)
                st.error(
                    "Unable to retrieve an answer. "
                    "Please try again or contact the property team."
                )

if "result" in st.session_state:
    result = st.session_state["result"]

    st.subheader("Answer")
    st.markdown(result["answer"])

    st.subheader("Supporting sources")

    for source in result["sources"]:
        title = (
            f"[{source['label']}] {source['source']} "
            f"— Page {source['page']}"
        )
        with st.expander(title):
            st.write(source["text"])
