import streamlit as st
from brain import InterviewAgent
from streamlit_ace import st_ace
import PyPDF2 as pdf

# 1. Page Settings
st.set_page_config(page_title="Placement AI Pro", layout="wide")

# 2. Corrected CSS
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stButton>button {
        border-radius: 8px;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: white; font-weight: bold; width: 100%; height: 3em;
    }
</style>
""", unsafe_allow_html=True)

# 3. Initialize Agent
if "agent" not in st.session_state:
    st.session_state.agent = InterviewAgent()

# 4. Navigation
menu = st.sidebar.selectbox("Go to Round:", 
    ["📄 Resume ATS", "🧠 Aptitude", "💬 AI Tutor", "💻 Coding IDE", "🎥 Mock Interview"])

# --- MODULE 1: RESUME ATS ---
if menu == "📄 Resume ATS":
    st.header("🔍 ATS Resume Scanner")
    jd = st.text_area("Paste Job Description:", key="jd_box")
    file = st.file_uploader("Upload PDF Resume", type="pdf", key="resume_up")
    if st.button("Analyze My Resume"):
        if file and jd:
            reader = pdf.PdfReader(file)
            text = "".join([page.extract_text() for page in reader.pages])
            st.markdown(st.session_state.agent.analyze_resume(text, jd))
        else:
            st.warning("Upload a file and paste the JD first.")

# --- MODULE 2: APTITUDE ---
elif menu == "🧠 Aptitude":
    st.header("Aptitude Round")
    topic = st.text_input("Enter Topic:", value="Percentages", key="apt_topic")
    if st.button("Generate Question"):
        st.session_state.q = st.session_state.agent.get_aptitude_q(topic)
    if "q" in st.session_state:
        st.info(st.session_state.q)
        st.text_input("Your Answer:", key="apt_ans")

# --- MODULE 3: AI TUTOR ---
elif menu == "💬 AI Tutor":
    st.header("Interactive Study Agent")
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        st.chat_message(m["role"]).write(m["content"])
    if p := st.chat_input("Ask anything..."):
        st.session_state.messages.append({"role": "user", "content": p})
        res = st.session_state.agent.model.generate_content(p).text
        st.session_state.messages.append({"role": "assistant", "content": res})
        st.rerun()

# --- MODULE 4: CODING IDE ---
elif menu == "💻 Coding IDE":
    st.header("Technical Coding Round")
    lang = st.selectbox("Language:", ["python", "java", "cpp", "javascript"], key="lang_sel")
    if st.button("Get Challenge"):
        st.session_state.prob = st.session_state.agent.get_coding_problem("Developer", lang, "Top Tech")
    if "prob" in st.session_state:
        st.info(st.session_state.prob)
        code = st_ace(language=lang, theme="monokai", height=300, key="ace_ide")
        c1, c2 = st.columns(2)
        if c1.button("Run Code"):
            st.code(st.session_state.agent.run_code_api(code, lang))
        if c2.button("Evaluate"):
            st.markdown(st.session_state.agent.evaluate_code_logic(st.session_state.prob, code, lang))

# --- MODULE 5: MOCK ---
elif menu == "🎥 Mock Interview":
    st.header("Video Mock Interview")
    st.camera_input("Recording...", key="cam")
    if st.button("Ask Me a Question"):
        st.warning(st.session_state.agent.model.generate_content("Ask a professional interview question.").text)
