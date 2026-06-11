import streamlit as st
import datetime

# --- 1. PAGE CONFIG & MODERN THEME ---
st.set_page_config(page_title="Amani Global Hub", page_icon="🌍", layout="wide")

# Custom CSS for the "Appetite" (Miro/Modern Startup look)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { 
        background: linear-gradient(45deg, #007bff, #00d4ff); 
        color: white; border: none; border-radius: 10px; 
        font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(0,212,255,0.4); }
    .opportunity-card {
        background-color: #1a1c24; border-left: 5px solid #00d4ff;
        padding: 20px; border-radius: 10px; margin-bottom: 20px;
    }
    .global-tag {
        background: #262730; padding: 5px 15px; border-radius: 50px;
        font-size: 0.8rem; border: 1px solid #444;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GLOBAL BRAIN (Data) ---
SCHOLARSHIPS = [
    {"name": "Mastercard Foundation", "link": "https://mastercardfdn.org/all/scholars/", "tag": "All Fields"},
    {"name": "Chevening UK", "link": "https://www.chevening.org/", "tag": "Leadership"},
    {"name": "Rhodes Scholar", "link": "https://www.rhodeshouse.ox.ac.uk/", "tag": "Oxford"}
]

# --- 3. THE APP INTERFACE ---
def main():
    # --- HEADER ---
    st.title("🌍 Amani Global Student Hub")
    st.markdown("### *Where African Excellence Meets Global Opportunity*")
    
    tab1, tab2, tab3 = st.tabs(["🚀 Profile Architect", "💬 Global Community", "🎓 Opportunities"])

    # --- TAB 1: AI ARCHITECT (Claude-Style Analysis) ---
    with tab1:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("#### Analyze your Profile")
            name = st.text_input("Full Name")
            field = st.selectbox("Your Vision", ["Medicine", "Engineering", "Law", "Tech", "Arts", "Business"])
            bio = st.text_area("Describe your impact (What have you built or led?)", height=150)
            
            if st.button("Generate My Roadmap"):
                st.balloons()
                score = 50 + (len(bio.split()) // 2)
                st.session_state['score'] = min(score, 100)
        
        with col2:
            if 'score' in st.session_state:
                st.markdown(f"### Score: {st.session_state['score']}%")
                st.progress(st.session_state['score'] / 100)
                st.markdown(f"""
                <div class='opportunity-card'>
                    <h4>🎯 Outstanding Move for {field}</h4>
                    <p>Stop waiting for permission. Start a local chapter of <b>'{field} for Africa'</b> in your city.</p>
                    <p><i>Recommendation:</i> Use LinkedIn to find 3 professors in {field} today.</p>
                </div>
                """, unsafe_allow_html=True)

    # --- TAB 2: GLOBAL COMMUNITY (Talk around the world) ---
    with tab2:
        st.header("💬 Global Student Message Board")
        st.write("Share your dream and connect with students globally.")
        
        with st.expander("➕ Post a Message to the World"):
            msg_name = st.text_input("Name", key="msg_name")
            msg_country = st.selectbox("Country", ["Nigeria", "Kenya", "Ghana", "Uganda", "Rwanda", "Other"], key="msg_country")
            msg_text = st.text_area("Your Dream/Message")
            if st.button("Post Message"):
                st.success("Your message is live! (In this demo, it shows below)")

        # Mock Global Feed
        st.markdown("---")
        posts = [
            {"name": "Kofi", "country": "Ghana", "msg": "Building a solar irrigation system in Kumasi! Looking for partners."},
            {"name": "Amara", "country": "Nigeria", "msg": "Applying for Law in the UK. Any tips on the personal statement?"},
            {"name": "Samuel", "country": "Kenya", "msg": "Medical student passionate about Tele-medicine in rural areas."}
        ]
        
        for p in posts:
            st.markdown(f"""
            <div class='opportunity-card'>
                <b>{p['name']}</b> from <span class='global-tag'>{p['country']}</span> says:
                <p style='margin-top:10px;'>"{p['msg']}"</p>
            </div>
            """, unsafe_allow_html=True)

    # --- TAB 3: OPPORTUNITIES ---
    with tab3:
        st.header("💰 World-Class Scholarships")
        for s in SCHOLARSHIPS:
            st.markdown(f"""
            <div class='opportunity-card'>
                <h4>{s['name']}</h4>
                <span class='global-tag'>{s['tag']}</span><br><br>
                <a href='{s['link']}' target='_blank'><button style='padding:5px 15px; border-radius:5px; border:none; background:#00d4ff; color:black; font-weight:bold; cursor:pointer;'>Apply Now</button></a>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
