 import streamlit as st
import os
import json

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Amani — Your African Opportunity Mentor",
    page_icon="🌍",
    layout="centered",
)

# ── STYLES ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 0 !important;
    max-width: 780px !important;
    margin: 0 auto;
}

/* ── Top bar ── */
.topbar {
    position: sticky;
    top: 0;
    z-index: 100;
    background: #fff;
    border-bottom: 1px solid #EBEBEB;
    padding: 14px 24px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.topbar-avatar {
    width: 36px; height: 36px;
    background: #0F6E56;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 18px; flex-shrink: 0;
}
.topbar-name { font-weight: 600; font-size: 15px; color: #111; }
.topbar-sub  { font-size: 12px; color: #8A8A8A; }
.topbar-dot  {
    width: 8px; height: 8px;
    background: #22C55E; border-radius: 50%;
    display: inline-block; margin-right: 4px;
}

/* ── Chat messages ── */
.chat-wrap {
    padding: 24px 24px 0;
}

.msg-row {
    display: flex;
    gap: 10px;
    margin-bottom: 18px;
    align-items: flex-start;
}
.msg-row.user { flex-direction: row-reverse; }

.msg-avatar {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px;
    flex-shrink: 0;
    margin-top: 2px;
}
.msg-avatar.amani { background: #0F6E56; color: white; }
.msg-avatar.user  { background: #F0F0F0; color: #333; }

.bubble {
    max-width: 82%;
    padding: 12px 16px;
    border-radius: 16px;
    font-size: 14.5px;
    line-height: 1.65;
    color: #1A1A1A;
}
.bubble.amani {
    background: #F7F7F5;
    border-top-left-radius: 4px;
}
.bubble.user {
    background: #0F6E56;
    color: white;
    border-top-right-radius: 4px;
    text-align: left;
}

/* ── Typing indicator ── */
.typing {
    display: flex; gap: 5px; align-items: center;
    padding: 12px 16px;
    background: #F7F7F5;
    border-radius: 16px;
    border-top-left-radius: 4px;
    width: fit-content;
}
.typing span {
    width: 7px; height: 7px;
    background: #9CA3AF;
    border-radius: 50%;
    animation: bounce 1.2s infinite;
}
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); opacity: 0.5; }
    40%           { transform: translateY(-6px); opacity: 1; }
}

/* ── Suggestion pills ── */
.pills-wrap {
    display: flex; flex-wrap: wrap; gap: 8px;
    padding: 12px 24px 0;
}
.pill {
    background: #F0FDF8;
    border: 1px solid #A7F3D0;
    color: #0F6E56;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    cursor: pointer;
    white-space: nowrap;
    font-weight: 500;
}

/* ── Input area ── */
.input-area {
    position: sticky;
    bottom: 0;
    background: white;
    border-top: 1px solid #EBEBEB;
    padding: 14px 24px 20px;
    margin-top: 16px;
}

/* Override Streamlit textarea */
.stTextArea textarea {
    border: 1.5px solid #D1D5DB !important;
    border-radius: 12px !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
    resize: none !important;
    padding: 12px 14px !important;
    box-shadow: none !important;
    line-height: 1.5 !important;
    min-height: 52px !important;
}
.stTextArea textarea:focus {
    border-color: #0F6E56 !important;
    box-shadow: 0 0 0 3px rgba(15,110,86,0.1) !important;
}

/* Send button */
div[data-testid="column"]:last-child .stButton > button {
    background: #0F6E56 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    height: 52px !important;
    width: 52px !important;
    font-size: 20px !important;
    padding: 0 !important;
    margin-top: 0 !important;
}
div[data-testid="column"]:last-child .stButton > button:hover {
    background: #0A5240 !important;
}

/* Pill buttons */
div[data-testid="column"] .stButton > button {
    background: #F0FDF8 !important;
    color: #0F6E56 !important;
    border: 1px solid #A7F3D0 !important;
    border-radius: 20px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 6px 14px !important;
    height: auto !important;
    white-space: nowrap !important;
}

.stSpinner > div { display: none; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! I'm **Amani**, your African student mentor. 🌍\n\nI can help you find scholarships, build your profile, connect with opportunities, write LinkedIn messages to professors, or just answer questions about your career path.\n\nWhat's on your mind?"
        }
    ]
if "pending" not in st.session_state:
    st.session_state.pending = None

# ── SYSTEM PROMPT ─────────────────────────────────────────────────────────────
SYSTEM = """You are Amani, a warm, smart, and direct AI mentor for African university students. You operate exactly like Claude — conversational, thoughtful, and specific. Never give generic advice.

Your expertise:
- African-specific scholarships: Mastercard Foundation, Chevening, Rhodes, DAAD, Mandela Rhodes, MEXT Japan, Carnegie Mellon Africa, Commonwealth
- African innovation hubs: Innovation Village (Uganda), iHub (Kenya), CcHub (Nigeria), MEST (Ghana), kLab (Rwanda), Buni Hub (Tanzania)
- Fields: Engineering, Medicine, Law, Tech/AI, Arts, Business, Agriculture
- Writing LinkedIn messages, cold emails, personal statements
- Career strategy for students in Nigeria, Kenya, Ghana, Uganda, Rwanda, South Africa, Egypt, Tanzania, and all of Africa
- How to build an "outstanding" profile: projects, volunteering, online presence, open source, research

Tone rules:
- Talk like a smart, encouraging older sibling or mentor — not a textbook
- Be direct and specific. Name actual programs, actual hubs, actual deadlines
- Keep replies concise. Use short paragraphs. Use **bold** for key terms
- If someone shares their bio or profile, give honest, structured feedback with a score and clear next steps
- Never say "Great question!" or use hollow filler phrases
- When writing networking scripts (LinkedIn, email), make them sound human and specific, not templated
- Uganda context: know about Innovation Village Kampala, Hive Colab, Makerere University, UCU (Uganda Christian University), UIRI

You are running inside a Streamlit app. Respond in markdown."""

# ── API CALL ──────────────────────────────────────────────────────────────────
def call_amani(messages):
    try:
        import anthropic
        api_key = os.environ.get("ANTHROPIC_API_KEY", st.secrets.get("ANTHROPIC_API_KEY", ""))
        if not api_key:
            return "⚠️ No API key found. Add `ANTHROPIC_API_KEY` to your Streamlit secrets to activate Amani."

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
        return "⚠️ The `anthropic` package is not installed. Check your requirements.txt."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ── RENDER CHAT ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div class="topbar-avatar">🌍</div>
  <div>
    <div class="topbar-name">Amani</div>
    <div class="topbar-sub"><span class="topbar-dot"></span>African Student Mentor · Always online</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    role = msg["role"]
    css_role = "amani" if role == "assistant" else "user"
    avatar = "🌍" if role == "assistant" else "👤"
    st.markdown(f"""
    <div class="msg-row {css_role}">
      <div class="msg-avatar {css_role}">{avatar}</div>
      <div class="bubble {css_role}">{msg["content"].replace(chr(10), "<br>")}</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── SUGGESTION PILLS (only at start) ─────────────────────────────────────────
SUGGESTIONS = [
    "Find me a scholarship",
    "Analyze my profile",
    "Write a LinkedIn message to a professor",
    "What hubs are near me?",
    "How do I stand out in Engineering?",
]

if len(st.session_state.messages) == 1:
    cols = st.columns(len(SUGGESTIONS))
    for i, suggestion in enumerate(SUGGESTIONS):
        with cols[i % len(cols)]:
            if st.button(suggestion, key=f"pill_{i}"):
                st.session_state.pending = suggestion
                st.rerun()

# ── INPUT BAR ─────────────────────────────────────────────────────────────────
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

# ── HANDLE SEND ───────────────────────────────────────────────────────────────
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
