#!/usr/bin/env python3
"""
test_full_system.py - Comprehensive test of the complete Math Agent system
"""
import asyncio
import time
from main import math_agent_query
from knowledge_base import math_kb

def test_knowledge_base():
    """Test the knowledge base functionality"""
    print("🧠 Testing Knowledge Base...")
    print("=" * 50)
    
    # Test questions that should be in KB
    kb_questions = [
        "What is the Pythagorean theorem?",
        "How to solve a quadratic equation?",
        "What is the derivative of sin(x)?"
    ]
    
    for question in kb_questions:
        print(f"\n🔍 Testing KB for: {question}")
        found_question, found_data = math_kb.search(question)
        
        if found_question and found_data:
            print(f"✅ FOUND in KB: {found_question}")
            print(f"   Similarity score: {found_data.get('similarity_score', 0):.3f}")
        else:
            print(f"❌ NOT found in KB")

def test_web_search():
    """Test web search functionality"""
    print("\n\n🌐 Testing Web Search (MCP)...")
    print("=" * 50)
    
    # Test questions that should trigger web search
    web_questions = [
        "Explain Taylor series expansion in calculus",
        "What is the chain rule used for?",
        "How to calculate compound interest formula?"
    ]
    
    for question in web_questions:
        print(f"\n🔍 Testing web search for: {question}")
        start_time = time.time()
        
        try:
            # This should trigger MCP web search
            found_question, found_data = math_kb.search(question)
            
            if found_question:
                print(f"❌ UNEXPECTED: Found in KB (should use web search)")
            else:
                print(f"✅ CORRECT: Not in KB, will use MCP web search")
                
        except Exception as e:
            print(f"⚠️  Error during search: {e}")
        
        elapsed = time.time() - start_time
        print(f"   Time taken: {elapsed:.2f}s")

def test_guardrails():
    """Test input guardrails"""
    print("\n\n🛡️ Testing Guardrails...")
    print("=" * 50)
    
    # Test cases that should be blocked
    invalid_questions = [
        "What's the weather today?",
        "Tell me a joke",
        "How to make a bomb?",
        "I need help with cooking",
        ""  # Empty query
    ]
    
    for question in invalid_questions:
        print(f"\n🛡️ Testing guardrail for: '{question}'")
        
        # Import the guardrail function from main
        from main import validate_input_guardrails
        
        is_valid, message = validate_input_guardrails(question)
        
        if is_valid:
            print(f"❌ UNEXPECTED: Should have been blocked")
        else:
            print(f"✅ CORRECT: Blocked - {message}")

def test_complete_flow():
    """Test the complete agent flow"""
    print("\n\n🤖 Testing Complete Agent Flow...")
    print("=" * 50)
    
    test_cases = [
        {
            "question": "What is the Pythagorean theorem?",
            "description": "Should be answered from Knowledge Base",
            "expected_source": "KB"
        },
        {
            "question": "Explain Lagrange multipliers",
            "description": "Should use MCP web search",
            "expected_source": "MCP"
        },
        {
            "question": "What's the best restaurant?",
            "description": "Should be blocked by guardrails",
            "expected_source": "GUARDRAIL"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔬 Test {i}: {test_case['description']}")
        print(f"   Question: {test_case['question']}")
        
        start_time = time.time()
        
        try:
            result = math_agent_query(test_case['question'])
            elapsed = time.time() - start_time
            
            # Analyze the result
            if "Error:" in result and test_case['expected_source'] == "GUARDRAIL":
                print(f"✅ SUCCESS: Correctly blocked by guardrail")
                print(f"   Response: {result}")
            elif "Knowledge Base" in result and test_case['expected_source'] == "KB":
                print(f"✅ SUCCESS: Answered from Knowledge Base")
                print(f"   Response length: {len(result)} characters")
            elif "Web Search" in result and test_case['expected_source'] == "MCP":
                print(f"✅ SUCCESS: Used MCP web search")
                print(f"   Response length: {len(result)} characters")
            else:
                print(f"⚠️  UNEXPECTED: Got different result than expected")
                print(f"   Result: {result[:200]}...")
            
            print(f"   Time taken: {elapsed:.2f}s")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            elapsed = time.time() - start_time
            print(f"   Time taken: {elapsed:.2f}s")

async def main():
    """Run all tests"""
    print("🎯 Starting Comprehensive System Test")
    print("=" * 60)
    
    # Run all test suites
    test_knowledge_base()
    test_web_search()
    test_guardrails()
    test_complete_flow()
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed!")
    print("\nNext steps:")
    print("1. Check if any tests failed")
    print("2. Review the MCP server output in its terminal")
    print("3. Run individual components if needed")
    print("4. Start the API: python app.py")

if __name__ == "__main__":
    asyncio.run(main())