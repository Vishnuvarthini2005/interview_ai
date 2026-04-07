import google.generativeai as genai
import os
import streamlit as st

class InterviewAgent:
    def __init__(self):
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if not api_key:
            st.error("API Key missing!")
            return
        genai.configure(api_key=api_key)
        # Using the most stable 2026 model
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def get_single_mcq(self, topic, history):
        """Asks exactly one MCQ based on the topic and previous history"""
        prompt = f"""
        You are an Aptitude Examiner. Topic: {topic}.
        Provide ONE multiple-choice question. 
        Format: 
        Question: [The Question]
        A) [Option]
        B) [Option]
        C) [Option]
        D) [Option]
        
        Do NOT provide the answer yet. Keep it challenging.
        """
        # We pass history so the AI doesn't repeat the same question
        response = self.model.generate_content(prompt)
        return response.text

    def evaluate_answer(self, question, user_answer):
        """Checks if the answer was correct and provides a brief explanation"""
        prompt = f"""
        Question: {question}
        User's Answer: {user_answer}
        Is this correct? Reply with 'CORRECT' or 'INCORRECT' and a 1-sentence explanation.
        """
        response = self.model.generate_content(prompt)
        return response.text

    def generate_final_feedback(self, full_transcript):
        """Analyzes the whole session for a final grade"""
        prompt = f"Analyze this exam transcript and give a score out of 10 and 3 tips to improve: {full_transcript}"
        response = self.model.generate_content(prompt)
        return response.text
