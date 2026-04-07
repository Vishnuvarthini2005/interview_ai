import google.generativeai as genai
import os
import streamlit as st
import requests
import PyPDF2 as pdf

class InterviewAgent:
    def __init__(self):
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if not api_key:
            st.error("API Key missing! Check Streamlit Secrets.")
            return
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    # --- NEW: ATS RESUME ANALYZER ---
    def analyze_resume(self, resume_text, job_description):
        prompt = f"""
        Act as an advanced ATS (Applicant Tracking System) Analyzer.
        Compare the Resume against the Job Description (JD).
        Provide:
        1. Match Score (Percentage %)
        2. Missing Keywords (Critical for ATS)
        3. Resume Improvements (Bullet points)
        4. Final Verdict (Hire/Proceed/Reject)
        
        Resume: {resume_text}
        JD: {job_description}
        """
        return self.model.generate_content(prompt).text

    # --- EXISTING REFINED LOGIC ---
    def get_aptitude_q(self, topic):
        return self.model.generate_content(f"One hard Aptitude MCQ for {topic} with options A-D. No answer.").text

    def get_coding_problem(self, role, language, company):
        return self.model.generate_content(f"Coding challenge for {role} at {company} in {language}.").text

    def run_code_api(self, code, language):
        url = "https://emkc.org/api/v2/piston/execute"
        payload = {"language": language.lower(), "version": "*", "files": [{"content": code}]}
        try:
            return requests.post(url, json=payload, timeout=7).json().get("run", {}).get("output", "Execution finished.")
        except: return "Compiler error. Use 'Evaluate Logic' for AI feedback."

    def evaluate_code_logic(self, problem, code, language):
        prompt = f"Problem: {problem}\nCode: {code}\nLanguage: {language}\nProvide logic check and Big O complexity."
        return self.model.generate_content(prompt).text

    def interview_audio_query(self, role):
        return self.model.generate_content(f"Ask one punchy interview question for a {role}.").text
