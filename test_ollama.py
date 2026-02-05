#!/usr/bin/env python3
"""
Test script to verify Ollama LLM functionality
"""
import os
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.llm.chat import ChatLLM
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_ollama_simple_question(question: str = "What is the capital of France?"):
    """
    Test Ollama LLM with a simple question.
    
    Args:
        question (str): The question to ask the LLM
        
    Returns:
        dict: Result containing success status and response/error
    """
    try:
        # Ensure we're using Ollama
        os.environ["LLM_PROVIDER"] = "ollama"
        
        print(f"🤖 Testing Ollama LLM...")
        print(f"📝 Question: {question}")
        print(f"⚙️ Provider: {os.getenv('LLM_PROVIDER', 'ollama')}")
        print(f"🔗 Endpoint: {os.getenv('LLM_ENDPOINT', 'http://localhost:11434/v1')}")
        print(f"🎯 Model: {os.getenv('OLLAMA_MODEL', 'llama3.2:1b')}")
        print("-" * 60)
        
        # Initialize ChatLLM
        chat_llm = ChatLLM()
        
        # Ask the question
        print("🚀 Sending question to Ollama...")
        response = chat_llm.invoke(question)
        
        print("✅ Response received!")
        print(f"💬 Answer: {response}")
        print("-" * 60)
        
        return {
            "success": True,
            "question": question,
            "response": response,
            "provider": "ollama",
            "model": chat_llm.model_name
        }
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error testing Ollama: {error_msg}")
        return {
            "success": False,
            "question": question,
            "error": error_msg,
            "provider": "ollama"
        }

def test_ollama_medical_question():
    """Test Ollama with a medical-related question."""
    medical_question = "What are the common symptoms of diabetes?"
    return test_ollama_simple_question(medical_question)

def test_ollama_multiple_questions():
    """Test Ollama with multiple questions."""
    questions = [
        "What is 2 + 2?",
        "Name three planets in our solar system.",
        "What is Python programming language used for?",
        "Explain what a neural network is in simple terms."
    ]
    
    results = []
    for i, question in enumerate(questions, 1):
        print(f"\n🔍 Test {i}/{len(questions)}")
        result = test_ollama_simple_question(question)
        results.append(result)
        
        if not result["success"]:
            print(f"⚠️ Test {i} failed, stopping...")
            break
    
    return results

def main():
    """Main function to run tests."""
    print("🧪 Ollama LLM Test Suite")
    print("=" * 60)
    
    # Test 1: Simple question
    print("\n1️⃣ Testing simple question...")
    result1 = test_ollama_simple_question()
    
    if result1["success"]:
        # Test 2: Medical question
        print("\n2️⃣ Testing medical question...")
        result2 = test_ollama_medical_question()
        
        if result2["success"]:
            # Test 3: Multiple questions
            print("\n3️⃣ Testing multiple questions...")
            results = test_ollama_multiple_questions()
            
            success_count = sum(1 for r in results if r["success"])
            print(f"\n📊 Summary: {success_count}/{len(results)} tests passed")
            
        else:
            print("❌ Medical question test failed")
    else:
        print("❌ Simple question test failed")

if __name__ == "__main__":
    main()