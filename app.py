import streamlit as st
from brain import InterviewAgent

st.set_page_config(page_title="One-Stop AI Career Coach", layout="wide")
agent = InterviewAgent()

# --- Global Session State ---
if "transcript" not in st.session_state: st.session_state.transcript = ""
if "current_q" not in st.session_state: st.session_state.current_q = ""

# --- Sidebar Navigation ---
st.sidebar.title("🚀 Career Mission Control")
role = st.sidebar.text_input("Target Role/Topic:", "Python Developer")
menu = st.sidebar.radio("Go to Module:", 
    ["📚 Revision Notes", "🧠 Aptitude Round", "🎥 Video Mock Interview", "📝 Text Mock Interview"])

# --- 1. REVISION NOTES ---
if menu == "📚 Revision Notes":
    st.header("Quick Revision Notes")
    if st.button("Generate Study Material"):
        with st.spinner("Writing notes..."):
            notes = agent.generate_notes(role)
            st.markdown(notes)

# --- 2. APTITUDE ROUND ---
elif menu == "🧠 Aptitude Round":
    st.header("Interactive Aptitude Test")
    if "apt_q" not in st.session_state: st.session_state.apt_q = ""
    
    if st.button("Get New Question"):
        st.session_state.apt_q = agent.get_single_mcq(role)
    
    if st.session_state.apt_q:
        st.info(st.session_state.apt_q)
        ans = st.text_input("Your Answer (A/B/C/D):")
        if st.button("Submit & Save"):
            st.session_state.transcript += f"Q: {st.session_state.apt_q}\nUser Answer: {ans}\n\n"
            st.success("Recorded! Get next or finish below.")

# --- 3. VIDEO MOCK INTERVIEW ---
elif menu == "🎥 Video Mock Interview":
    st.header("AI Video Interviewer")
    st.camera_input("Maintain eye contact with the camera")
    
    if st.button("Start Interview / Ask Question"):
        st.session_state.current_q = agent.get_mock_question(role)
        
    if st.session_state.current_q:
        st.warning(f"**AI:** {st.session_state.current_q}")
        response = st.text_area("Your Response (Speak/Type):")
        if st.button("Submit Response"):
            st.session_state.transcript += f"Int: {st.session_state.current_q}\nCand: {response}\n\n"
            st.success("Response logged.")

# --- 4. TEXT MOCK INTERVIEW ---
elif menu == "📝 Text Mock Interview":
    st.header("Chat-based Interview")
    if st.button("Ask Me Something"):
        st.session_state.current_q = agent.get_mock_question(role)
    
    if st.session_state.current_q:
        st.chat_message("assistant").write(st.session_state.current_q)
        chat_ans = st.text_input("Chat here...")
        if st.button("Send"):
            st.session_state.transcript += f"Chat Q: {st.session_state.current_q}\nChat A: {chat_ans}\n\n"

# --- UNIVERSAL FEEDBACK & DOWNLOADER ---
st.divider()
st.sidebar.subheader("🏁 Finish Session")
if st.sidebar.button("Generate Final Report"):
    if st.session_state.transcript:
        report = agent.analyze_performance(st.session_state.transcript)
        st.header("📊 Final Feedback Report")
        st.markdown(report)
        # Download Button
        st.download_button("📥 Download Feedback as TXT", report, file_name="interview_feedback.txt")
    else:
        st.sidebar.error("No transcript found. Please complete some tasks first!")
