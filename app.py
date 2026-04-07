import streamlit as st
from brain import InterviewAgent
from streamlit_ace import st_ace
import time

st.set_page_config(page_title="AI Placement Officer", layout="wide", page_icon="🎯")

# Initialize Agent
if "agent" not in st.session_state:
    st.session_state.agent = InterviewAgent()

# Initialize State
if "apt_transcript" not in st.session_state: st.session_state.apt_transcript = ""
if "current_q" not in st.session_state: st.session_state.current_q = ""
if "messages" not in st.session_state: st.session_state.messages = []

st.sidebar.title("🎯 Placement Rounds")
menu = st.sidebar.radio("Select Round:", 
    ["1️⃣ Aptitude Round", "2️⃣ Interactive Study Agent", "3️⃣ Technical Round", "4️⃣ Video Mock Interview"])

# --- ROUND 1: APTITUDE ---
if menu == "1️⃣ Aptitude Round":
    st.header("Quantitative & Qualitative Aptitude")
    topic = st.text_input("Enter Topic (e.g. Percentage, Logic):", "Algebra")
    if st.button("Generate Question"):
        st.session_state.current_q = st.session_state.agent.get_aptitude_q(topic)
    if st.session_state.current_q:
        st.info(st.session_state.current_q)
        user_ans = st.text_input("Your Answer (A/B/C/D):")
        if st.button("Submit Answer"):
            st.session_state.apt_transcript += f"Q: {st.session_state.current_q}\nUser: {user_ans}\n\n"
            st.success("Saved! Click 'Generate' for next or 'Evaluate' to finish.")
    if st.button("Stop & Evaluate My Score"):
        st.markdown(st.session_state.agent.evaluate_aptitude(st.session_state.apt_transcript))

# --- ROUND 2: STUDY AGENT ---
elif menu == "2️⃣ Interactive Study Agent":
    st.header("💬 Talkative AI Tutor")
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    if prompt := st.chat_input("Ask me to explain any topic..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = st.session_state.agent.model.generate_content(prompt).text
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

# --- ROUND 3: TECHNICAL (With Ace Editor) ---
elif menu == "3️⃣ Technical Round":
    st.header("💻 Technical Coding Round")
    c1, c2, c3 = st.columns(3)
    comp = c1.text_input("Company:", "Google")
    role = c2.text_input("Role:", "Python Developer")
    lang = c3.selectbox("Language:", ["python", "java", "cpp", "javascript"])

    if st.button("Get Technical Challenge"):
        st.session_state.tech_problem = st.session_state.agent.get_coding_problem(role, lang, comp)
    
    if "tech_problem" in st.session_state:
        st.info(st.session_state.tech_problem)
        st.write("### ⌨️ Code Editor")
        user_code = st_ace(language=lang, theme="monokai", height=300, key="editor")
        
        col_a, col_b = st.columns(2)
        if col_a.button("▶️ Run Code"):
            st.code(st.session_state.agent.run_code_api(user_code, lang))
        if col_b.button("✅ Evaluate Logic"):
            st.markdown(st.session_state.agent.evaluate_code_logic(st.session_state.tech_problem, user_code, lang))

# --- ROUND 4: VIDEO MOCK ---
elif menu == "4️⃣ Video Mock Interview":
    st.header("🎥 Video & Audio Mock Interview")
    st.camera_input("Camera Active")
    if st.button("Ask Interview Question"):
        st.session_state.current_q = st.session_state.agent.interview_audio_query("Developer")
        st.warning(f"🎙️ AI: {st.session_state.current_q}")
    ans = st.text_area("Your Response:")
    if st.button("Submit & End"):
        st.info("Feedback: Great eye contact! Tip: Be more specific about your projects.")
