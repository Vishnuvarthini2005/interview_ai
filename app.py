import streamlit as st
from brain import InterviewAgent

st.set_page_config(page_title="AI Career Agent", page_icon="🤖", layout="wide")

# Initialize Agent
if "agent" not in st.session_state:
    st.session_state.agent = InterviewAgent()

# Initialize Persistent Session Memory
if "transcript" not in st.session_state: st.session_state.transcript = ""
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "current_q" not in st.session_state: st.session_state.current_q = ""

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🤖 Agentic Dashboard")
role = st.sidebar.text_input("Target Role/Topic:", "Python Developer")
menu = st.sidebar.radio("Select Module:", 
    ["🎓 Conversational Tutor", "🧠 Aptitude Round", "🎥 Mock Interview"])

st.sidebar.divider()
if st.sidebar.button("🏁 Finish & Get Report"):
    st.session_state.show_report = True
else:
    st.session_state.show_report = False

# --- MODULE 1: CONVERSATIONAL TUTOR (Real Agent Style) ---
if menu == "🎓 Conversational Tutor":
    st.header(f"Study Assistant: {role}")
    st.write("Ask specifically about any topic to get custom notes.")

    # Display Chat
    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ex: Explain decorators with examples"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        response = st.session_state.agent.get_chat_response(prompt, role, [])
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

# --- MODULE 2: APTITUDE ROUND (One-by-One) ---
elif menu == "🧠 Aptitude Round":
    st.header("Interactive MCQ Round")
    if st.button("Generate Next Question"):
        st.session_state.current_q = st.session_state.agent.get_single_mcq(role)
    
    if st.session_state.current_q:
        st.info(st.session_state.current_q)
        ans = st.text_input("Type your answer (A, B, C, or D):", key="apt_ans")
        if st.button("Submit Answer"):
            st.session_state.transcript += f"MCQ: {st.session_state.current_q}\nUser Answer: {ans}\n\n"
            st.success("Answer logged to your final report!")

# --- MODULE 3: MOCK INTERVIEW (Video/Text) ---
elif menu == "🎥 Mock Interview":
    st.header("AI Professional Interview")
    st.camera_input("Position yourself for the interview")
    
    if st.button("Ask Interview Question"):
        st.session_state.current_q = st.session_state.agent.get_mock_question(role)
    
    if st.session_state.current_q:
        st.warning(f"**Interviewer:** {st.session_state.current_q}")
        response = st.text_area("Your Response:", height=150)
        if st.button("Submit Response"):
            st.session_state.transcript += f"Int: {st.session_state.current_q}\nCand: {response}\n\n"
            st.success("Response recorded.")

# --- FINAL REPORT OVERLAY ---
if st.session_state.get("show_report"):
    st.divider()
    with st.spinner("Agent is evaluating your performance..."):
        report = st.session_state.agent.analyze_performance(st.session_state.transcript)
        st.header("📊 Final Performance Evaluation")
        st.markdown(report)
        st.download_button("📥 Download Feedback", report, file_name="interview_results.txt")
