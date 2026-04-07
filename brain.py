import google.generativeai as genai
import streamlit as st
import requests
import PyPDF2 as pdf
from google.api_core import exceptions

class InterviewAgent:
    def __init__(self):
        # Get API key from Streamlit Secrets
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if not api_key:
            st.error("API Key missing! Add 'GOOGLE_API_KEY' to Streamlit Secrets.")
            return
        
        genai.configure(api_key=api_key)
        # Using the most stable 2026 model for Free Tier
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def safe_generate(self, prompt):
        """Helper to handle Rate Limits (ResourceExhausted)"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except exceptions.ResourceExhausted:
            return "⚠️ **AI is busy (Rate Limit).** Please wait 30 seconds and try again. This is a Free Tier limit."
        except Exception as e:
            return f"⚠️ **Error:** {str(e)}"

    def analyze_resume(self, resume_text, job_description):
        prompt = f"Analyze this Resume against the JD. Provide Match % and 3 tips. Resume: {resume_text} JD: {job_description}"
        return self.safe_generate(prompt)

    def get_aptitude_q(self, topic):
        prompt = f"Generate 1 hard Aptitude MCQ for {topic} with options A-D. No answer."
        return self.safe_generate(prompt)

    def get_coding_problem(self, role, lang, comp):
        prompt = f"Provide 1 coding challenge for a {role} at {comp} using {lang}."
        return self.safe_generate(prompt)

    def run_code_api(self, code, language):
        lang_map = {"python": "python", "java": "java", "cpp": "cpp", "javascript": "javascript"}
        p_lang = lang_map.get(language.lower(), "python")
        url = "https://emkc.org/api/v2/piston/execute"
        payload = {"language": p_lang, "version": "*", "files": [{"content": code}]}
        try:
            res = requests.post(url, json=payload, timeout=10).json()
            return res.get("run", {}).get("output", "Code executed successfully.")
        except:
            return "Compiler error. Use 'Evaluate' for AI feedback."

    def evaluate_code_logic(self, problem, code, language):
        prompt = f"Problem: {problem}\nUser Code: {code}\nEvaluate the logic and give Big O complexity."
        return self.safe_generate(prompt)
