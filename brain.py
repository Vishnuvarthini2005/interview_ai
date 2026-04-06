import google.generativeai as genai
import os
import streamlit as st

class InterviewAgent:
    def __init__(self):
        # Checks Streamlit Secrets first, then local environment
        api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            st.error("API Key not found! Please add GOOGLE_API_KEY to Streamlit Secrets.")
            return
        
        genai.configure(api_key=api_key)
        # Use the full model path to avoid 'NotFound' errors
        self.model = genai.GenerativeModel('models/gemini-1.5-flash')

    def generate_study_kit(self, topic):
        """Generates Revision Notes and MCQs"""
        prompt = f"Act as a Technical Tutor. Provide 5 detailed revision notes and 3 MCQs for the topic: {topic}. Provide answers at the end."
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating content: {str(e)}"

    def get_interview_question(self, role):
        """Generates a single interview question"""
        prompt = f"You are a hiring manager. Ask one short, challenging interview question for a {role} position."
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
