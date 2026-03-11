import streamlit as st
import requests
import os

# Page config
st.set_page_config(
    page_title="EduTutor AI",
    page_icon="🎓",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Playfair+Display:wght@700&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* Header */
.edu-header {
    text-align: center;
    padding: 2rem 0 1rem 0;
}
.edu-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    color: #fff;
    margin-bottom: 0.2rem;
    text-shadow: 0 0 30px rgba(130,100,255,0.6);
}
.edu-header p {
    color: #a78bfa;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* Chat messages */
.chat-bubble-user {
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: white;
    padding: 0.9rem 1.2rem;
    border-radius: 18px 18px 4px 18px;
    margin: 0.5rem 0;
    max-width: 80%;
    margin-left: auto;
    box-shadow: 0 4px 15px rgba(124,58,237,0.3);
    font-size: 0.95rem;
}
.chat-bubble-assistant {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color: #e2e8f0;
    padding: 0.9rem 1.2rem;
    border-radius: 18px 18px 18px 4px;
    margin: 0.5rem 0;
    max-width: 85%;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    font-size: 0.95rem;
    line-height: 1.6;
}
.role-label-user {
    text-align: right;
    font-size: 0.72rem;
    color: #a78bfa;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 2px;
}
.role-label-assistant {
    font-size: 0.72rem;
    color: #34d399;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 2px;
}

/* Session info */
.session-badge {
    background: rgba(167,139,250,0.15);
    border: 1px solid rgba(167,139,250,0.3);
    color: #a78bfa;
    border-radius: 20px;
    padding: 0.3rem 1rem;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1px;
    display: inline-block;
    margin-bottom: 1rem;
}

/* Input area */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.07) !important;
    border: 1.5px solid rgba(167,139,250,0.35) !important;
    border-radius: 12px !important;
    color: white !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.2) !important;
}
.stTextInput > div > div > input::placeholder {
    color: rgba(255,255,255,0.35) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s !important;
    letter-spacing: 0.5px !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.4) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(15,12,41,0.95) !important;
    border-right: 1px solid rgba(167,139,250,0.2) !important;
}
section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Divider */
hr {
    border-color: rgba(255,255,255,0.08) !important;
}

/* Hide streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# API URL - can be overridden via env variable
API_URL = os.getenv("CHATBOT_API_URL", "https://student-chatbot-3uft.onrender.com")

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "pending_message" not in st.session_state:
    st.session_state.pending_message = ""

# Sidebar
with st.sidebar:
    st.markdown("## 🎓 EduTutor AI")
    st.markdown("---")
    st.markdown("**Model:** DeepSeek R1 Distill 70B")
    st.markdown("**Powered by:** OpenRouter")
    st.markdown("---")
    st.markdown("**📚 Topics I can help with:**")
    topics = ["Mathematics", "Science", "English", "History", "Geography",
              "Physics", "Chemistry", "Biology", "Computer Science"]
    for t in topics:
        st.markdown(f"• {t}")
    st.markdown("---")
    st.markdown("**🎯 Class Level:** 1 to 12")
    st.markdown("---")
    if st.button("🔄 New Conversation"):
        st.session_state.session_id = None
        st.session_state.messages = []
        st.rerun()
    if st.session_state.session_id:
        st.markdown(f"**Session ID:**")
        st.code(st.session_state.session_id[:16] + "...", language=None)

# Header
st.markdown("""
<div class="edu-header">
    <h1>🎓 EduTutor AI</h1>
    <p>Your Personal Learning Companion · Class 1–12</p>
</div>
""", unsafe_allow_html=True)

# Display chat history
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center; padding: 2rem; color: rgba(255,255,255,0.4);">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📖</div>
        <div style="font-size: 1rem; font-weight: 600;">Ask me anything — Math, Science, English, History & more!</div>
        <div style="font-size: 0.85rem; margin-top: 0.5rem;">Type your question below to get started</div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="role-label-user">You</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            st.markdown(f'<div class="role-label-assistant">🎓 EduTutor</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble-assistant">{msg["content"]}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Input area
def submit():
    if st.session_state.user_input.strip():
        st.session_state.submitted = True
        st.session_state.pending_message = st.session_state.user_input.strip()

col1, col2 = st.columns([5, 1])
with col1:
    st.text_input(
        "message",
        placeholder="Ask a question... e.g. Explain photosynthesis for Class 8",
        label_visibility="collapsed",
        key="user_input",
        on_change=submit
    )
with col2:
    if st.button("Send ➤"):
        submit()

# Handle message send — only fires once per actual submission
if st.session_state.submitted and st.session_state.pending_message:
    user_text = st.session_state.pending_message
    st.session_state.submitted = False
    st.session_state.pending_message = ""

    # Add user message to display
    st.session_state.messages.append({"role": "user", "content": user_text})

    # Call API
    with st.spinner("EduTutor is thinking..."):
        try:
            import re
            payload = {"message": user_text}
            if st.session_state.session_id:
                payload["session_id"] = st.session_state.session_id

            response = requests.post(
                f"{API_URL}/chat",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            data = response.json()

            st.session_state.session_id = data["session_id"]
            assistant_reply = data["response"]

            # Clean up <think> tags if model returns them
            if "<think>" in assistant_reply:
                assistant_reply = re.sub(r'<think>.*?</think>', '', assistant_reply, flags=re.DOTALL).strip()

            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. The server may be waking up — please try again!")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to the chatbot API. Please check the server URL.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

    st.rerun()