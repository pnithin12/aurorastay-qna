
import os
import re
from html import escape

import requests
import streamlit as st
import streamlit.components.v1 as components

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
[data-testid="stHeader"] {display:none;}
.stApp {background:#F6F7F9; color:#243247;}
.block-container {
    max-width:1200px;
    padding:1.6rem 2rem 160px;
    font-family:"Segoe UI",Arial,sans-serif;
}
.brand {
    display:flex; justify-content:space-between;
    align-items:center; margin-bottom:30px;
}
.brand-name {font-size:25px; font-weight:700; color:#243247;}
.subtitle,.author {font-size:13px; color:#64748B;}
.author {text-align:right;}

.question-row {
    display:flex; justify-content:flex-end;
    margin:24px 0 18px;
    scroll-margin-top:24px;
}
.question-box {
    max-width:78%; padding:16px 20px;
    background:#E2EAF5; color:#263B57;
    border-radius:22px 22px 6px 22px;
    font-size:16px; line-height:1.65;
    white-space:pre-wrap; overflow-wrap:anywhere;
}
.reply-box {
    background:#EDF3FA;
    border:1px solid #DFE7F1;
    border-radius:20px;
    overflow:hidden; margin-bottom:12px;
}
.box-heading {
    padding:12px 20px; background:#E5EDF7;
    color:#3D5575; font-size:14px; font-weight:600;
}
.answer-body {
    padding:18px 20px;
    font-size:16px; line-height:1.75;
    color:#243247;
    white-space:pre-wrap; overflow-wrap:anywhere;
}
.sources-box {
    background:#FFFFFF; border:1px solid #DFE4EC;
    border-radius:20px; overflow:hidden; margin-bottom:30px;
}
.sources-box > .box-heading {background:#EEF1F5;}
.source-item {padding:0 20px; border-top:1px solid #E8ECF2;}
.source-item summary {
    cursor:pointer; padding:14px 0;
    color:#3B506D; font-size:14px; line-height:1.5;
}
.source-item summary:focus-visible {
    outline:2px solid #8299B8; outline-offset:3px;
}
.source-text {
    padding:0 0 14px; font-size:15px; line-height:1.75;
    color:#334155; overflow-wrap:anywhere;
}
.source-file {
    color:#68778A; font-size:12px;
    padding-bottom:14px; overflow-wrap:anywhere;
}

/* Landing page and clickable suggestion cards */
.welcome {text-align:center; padding:9vh 0 24px;}
.welcome h2 {font-size:30px; color:#243247; font-weight:600;}
.welcome p {font-size:16px; color:#64748B;}

.st-key-quick_arrival button,
.st-key-quick_rooms button,
.st-key-quick_animals button,
.st-key-quick_refunds button {
    min-height:126px;
    width:100%;
    padding:18px !important;
    border:1px solid rgba(60,80,110,0.10) !important;
    border-radius:18px !important;
    color:#293B52 !important;
    text-align:left !important;
    justify-content:flex-start !important;
    transition:transform 0.15s, box-shadow 0.15s;
}
.st-key-quick_arrival button {background:#E8F0FC !important;}
.st-key-quick_rooms button {background:#F0EAF9 !important;}
.st-key-quick_animals button {background:#FFF0E5 !important;}
.st-key-quick_refunds button {background:#E5F3F2 !important;}

.st-key-quick_arrival button p,
.st-key-quick_rooms button p,
.st-key-quick_animals button p,
.st-key-quick_refunds button p {
    color:#293B52 !important;
    font-size:15px !important;
    line-height:1.6 !important;
    text-align:left !important;
}
.st-key-quick_arrival button:hover,
.st-key-quick_rooms button:hover,
.st-key-quick_animals button:hover,
.st-key-quick_refunds button:hover {
    transform:translateY(-3px);
    box-shadow:0 6px 16px rgba(35,55,85,0.09);
}

/* Opaque footer behind the centered composer */
.composer-backdrop {
    position:fixed; left:0; right:0; bottom:0;
    height:120px; background:#F6F7F9;
    z-index:98; pointer-events:none;
}
[data-testid="stForm"] {
    position:fixed !important;
    inset:auto auto 20px 50% !important;
    transform:translateX(-50%) !important;
    width:calc(100% - 40px) !important;
    max-width:1060px !important;
    height:82px !important;
    min-height:82px !important;
    max-height:82px !important;
    box-sizing:border-box !important;
    padding:16px !important;
    margin:0 !important;
    background:#FFFFFF !important;
    border:1px solid #A8B9CF !important;
    border-radius:26px !important;
    box-shadow:0 5px 24px rgba(40,60,90,0.14) !important;
    overflow:hidden !important;
    z-index:99 !important;
}
[data-testid="stForm"] [data-testid="stHorizontalBlock"] {
    flex-wrap:nowrap !important;
    align-items:center !important;
    gap:12px !important;
}
[data-testid="stForm"] [data-testid="stColumn"]:first-child {
    flex:1 1 0 !important; min-width:0 !important;
}
[data-testid="stForm"] [data-testid="stColumn"]:last-child {
    flex:0 0 76px !important; min-width:76px !important;
}
[data-testid="stForm"] [data-testid="stTextInput"] div,
[data-testid="stForm"] [data-baseweb="input"],
[data-testid="stForm"] [data-baseweb="base-input"],
[data-testid="stForm"] input {
    background:#FFFFFF !important;
    color:#243247 !important;
    -webkit-text-fill-color:#243247 !important;
    color-scheme:light !important;
}
[data-testid="stForm"] [data-baseweb="input"] {
    border:0 !important; box-shadow:none !important;
}
[data-testid="stForm"] input {
    font-size:16px !important;
    height:46px !important;
    padding:0 8px !important;
    opacity:1 !important;
}
[data-testid="stForm"] input::placeholder {
    color:#596C85 !important;
    -webkit-text-fill-color:#596C85 !important;
    opacity:1 !important;
}
[data-testid="stForm"] [data-testid="InputInstructions"] {
    display:none !important;
}
[data-testid="stFormSubmitButton"] button {
    height:46px !important; min-height:46px !important;
    width:76px !important;
    background:#344E70 !important;
    color:#FFFFFF !important;
    border:0 !important; border-radius:18px !important;
}
[data-testid="stFormSubmitButton"] button p {
    color:#FFFFFF !important;
    font-size:15px !important; font-weight:600 !important;
}
[data-testid="stFormSubmitButton"] button:hover {
    background:#263E5D !important;
}
@media(max-width:700px) {
    .block-container {padding:1.2rem 1rem 150px;}
    .brand-name {font-size:22px;}
    .question-box {max-width:92%;}
    .welcome {padding-top:5vh;}
    [data-testid="stForm"] {
        width:calc(100% - 24px) !important;
        padding:16px 10px !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="brand">
    <div>
        <div class="brand-name">🏨 AuroraStay</div>
        <div class="subtitle">Staff Assistant · Hotel policy Q&A</div>
    </div>
    <div class="author">Internal POC<br><strong>By Nithin P</strong></div>
</div>
<div class="composer-backdrop"></div>
""", unsafe_allow_html=True)

if "answers" not in st.session_state:
    st.session_state.answers = []

def choose_question(question):
    st.session_state["pending_question"] = question

with st.form("ask_form", clear_on_submit=True):
    entry, action = st.columns([9, 1], vertical_alignment="center")
    with entry:
        question = st.text_input(
            "Hotel policy question",
            label_visibility="collapsed",
            placeholder="Ask about your hotel policies…"
        )
    with action:
        submitted = st.form_submit_button("Ask")

pending_question = st.session_state.pop("pending_question", None)

if submitted:
    if not question.strip():
        st.warning("Please enter a question.")
    elif len(question.strip()) > 4000:
        st.warning("Please keep your question within 4,000 characters.")
    else:
        pending_question = question.strip()

if pending_question:
    with st.spinner("Finding your answer…"):
        try:
            response = requests.post(
                f"{BACKEND_URL}/answer",
                json={"question": pending_question},
                timeout=180
            )
            response.raise_for_status()
            st.session_state.answers.append(response.json())
            st.session_state["scroll_to_latest"] = True
        except (requests.RequestException, ValueError):
            st.error(
                "Unable to answer the new question. Please try again. "
                "Previous answers remain below."
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

if not st.session_state.answers:
    st.markdown("""
    <div class="welcome">
        <h2>How can I help you?</h2>
        <p>Choose a question below or ask your own.</p>
    </div>
    """, unsafe_allow_html=True)

    suggestions = [
        (
            "quick_arrival",
            "🕒 **Check-in & check-out**\n\nTimes at Chicago Loop",
            "What are the check-in and check-out times at ASH-CHI Loop?"
        ),
        (
            "quick_rooms",
            "🛏️ **Room occupancy**\n\nDouble Queen capacity",
            "How many people can stay in a Double Queen room?"
        ),
        (
            "quick_animals",
            "🐕 **Service animals**\n\nFees at Boston Harbor",
            "I have a service dog at ASH-BOS Harbor. Do I need to pay a pet fee?"
        ),
        (
            "quick_refunds",
            "💳 **Card holds**\n\nPending amount after checkout",
            "Why is there still a pending hold on my card after checkout?"
        )
    ]

    for column, (key, label, suggested_question) in zip(
        st.columns(4), suggestions
    ):
        with column:
            st.button(
                label,
                key=key,
                use_container_width=True,
                on_click=choose_question,
                args=(suggested_question,)
            )

for number, result in enumerate(st.session_state.answers, start=1):
    st.markdown(
        '<div class="question-row"><div class="question-box">'
        f'{escape(result["question"])}</div></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="reply-box">'
        f'<div class="box-heading">AuroraStay · Answer {number}</div>'
        f'<div class="answer-body">{escape(result["answer"])}</div>'
        '</div>',
        unsafe_allow_html=True
    )

    cited = set(re.findall(r"\[(S\d+)\]", result["answer"]))
    sources = sorted(
        result["sources"],
        key=lambda source: source["label"] not in cited
    )

    source_cards = []

    for position, source in enumerate(sources):
        title = titles.get(source["source"], source["source"])
        label = (
            f"[{source['label']}] {title} · Page {source['page']}"
            + (" · Cited" if source["label"] in cited else "")
        )
        open_state = " open" if position == 0 else ""
        text = " ".join(source["text"].split())

        source_cards.append(
            f'<details class="source-item"{open_state}>'
            f'<summary>{escape(label)}</summary>'
            f'<div class="source-text">{escape(text)}</div>'
            f'<div class="source-file">{escape(source["source"])}</div>'
            '</details>'
        )

    st.markdown(
        '<div class="sources-box">'
        '<div class="box-heading">Supporting sources</div>'
        + "".join(source_cards)
        + '</div>',
        unsafe_allow_html=True
    )

if st.session_state.answers:
    st.caption(
        "Questions are answered independently. Review sources before "
        "advising guests. Live reservation records are not connected."
    )

if st.session_state.pop("scroll_to_latest", False):
    components.html(
        """
        <script>
        let attempts = 0;
        const timer = setInterval(() => {
            try {
                const questions =
                    window.parent.document.querySelectorAll(".question-row");
                if (questions.length) {
                    questions[questions.length - 1].scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });
                    clearInterval(timer);
                }
            } catch (error) {
                clearInterval(timer);
            }
            if (++attempts >= 10) clearInterval(timer);
        }, 150);
        </script>
        """,
        height=0
    )
