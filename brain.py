import google.generativeai as genai
import streamlit as st
import requests
import PyPDF2 as pdf

class InterviewAgent:
    def __init__(self):
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if not api_key:
            st.error("API Key missing in Secrets!")
            return
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def analyze_resume(self, resume_text, job_description):
        if not resume_text or not job_description:
            return "Please provide both resume and job description."
        prompt = f"Analyze Resume: {resume_text} against JD: {job_description}. Provide Match % and 3 tips."
        return self.model.generate_content(prompt).text

    def get_aptitude_q(self, topic):
        return self.model.generate_content(f"One hard MCQ for {topic} with options A-D. No answer.").text

    def get_coding_problem(self, role, lang, comp):
        return self.model.generate_content(f"Coding challenge for {role} at {comp} in {lang}.").text

    def run_code_api(self, code, language):
        if not code or len(code) < 5:
            return "Please write some code first."
        lang_map = {"python": "python", "java": "java", "cpp": "cpp", "javascript": "javascript"}
        piston_lang = lang_map.get(language.lower(), "python")
        url = "https://emkc.org/api/v2/piston/execute"
        payload = {"language": piston_lang, "version": "*", "files": [{"content": code}]}
        try:
            res = requests.post(url, json=payload, timeout=7).json()
            return res.get("run", {}).get("output", "No output generated.")
        except:
            return "Execution failed. Check your internet or code logic."

    def evaluate_code_logic(self, problem, code, language):
        if not code: return "No code to evaluate."
        prompt = f"Problem: {problem}\nCode: {code}\nEvaluate logic and Big O."
        return self.model.generate_content(prompt).text
