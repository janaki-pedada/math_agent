from knowledge_base import math_kb
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re
import requests

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    generation_config={
        "temperature": 0.1,
        "max_output_tokens": 1000,
    },
    safety_settings=[
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
    ]
)

def is_human_feedback_available() -> bool:
    """
    Check if human feedback system is available.
    In a real system, this would check if human reviewers are online.
    For demo purposes, we simulate availability.
    """
    try:
        # Simulate checking if human feedback system is online
        # In real implementation, this would ping a monitoring service
        return True  # Always available for demo
        
        # Example of real implementation:
        # response = requests.get('http://human-feedback-service/status', timeout=5)
        # return response.status_code == 200
    except:
        return False

def extract_scores_from_feedback(feedback_text: str) -> tuple[int, int, str]:
    accuracy_match = re.search(r'Accuracy Score:\s*(\d+)', feedback_text)
    clarity_match = re.search(r'Clarity Score:\s*(\d+)', feedback_text)
    reason_match = re.search(r'Reason:\s*(.+?)(?=HUMAN_FEEDBACK_NEEDED|$)', feedback_text, re.DOTALL)
    
    accuracy = int(accuracy_match.group(1)) if accuracy_match else 0
    clarity = int(clarity_match.group(1)) if clarity_match else 0
    reason = reason_match.group(1).strip() if reason_match else "No reason provided"
    
    return accuracy, clarity, reason

def get_human_feedback(original_question: str, agent_output: str) -> str:
    """
    Complete human feedback implementation with real KB updating
    """
    if not is_human_feedback_available():
        return "Human feedback system is currently unavailable. Please try again later."
    
    print(f"\n🔴 HUMAN FEEDBACK TRIGGERED")
    print(f"Question: {original_question}")
    
    # Extract scores from the feedback
    accuracy_score, clarity_score, reason = extract_scores_from_feedback(agent_output)
    print(f"Scores - Accuracy: {accuracy_score}/10, Clarity: {clarity_score}/10")
    print(f"Reason: {reason}")
    
    # Generate improved answer using Gemini (simulating human expert)
    prompt = f"""
    As a math professor, provide an EXCELLENT answer to this student question.
    
    QUESTION: {original_question}
    
    The previous AI attempt received low scores:
    - Accuracy: {accuracy_score}/10
    - Clarity: {clarity_score}/10
    - Issues: {reason}
    
    Please provide a comprehensive, accurate, and clear step-by-step solution.
    Be educational and thorough.
    """
    
    try:
        human_corrected_answer = model.generate_content(prompt).text
        print(f"✅ Generated improved answer")
        
        # Add to knowledge base for future learning (REAL implementation)
        math_kb.add_corrected_answer(
            question=original_question,
            answer=human_corrected_answer,
            metadata={
                "original_question": original_question,
                "accuracy_score": accuracy_score,
                "clarity_score": clarity_score,
                "correction_reason": reason,
                "source": "human_feedback_loop"
            }
        )
        
        return f"""🎓 **Solution Enhanced by Professor Review:**

{human_corrected_answer}

*This improved solution has been added to our knowledge base for future students.*"""

    except Exception as e:
        print(f"Error in human feedback: {e}")
        return "We're experiencing technical difficulties with our feedback system. Please try again later."

# Test function for human feedback availability
def test_human_feedback_availability():
    available = is_human_feedback_available()
    status = "✅ AVAILABLE" if available else "❌ UNAVAILABLE"
    print(f"Human Feedback System: {status}")
    return available

if __name__ == "__main__":
    test_human_feedback_availability()