import streamlit as st
from brain import InterviewAgent
from streamlit_ace import st_ace
import PyPDF2 as pdf

# 1. Page Config
st.set_page_config(page_title="AI Placement Elite", layout="wide")

# 2. Fixed CSS (No Triple-Quote errors)
st.markdown("<style> .main { background-color: #0e1117; } .stButton>button { border-radius: 10px; background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); color: white; font-weight: bold; border: none; } </style>", unsafe_allow_index=True)

# 3. Initialize Agent
if "agent" not in st.session_state:
    st.session_state.agent = InterviewAgent()

# 4. Sidebar Navigation
st.sidebar.title("💎 Placement Elite")
menu = st.sidebar.radio("Navigate:", ["📄 ATS Resume Scanner", "1️⃣ Aptitude Round", "2️⃣ Study Agent", "3️⃣ Tech Coding IDE", "4️⃣ Video Mock Interview"])

# --- ATS SCANNER ---
if menu == "📄 ATS Resume Scanner":
    st.header("🔍 ATS Optimizer")
    jd_input = st.text_area("Paste Job Description:")
    file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    if st.button("Run Analysis"):
        if file and jd_input:
            reader = pdf.PdfReader(file)
            text = "".join([page.extract_text() for page in reader.pages])
            st.markdown(st.session_state.agent.analyze_resume(text, jd_input))

# --- APTITUDE ---
elif menu == "1️⃣ Aptitude Round":
    st.header("🧠 Quant Round")
    topic = st.text_input("Topic:", "Logic")
    if st.button("Generate"):
        st.session_state.q = st.session_state.agent.get_aptitude_q(topic)
    if "q" in st.session_state:
        st.info(st.session_state.q)
        st.text_input("Answer (A/B/C/D):")

# --- STUDY AGENT ---
elif menu == "2️⃣ Interactive Study Agent":
    st.header("💬 AI Tutor")
    if "chat" not in st.session_state: st.session_state.chat = []
    for m in st.session_state.chat: st.chat_message(m["role"]).write(m["content"])
    if p := st.chat_input("Ask me anything..."):
        st.session_state.chat.append({"role": "user", "content": p})
        res = st.session_state.agent.model.generate_content(p).text
        st.session_state.chat.append({"role": "assistant", "content": res})
        st.rerun()

# --- TECH CODING ---
elif menu == "3️⃣ Tech Coding IDE":
    st.header("💻 Coding IDE")
    lang = st.selectbox("Lang:", ["python", "java", "cpp"])
    if st.button("Get Problem"):
        st.session_state.prob = st.session_state.agent.get_coding_problem("Developer", lang, "Google")
    if "prob" in st.session_state:
        st.info(st.session_state.prob)
        code = st_ace(language=lang, theme="monokai", height=300)
        if st.button("Run & Evaluate"):
            st.code(st.session_state.agent.run_code_api(code, lang))
            st.markdown(st.session_state.agent.evaluate_code_logic(st.session_state.prob, code, lang))

# --- VIDEO MOCK ---
elif menu == "4️⃣ Video Mock Interview":
    st.header("🎥 Video Interview")
    st.camera_input("Recording...")
    if st.button("Ask Question"):
        st.warning(st.session_state.agent.interview_audio_query("Developer"))
    st.text_area("Response:")
