import streamlit as st
from brain import InterviewAgent

st.set_page_config(page_title="One-Stop AI Interviewer", page_icon="🎤", layout="wide")
agent = InterviewAgent()

# --- Global State Management ---
if "transcript" not in st.session_state: st.session_state.transcript = ""
if "current_q" not in st.session_state: st.session_state.current_q = ""

st.title("🤖 One-Stop Agentic Interviewer")

# --- SIDEBAR: Navigation & Permissions ---
st.sidebar.header("Agent Settings")
target_role = st.sidebar.text_input("What role are you targeting?", "Python Developer")
mode = st.sidebar.selectbox("Select Mode", ["Waiting", "Study Mode", "Video Mock Interview"])

# --- MODULE 1: STUDY MODE ---
if mode == "Study Mode":
    st.subheader(f"📚 Preparation for {target_role}")
    if st.button("Generate My Study Kit"):
        with st.spinner("AI is researching..."):
            kit = agent.generate_study_kit(target_role)
            st.markdown(kit)

# --- MODULE 2: VIDEO INTERVIEW ---
elif mode == "Video Mock Interview":
    st.subheader("🎬 Live Video Interview")
    
    # 1. Video Component (Permission required by browser)
    st.camera_input("Your camera is active for the interview")
    
    # 2. Question Logic
    if st.button("Ask Me a Question"):
        st.session_state.current_q = agent.get_question(target_role, [])
        
    if st.session_state.current_q:
        st.info(f"**Interviewer:** {st.session_state.current_q}")
        user_ans = st.text_area("Your Response:")
        
        if st.button("Submit Answer"):
            st.session_state.transcript += f"Q: {st.session_state.current_q}\nA: {user_ans}\n"
            st.success("Answer recorded! Click 'Ask Me a Question' for the next one.")

    # 3. Final Feedback
    if st.session_state.transcript:
        if st.button("End Interview & Get Feedback"):
            report = agent.get_feedback(st.session_state.transcript)
            st.divider()
            st.header("📊 Performance Report")
            st.markdown(report)