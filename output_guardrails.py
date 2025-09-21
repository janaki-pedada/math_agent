import re
import math
from typing import Tuple

class OutputGuardrails:
    def __init__(self):
        self.math_keywords = [
            'step', 'solution', 'calculate', 'formula', 'equation',
            'theorem', 'proof', 'derivative', 'integral', 'solve',
            'therefore', 'thus', 'hence', 'result', 'answer'
        ]
        
        self.inappropriate_patterns = [
            r'\b(cannot|can\'t|don\'t know|unsure|guess|maybe|perhaps)\b',
            r'\b(illegal|dangerous|harmful|violent|inappropriate)\b',
            r'\b(\$\$|money|cash|price|cost|buy|sell)\b'
        ]

    def validate_educational_content(self, response: str) -> Tuple[bool, str]:
        """Validate response meets educational standards"""
        
        # Check for step-by-step structure
        step_count = len(re.findall(r'(Step \d+|step \d+|•|\d+\.)', response))
        if step_count < 2:
            return False, "Response should provide step-by-step solution"
        
        # Check for mathematical content
        math_content = any(keyword in response.lower() for keyword in self.math_keywords)
        if not math_content:
            return False, "Response should contain mathematical explanations"
        
        # Check for inappropriate content
        for pattern in self.inappropriate_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                return False, "Response contains inappropriate content"
        
        # Check length (not too short)
        if len(response.split()) < 20:
            return False, "Response should be sufficiently detailed"
        
        return True, "Valid educational response"

    def sanitize_output(self, response: str) -> str:
        """Sanitize and format the output for educational purposes"""
        
        # Remove any potentially harmful content
        for pattern in self.inappropriate_patterns:
            response = re.sub(pattern, '[REDACTED]', response, flags=re.IGNORECASE)
        
        # Ensure proper formatting
        response = re.sub(r'\n{3,}', '\n\n', response)  # Remove extra newlines
        response = response.strip()
        
        return response

# Global instance
output_guardrails = OutputGuardrails()