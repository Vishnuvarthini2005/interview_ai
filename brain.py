import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class InterviewAgent:
    def __init__(self):
        # We use Flash because it is fast and free
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_study_kit(self, role):
        """Task: Generate Notes and MCQs"""
        prompt = f"""
        You are an expert technical tutor. For the role of '{role}':
        1. Provide a 'Quick Revision' list of 5 key technical concepts.
        2. Provide 3 Multiple Choice Questions (MCQs) with answers hidden at the bottom.
        Focus on accuracy. Do not hallucinate facts.
        """
        response = self.model.generate_content(prompt)
        return response.text

    def get_question(self, role, history):
        """Task: Be the Interviewer"""
        # System instruction to keep the AI in character
        chat = self.model.start_chat(history=history)
        prompt = f"Ask me one professional interview question for a {role} position. Short and direct."
        response = chat.send_message(prompt)
        return response.text

    def get_feedback(self, transcript):
        """Task: The Evaluator"""
        prompt = f"Review this interview transcript and give a score (1-10) and two points for improvement: {transcript}"
        response = self.model.generate_content(prompt)
        return response.text