import google.generativeai as genai
import os
import streamlit as st

class InterviewAgent:
    def __init__(self):
        # Fetch key from Streamlit Secrets
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if not api_key:
            st.error("API Key missing! Check Streamlit Cloud Secrets.")
            return
        
        genai.configure(api_key=api_key)
        # Using the stable 2026 flash model
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def get_chat_response(self, user_input, role, history):
        """Conversational Tutor for specific notes"""
        chat = self.model.start_chat(history=history)
        prompt = f"Context: I am preparing for a {role} role. User Request: {user_input}"
        response = chat.send_message(prompt)
        return response.text

    def get_single_mcq(self, topic):
        """Generates one MCQ at a time"""
        prompt = f"Provide ONE challenging MCQ for {topic} with 4 options (A, B, C, D). Do not provide the answer."
        return self.model.generate_content(prompt).text

    def get_mock_question(self, role):
        """Acting as a Senior Interviewer"""
        prompt = f"You are a Senior Recruiter. Ask ONE professional interview question for a {role} candidate."
        return self.model.generate_content(prompt).text

    def analyze_performance(self, transcript):
        """Final Evaluation logic"""
        if not transcript:
            return "No data to analyze."
        prompt = f"Analyze this interview/test transcript. Provide a score out of 10, 3 strengths, and 3 specific tips to improve: {transcript}"
        return self.model.generate_content(prompt).text
