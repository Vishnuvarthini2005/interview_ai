import google.generativeai as genai
import os
import streamlit as st

class InterviewAgent:
    def __init__(self):
        # Fetch key from Streamlit Secrets
        api_key = st.secrets.get("GOOGLE_API_KEY")
        
        if not api_key:
            st.error("API Key missing in Secrets!")
            return
        
        genai.configure(api_key=api_key, transport='rest')
        
        # Use the standard model name (no prefix) for the stable v1 API
        try:
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            st.error(f"Failed to initialize model: {e}")

    def generate_study_kit(self, topic):
        """Generates Revision Notes and MCQs"""
        prompt = f"Provide 5 revision notes and 3 MCQs for: {topic}. Give answers at the end."
        try:
            # Explicitly using the model to generate content
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Model Error: {str(e)}"

    def get_interview_question(self, role):
        """Generates a single interview question"""
        prompt = f"Ask one short technical interview question for a {role}."
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
            
