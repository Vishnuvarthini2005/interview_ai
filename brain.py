import google.generativeai as genai
import os
import streamlit as st
import requests

class InterviewAgent:
    def __init__(self):
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if not api_key:
            st.error("API Key missing! Add GOOGLE_API_KEY to Streamlit Secrets.")
            return
        genai.configure(api_key=api_key)
        # Using the most stable model name for 2026
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    # --- ROUND 1: APTITUDE ---
    def get_aptitude_q(self, topic):
        prompt = f"Generate ONE Quantitative or Qualitative Aptitude MCQ for {topic}. Provide Question and 4 Options (A, B, C, D). No answer."
        return self.model.generate_content(prompt).text

    def evaluate_aptitude(self, transcript):
        prompt = f"Score this aptitude test out of 10. For every WRONG answer, provide a detailed step-by-step mathematical solution: {transcript}"
        return self.model.generate_content(prompt).text

    # --- ROUND 3: TECHNICAL ---
    def get_coding_problem(self, role, language, company):
        prompt = f"Act as a technical interviewer for {company}. Provide ONE coding challenge for a {role} in {language}. Include Problem Statement and Example Input/Output."
        return self.model.generate_content(prompt).text

    def evaluate_code_logic(self, problem, code, language):
        prompt = f"Problem: {problem}\nUser Code: {code}\nLanguage: {language}\nAnalyze if this is logically correct, explain any bugs, and give the Time Complexity."
        return self.model.generate_content(prompt).text

    def run_code_api(self, code, language):
        lang_map = {"python": "python", "java": "java", "cpp": "cpp", "javascript": "javascript"}
        piston_lang = lang_map.get(language.lower(), "python")
        url = "https://emkc.org/api/v2/piston/execute"
        payload = {"language": piston_lang, "version": "*", "files": [{"content": code}]}
        try:
            response = requests.post(url, json=payload, timeout=10).json()
            return response.get("run", {}).get("output", "Execution finished.")
        except:
            return "Compiler currently busy. Please use 'Evaluate Logic' for AI feedback."

    # --- ROUND 4: MOCK ---
    def interview_audio_query(self, role):
        prompt = f"You are a video interviewer. Ask ONE short, professional interview question for a {role}."
        return self.model.generate_content(prompt).text
