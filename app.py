import streamlit as st
from brain import InterviewAgent
from streamlit_ace import st_ace
import PyPDF2 as pdf
import time

# 1. Page Config
st.set_page_config(page_title="AI Placement Elite", layout="wide", page_icon="🚀")

# 2. Safety-First UI CSS
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stButton>button {
        border-radius: 10px;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: white; font-weight: bold; width: 100%; border: none;
    }
</style>
""", unsafe_allow_html=True)

# 3. Initialize Agent
if "agent" not in st.session_state:
    st.session_state.agent = InterviewAgent()

# 4. Sidebar Navigation
st.sidebar.title("💎 Career Dashboard")
menu = st.sidebar.radio("Select Module:", 
    ["📄 ATS Resume Scanner", "🧠 Aptitude Round", "💬 Study Agent", "💻 Technical Round", "🎥 Mock Interview"])

# --- MODULE: ATS RESUME SCANNER ---
if menu == "📄 ATS Resume Scanner":
    st.header("🔍 ATS Resume Optimizer")
    jd = st.text_area("Paste Job Description:", placeholder="Enter job requirements...")
    file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    
    if st.button("🔥 Scan Resume"):
        if file and jd:
            with st.spinner("Parsing PDF..."):
                reader = pdf.PdfReader(file)
                text = "".join([page.extract_text() for page in reader.pages])
                report = st.session_state.agent.analyze_resume(text, jd)
                st.markdown("### Evaluation Report")
                st.write(report)
        else:
            st.warning("Please upload a PDF and paste the JD.")

# --- MODULE: APTITUDE ---
elif menu == "🧠 Aptitude Round":
    st.header("Aptitude Testing")
    topic = st.text_input("Topic (e.g. Profit/Loss):", "Logic")
    if st.button("Generate Question"):
        st.session_state.apt_q = st.session_state.agent.get_aptitude_q(topic)
    if "apt_q" in st.session_state:
        st.info(st.session_state.apt_q)
        st.text_input("Your Answer (A/B/C/D):", key="apt_ans")

# --- MODULE: STUDY AGENT ---
elif menu == "💬 Study Agent":
    st.header("Talkative AI Tutor")
    if "msgs" not in st.session_state: st.session_state.msgs = []
    for m in st.session_state.msgs:
        st.chat_message(m["role"]).write(m["content"])
    if p := st.chat_input("Ask a concept..."):
        st.session_state.msgs.append({"role": "user", "content": p})
        st.chat_message("user").write(p)
        res = st.session_state.agent.safe_generate(p)
        st.session_state.msgs.append({"role": "assistant", "content": res})
        st.chat_message("assistant").write(res)

# --- MODULE: TECHNICAL ---
elif menu == "💻 Technical Round":
    st.header("Coding Challenge")
    lang = st.selectbox("Language:", ["python", "java", "cpp", "javascript"])
    if st.button("Get Problem"):
        st.session_state.prob = st.session_state.agent.get_coding_problem("Developer", lang, "Google")
    if "prob" in st.session_state:
        st.info(st.session_state.prob)
        # Professional Code Editor
        code = st_ace(language=lang, theme="monokai", height=300, key="ace_ide")
        c1, c2 = st.columns(2)
        if c1.button("▶️ Run Code"):
            st.code(st.session_state.agent.run_code_api(code, lang))
        if c2.button("✅ Evaluate Logic"):
            st.markdown(st.session_state.agent.evaluate_code_logic(st.session_state.prob, code, lang))

# --- MODULE: MOCK ---
elif menu == "🎥 Mock Interview":
    st.header("Video Interview Round")
    st.camera_input("Recording...")
    if st.button("Ask Interview Question"):
        q = st.session_state.agent.safe_generate("Ask 1 professional interview question.")
        st.warning(f"🎙️ AI: {q}")
