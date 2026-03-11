import streamlit as st
import requests
import os
import re

st.set_page_config(
    page_title="EduTutor AI",
    page_icon="🎓",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Playfair+Display:wght@700&display=swap');
html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
.stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); min-height: 100vh; }
.edu-header { text-align: center; padding: 1.5rem 0 1rem 0; }
.edu-header h1 { font-family: 'Playfair Display', serif; font-size: 2.5rem; color: #fff; margin-bottom: 0.2rem; text-shadow: 0 0 30px rgba(130,100,255,0.6); }
.edu-header p { color: #a78bfa; font-size: 0.9rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; }
section[data-testid="stSidebar"] { background: rgba(15,12,41,0.95) !important; border-right: 1px solid rgba(167,139,250,0.2) !important; }
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

API_URL = os.getenv("CHATBOT_API_URL", "https://student-chatbot-3uft.onrender.com")

if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("## 🎓 EduTutor AI")
    st.markdown("---")
    st.markdown("**Model:** DeepSeek R1 Distill 70B")
    st.markdown("**Powered by:** OpenRouter")
    st.markdown("---")
    st.markdown("**📚 Topics:**")
    for t in ["Mathematics", "Science", "English", "History",
              "Geography", "Physics", "Chemistry", "Biology", "Computer Science"]:
        st.markdown(f"• {t}")
    st.markdown("---")
    st.markdown("**🎯 Class Level:** 1 to 12")
    st.markdown("---")
    if st.button("🔄 New Conversation"):
        st.session_state.session_id = None
        st.session_state.messages = []
        st.rerun()
    if st.session_state.session_id:
        st.markdown("**Session:**")
        st.code(st.session_state.session_id[:20] + "...", language=None)

st.markdown("""
<div class="edu-header">
    <h1>🎓 EduTutor AI</h1>
    <p>Your Personal Learning Companion · Class 1–12</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.messages:
    st.info("👋 Hello! Ask me anything — Maths, Science, English, History and more!")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask a question... e.g. Explain photosynthesis for Class 8")

if user_input and user_input.strip():
    user_text = user_input.strip()

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
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
                reply = data["response"]
                reply = re.sub(r'<think>.*?</think>', '', reply, flags=re.DOTALL).strip()

                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

            except requests.exceptions.Timeout:
                st.error("⏱️ Timed out. The free server may be waking up (~50s). Please try again!")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to the API. Please check the server is running.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")