import dspy
from typing import List, Dict

class MathSolutionSignature(dspy.Signature):
    """Signature for math solution generation."""
    question = dspy.InputField(desc="Mathematical question to solve")
    context = dspy.InputField(desc="Additional context from KB or web")
    solution = dspy.OutputField(desc="Step-by-step mathematical solution")

class MathFeedbackSignature(dspy.Signature):
    """Signature for solution evaluation."""
    question = dspy.InputField(desc="Original mathematical question")
    solution = dspy.InputField(desc="Proposed solution to evaluate")
    evaluation = dspy.OutputField(desc="Evaluation scores and feedback")

class MathTutorOptimizer:
    def __init__(self):
        self.lm = dspy.LM("google/gemini-1.5-flash")
        dspy.configure(lm=self.lm)
        
        self.solution_generator = dspy.ChainOfThought(MathSolutionSignature)
        self.feedback_evaluator = dspy.ChainOfThought(MathFeedbackSignature)
        
        # Training data for optimization
        self.training_examples = []

    def generate_solution(self, question: str, context: str = "") -> str:
        """Generate solution using DSPy optimized prompt"""
        return self.solution_generator(question=question, context=context).solution

    def evaluate_solution(self, question: str, solution: str) -> dict:
        """Evaluate solution quality"""
        evaluation = self.feedback_evaluator(question=question, solution=solution).evaluation
        return self._parse_evaluation(evaluation)

    def add_feedback_example(self, question: str, solution: str, human_feedback: str):
        """Add example for DSPy optimization"""
        self.training_examples.append({
            'question': question,
            'solution': solution,
            'feedback': human_feedback
        })

    def optimize(self):
        """Optimize the DSPy modules using collected feedback"""
        if len(self.training_examples) < 5:  # Minimum examples for optimization
            return
            
        # Create teleprompter and optimize
        teleprompter = dspy.teleprompt.BootstrapFinetune()
        optimized_program = teleprompter.compile(
            self.solution_generator, 
            trainset=self.training_examples
        )
        self.solution_generator = optimized_program

    def _parse_evaluation(self, eval_text: str) -> dict:
        """Parse evaluation text into structured format"""
        # Extract scores from evaluation text
        accuracy_match = re.search(r'Accuracy[:\s]*(\d+)/10', eval_text)
        clarity_match = re.search(r'Clarity[:\s]*(\d+)/10', eval_text)
        
        return {
            'accuracy': int(accuracy_match.group(1)) if accuracy_match else 0,
            'clarity': int(clarity_match.group(1)) if clarity_match else 0,
            'feedback': eval_text
        }

# Global instance
math_optimizer = MathTutorOptimizer()