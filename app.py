import streamlit as st
from brain import InterviewAgent

st.set_page_config(page_title="Agentic Interviewer", page_icon="🤖")

# Initialize the Agent
agent = InterviewAgent()

st.title("🤖 One-Stop Agentic Interviewer")
st.caption("Your AI-powered guide for Interview Preparation")

# Sidebar for Setup
st.sidebar.header("Settings")
target_role = st.sidebar.text_input("Target Role/Subject:", "Python Developer")
mode = st.sidebar.selectbox("Select Module", ["Preparation (Notes & MCQs)", "Mock Interview (Video)"])

# Module 1: Preparation
if mode == "Preparation (Notes & MCQs)":
    st.header(f"📚 Study Kit for {target_role}")
    if st.button("Generate Study Material"):
        with st.spinner("Agent is gathering data..."):
            kit = agent.generate_study_kit(target_role)
            st.markdown(kit)

# Module 2: Mock Interview
elif mode == "Mock Interview (Video)":
    st.header("🎥 AI Video Mock Interview")
    st.write("Enable your camera for the full experience.")
    
    # Permission-based camera input
    st.camera_input("Check your posture and focus")
    
    if st.button("Get Interview Question"):
        with st.spinner("Interviewer is thinking..."):
            question = agent.get_interview_question(target_role)
            st.info(f"**Interviewer:** {question}")
            
    answer = st.text_area("Type your response here or speak into the mic:")
    if st.button("Submit Response"):
        st.success("Response recorded. In a full version, this would be analyzed for feedback!")
