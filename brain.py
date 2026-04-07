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
        # Using 1.5 Flash for speed and multimodal capabilities
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def get_aptitude_q(self, topic):
        prompt = f"Generate ONE Quantitative/Qualitative Aptitude MCQ for {topic}. Provide Question and 4 Options. No answer."
        return self.model.generate_content(prompt).text

    def get_tech_questions(self, company, role, language):
        # This prompt triggers Gemini's internal knowledge of past papers
        prompt = f"Search for real-world technical interview questions for {role} at {company} using {language}. Provide 5 frequent questions and their ideal logical approach."
        return self.model.generate_content(prompt).text

    def evaluate_aptitude(self, transcript):
        prompt = f"Score this aptitude test out of 10. For every WRONG answer, provide a detailed step-by-step mathematical solution: {transcript}"
        return self.model.generate_content(prompt).text

    def interview_audio_query(self, role):
        # We ask the model to provide a question specifically meant to be read aloud
        prompt = f"You are a video interviewer. Ask ONE short, punchy interview question for a {role}."
        return self.model.generate_content(prompt).text
