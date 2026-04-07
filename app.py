import streamlit as st
from brain import InterviewAgent

st.set_page_config(page_title="AI Aptitude Agent", layout="wide")
agent = InterviewAgent()

# --- Initialize Session Memory ---
if "quiz_active" not in st.session_state: st.session_state.quiz_active = False
if "current_q" not in st.session_state: st.session_state.current_q = ""
if "transcript" not in st.session_state: st.session_state.transcript = ""
if "score" not in st.session_state: st.session_state.score = 0
if "q_count" not in st.session_state: st.session_state.q_count = 0

st.title("🧠 Interactive Aptitude Agent")

# Sidebar Setup
topic = st.sidebar.text_input("Enter Topic for MCQ:", "Python Loops")

# --- THE SEPARATE MCQ BUTTON ---
if st.sidebar.button("Start Aptitude Round"):
    st.session_state.quiz_active = True
    st.session_state.transcript = ""
    st.session_state.score = 0
    st.session_state.q_count = 0
    st.session_state.current_q = agent.get_single_mcq(topic, "")

# --- QUIZ INTERFACE ---
if st.session_state.quiz_active:
    st.subheader(f"Round: {topic} (Question {st.session_state.q_count + 1})")
    
    # Display the Question
    st.info(st.session_state.current_q)
    
    # User Interaction
    user_choice = st.radio("Select your answer:", ["A", "B", "C", "D"], key=f"q_{st.session_state.q_count}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Submit Answer"):
            # Evaluate
            result = agent.evaluate_answer(st.session_state.current_q, user_choice)
            st.session_state.transcript += f"Q: {st.session_state.current_q}\nUser: {user_choice}\nResult: {result}\n\n"
            
            if "CORRECT" in result.upper() and "INCORRECT" not in result.upper():
                st.session_state.score += 1
                st.success(result)
            else:
                st.error(result)
            
            # Prepare next question
            st.session_state.q_count += 1
            st.session_state.current_q = agent.get_single_mcq(topic, st.session_state.transcript)
            st.rerun()

    with col2:
        if st.button("Stop & Evaluate"):
            st.session_state.quiz_active = False
            feedback = agent.generate_final_feedback(st.session_state.transcript)
            st.divider()
            st.header("📊 Final Performance Report")
            st.write(f"**Total Questions Answered:** {st.session_state.q_count}")
            st.write(f"**Correct Answers:** {st.session_state.score}")
            st.markdown(feedback)

else:
    st.write("Click the button in the sidebar to start your personalized aptitude round.")
