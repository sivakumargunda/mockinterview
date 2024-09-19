
import streamlit as st
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(page_title="AI Interviewer", layout="wide")

# Styling with CSS for a more modern and visually appealing look
st.markdown("""
<style>
body {
    background-color: #333;           
}
.main {
    background-color: #111; /* Light gray background */
}
.sidebar .sidebar-content {
    background-color: #333333; /* Darker sidebar background */
    color: white;
}
.sidebar .sidebar-content a {
    color: #61dafb;
}
.button-style {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 20px;
    text-align: center;
    display: inline-block;
    font-size: 16px;
    margin: 10px 2px;
    cursor: pointer;
    border-radius: 8px;
}
.title-style {
    font-size: 36px;
    color: #4CAF50;
    text-align: center;
    font-weight: bold;
}
.subtitle-style {
    font-size: 24px;
    color: #f5f5f5;
    text-align: center;
    margin-bottom: 20px;
}
.section-header {
    font-size: 20px;
    color: #4CAF50;
    text-align: left;
    margin-bottom: 10px;
}
.content-text {
    font-size: 16px;
    color: #333333;
    text-align: left;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Define app pages
def homepage():
    st.markdown('<h1 class="title-style">AI Interviewer Beta</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle-style">Welcome to the AI Interviewer Beta!</h2>', unsafe_allow_html=True)
    st.write("""
        This tool helps you prepare for interviews by generating job-specific questions,
        offering feedback, and simulating realistic interview scenarios.
    """)

    # Add images and icons for a professional touch
    st.image("https://image.shutterstock.com/image-photo/job-interview-concept-professional-interviewer-260nw-1037430767.jpg", use_column_width=True)

    st.markdown('<h3 class="subtitle-style">Tool Overview</h3>', unsafe_allow_html=True)
    st.write("This AI Interviewer covers several aspects including behavioral, professional, and resume-based questions.")

    # Collapsible sections for additional information
    with st.expander("🔄 Updates"):
        st.write("Version 1.1: Enhanced UI, added interview feedback system.")

    with st.expander("🛠 Tool Features"):
        st.write("✔ Behavioral Interview")
        st.write("✔ Professional Interview")
        st.write("✔ Resume-based Interview")
        st.write("✔ Customizable interview based on the job description.")
        st.write("✔ AI-Powered Feedback System")

def behavioral_screen():
    st.markdown('<h1 class="title-style">Behavioral Interview</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle-style">Practice for behavioral questions typically asked in interviews.</h2>', unsafe_allow_html=True)

    # Button to start the behavioral interview
    if st.button("Start Behavioral Interview", key="behavioral", help="Click to begin behavioral interview"):
        st.success("Behavioral interview started!")
        st.info("**Question:** Tell me about a time you faced a challenging situation and how you handled it.")

def professional_screen():
    st.markdown('<h1 class="title-style">Professional Interview</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle-style">Practice for professional questions based on your selected role.</h2>', unsafe_allow_html=True)

    if st.button("Start Professional Interview", key="professional", help="Click to begin professional interview"):
        st.success("Professional interview started!")
        st.info("**Question:** What technical challenges have you faced in your previous projects, and how did you solve them?")

def resume_screen():
    st.markdown('<h1 class="title-style">Resume-based Interview</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle-style">Practice questions based on your resume.</h2>', unsafe_allow_html=True)

    if st.button("Start Resume Interview", key="resume", help="Click to begin resume-based interview"):
        st.success("Resume-based interview started!")
        st.info("**Question:** Can you explain a project from your resume in detail? What challenges did you encounter?")

# Create the navigation menu on the left sidebar with icons and improved look
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation Options",
        options=["🏠 Homepage", "📝 Behavioral Screen", "💼 Professional Screen", "📄 Resume Screen"],
        icons=["house", "chat-left-dots", "briefcase", "file-earmark-person"],
        menu_icon="cast", default_index=0,
        styles={
            "container": {"background-color": "#333333"},  # Darker sidebar background
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {"font-size": "18px", "color": "white", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#4CAF50"},
        }
    )

# Additional Info in Sidebar
st.sidebar.title("📧 Additional Info")
st.sidebar.write("Contact Info: [email@example.com](mailto:email@example.com)")
st.sidebar.write("Feedback: [Link to feedback form](#)")
st.sidebar.write("Tools Overview: This tool uses **OpenAI**, **FAISS**, and **Langchain** for question generation.")
st.sidebar.write("🔗 [Streamlit Documentation](https://docs.streamlit.io/)")

# Main Content Logic
if selected == "🏠 Homepage":
    homepage()
elif selected == "📝 Behavioral Screen":
    behavioral_screen()
elif selected == "💼 Professional Screen":
    professional_screen()
elif selected == "📄 Resume Screen":
    resume_screen()

# Footer
st.markdown("""
<hr style="border:2px solid #4CAF50">
<p style="text-align:center; color: #f5f5f5;">Powered by OpenAI | Streamlit | FAISS | Langchain | © 2024 AI Interviewer</p>
""", unsafe_allow_html=True)
