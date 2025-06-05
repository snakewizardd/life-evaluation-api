#!/usr/bin/env python3
"""
Simplified API test script designed for CI/CD environments
No user interaction required - fully automated testing
"""

import requests
import json
import time
import sys
from typing import Dict, Any

API_BASE = "http://localhost:8000"

class CIAPITester:
    def __init__(self):
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   {details}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
        
    def wait_for_api(self, timeout: int = 30) -> bool:
        """Wait for API to be ready"""
        print("🔄 Waiting for API to be ready...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{API_BASE}/", timeout=2)
                if response.status_code == 200:
                    print("✅ API is ready!")
                    return True
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)
            
        print("❌ API failed to start within timeout")
        return False
        
    def test_models_endpoint(self) -> bool:
        """Test the models endpoint"""
        try:
            response = requests.get(f"{API_BASE}/api/models", timeout=10)
            
            if response.status_code != 200:
                self.log_test("Models Endpoint", False, f"Status: {response.status_code}")
                return False
                
            data = response.json()
            if "models" not in data:
                self.log_test("Models Endpoint", False, "Missing 'models' key in response")
                return False
                
            models = data["models"]
            expected_models = ["gpt-4.1-nano", "gpt-4.1-mini", "gpt-4.1"]
            
            for model in expected_models:
                if model not in models:
                    self.log_test("Models Endpoint", False, f"Missing model: {model}")
                    return False
                    
            self.log_test("Models Endpoint", True, f"Found {len(models)} models")
            return True
            
        except Exception as e:
            self.log_test("Models Endpoint", False, str(e))
            return False
            
    def test_question_generation(self) -> bool:
        """Test first question generation"""
        try:
            payload = {
                "prompt": "get better at coding",
                "model": "gpt-4.1-nano"
            }
            
            response = requests.post(
                f"{API_BASE}/api/generate-first-question",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code != 200:
                self.log_test("Question Generation", False, f"Status: {response.status_code}")
                return False
                
            data = response.json()
            if "question" not in data:
                self.log_test("Question Generation", False, "Missing 'question' key")
                return False
                
            question = data["question"]
            if not question or len(question.strip()) < 10:
                self.log_test("Question Generation", False, "Question too short or empty")
                return False
                
            self.log_test("Question Generation", True, f"Generated: {question[:50]}...")
            return True
            
        except Exception as e:
            self.log_test("Question Generation", False, str(e))
            return False
            
    def test_answer_analysis(self) -> bool:
        """Test answer analysis endpoint"""
        try:
            payload = {
                "prompt": "get better at coding",
                "questions": ["How many hours per day do you actually code?"],
                "answers": ["I spend most of my time watching coding tutorials instead of actually coding"],
                "current_answer": "I spend most of my time watching coding tutorials instead of actually coding",
                "model": "gpt-4.1-nano"
            }
            
            response = requests.post(
                f"{API_BASE}/api/analyze-answer-bro",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code != 200:
                self.log_test("Answer Analysis", False, f"Status: {response.status_code}")
                return False
                
            data = response.json()
            if "analysis" not in data:
                self.log_test("Answer Analysis", False, "Missing 'analysis' key")
                return False
                
            analysis = data["analysis"]
            if not analysis or len(analysis.strip()) < 5:
                self.log_test("Answer Analysis", False, "Analysis too short or empty")
                return False
                
            self.log_test("Answer Analysis", True, f"Analysis: {analysis[:50]}...")
            return True
            
        except Exception as e:
            self.log_test("Answer Analysis", False, str(e))
            return False
            
    def test_next_question(self) -> bool:
        """Test next question generation"""
        try:
            payload = {
                "prompt": "get better at coding",
                "questions": ["How many hours per day do you actually code?"],
                "answers": ["I spend most of my time watching coding tutorials instead of actually coding"],
                "model": "gpt-4.1-nano"
            }
            
            response = requests.post(
                f"{API_BASE}/api/generate-next-question-bro",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code != 200:
                self.log_test("Next Question", False, f"Status: {response.status_code}")
                return False
                
            data = response.json()
            if "question" not in data:
                self.log_test("Next Question", False, "Missing 'question' key")
                return False
                
            question = data["question"]
            if not question or len(question.strip()) < 10:
                self.log_test("Next Question", False, "Question too short or empty")
                return False
                
            self.log_test("Next Question", True, f"Generated: {question[:50]}...")
            return True
            
        except Exception as e:
            self.log_test("Next Question", False, str(e))
            return False
            
    def test_final_roast(self) -> bool:
        """Test final analysis generation"""
        try:
            payload = {
                "prompt": "get better at coding",
                "questions": [
                    "How many hours per day do you actually code?",
                    "What's stopping you from coding more consistently?"
                ],
                "answers": [
                    "I spend most of my time watching coding tutorials instead of actually coding",
                    "I keep telling myself I need to learn more before I start building projects"
                ],
                "model": "gpt-4.1-nano"
            }
            
            response = requests.post(
                f"{API_BASE}/api/generate-final-roast",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=20
            )
            
            if response.status_code != 200:
                self.log_test("Final Roast", False, f"Status: {response.status_code}")
                return False
                
            data = response.json()
            
            # Check required fields
            required_fields = ["title", "summary", "insights"]
            for field in required_fields:
                if field not in data:
                    self.log_test("Final Roast", False, f"Missing '{field}' key")
                    return False
                    
            # Validate content
            if not data["title"] or len(data["title"]) < 5:
                self.log_test("Final Roast", False, "Title too short or empty")
                return False
                
            if not data["summary"] or len(data["summary"]) < 10:
                self.log_test("Final Roast", False, "Summary too short or empty")
                return False
                
            if not isinstance(data["insights"], list) or len(data["insights"]) == 0:
                self.log_test("Final Roast", False, "Insights should be non-empty list")
                return False
                
            self.log_test("Final Roast", True, f"Title: {data['title']}")
            return True
            
        except Exception as e:
            self.log_test("Final Roast", False, str(e))
            return False
            
    def run_all_tests(self) -> bool:
        """Run all tests and return overall success"""
        print("🚀 Starting Life Evaluation API CI Tests")
        print("=" * 50)
        
        # Wait for API to be ready
        if not self.wait_for_api():
            return False
            
        # Run all tests
        tests = [
            self.test_models_endpoint,
            self.test_question_generation,
            self.test_answer_analysis,
            self.test_next_question,
            self.test_final_roast
        ]
        
        all_passed = True
        for test in tests:
            try:
                success = test()
                if not success:
                    all_passed = False
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
                all_passed = False
                
            time.sleep(1)  # Brief pause between tests
            
        # Print summary
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Tests passed: {passed}/{total}")
        
        if all_passed:
            print("🎉 All tests passed!")
            return True
        else:
            print("❌ Some tests failed!")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   ❌ {result['test']}: {result['details']}")
            return False

def main():
    tester = CIAPITester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code for CI
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()