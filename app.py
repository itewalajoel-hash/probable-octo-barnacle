import streamlit as st
import random

# 1. Basic Page Setup
st.set_page_config(page_title="Amani AI", page_icon="🌍")

# 2. Scholarship Database
SCHOLARSHIPS = [
    {"name": "Mastercard Foundation", "link": "https://mastercardfdn.org/all/scholars/"},
    {"name": "Chevening Scholarship (UK)", "link": "https://www.chevening.org/"},
    {"name": "Rhodes Scholarship", "link": "https://www.rhodeshouse.ox.ac.uk/"},
    {"name": "DAAD Germany", "link": "https://www2.daad.de/"},
    {"name": "Mandela Rhodes", "link": "https://www.mandelarhodes.org/"}
]

# 3. AI Analysis Function
def run_analysis(bio, field):
    score = 50
    if len(bio.split()) < 30: score -= 20
    if "lead" in bio.lower() or "built" in bio.lower(): score += 20
    return min(score, 100)

# 4. The Website Interface
def main():
    st.title("🌍 Amani AI: African Excellence Architect")
    st.write("Analyze your profile and find global opportunities.")

    # Sidebar
    name = st.sidebar.text_input("Your Name")
    country = st.sidebar.selectbox("Country", ["Nigeria", "Kenya", "Ghana", "Uganda", "South Africa", "Egypt", "Rwanda", "Tanzania", "Niger"])
    field = st.sidebar.selectbox("Field", ["Medicine", "Engineering", "Tech", "Law", "Arts", "Business"])

    # Input Area
    user_bio = st.text_area("Tell us about your projects or goals:", height=150)

    if st.button("Analyze My Profile"):
        if user_bio:
            score = run_analysis(user_bio, field)
            st.metric(label="Profile Readiness Score", value=f"{score}%")
            
            # Advice logic
            st.subheader("💡 Outstanding Project Idea")
            if field == "Medicine":
                st.info("Project: Create a first-aid guide in your local language.")
            elif field == "Engineering":
                st.info("Project: Design a low-cost water filtration system.")
            elif field == "Law":
                st.info("Project: Create a simplified 'Know Your Rights' pamphlet for local traders.")
            else:
                st.info("Project: Start a local mentorship group for younger students.")

            st.subheader("💰 Recommended Scholarships")
            for s in SCHOLARSHIPS:
                st.write(f"- [{s['name']}]({s['link']})")

            st.subheader("🤝 Networking Script")
            st.code(f"Hi, I am {name}, a {field} student from {country}. I am working on a project to help my community. Can I ask you one question about your career?")
        else:
            st.error("Please type something in the box first!")

if __name__ == "__main__":
    main()
