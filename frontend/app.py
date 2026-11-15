
import os
import re

import requests
import streamlit as st

st.set_page_config(
    page_title="AuroraStay | Staff Assistant",
    page_icon="🏨",
    layout="wide"
)

BACKEND_URL = os.environ.get(
    "BACKEND_URL", "http://localhost:7860"
).rstrip("/")

st.markdown("""
<style>
.stApp {
    background: #F7F8F4;
    color: #243D3B;
    font-family: "Segoe UI", Arial, sans-serif;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 1.5rem;
    max-width: 1600px;
}
h1, h2, h3 {
    color: #173F3B !important;
    font-family: "Segoe UI", Arial, sans-serif !important;
}
h1 {font-size: 2rem !important; letter-spacing: -0.6px;}
h3 {font-size: 1.2rem !important;}
p, li {font-size: 1rem; line-height: 1.65;}
[data-testid="stVerticalBlockBorderWrapper"] > div {
    border-color: #DCE5DD !important;
    border-radius: 14px !important;
}
[data-testid="stForm"] {
    background: #FFFFFF;
    padding: 1rem;
}
[data-testid="stTextInput"] input {
    background: #FFFFFF;
    color: #243D3B;
    font-size: 1rem;
}
[data-testid="stExpander"] {
    background: #FFFFFF;
    border-color: #DCE5DD;
}
.stButton button, .stFormSubmitButton button {
    background: #176B60;
    color: #FFFFFF;
    border: none;
    border-radius: 9px;
    font-weight: 600;
}
.stButton button:hover, .stFormSubmitButton button:hover {
    background: #10564D;
    color: #FFFFFF;
}
.brand-note {color: #647B74; font-size: 0.95rem;}
.byline {text-align: right; color: #526E65; padding-top: 0.6rem;}
.badge {
    display: inline-block;
    background: #E6EFE7;
    color: #285B4D;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.8rem;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

header, author = st.columns([4, 1])

with header:
    st.title("🏨 AuroraStay")
    st.markdown(
        '<div class="brand-note">Staff Assistant · '
        'Answers grounded in hotel policies</div>',
        unsafe_allow_html=True
    )

with author:
    st.markdown(
        '<div class="byline"><span class="badge">Internal POC</span>'
        '<br>By Nithin P</div>',
        unsafe_allow_html=True
    )

st.write("")

with st.form("question_form"):
    question_col, button_col = st.columns(
        [7, 1], vertical_alignment="bottom"
    )
    with question_col:
        question = st.text_input(
            "Ask a policy question",
            placeholder="Include the property and rate plan where relevant.",
            max_chars=4000
        )
    with button_col:
        submitted = st.form_submit_button(
            "Ask question", use_container_width=True
        )

if submitted:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Finding the relevant policy..."):
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
                    "Unable to retrieve an answer. Please try again "
                    "or contact the property team."
                )

titles = {
    "aurorastay_booking_terms_and_cancellation_policy.pdf":
        "Booking & cancellation",
    "aurorastay_room_and_property_information.pdf":
        "Rooms & property information",
    "aurorastay_refunds_and_additional_charges_guide.pdf":
        "Refunds & additional charges",
    "aurorastay_guest_conduct_accessibility_and_resolution_guidelines.pdf":
        "Guest conduct & accessibility"
}

if "result" in st.session_state:
    result = st.session_state["result"]
    cited = set(re.findall(r"\[(S\d+)\]", result["answer"]))

    answer_col, source_col = st.columns([1.7, 1], gap="large")

    with answer_col:
        with st.container(border=True):
            st.subheader("Answer")
            st.caption(result["question"])
            st.markdown(result["answer"])
            st.divider()
            st.caption(
                "Review the supporting policy before advising a guest. "
                "Confirm current property details where required."
            )

    with source_col:
        st.subheader("Supporting sources")
        st.caption(f"{len(result['sources'])} retrieved passages")

        ordered_sources = sorted(
            result["sources"],
            key=lambda source: source["label"] not in cited
        )

        for source in ordered_sources:
            is_cited = source["label"] in cited
            title = titles.get(source["source"], source["source"])
            label = (
                f"[{source['label']}] {title} · Page {source['page']}"
                + (" · Cited" if is_cited else "")
            )
            with st.expander(label, expanded=is_cited):
                st.text(source["text"])
                st.caption(source["source"])
else:
    st.markdown("### How can I help?")
    st.caption(
        "Ask about bookings, cancellations, rooms, parking, pets, "
        "refunds, or guest guidelines."
    )

st.caption(
    "Internal staff tool · Live availability and reservation records "
    "are not connected."
)
