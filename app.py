import streamlit as st
import os

st.set_page_config(
    page_title="Amani - African Student Mentor",
    page_icon="🌍",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 780px !important; margin: 0 auto; }
.topbar {
    position: sticky; top: 0; z-index: 100;
    background: #fff; border-bottom: 1px solid #EBEBEB;
    padding: 14px 24px; display: flex; align-items: center; gap: 12px;
}
.topbar-avatar {
    width: 36px; height: 36px; background: #0F6E56; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 18px; flex-shrink: 0;
}
.topbar-name { font-weight: 600; font-size: 15px; color: #111; }
.topbar-sub { font-size: 12px; color: #8A8A8A; }
.topbar-dot { width: 8px; height: 8px; background: #22C55E; border-radius: 50%; display: inline-block; margin-right: 4px; }
.chat-wrap { padding: 24px 24px 0; }
.msg-row { display: flex; gap: 10px; margin-bottom: 18px; align-items: flex-start; }
.msg-row.user { flex-direction: row-reverse; }
.msg-avatar {
    width: 32px; height: 32px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; flex-shrink: 0; margin-top: 2px;
}
.msg-avatar.amani { background: #0F6E56; color: white; }
.msg-avatar.user { background: #F0F0F0; color: #333; }
.bubble {
    max-width: 82%; padding: 12px 16px; border-radius: 16px;
    font-size: 14.5px; line-height: 1.65; color: #1A1A1A;
}
.bubble.amani { background: #F7F7F5; border-top-left-radius: 4px; }
.bubble.user { background: #0F6E56; color: white; border-top-right-radius: 4px; }
.input-area {
    position: sticky; bottom: 0; background: white;
    border-top: 1px solid #EBEBEB; padding: 14px 24px 20px; margin-top: 16px;
}
.stTextArea textarea {
    border: 1.5px solid #D1D5DB !important; border-radius: 12px !important;
    font-size: 14px !important; resize: none !important;
    padding: 12px 14px !important; min-height: 52px !important;
}
.stTextArea textarea:focus { border-color: #0F6E56 !important; }
.stButton > button {
    background: #0F6E56 !important; color: white !important;
    border: none !important; border-radius: 10px !important;
    font-size: 20px !important; height: 52px !important; width: 52px !important;
    padding: 0 !important;
}
.stButton > button:hover { background: #0A5240 !important; }
</style>
""", unsafe_allow_html=True)

SYSTEM = """You are Amani, a warm and direct AI mentor for African university students. You work like Claude — conversational, specific, never generic.

Your expertise:
- African scholarships: Mastercard Foundation, Chevening, Rhodes, DAAD, Mandela Rhodes, MEXT Japan, Carnegie Mellon Africa, Commonwealth
- African hubs: Innovation Village & Hive Colab (Uganda), iHub (Kenya), CcHub (Nigeria), MEST (Ghana), kLab (Rwanda)
- Fields: Engineering, Medicine, Law, Tech/AI, Arts, Business, Agriculture
- Writing LinkedIn messages, cold emails, personal statements
- Building an outstanding profile through projects, volunteering, online presence
- Uganda specifics: Innovation Village Kampala, Hive Colab, Makerere University, UCU (Uganda Christian University), UIRI

Tone:
- Talk like a smart encouraging older sibling, not a textbook
- Be direct and specific — name actual programs, hubs, deadlines
- Short paragraphs, use bold for key terms
- When given a bio, score it and give clear next steps
- Never say "Great question!" or use hollow filler phrases
- Networking scripts must sound human, not templated
- Respond in markdown"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! I am **Amani**, your African student mentor. 🌍\n\nI can help you find scholarships, build your profile, write LinkedIn messages to professors, or answer any questions about your career path.\n\nWhat is on your mind?"
        }
    ]

if "pending" not in st.session_state:
    st.session_state.pending = None

def call_amani(messages):
    try:
        import anthropic
        try:
            api_key = st.secrets["ANTHROPIC_API_KEY"]
        except Exception:
            api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return "Add your ANTHROPIC_API_KEY to Streamlit secrets to activate Amani."
        client = anthropic.Anthropic(api_key=api_key)
        history = [{"role": m["role"], "content": m["content"]} for m in messages]
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM,
            messages=history,
        )
        return response.content[0].text
    except ImportError:
        return "The anthropic package is not installed. Check your requirements.txt."
    except Exception as e:
        return f"Error: {str(e)}"

st.markdown("""
<div class="topbar">
  <div class="topbar-avatar">🌍</div>
  <div>
    <div class="topbar-name">Amani</div>
    <div class="topbar-sub"><span class="topbar-dot"></span>African Student Mentor</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    role = msg["role"]
    css_role = "amani" if role == "assistant" else "user"
    avatar = "🌍" if role == "assistant" else "👤"
    content = msg["content"].replace("\n", "<br>")
    st.markdown(f"""
    <div class="msg-row {css_role}">
      <div class="msg-avatar {css_role}">{avatar}</div>
      <div class="bubble {css_role}">{content}</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

SUGGESTIONS = [
    "Find me a scholarship",
    "Analyze my profile",
    "Write a LinkedIn message to a professor",
    "What hubs are near me?",
]

if len(st.session_state.messages) == 1:
    cols = st.columns(len(SUGGESTIONS))
    for i, suggestion in enumerate(SUGGESTIONS):
        with cols[i]:
            if st.button(suggestion, key=f"pill_{i}"):
                st.session_state.pending = suggestion
                st.rerun()

st.markdown('<div class="input-area">', unsafe_allow_html=True)
input_col, btn_col = st.columns([10, 1])
with input_col:
    user_input = st.text_area(
        label="",
        placeholder="Ask Amani anything...",
        key="chat_input",
        label_visibility="collapsed",
        height=52,
    )
with btn_col:
    send = st.button("↑", key="send_btn")
st.markdown('</div>', unsafe_allow_html=True)

message_to_send = None
if send and user_input.strip():
    message_to_send = user_input.strip()
elif st.session_state.pending:
    message_to_send = st.session_state.pending
    st.session_state.pending = None

if message_to_send:
    st.session_state.messages.append({"role": "user", "content": message_to_send})
    with st.spinner("Amani is thinking..."):
        reply = call_amani(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
