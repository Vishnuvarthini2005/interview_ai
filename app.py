import streamlit as st
from brain import InterviewAgent
from streamlit_monaco import st_monaco
import time

st.set_page_config(page_title="AI Placement Officer", layout="wide")
agent = InterviewAgent()

if "apt_transcript" not in st.session_state: st.session_state.apt_transcript = ""
if "current_q" not in st.session_state: st.session_state.current_q = ""

st.sidebar.title("🎯 Placement Rounds")
menu = st.sidebar.radio("Select Round:", 
    ["1️⃣ Aptitude Round", "2️⃣ Interactive Study Agent", "3️⃣ Technical Round", "4️⃣ Video Mock Interview"])

# --- ROUND 1 & 2 REMAIN UNCHANGED ---
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
    if st.button("Stop & Evaluate My Score"):
        st.markdown(agent.evaluate_aptitude(st.session_state.apt_transcript))

elif menu == "2️⃣ Interactive Study Agent":
    st.header("💬 Real-Time Tutor (Gemini-Powered)")
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = agent.model.generate_content(prompt).text
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

# --- UPDATED ROUND 3: TECHNICAL (With IDE & Compiler) ---
elif menu == "3️⃣ Technical Round":
    st.header("💻 Technical Coding Round")
    c1, c2, c3 = st.columns(3)
    comp = c1.text_input("Company:", "Amazon")
    role = c2.text_input("Role:", "Software Engineer")
    lang = c3.selectbox("Language:", ["Python", "Java", "C++", "JavaScript"])

    if st.button("Generate Technical Challenge"):
        st.session_state.tech_problem = agent.get_coding_problem(role, lang, comp)
    
    if "tech_problem" in st.session_state:
        st.info(st.session_state.tech_problem)
        # Professional Editor
        st.write(f"### Editor ({lang})")
        user_code = st_monaco(value="# Write code here...", language=lang.lower(), height="300px")
        
        col_a, col_b = st.columns(2)
        if col_a.button("▶️ Run Code"):
            output = agent.run_code_api(user_code, lang)
            st.code(output, language="text")
        
        if col_b.button("✅ Evaluate Logic & Feedback"):
            feedback = agent.evaluate_code_logic(st.session_state.tech_problem, user_code, lang)
            st.success("Analysis Complete!")
            st.markdown(feedback)

# --- ROUND 4 REMAINS UNCHANGED ---
elif menu == "4️⃣ Video Mock Interview":
    st.header("🎥 AI Video & Audio Interview")
    st.camera_input("Interview Camera Active")
    if st.button("Start Audio Interview"):
        q = agent.interview_audio_query(role="Developer")
        st.session_state.current_q = q
        st.warning(f"🎙️ **AI Interviewer asks:** {q}")
    ans = st.text_area("Your Verbal Response:")
    if st.button("End Interview"):
        st.info("Feedback: High confidence. Improve your explanation of Big O.")
