import streamlit as st
import asyncio

from ChatBot.chain import ChatChain
from ChatBot.resolve import resolve_shortcut
from ChatBot.rate_limit import RateLimiter
from ChatBot.retry import invoke_with_retry

# Init
chatbot = ChatChain()
limiter = RateLimiter()

st.set_page_config(
    page_title="Trip Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session
if "messages" not in st.session_state:
    st.session_state.messages = []

if "shortcut" not in st.session_state:
    st.session_state.shortcut = ""

# CSS
st.markdown("""
<style>
.stAppDeployDropdown, [data-testid="stHeader"] {
    background: transparent !important;
}

html, body, .stApp {
    margin: 0;
    padding: 0;
    height: 100%;
}

.stApp {
    background:
    linear-gradient(rgba(0,0,0,.45), rgba(0,0,0,.45)),
    url("https://www.pixelstalk.net/wp-content/uploads/images6/4K-Travel-Wallpaper-HD-Free-download.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

.main {
    background: transparent !important;
}

.block-container {
    max-width: 100% !important;
    padding: 2rem 3rem 8rem 3rem !important;
}

section[data-testid="stSidebar"] {
    width: 320px !important;
    background: rgba(0, 0, 0, 0.4) !important;
    backdrop-filter: blur(25px);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

h1 {
    text-align: center;
    color: white;
    font-size: 42px !important;
    font-weight: 700 !important;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    margin-bottom: 2rem !important;
}

.chat-container {
    display: flex;
    flex-direction: column;
    gap: 15px;
    width: 100%;
    margin-bottom: 20px;
}

.chat-row {
    display: flex;
    width: 100%;
}

.row-user {
    justify-content: flex-end;
}

.row-ai {
    justify-content: flex-start;
}

.user-msg {
    background: #800080 !important;
    padding: 14px 20px;
    border-radius: 20px 20px 4px 20px;
    color: white !important;
    max-width: 65%;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    direction: rtl;
    text-align: right;
}

.ai-msg {
    background: rgba(255, 255, 255, 0.12) !important;
    backdrop-filter: blur(12px);
    padding: 14px 20px;
    border-radius: 20px 20px 20px 4px;
    color: white !important;
    max-width: 65%;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.15);
    border: 1px solid rgba(255,255,255,0.08);
    direction: rtl;
    text-align: right;
}

.stChatInput {
    position: fixed !important;
    bottom: 24px;
    left: 350px !important;
    right: 120px !important;
    z-index: 999;
}

section[data-testid="stSidebar"][aria-expanded="false"] ~ div .stChatInput {
    left: 40px !important;
}

.stChatInput input {
    background: rgba(255, 255, 255, 0.12) !important;
    backdrop-filter: blur(20px);
    color: white !important;
    border-radius: 30px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    padding: 12px 24px !important;
}

.shortcut-wrap {
    position: fixed;
    right: 30px;
    bottom: 24px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    z-index: 9999;
}

div[data-testid="column"] button {
    background: rgba(255, 255, 255, 0.15) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 50% !important;
    width: 45px !important;
    height: 45px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 20px !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    transition: all 0.2s ease;
}

div[data-testid="column"] button:hover {
    background: #800080 !important;
    transform: scale(1.1);
}

.history-box {
    background: rgba(255, 255, 255, 0.08);
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0;
    border-left: 3px solid #800080;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.title("🧳Trips")
    if st.button("🗑Clear History"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.subheader("History")
    for msg in st.session_state.messages[-8:]:
        role = "🧑" if msg["role"] == "user" else "🤖"
        clean_content = msg['content'].replace("budget","").replace("weather","").replace("places","").replace("hotel","").replace("plan","").strip()
        st.markdown(
            f"<div class='history-box'>{role} {clean_content[:25]}...</div>",
            unsafe_allow_html=True
        )

# Title
st.title("🌍 Trip Planner")
# Messages
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":

        st.markdown(
            f"<div class='chat-row row-user'><div class='user-msg'>{msg['content']}</div></div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='chat-row row-ai'><div class='ai-msg'>{msg['content']}</div></div>",
            unsafe_allow_html=True
        )
st.markdown('</div>', unsafe_allow_html=True)

# Floating Shortcut Buttons
st.markdown('<div class="shortcut-wrap">', unsafe_allow_html=True)
c1 = st.container()
c2 = st.container()
c3 = st.container()
c4 = st.container()
c5 = st.container()
with c1:
    if st.button("💰", key="btn_b"): st.session_state.shortcut="budget"
with c2:
    if st.button("🌦", key="btn_w"): st.session_state.shortcut="weather"
with c3:
    if st.button("📍", key="btn_p"): st.session_state.shortcut="places"
with c4:
    if st.button("🏨", key="btn_h"): st.session_state.shortcut="hotel"
with c5:
    if st.button("🗺", key="btn_pl"): st.session_state.shortcut="plan"
st.markdown('</div>', unsafe_allow_html=True)

# Input
placeholder_text = f"{st.session_state.shortcut} " if st.session_state.shortcut else ""
user_input = st.chat_input(
    f"{placeholder_text}Plan your dream trip..."
)

# Chat Logic
if user_input:
    final_input = (st.session_state.shortcut + " " + user_input).strip()
    st.session_state.shortcut = ""
    st.session_state.messages.append({"role":"user", "content":final_input})
    resolved_input = resolve_shortcut(final_input)
    with st.spinner("✈️ Planning..."):
        config_data = {
            "configurable": {
                "temperature": resolved_input.temperature,
                "max_tokens": resolved_input.max_tokens
            }
        }
        response = asyncio.run(
            invoke_with_retry(
                chain=chatbot.chain,
                payload={
                    "question": resolved_input.prompt,
                    "chat_history": st.session_state.messages
                },
                rate_limiter=limiter,
                run_config=config_data 
            )
        )
    st.session_state.messages.append({"role":"assistant", "content":response})
    st.rerun()