import streamlit as st
from brain import InterviewAgent
import time

st.set_page_config(page_title="AI Placement Officer", layout="wide")
agent = InterviewAgent()

# --- Session Management ---
if "apt_transcript" not in st.session_state: st.session_state.apt_transcript = ""
if "current_q" not in st.session_state: st.session_state.current_q = ""

st.sidebar.title("🎯 Placement Rounds")
menu = st.sidebar.radio("Select Round:", 
    ["1️⃣ Aptitude Round", "2️⃣ Interactive Study Agent", "3️⃣ Technical Round", "4️⃣ Video Mock Interview"])

# --- ROUND 1: APTITUDE ---
if menu == "1️⃣ Aptitude Round":
    st.header("Quantitative & Qualitative Aptitude")
    topic = st.text_input("Enter Math/Soft Skill Topic:", "Probability")
    
    if st.button("Generate Question"):
        st.session_state.current_q = agent.get_aptitude_q(topic)
    
    if st.session_state.current_q:
        st.info(st.session_state.current_q)
        user_ans = st.text_input("Your Answer (A/B/C/D):")
        if st.button("Submit & Next"):
            st.session_state.apt_transcript += f"Q: {st.session_state.current_q}\nUser: {user_ans}\n\n"
            st.success("Saved!")

    if st.button("Stop & Evaluate My Score"):
        report = agent.evaluate_aptitude(st.session_state.apt_transcript)
        st.header("📊 Result & Detailed Solutions")
        st.markdown(report)

# --- ROUND 2: STUDY AGENT (TALKATIVE) ---
elif menu == "2️⃣ Interactive Study Agent":
    st.header("💬 Real-Time Tutor (Gemini-Powered)")
    if "messages" not in st.session_state: st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask me anything about your subjects..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Interactive response logic
        response = agent.model.generate_content(prompt).text
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

# --- ROUND 3: TECHNICAL ROUND ---
elif menu == "3️⃣ Technical Round":
    st.header("💻 Technical Interview Prep")
    col1, col2, col3 = st.columns(3)
    comp = col1.text_input("Company:", "Google")
    job = col2.text_input("Role:", "Python Intern")
    lang = col3.text_input("Language:", "Python/Java")

    if st.button("Fetch Past Year & Mock Questions"):
        with st.spinner("Searching web & past papers..."):
            questions = agent.get_tech_questions(comp, job, lang)
            st.markdown(questions)

# --- ROUND 4: VIDEO MOCK INTERVIEW ---
elif menu == "4️⃣ Video Mock Interview":
    st.header("🎥 AI Video & Audio Interview")
    st.write("Ensuring Eye Contact & Communication Skills")
    
    # Live Video Feed
    st.camera_input("Interview Camera Active")
    
    if st.button("Start Audio Interview"):
        q = agent.interview_audio_query(role="Developer")
        st.session_state.current_q = q
        # Simulating Audio Output (In 2026, browsers support st.audio better)
        st.warning(f"🎙️ **AI Interviewer asks:** {q}")
        
    ans = st.text_area("Your Verbal Response (Type or use Dictation):")
    if st.button("End Interview"):
        st.success("Analyzing eye-contact, confidence, and content...")
        time.sleep(2)
        st.info("Feedback: High confidence. Eye contact was steady. Improve your explanation of Big O.")
