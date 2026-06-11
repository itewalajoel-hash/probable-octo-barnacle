import streamlit as st
import anthropic
import json
import datetime
import os

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Amani Global Hub",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── DESIGN SYSTEM ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Remove Streamlit default chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1100px; }

/* Custom header */
.amani-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem 0 1rem;
    border-bottom: 1px solid #E8EDEA;
    margin-bottom: 2rem;
}
.amani-logo {
    font-size: 1.4rem;
    font-weight: 600;
    color: #0F6E56;
    letter-spacing: -0.5px;
}
.amani-live {
    background: #E1F5EE;
    color: #0F6E56;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
}

/* Cards */
.card {
    background: #ffffff;
    border: 1px solid #E8EDEA;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.card-accent {
    border-left: 3px solid #0F6E56;
}

/* Expert vs Student badge */
.badge-expert {
    background: #E1F5EE;
    color: #085041;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.badge-student {
    background: #F1EFE8;
    color: #5F5E5A;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Score meter */
.score-display {
    text-align: center;
    padding: 2rem;
    background: #F8FCFA;
    border-radius: 14px;
    border: 1px solid #9FE1CB;
}
.score-number {
    font-size: 3.5rem;
    font-weight: 600;
    color: #0F6E56;
    line-height: 1;
}
.score-label {
    font-size: 13px;
    color: #888780;
    margin-top: 4px;
}

/* Tabs override */
div[data-testid="stTabs"] button {
    font-size: 14px !important;
    padding: 8px 16px !important;
}

/* Primary button */
.stButton > button {
    background: #0F6E56 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    transition: background 0.2s !important;
}
.stButton > button:hover {
    background: #085041 !important;
}

/* Text areas and inputs */
.stTextArea textarea, .stTextInput input, .stSelectbox select {
    border-radius: 8px !important;
    border: 1px solid #D3D1C7 !important;
    font-size: 14px !important;
}

/* Community post form */
.post-form {
    background: #F8FCFA;
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1.5rem;
    border: 1px solid #9FE1CB;
}

/* Opportunity card */
.opp-card {
    background: white;
    border: 1px solid #E8EDEA;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}
.opp-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
}

/* Analysis result blocks */
.strength-block {
    background: #EAF3DE;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin: 0.4rem 0;
    font-size: 14px;
    color: #3B6D11;
}
.warning-block {
    background: #FAEEDA;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin: 0.4rem 0;
    font-size: 14px;
    color: #633806;
}

/* Networking script box */
.script-box {
    background: #F8FCFA;
    border: 1px solid #9FE1CB;
    border-radius: 10px;
    padding: 1.25rem;
    font-size: 13px;
    line-height: 1.7;
    color: #2C2C2A;
    white-space: pre-wrap;
}

hr { border: none; border-top: 1px solid #E8EDEA; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ─── ANTHROPIC CLIENT ────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if api_key:
        return anthropic.Anthropic(api_key=api_key)
    return None

client = get_client()

# ─── SESSION STATE ───────────────────────────────────────────────────────────
if "community_posts" not in st.session_state:
    st.session_state.community_posts = [
        {
            "name": "Dr. Sarah Okonkwo",
            "location": "London, UK",
            "role": "expert",
            "field": "Medicine",
            "msg": "To all medical students in Nigeria and Kenya — the 2025 Wellcome Trust Africa Initiative is now open. Focus your application on community impact and rural access. I am happy to review personal statements. DM me.",
            "likes": 94,
            "time": "2 hours ago"
        },
        {
            "name": "Emmanuel Tunde",
            "location": "Lagos, Nigeria",
            "role": "student",
            "field": "Engineering",
            "msg": "I just finished building a solar-powered SMS alert system for flood warnings in my community. How do I present this to international companies? Looking for advice from engineers abroad.",
            "likes": 47,
            "time": "5 hours ago"
        },
        {
            "name": "Prof. Klaus Weber",
            "location": "Berlin, Germany",
            "role": "expert",
            "field": "Engineering",
            "msg": "African engineering students: DAAD fellowships for 2026 applications are open now. Germany specifically wants candidates with hands-on prototyping experience. Build something. Document it. That is your ticket.",
            "likes": 61,
            "time": "Yesterday"
        },
        {
            "name": "Amara Diallo",
            "location": "Accra, Ghana",
            "role": "student",
            "field": "Law",
            "msg": "Just got accepted into the African Court on Human and Peoples' Rights internship! Happy to share what worked in my application letter for any law students who want tips.",
            "likes": 112,
            "time": "2 days ago"
        }
    ]

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# ─── DATA ────────────────────────────────────────────────────────────────────
SCHOLARSHIPS = [
    {"name": "Mastercard Foundation Scholars", "focus": "Academic excellence & leadership, all fields", "link": "https://mastercardfdn.org/all/scholars/", "icon": "🎓"},
    {"name": "Chevening (UK Government)", "focus": "Law, politics, business, public policy", "link": "https://www.chevening.org/", "icon": "🇬🇧"},
    {"name": "Rhodes Scholarship", "focus": "Post-graduate study at Oxford University", "link": "https://www.rhodeshouse.ox.ac.uk/", "icon": "📚"},
    {"name": "DAAD — Germany", "focus": "Engineering, science, medicine, research", "link": "https://www2.daad.de/", "icon": "🇩🇪"},
    {"name": "Mandela Rhodes Scholarship", "focus": "African leadership across all fields", "link": "https://www.mandelarhodes.org/", "icon": "✊"},
    {"name": "MEXT — Japan", "focus": "Technology, robotics, and specialized research", "link": "https://www.studyinjapan.go.jp/", "icon": "🇯🇵"},
    {"name": "Carnegie Mellon Africa", "focus": "Engineering, IT, and data science (Rwanda campus)", "link": "https://www.cmu.edu/africa/", "icon": "🏫"},
    {"name": "Commonwealth Scholarship", "focus": "Development, health, education (UK partnership)", "link": "https://cscuk.fcdo.gov.uk/", "icon": "🌐"},
]

HUBS = {
    "Uganda": {"hub": "Innovation Village, Kampala", "org": "Hive Colab, Makerere University Research Grants", "link": "https://innovationvillage.co.ug/"},
    "Nigeria": {"hub": "CcHub, Lagos / Abuja Tech Village", "org": "Tony Elumelu Foundation, StartupList Africa", "link": "https://cchubnigeria.com/"},
    "Kenya": {"hub": "iHub, Nairobi (Silicon Savannah)", "org": "Safaricom Spark, Strathmore University", "link": "https://ihub.co.ke/"},
    "Ghana": {"hub": "MEST Africa, Accra", "org": "Ghana Tech Lab, Meltwater School", "link": "https://meltwater.org/mest/"},
    "Rwanda": {"hub": "Kigali Innovation City / CMU Africa", "org": "Rwanda ICT Chamber, kLab", "link": "https://klab.rw/"},
    "South Africa": {"hub": "Innovation Hub, Pretoria", "org": "SKA Project, Cape Town Science Centre", "link": "https://www.theinnovationhub.com/"},
    "Egypt": {"hub": "TIEC Cairo", "org": "AUC Venture Lab, Cairo Angels", "link": "https://www.tiec.gov.eg/"},
    "Tanzania": {"hub": "Buni Hub, Dar es Salaam", "org": "Nelson Mandela African Institution of Science", "link": "https://bunihub.or.tz/"},
}

# ─── AI ANALYSIS ─────────────────────────────────────────────────────────────
def ai_analyze(bio: str, field: str, country: str, name: str) -> dict:
    if not client:
        # Fallback heuristic analysis if no API key
        score = 40
        strengths = []
        warnings = []
        action_words = ["built", "led", "created", "organized", "researched", "designed", "founded", "volunteered", "developed", "managed"]
        found = [w for w in action_words if w in bio.lower()]
        score += len(found) * 8
        if len(bio.split()) > 60: score += 15
        if found:
            strengths.append(f"Strong action-oriented language detected: {', '.join(found[:4])}.")
        if len(bio.split()) < 40:
            warnings.append("Your bio is too short. International reviewers expect 60+ words with specific achievements.")
        if not any(w in bio.lower() for w in ["international", "global", "award", "publish", "partner"]):
            warnings.append("Add international exposure — competitions, collaborations, or publications strengthen your profile significantly.")
        return {
            "score": min(score, 100),
            "strengths": strengths or ["General potential detected. Use more specific achievement language."],
            "warnings": warnings or ["Profile looks solid. Focus on quantifying your impact (numbers, reach, outcomes)."],
            "idea": f"Start a local chapter of {field} for Africa in your city — connect with the nearest tech hub to launch.",
            "networking": f"Hi [Professor's Name],\n\nMy name is {name}, a {field} student from {country}. I came across your work on [specific topic] and I am currently developing a project around [your project]. I would be honoured to ask you one focused question about your career path.\n\nThank you for your time.",
        }

    prompt = f"""You are a world-class career coach specializing in helping African students access global opportunities. Analyze this student's profile and return ONLY a valid JSON object with no extra text.

Student:
- Name: {name}
- Country: {country}
- Field: {field}
- Bio/Profile: {bio}

Return this exact JSON structure:
{{
  "score": <integer 0-100, their global competitiveness score>,
  "strengths": [<2-3 specific strengths as strings>],
  "warnings": [<2-3 specific, actionable improvements as strings>],
  "idea": "<one outstanding project idea specific to their field and African context, 1-2 sentences>",
  "networking": "<a professional LinkedIn/email outreach message they can send to a professor or engineer, personalized for their field and country>"
}}

Be specific, honest, and Africa-aware. Reference real African programs, hubs, or opportunities where relevant. Score ruthlessly — most profiles need work."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.content[0].text.strip()
        # Strip markdown fences if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except Exception as e:
        return {
            "score": 70,
            "strengths": ["Profile submitted successfully.", "AI analysis encountered an error — see raw feedback below."],
            "warnings": [f"Error: {str(e)}. Check your API key in Streamlit secrets."],
            "idea": "Build a local mentorship network in your university department.",
            "networking": f"Hi [Name],\nI am {name}, a {field} student from {country}. I would love to ask one question about your career journey. Thank you."
        }

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="amani-header">
    <div class="amani-logo">🌍 Amani Global Hub</div>
    <div class="amani-live">● 1,240 Online</div>
</div>
""", unsafe_allow_html=True)

st.markdown("**Connecting African students with international experts and real opportunities.**")
st.markdown("")

# ─── MAIN TABS ───────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🧬 AI Profile Analyzer", "🌎 Global Community", "🎓 Opportunities & Hubs"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — AI PROFILE ANALYZER
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown("#### Your profile")
        name = st.text_input("Full name", placeholder="e.g. Joel Lubwama")
        colA, colB = st.columns(2)
        with colA:
            country = st.selectbox("Country", list(HUBS.keys()) + ["Niger", "Other"])
        with colB:
            field = st.selectbox("Field of study", ["Engineering & Architecture", "Medicine & Health", "Technology & Data", "Law & Policy", "Arts & Creative", "Business & Agri-business"])

        bio = st.text_area(
            "Describe what you have built, led, or achieved",
            height=180,
            placeholder="Be specific. What projects have you worked on? What problems did you solve? Who did you help? Have you won any competitions or led any initiatives?"
        )

        if not client:
            st.caption("⚠️ Add your ANTHROPIC_API_KEY to Streamlit secrets for AI-powered analysis. Fallback scoring is active.")

        analyze_clicked = st.button("Analyze my profile →", use_container_width=True)

        if analyze_clicked:
            if not bio.strip():
                st.error("Please describe your background first.")
            elif not name.strip():
                st.error("Please enter your name.")
            else:
                with st.spinner("Analyzing your global competitiveness..."):
                    result = ai_analyze(bio, field, country, name)
                    st.session_state.analysis_result = result

    with col_right:
        result = st.session_state.analysis_result
        if result:
            score = result.get("score", 0)
            st.markdown(f"""
            <div class="score-display">
                <div class="score-number">{score}%</div>
                <div class="score-label">Global competitiveness score</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("")
            st.progress(score / 100)

            st.markdown("**Strengths detected**")
            for s in result.get("strengths", []):
                st.markdown(f'<div class="strength-block">✓ {s}</div>', unsafe_allow_html=True)

            st.markdown("**How to improve**")
            for w in result.get("warnings", []):
                st.markdown(f'<div class="warning-block">→ {w}</div>', unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown("**Outstanding project idea for you**")
            st.info(result.get("idea", ""))

            st.markdown("**Your networking script**")
            st.markdown(f'<div class="script-box">{result.get("networking", "")}</div>', unsafe_allow_html=True)

            if country in HUBS:
                hub = HUBS[country]
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(f"**Your local launchpad in {country}**")
                st.markdown(f"🏢 **Hub:** {hub['hub']}")
                st.markdown(f"🤝 **Orgs:** {hub['org']}")
                st.markdown(f"[Visit →]({hub['link']})")
        else:
            st.markdown("""
            <div style="background:#F8FCFA; border-radius:14px; padding:2rem; text-align:center; color:#888780; margin-top:1rem;">
                <div style="font-size:2.5rem; margin-bottom:1rem;">🎯</div>
                <div style="font-size:15px; font-weight:500; color:#2C2C2A;">Your analysis will appear here</div>
                <div style="font-size:13px; margin-top:8px;">Fill in your profile on the left and click Analyze.</div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — GLOBAL COMMUNITY
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    col_feed, col_post = st.columns([2, 1], gap="large")

    with col_post:
        st.markdown("#### Post to the community")
        st.markdown("""
        <div style="font-size:13px; color:#888780; margin-bottom:1rem;">
        Share an opportunity, ask a question, or offer advice to students across Africa and beyond.
        </div>
        """, unsafe_allow_html=True)

        p_name = st.text_input("Your name", key="p_name", placeholder="e.g. Kofi Mensah")
        p_loc = st.text_input("Location", key="p_loc", placeholder="e.g. Accra, Ghana")
        p_role = st.radio("I am a", ["Student", "Expert / Professional"], horizontal=True, key="p_role")
        p_field = st.selectbox("Field", ["Engineering", "Medicine", "Law", "Technology", "Arts", "Business", "Other"], key="p_field")
        p_msg = st.text_area("Your message", height=120, key="p_msg", placeholder="Share something useful for the community...")

        if st.button("Post to global feed", use_container_width=True):
            if p_name.strip() and p_msg.strip():
                st.session_state.community_posts.insert(0, {
                    "name": p_name.strip(),
                    "location": p_loc.strip() or "Africa",
                    "role": "expert" if "Expert" in p_role else "student",
                    "field": p_field,
                    "msg": p_msg.strip(),
                    "likes": 0,
                    "time": "Just now"
                })
                st.success("Posted! Your message is now live.")
                st.rerun()
            else:
                st.error("Please add your name and a message.")

    with col_feed:
        st.markdown("#### Global feed")

        for post in st.session_state.community_posts:
            badge_class = "badge-expert" if post["role"] == "expert" else "badge-student"
            badge_text = "Expert" if post["role"] == "expert" else "Student"
            st.markdown(f"""
            <div class="card">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
                    <span class="{badge_class}">{badge_text}</span>
                    <span style="font-size:12px; color:#888780;">{post["field"]}</span>
                    <span style="font-size:12px; color:#B4B2A9; margin-left:auto;">{post["time"]}</span>
                </div>
                <div style="font-weight:500; font-size:15px; color:#2C2C2A;">{post["name"]}</div>
                <div style="font-size:13px; color:#888780; margin-bottom:10px;">{post["location"]}</div>
                <div style="font-size:14px; color:#444441; line-height:1.65;">{post["msg"]}</div>
                <div style="margin-top:12px; font-size:12px; color:#B4B2A9;">❤️ {post["likes"]} &nbsp;&nbsp; 💬 Reply</div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — OPPORTUNITIES & HUBS
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("#### World-class scholarships")
    st.markdown('<div style="font-size:13px; color:#888780; margin-bottom:1.5rem;">These are real scholarships with direct links. Apply to at least 3 simultaneously.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    for i, s in enumerate(SCHOLARSHIPS):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div class="card card-accent">
                <div style="font-size:1.4rem;">{s["icon"]}</div>
                <div style="font-weight:600; font-size:15px; margin:8px 0 4px; color:#2C2C2A;">{s["name"]}</div>
                <div style="font-size:13px; color:#888780; margin-bottom:12px;">{s["focus"]}</div>
                <a href="{s["link"]}" target="_blank" style="background:#0F6E56; color:white; padding:6px 16px; border-radius:6px; font-size:13px; text-decoration:none; font-weight:500;">Apply →</a>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("#### African innovation hubs by country")
    st.markdown('<div style="font-size:13px; color:#888780; margin-bottom:1.5rem;">Walk into these hubs. Introduce yourself. Many students have found mentors and opportunities just by showing up.</div>', unsafe_allow_html=True)

    hub_country = st.selectbox("Select your country", list(HUBS.keys()), key="hub_country")
    if hub_country in HUBS:
        hub = HUBS[hub_country]
        st.markdown(f"""
        <div class="card" style="max-width:500px;">
            <div style="font-weight:600; font-size:16px; color:#2C2C2A; margin-bottom:6px;">🏢 {hub["hub"]}</div>
            <div style="font-size:14px; color:#444441; margin-bottom:12px;">Also connect with: <strong>{hub["org"]}</strong></div>
            <a href="{hub["link"]}" target="_blank" style="background:#0F6E56; color:white; padding:6px 16px; border-radius:6px; font-size:13px; text-decoration:none; font-weight:500;">Visit website →</a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("#### Pro tip: remote internships")
    st.info("Search for 'Remote First' companies on LinkedIn and AngelList. They hire on skill, not location. You can intern for a UK or US company from Kampala, Lagos, or Nairobi — with no visa required.")
