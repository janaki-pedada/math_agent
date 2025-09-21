import asyncio
import json
import time
from typing import List, Dict
from main import math_agent_query

class JEEBenchmark:
    def __init__(self):
        self.results = []
        self.metrics = {
            'total_questions': 0,
            'correct_answers': 0,
            'kb_hits': 0,
            'web_searches': 0,
            'avg_response_time': 0,
            'accuracy_rate': 0
        }

    def load_jee_dataset(self, file_path: str = "jee_questions.json") -> List[Dict]:
        """Load JEE benchmark questions"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Fallback to built-in questions
            return [
                {
                    "question": "Find the derivative of f(x) = x²sin(x)",
                    "expected_keywords": ["2x sin(x)", "x² cos(x)", "product rule"]
                },
                {
                    "question": "Solve the differential equation: dy/dx = y/x",
                    "expected_keywords": ["separation of variables", "ln|y| = ln|x| + C", "y = Cx"]
                },
                {
                    "question": "Evaluate ∫(0 to π) x sin(x) dx",
                    "expected_keywords": ["integration by parts", "π", "sin(x)", "cos(x)"]
                }
            ]

    async def run_benchmark(self, questions: List[Dict]):
        """Run benchmark against JEE questions"""
        total_time = 0
        
        for i, q in enumerate(questions):
            print(f"🧪 Testing question {i+1}/{len(questions)}: {q['question'][:50]}...")
            
            start_time = time.time()
            response = await math_agent_query(q['question'])
            elapsed = time.time() - start_time
            total_time += elapsed
            
            # Evaluate response
            is_correct = self.evaluate_response(q['question'], response, q.get('expected_keywords', []))
            source = self.detect_source(response)
            
            result = {
                'question': q['question'],
                'response': response,
                'time_taken': elapsed,
                'correct': is_correct,
                'source': source
            }
            
            self.results.append(result)
            self.update_metrics(result, is_correct, source)
            
            print(f"   Time: {elapsed:.2f}s, Correct: {is_correct}, Source: {source}")
        
        self.metrics['avg_response_time'] = total_time / len(questions)
        self.metrics['accuracy_rate'] = self.metrics['correct_answers'] / self.metrics['total_questions']

    def evaluate_response(self, question: str, response: str, expected_keywords: List[str]) -> bool:
        """Evaluate if response contains expected mathematical concepts"""
        response_lower = response.lower()
        
        # Check for expected keywords
        keyword_matches = sum(1 for kw in expected_keywords if kw.lower() in response_lower)
        
        # Basic heuristics for mathematical correctness
        has_steps = response.count('\n') >= 2
        has_math_symbols = any(c in response for c in '∫∑√πθαβγΔ≠≈±→')
        
        return keyword_matches >= len(expected_keywords) * 0.7 and has_steps and has_math_symbols

    def detect_source(self, response: str) -> str:
        """Detect where the answer came from"""
        if "Knowledge Base" in response:
            return "KB"
        elif "Web Search" in response:
            return "Web"
        elif "Error" in response:
            return "Error"
        else:
            return "Unknown"

    def update_metrics(self, result: Dict, is_correct: bool, source: str):
        """Update benchmark metrics"""
        self.metrics['total_questions'] += 1
        if is_correct:
            self.metrics['correct_answers'] += 1
        if source == "KB":
            self.metrics['kb_hits'] += 1
        elif source == "Web":
            self.metrics['web_searches'] += 1

    def generate_report(self) -> str:
        """Generate benchmark report"""
        report = [
            "📊 JEE Benchmark Results",
            "=" * 50,
            f"Total Questions: {self.metrics['total_questions']}",
            f"Correct Answers: {self.metrics['correct_answers']}",
            f"Accuracy Rate: {self.metrics['accuracy_rate']:.2%}",
            f"Knowledge Base Hits: {self.metrics['kb_hits']}",
            f"Web Searches: {self.metrics['web_searches']}",
            f"Average Response Time: {self.metrics['avg_response_time']:.2f}s",
            "",
            "Detailed Results:",
            "-" * 30
        ]
        
        for i, result in enumerate(self.results):
            report.append(f"{i+1}. {result['question'][:30]}...")
            report.append(f"   Correct: {result['correct']}, Time: {result['time_taken']:.2f}s, Source: {result['source']}")
        
        return "\n".join(report)

async def main():
    """Run JEE benchmark"""
    benchmark = JEEBenchmark()
    questions = benchmark.load_jee_dataset()
    
    print("🚀 Starting JEE Benchmark...")
    await benchmark.run_benchmark(questions)
    
    report = benchmark.generate_report()
    print("\n" + report)
    
    # Save results to file
    with open("jee_benchmark_results.txt", "w") as f:
        f.write(report)

if __name__ == "__main__":
    asyncio.run(main())