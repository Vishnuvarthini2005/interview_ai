import streamlit as st
from brain import InterviewAgent
from streamlit_ace import st_ace
import PyPDF2 as pdf

st.set_page_config(page_title="AI Placement Elite", layout="wide", page_icon="🚀")

# Professional UI Styling
st.markdown("<style>.stButton>button{background:#4facfe;color:white;width:100%;border-radius:8px;}</style>", unsafe_allow_html=True)

if "agent" not in st.session_state:
    st.session_state.agent = InterviewAgent()

menu = st.sidebar.selectbox("Go to Round:", ["📄 Resume Scanner", "🧠 Aptitude Round", "💬 AI Notes Tutor", "💻 Technical IDE"])

# --- MODULE 1: RESUME ---
if menu == "📄 Resume Scanner":
    st.header("ATS Resume Scanner")
    jd = st.text_area("Paste Job Description:")
    file = st.file_uploader("Upload PDF Resume", type="pdf")
    if st.button("Start Analysis"):
        if file and jd:
            reader = pdf.PdfReader(file)
            text = "".join([p.extract_text() for p in reader.pages])
            st.markdown(st.session_state.agent.analyze_resume(text, jd))

# --- MODULE 2: APTITUDE ---
elif menu == "🧠 Aptitude Round":
    st.header("Quant/Logic Round")
    topic = st.text_input("Topic:", "Averages")
    if st.button("Generate MCQ"):
        st.session_state.apt_q = st.session_state.agent.get_aptitude_q(topic)
    if "apt_q" in st.session_state:
        st.info(st.session_state.apt_q)
        st.text_input("Answer (A/B/C/D):", key="ans_input")

# --- MODULE 3: AI TUTOR ---
elif menu == "💬 AI Notes Tutor":
    st.header("Interactive Study Agent")
    if "chat" not in st.session_state: st.session_state.chat = []
    for m in st.session_state.chat: st.chat_message(m["role"]).write(m["content"])
    if p := st.chat_input("Ask a concept..."):
        st.session_state.chat.append({"role": "user", "content": p})
        res = st.session_state.agent.safe_generate(p)
        st.session_state.chat.append({"role": "assistant", "content": res})
        st.rerun()

# --- MODULE 4: TECHNICAL ---
elif menu == "💻 Technical IDE":
    st.header("Coding Round")
    lang = st.selectbox("Language:", ["python", "java", "cpp"])
    if st.button("New Challenge"):
        st.session_state.prob = st.session_state.agent.get_coding_problem("Dev", lang, "Tech Corp")
    if "prob" in st.session_state:
        st.info(st.session_state.prob)
        code = st_ace(language=lang, theme="monokai", height=300, key="editor")
        if st.button("Run & Evaluate"):
            st.code(st.session_state.agent.run_code_api(code, lang))
            st.write(st.session_state.agent.evaluate_code_logic(st.session_state.prob, code, lang))
