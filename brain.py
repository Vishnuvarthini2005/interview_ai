import google.generativeai as genai
import os
import streamlit as st

class InterviewAgent:
    def __init__(self):
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if not api_key:
            st.error("API Key missing in Secrets!")
            return
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_notes(self, topic):
        prompt = f"Provide 5 high-impact revision notes for: {topic}. Be concise and professional."
        return self.model.generate_content(prompt).text

    def get_single_mcq(self, topic):
        prompt = f"Ask ONE challenging MCQ for {topic} with 4 options (A, B, C, D). Do not give the answer."
        return self.model.generate_content(prompt).text

    def get_mock_question(self, role):
        prompt = f"You are a Senior Recruiter. Ask one professional interview question for a {role} candidate."
        return self.model.generate_content(prompt).text

    def analyze_performance(self, transcript):
        prompt = f"Review this interview/test transcript. Provide a score (x/10), 3 strengths, and 3 areas for improvement: {transcript}"
        return self.model.generate_content(prompt).text
