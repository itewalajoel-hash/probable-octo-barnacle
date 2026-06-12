import streamlit as st
import os

st.set_page_config(
    page_title="Amani - African Student Mentor",
    page_icon="🌍",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600&family=Inter:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #1C1410 !important;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 0 !important;
    max-width: 760px !important;
    margin: 0 auto;
    background: #1C1410;
}

/* ── Top bar ── */
.topbar {
    position: sticky; top: 0; z-index: 100;
    background: #231A12;
    border-bottom: 1px solid #3D2B1A;
    padding: 14px 24px;
    display: flex; align-items: center; gap: 14px;
}
.topbar-avatar {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, #C4622D, #8B3A1A);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(196,98,45,0.35);
}
.topbar-name {
    font-family: 'Fraunces', serif;
    font-weight: 600; font-size: 17px;
    color: #F5E6C8;
    letter-spacing: 0.2px;
}
.topbar-sub { font-size: 12px; color: #8A7560; margin-top: 1px; }
.topbar-dot {
    width: 7px; height: 7px;
    background: #7CB87A;
    border-radius: 50%;
    display: inline-block; margin-right: 5px;
}

/* ── Chat area ── */
.chat-wrap { padding: 28px 24px 0; }

.msg-row {
    display: flex; gap: 10px;
    margin-bottom: 20px; align-items: flex-start;
}
.msg-row.user { flex-direction: row-reverse; }

.msg-avatar {
    width: 34px; height: 34px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0; margin-top: 2px;
}
.msg-avatar.amani {
    background: linear-gradient(135deg, #C4622D, #8B3A1A);
    box-shadow: 0 2px 6px rgba(196,98,45,0.3);
}
.msg-avatar.user { background: #2E2018; border: 1px solid #3D2B1A; }

.bubble {
    max-width: 80%; padding: 13px 17px;
    border-radius: 18px; font-size: 14.5px;
    line-height: 1.7; 
}
.bubble.amani {
    background: #2A1E13;
    border: 1px solid #3D2B1A;
    color: #E8D5B5;
    border-top-left-radius: 4px;
}
.bubble.user {
    background: linear-gradient(135deg, #C4622D, #A04E24);
    color: #FDF3E3;
    border-top-right-radius: 4px;
    box-shadow: 0 2px 10px rgba(196,98,45,0.25);
}

/* bold inside bubbles */
.bubble strong { color: #E8A87C; }
.bubble.user strong { color: #FDF3E3; }

/* ── Suggestion pills ── */
.pills-row {
    display: flex; flex-wrap: wrap; gap: 8px;
    padding: 4px 24px 16px;
}

/* ── Input area ── */
.input-wrap {
    position: sticky; bottom: 0;
    background: #1C1410;
    border-top: 1px solid #3D2B1A;
    padding: 14px 24px 22px;
    margin-top: 12px;
}

.stTextArea textarea {
    background: #2A1E13 !important;
    border: 1.5px solid #3D2B1A !important;
    border-radius: 14px !important;
    color: #E8D5B5 !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
    resize: none !important;
    padding: 13px 16px !important;
    min-height: 52px !important;
    caret-color: #C4622D !important;
}
.stTextArea textarea::placeholder { color: #5C4A35 !important; }
.stTextArea textarea:focus {
    border-color: #C4622D !important;
    box-shadow: 0 0 0 3px rgba(196,98,45,0.15) !important;
    outline: none !important;
}

/* Send button */
.stButton > button {
    background: linear-gradient(135deg, #C4622D, #A04E24) !important;
    color: #FDF3E3 !important;
    border: none !important;
    border-radius: 12px !important;
    height: 52px !important;
    width: 52px !important;
    font-size: 22px !important;
    padding: 0 !important;
    box-shadow: 0 2px 10px rgba(196,98,45,0.3) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #D4723D, #B05E34) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(196,98,45,0.4) !important;
}

/* Pill buttons override — only for suggestion row */
div[data-testid="stHorizontalBlock"] .stButton > button {
    background: #2A1E13 !important;
    color: #C4622D !important;
    border: 1px solid #3D2B1A !important;
    border-radius: 20px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    height: auto !important;
    width: auto !important;
    padding: 6px 16px !important;
    box-shadow: none !important;
    transition: all 0.15s !important;
}
div[data-testid="stHorizontalBlock"] .stButton > button:hover {
    background: #3D2B1A !important;
    border-color: #C4622D !important;
    transform: none !important;
    box-shadow: none !important;
}

.stSpinner > div { display: none !important; }

/* scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #1C1410; }
::-webkit-scrollbar-thumb { background: #3D2B1A; border-radius: 10px; }
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
- Mechatronics and Robotics: relevant for students pursuing embedded systems, drones, autonomous systems, aerospace

Tone:
- Talk like a smart encouraging older sibling, not a textbook
- Be direct and specific — name actual programs, hubs, deadlines
- Short paragraphs, use bold for key terms
- When given a bio, score it and give clear next steps
- Never say "Great question!" or use hollow filler phrases
- Networking scripts must sound human and specific, not templated
- Respond in markdown"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Habari! I am **Amani** — your African student mentor. 🌍\n\nI can help you find scholarships, sharpen your profile, write outreach messages to professors, or map out your next move in Engineering, Medicine, Law, Tech, or any other field.\n\nWhat are you working on?"
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
            return "Add your **ANTHROPIC_API_KEY** to Streamlit secrets to activate me."
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
        return "The `anthropic` package is not installed. Check your requirements.txt."
    except Exception as e:
        return f"Error: {str(e)}"

# ── TOP BAR ──
st.markdown("""
<div class="topbar">
  <div class="topbar-avatar">🌍</div>
  <div>
    <div class="topbar-name">Amani</div>
    <div class="topbar-sub"><span class="topbar-dot"></span>African Student Mentor · Always here</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── MESSAGES ──
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

# ── SUGGESTION PILLS ──
SUGGESTIONS = [
    "Find me a scholarship",
    "Analyze my profile",
    "Write a message to a professor",
    "Hubs near me",
]

if len(st.session_state.messages) == 1:
    cols = st.columns(len(SUGGESTIONS))
    for i, suggestion in enumerate(SUGGESTIONS):
        with cols[i]:
            if st.button(suggestion, key=f"pill_{i}"):
                st.session_state.pending = suggestion
                st.rerun()

# ── INPUT BAR ──
st.markdown('<div class="input-wrap">', unsafe_allow_html=True)
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

# ── HANDLE SEND ──
message_to_send = None
if send and user_input.strip():
    message_to_send = user_input.strip()
elif st.session_state.pending:
    message_to_send = st.session_state.pending
    st.session_state.pending = None

if message_to_send:
    st.session_state.messages.append({"role": "user", "content": message_to_send})
    with st.spinner(""):
        reply = call_amani(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
