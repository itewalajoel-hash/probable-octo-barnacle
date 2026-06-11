import streamlit as st

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Amani Global", layout="wide")

# --- 2. THE DESIGN (Miro-Style Clean White) ---
st.markdown("<style>div.block-container{padding-top:2rem;} .stButton>button{width:100%; background-color:black; color:white; border-radius:10px;}</style>", unsafe_allow_html=True)

def main():
    # --- HEADER ---
    st.title("🌐 Amani Global Hub")
    st.write("Connecting African Students with International Experts & Opportunities.")
    st.markdown("---")

    # --- NAVIGATION TABS ---
    tab1, tab2, tab3 = st.tabs(["🌎 Global Community Feed", "🧬 Profile AI Analyzer", "🎓 International Experts"])

    # --- TAB 1: GLOBAL FEED (The 'Miro/Social' Feel) ---
    with tab1:
        st.subheader("Global Discussion Board")
        st.info("Experts from UK, USA, and Germany are active here.")
        
        # Post area
        with st.expander("Write a message to the Global Community"):
            u_name = st.text_input("Name")
            u_msg = st.text_area("What is your question or opportunity?")
            if st.button("Post to Global Feed"):
                st.success("Message sent to the network!")

        # Mock Posts (African Students + Global Experts)
        st.write("---")
        
        # Post 1 (Expert)
        st.markdown("🔹 **Dr. Linda Smith (Oxford University, UK)**")
        st.write("For my Medicine students in Nigeria and Kenya: The 2025 Health Research Grant is now open. Focus your bio on 'Community Impact' to stand out.")
        st.caption("💬 24 Comments | ❤️ 89 Likes")
        st.write("---")

        # Post 2 (Student)
        st.markdown("🔸 **Kofi Mensah (Engineering Student, Ghana)**")
        st.write("I am building a solar-powered irrigation pump. Can any international engineers advise on the best battery type for high-heat environments?")
        st.caption("💬 12 Comments | ❤️ 34 Likes")
        st.write("---")

        # Post 3 (Expert)
        st.markdown("🔹 **Prof. Hans Müller (Berlin, Germany)**")
        st.write("Law students: We are looking for interns who understand African Trade Law. Please ensure your LinkedIn profiles are updated.")
        st.caption("💬 5 Comments | ❤️ 12 Likes")

    # --- TAB 2: AI PROFILE ANALYZER (Claude Style) ---
    with tab2:
        st.subheader("Data Analysis: Global Competitiveness")
        f_choice = st.selectbox("Your Field", ["Medicine", "Engineering", "Law", "Tech", "Arts", "Business"])
        bio_input = st.text_area("Paste your bio/resume summary here for analysis:", height=150)
        
        if st.button("Run AI Analysis"):
            if bio_input:
                st.balloons()
                st.write("### Analysis Report")
                st.progress(75)
                st.write("✅ **Strengths:** Your practical experience is excellent.")
                st.write("⚠️ **Warning:** You need to mention more 'Global Standards' (e.g., ISO for Engineering or WHO for Medicine).")
                st.write("💡 **International Tip:** Experts in the West look for 'Systemic Thinking'—show how your project scales.")
            else:
                st.error("Please enter your bio first.")

    # --- TAB 3: SCHOLARSHIPS & CONNECTIONS ---
    with tab3:
        st.subheader("Global Opportunities")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("🏆 **Mastercard Foundation**")
            st.write("Focus: Leadership and Tech.")
            st.markdown("[Visit Website](https://mastercardfdn.org/)")
            
        with col2:
            st.write("🏆 **Chevening Scholarship**")
            st.write("Focus: Law, Politics, and Business.")
            st.markdown("[Visit Website](https://www.chevening.org/)")

if __name__ == "__main__":
    main()
