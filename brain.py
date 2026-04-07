import google.generativeai as genai
import streamlit as st
import requests
import PyPDF2 as pdf
from google.api_core import exceptions

class InterviewAgent:
    def __init__(self):
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if not api_key:
            st.error("API Key missing! Add it to Streamlit Secrets.")
            return
        
        genai.configure(api_key=api_key)
        
        # FIX: gemini-1.5-flash is shut down. Using gemini-2.5-flash instead.
        # This model is faster and more stable for 2026.
        try:
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception:
            # Emergency fallback to Gemini 2.0 if 2.5 is not yet in your region
            self.model = genai.GenerativeModel('gemini-2.0-flash')

    def safe_generate(self, prompt):
        """Unified caller to handle rate limits and 404s"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except exceptions.ResourceExhausted:
            return "⚠️ **AI is busy (Rate Limit).** Please wait 60 seconds."
        except exceptions.NotFound:
            return "❌ **Model Error:** Please update 'brain.py' to use 'gemini-3-flash-preview'."
        except Exception as e:
            return f"⚠️ **Error:** {str(e)}"

    def analyze_resume(self, resume_text, job_description):
        prompt = f"Analyze Resume: {resume_text} against JD: {job_description}. Give Match Score and 3 tips."
        return self.safe_generate(prompt)

    def get_aptitude_q(self, topic):
        prompt = f"Generate 1 hard Aptitude MCQ for {topic} with options A-D. No answer."
        return self.safe_generate(prompt)

    def get_coding_problem(self, role, lang, comp):
        prompt = f"Provide 1 coding challenge for a {role} at {comp} using {lang}."
        return self.safe_generate(prompt)

    def run_code_api(self, code, language):
        url = "https://emkc.org/api/v2/piston/execute"
        payload = {"language": language.lower(), "version": "*", "files": [{"content": code}]}
        try:
            res = requests.post(url, json=payload, timeout=10).json()
            return res.get("run", {}).get("output", "Done.")
        except: return "Execution error."

    def evaluate_code_logic(self, problem, code, language):
        prompt = f"Problem: {problem}\nCode: {code}\nEvaluate logic and complexity."
        return self.safe_generate(prompt)
