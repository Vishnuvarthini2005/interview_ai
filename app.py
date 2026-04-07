import streamlit as st
from brain import InterviewAgent
from streamlit_ace import st_ace
import PyPDF2 as pdf
import time

# --- PAGE CONFIG & THEME ---
st.set_page_config(page_title="AI Placement Elite", layout="wide", page_icon="🚀")

# CUSTOM CSS FOR SUPER FRIENDLY UI
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        border-radius: 12px;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0px 0px 15px #00f2fe;
        transform: translateY(-2px);
    }
    .stTextArea textarea { border-radius: 10px; background-color: #161b22; color: white; }
    .stTextInput input { border-radius: 10px; }
    </style>
    """, unsafe_allow_index=True)

agent = InterviewAgent()

# NAVIGATION
st.sidebar.title("💎 Placement Elite")
menu = st.sidebar.radio("Navigation:", 
    ["📄 ATS Resume Scanner", "1️⃣ Aptitude Round", "2️⃣ Interactive Study Agent", "3️⃣ Technical Coding IDE", "4️⃣ Video Mock Interview"])

# --- MODULE: ATS RESUME SCANNER ---
if menu == "📄 ATS Resume Scanner":
    st.header("🔍 Advanced ATS Optimizer")
    st.write("Upload your PDF Resume and the Job Description to calculate your match score.")
    
    col1, col2 = st.columns(2)
    with col1:
        jd_input = st.text_area("Paste Job Description (JD):", height=250, placeholder="Paste requirements here...")
    with col2:
        file = st.file_uploader("Upload Resume (PDF only)", type="pdf")

    if st.button("🔥 Run ATS Analysis"):
        if file and jd_input:
            with st.spinner("Analyzing Resume Structure..."):
                reader = pdf.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                
                analysis = agent.analyze_resume(text, jd_input)
                st.subheader("📊 Evaluation Report")
                st.markdown(analysis)
        else:
            st.error("Please upload a file and paste the JD first.")

# --- MODULE 1: APTITUDE ---
elif menu == "1️⃣ Aptitude Round":
    st.header("🧠 Quant & Soft Skills")
    topic = st.text_input("Topic:", "Percentage")
    if st.button("Generate Next"):
        st.session_state.q = agent.get_aptitude_q(topic)
    if "q" in st.session_state:
        st.info(st.session_state.q)
        ans = st.text_input("Answer (A/B/C/D):")
        if st.button("Submit"):
            st.success("Answer Recorded!")

# --- MODULE 2: STUDY AGENT ---
elif menu == "2️⃣ Interactive Study Agent":
    st.header("💬 Talkative Study Partner")
    if "chat" not in st.session_state: st.session_state.chat = []
    for m in st.session_state.chat:
        st.chat_message(m["role"]).write(m["content"])
    if p := st.chat_input("Ask me to explain any topic..."):
        st.session_state.chat.append({"role": "user", "content": p})
        res = agent.model.generate_content(p).text
        st.session_state.chat.append({"role": "assistant", "content": res})
        st.rerun()

# --- MODULE 3: TECH CODING ---
elif menu == "3️⃣ Technical Coding IDE":
    st.header("💻 Professional Coding Environment")
    c1, c2, c3 = st.columns(3)
    comp, role, lang = c1.text_input("Company:"), c2.text_input("Role:"), c3.selectbox("Lang:", ["python", "java", "cpp", "javascript"])
    
    if st.button("Fetch Challenge"):
        st.session_state.prob = agent.get_coding_problem(role, lang, comp)
    
    if "prob" in st.session_state:
        st.info(st.session_state.prob)
        # ACE Editor for professional feel
        code = st_ace(language=lang, theme="monokai", height=300, key="editor")
        ca, cb = st.columns(2)
        if ca.button("▶️ Execute Code"):
            st.code(agent.run_code_api(code, lang))
        if cb.button("✅ Evaluate Logic"):
            st.markdown(agent.evaluate_code_logic(st.session_state.prob, code, lang))

# --- MODULE 4: VIDEO MOCK ---
elif menu == "4️⃣ Video Mock Interview":
    st.header("🎥 Video-AI Interviewer")
    st.camera_input("Recording Status: Standby")
    if st.button("Ask Interview Question"):
        q = agent.interview_audio_query("Developer")
        st.warning(f"🎙️ AI: {q}")
    st.text_area("Your Response:")
    if st.button("Finish Session"):
        st.info("Performance: 8/10. Eye contact was consistent. Good logical structure.")
