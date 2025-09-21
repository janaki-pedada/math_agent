import os
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from knowledge_base import math_kb
from human_feedback import get_human_feedback, is_human_feedback_available
from mcp_client import mcp_client_instance
from output_guardrails import output_guardrails
from dotenv import load_dotenv
import google.generativeai as genai
import aiohttp
import re
import asyncio      
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Replace the MCPSearchTool class with this updated version
from mcp_client import mcp_client_instance

class MCPSearchTool(BaseTool):
    name: str = "mcp_web_search"
    description: str = "Searches the web using MCP protocol for mathematical concepts"
    
    async def _arun(self, query: str) -> str:
        """Async version that works with FastAPI"""
        try:
            results = await mcp_client_instance.search(query)
            if results:
                formatted = "\n".join([f"• {result}" for result in results[:3]])
                return f"Web Search Results for '{query}':\n{formatted}"
            return f"No relevant web results found for '{query}'"
        except Exception as e:
            return f"MCP search error: {str(e)}"
    
    def _run(self, query: str) -> str:
        """Sync version for CrewAI compatibility"""
        return asyncio.run(self._arun(query))
# Create tool instance
mcp_tool = MCPSearchTool()

# SIMPLE GEMINI CALL
def gemini_call(prompt: str) -> str:
    """Simple Gemini call"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text if response.text else "I don't have enough information to answer this question."
    except Exception as e:
        return f"Error: {str(e)}"

def validate_input_guardrails(input_text: str) -> tuple[bool, str]:
    if not input_text or len(input_text.strip()) < 3:
        return False, "Query too short. Please provide a complete question."
    
    math_keywords = [
        'calculate', 'solve', 'equation', 'derivative', 'integral', 
        'algebra', 'geometry', 'theorem', 'formula', 'math', 'probability',
        'trigonometry', 'calculus', 'matrix', 'vector', 'statistics'
    ]
    
    input_lower = input_text.lower()
    has_math_content = any(keyword in input_lower for keyword in math_keywords)
    
    if not has_math_content:
        return False, "This system only processes mathematics-related queries. Please ask a math question."
    
    return True, ""

def contains_uncertainty(response: str) -> bool:
    uncertainty_phrases = [
        "i don't know", "i cannot", "not sure", "uncertain", 
        "no information", "not found", "unable to", "don't have"
    ]
    response_lower = response.lower()
    return any(phrase in response_lower for phrase in uncertainty_phrases)

async def math_agent_query(user_question: str) -> str:
    # 1. INPUT GUARDRAIL
    is_valid, message = validate_input_guardrails(user_question)
    if not is_valid:
        return f"Error: {message}"

    # 2. KNOWLEDGE BASE ROUTING
    kb_question, kb_answer = math_kb.search(user_question)
    context = ""
    source = ""

    if kb_answer:
        context = f"""
        The answer was found in the knowledge base.
        QUESTION IN KB: {kb_question}
        ANSWER IN KB: {kb_answer['answer']}
        Please use this information to create a step-by-step solution.
        """
        source = "Knowledge Base"
    else:
        # 3. MCP WEB SEARCH ROUTING
        print("🔍 Answer not in Knowledge Base. Searching via MCP...")
        try:
            web_context = await mcp_tool._arun(user_question)  # Use async version
            
            # Check if MCP search failed or found nothing useful
            if "MCP search encountered an issue" in web_context:
                print("⚠️ MCP server not available.")
                context = f"The answer was not in our knowledge base. MCP search result: {web_context}"
                source = "MCP Web Search (Failed)"
            elif contains_uncertainty(web_context):
                return "I don't have enough information to answer this question accurately. The topic may be too specialized or I need more context."
            else:
                context = f"The answer was not in our knowledge base. Web search context: {web_context}"
                source = "Web Search (via MCP)"
                
        except Exception as e:
            # Handle any unexpected errors during MCP search
            print(f"⚠️ Unexpected error during MCP search: {e}")
            context = f"The answer was not in our knowledge base. MCP search encountered an unexpected error: {str(e)}"
            source = "MCP Web Search (Error)"

    # 4. SOLUTION GENERATION
    solution_prompt = f"""Create a step-by-step solution. If information is incomplete, be honest about limitations.
    STUDENT'S QUESTION: {user_question}
    SOURCE: {source}
    CONTEXT: {context}
    
    IMPORTANT: Provide a clear, step-by-step mathematical solution.
    Your solution must be accurate, educational, and honest about knowledge limits.
    """
    
    solution = gemini_call(solution_prompt)
    
    # Apply output guardrails
    is_valid, validation_msg = output_guardrails.validate_educational_content(solution)
    if not is_valid:
        solution = f"Note: {validation_msg}\n\nProceeding with caution:\n{solution}"
    
    solution = output_guardrails.sanitize_output(solution)

    # 5. FEEDBACK EVALUATION
    evaluation_prompt = f"""Evaluate this solution for the question: '{user_question}'.
    Score it from 1-10 on Accuracy and 1-10 on Clarity.
    If both scores are 8 or above, respond with "APPROVED: [solution]".
    If any score is below 8, respond with exactly this phrase:
    'HUMAN_FEEDBACK_NEEDED: Accuracy Score: [score], Clarity Score: [score]. Reason: [brief reason]'.
    
    SOLUTION TO EVALUATE: {solution}
    """
    
    evaluation = gemini_call(evaluation_prompt)

    # 6. Check if feedback is needed AND human feedback is available
    if "HUMAN_FEEDBACK_NEEDED" in evaluation and is_human_feedback_available():
        print("\n--- Triggering Human-in-the-Loop ---")
        refined_answer = get_human_feedback(user_question, evaluation)
        return refined_answer
    elif "HUMAN_FEEDBACK_NEEDED" in evaluation:
        print("\n--- Human Feedback Needed but Not Available ---")
        return "I need human review for this answer, but the feedback system is currently unavailable. Please try again later or ask a different question."
    elif "APPROVED:" in evaluation:
        return solution
    else:
        return solution

# Test function (keep this sync for command line testing)
def test_math_agent(query: str) -> str:
    """Sync wrapper for testing"""
    import asyncio
    return asyncio.run(math_agent_query(query))

if __name__ == "__main__":
    test_questions = [
        "What is the Pythagorean theorem?",
        "How to solve for x in equation 2x + 5 = 15?",
        "What is the derivative of sin(x)?"
    ]

    for q in test_questions:
        print(f"\n🧠 Query: {q}")
        result = test_math_agent(q)
        print(f"📝 Result: {result[:200]}...")
        print("-" * 50)