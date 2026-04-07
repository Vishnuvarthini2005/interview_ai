import google.generativeai as genai
import os
import streamlit as st
import requests
import PyPDF2 as pdf

class InterviewAgent:
    def __init__(self):
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if not api_key:
            st.error("API Key missing in Streamlit Secrets!")
            return
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def analyze_resume(self, resume_text, job_description):
        prompt = f"Analyze this Resume against the JD. Provide: 1. Match Score (%) 2. Missing Keywords 3. Improvement Tips. Resume: {resume_text} JD: {job_description}"
        return self.model.generate_content(prompt).text

    def get_aptitude_q(self, topic):
        return self.model.generate_content(f"One hard Aptitude MCQ for {topic} with options A-D. No answer.").text

    def get_coding_problem(self, role, language, company):
        return self.model.generate_content(f"Coding challenge for {role} at {company} in {language}.").text

    def run_code_api(self, code, language):
        url = "https://emkc.org/api/v2/piston/execute"
        payload = {"language": language.lower(), "version": "*", "files": [{"content": code}]}
        try:
            res = requests.post(url, json=payload, timeout=7).json()
            return res.get("run", {}).get("output", "Execution finished.")
        except: return "Compiler error."

    def evaluate_code_logic(self, problem, code, language):
        prompt = f"Problem: {problem}\nCode: {code}\nLanguage: {language}\nProvide logic check and complexity."
        return self.model.generate_content(prompt).text

    def interview_audio_query(self, role):
        return self.model.generate_content(f"Ask one short interview question for a {role}.").text
