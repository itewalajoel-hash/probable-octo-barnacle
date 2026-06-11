import streamlit as st

# --- 1. SETTING THE PAGE ---
st.set_page_config(page_title="Amani Global Network", page_icon="🌐", layout="wide")

# --- 2. THE "PREMIUM" DESIGN (Custom CSS) ---
st.markdown("""
    <style>
    /* Miro/Modern Startup Style */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #f4f7f9;
    }
    
    .stApp {
        background: white;
    }

    /* Professional Card Design */
    .card {
        background: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #eef2f6;
        margin-bottom: 20px;
    }

    /* Expert Badge */
    .expert-badge {
        background: #e1f5fe;
        color: #039be5;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
    }

    /* Global Student Tag */
    .student-tag {
        background: #f1f8e9;
        color: #558b2f;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }

    /* High-end Buttons */
    .stButton>button {
        background: #000000;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #333333;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE GLOBAL HUB INTERFACE ---

def main():
    # --- HEADER SECTION ---
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.title("Amani Global Hub")
        st.markdown("##### Connecting African Ambition with Global Expertise.")
    with col_h2:
        st.write("")
        st.markdown("<div style='text-align: right;'><span class='expert-badge'>LIVE: 1,240 Online</span></div>", unsafe_allow_html=True)

    st.markdown("---")

    # --- TOP NAVIGATION ---
    tab_feed, tab_experts, tab_analyze = st.tabs(["🌎 Global Feed", "🎓 Expert Advice", "🧬 Profile Analyzer"])

    with tab_feed:
        st.subheader("Community Discussions")
        
        # Post a message (UI Only for now)
        with st.container():
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            t_col1, t_col2 = st.columns([0.1, 0.9])
            t_col1.image("https://ui-avatars.com/api/?name=You&background=random", width=50)
            t_col2.text_input("Share an opportunity or ask a global question...", key="main_input")
            st.markdown("</div>", unsafe_allow_html=True)

        # MOCK GLOBAL POSTS
        posts = [
            {"name": "Dr. Sarah Miller", "loc": "London, UK", "type": "EXPERT", "msg": "To all the engineering students in Kenya: The Dyson Fellowship is now open for African residents. Don't forget to focus on sustainability in your application!"},
            {"name": "Emmanuel Tunde", "loc": "Lagos, Nigeria", "type": "STUDENT", "msg": "I just finished my first Python project for a local hospital! How do I show this to international recruiters?"},
            {"name": "Prof. Karl Heinz", "loc": "Berlin, Germany", "type": "EXPERT", "msg": "For Law students in Ghana and Uganda: We are looking for 5 research assistants for the African Policy Review. Apply via DM."}
        ]

        for p in posts:
            badge = "expert-badge" if p['type'] == "EXPERT" else "student-tag"
            st.markdown(f"""
            <div class='card'>
                <span class='{badge}'>{p['type']}</span>
                <p style='margin-top:10px;'><b>{p['name']}</b> • {p['loc']}</p>
                <p style='color: #444;'>{p['msg']}</p>
                <hr style='border: 0.5px solid #eee;'>
                <small style='color: #888;'>💬 12 Comments • ❤️ 45 Likes</small>
            </div>
            """, unsafe_allow_html=True)

    with tab_experts:
        st.subheader("International Mentors")
        st.write("Talk to professionals from Europe, USA, and Asia who want to help African youth.")
        
        e_col1, e_col2 = st.columns(2)
        with e_col1:
            st.markdown("""
            <div class='card'>
                <h4>Dr. John Peterson</h4>
                <p><i>Senior Engineer at Google, California</i></p>
                <p>Expertise: Software Architecture, AI, Career Growth.</p>
                <button style='width:100%; padding:10px; border-radius:5px; border:1px solid #000; backgrou
