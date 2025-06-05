#!/usr/bin/env python3
"""
Life Evaluation API Test Script
Simulates a complete user journey through the brutally honest AI coaching system
"""

import requests
import json
import time
from typing import List, Dict

API_BASE = "http://localhost:8000"

class LifeEvaluationTester:
    def __init__(self, goal: str, model: str = "gpt-4.1-nano"):
        self.goal = goal
        self.model = model
        self.questions: List[str] = []
        self.answers: List[str] = []
        self.analyses: List[str] = []
        
    def print_section(self, title: str, content: str = ""):
        print(f"\n{'='*50}")
        print(f"🔥 {title}")
        print(f"{'='*50}")
        if content:
            print(content)
    
    def test_models_endpoint(self):
        """Test the models endpoint"""
        self.print_section("TESTING MODELS ENDPOINT")
        
        response = requests.get(f"{API_BASE}/api/models")
        if response.status_code == 200:
            models = response.json()
            print("✅ Models endpoint working!")
            for model_key, model_info in models["models"].items():
                print(f"  📱 {model_info['name']} - {model_info['price']}")
        else:
            print(f"❌ Models endpoint failed: {response.status_code}")
            return False
        return True
    
    def generate_first_question(self):
        """Generate the first brutally honest question"""
        self.print_section("GENERATING FIRST QUESTION")
        
        payload = {
            "prompt": self.goal,
            "model": self.model
        }
        
        response = requests.post(
            f"{API_BASE}/api/generate-first-question",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            question = response.json()["question"]
            self.questions.append(question)
            print(f"✅ Question generated!")
            print(f"🤔 {question}")
            return True
        else:
            print(f"❌ Question generation failed: {response.status_code}")
            print(response.text)
            return False
    
    def simulate_answer(self, question_num: int) -> str:
        """Simulate realistic user answers based on the goal"""
        answers_by_goal = {
            "get jacked": [
                "Honestly, I avoid the gym when it's busy because I feel intimidated by all the muscular guys. I usually go late at night or not at all.",
                "I've started and stopped working out like 6 times in the past 2 years. I get motivated for 2-3 weeks then something always comes up.",
                "I eat pretty well during the day but I binge on junk food at night when I'm stressed or bored watching Netflix.",
                "I tell myself I'll start next Monday every week. I have a gym membership I barely use but I keep paying for it out of guilt.",
                "I spend more time watching fitness YouTube videos and planning routines than actually working out. I have like 10 different workout plans saved."
            ],
            "get a girlfriend": [
                "I haven't approached a girl I found attractive in like 8 months. I always find excuses or convince myself she's probably taken.",
                "I swipe on dating apps for hours but rarely message matches. When I do message, it's usually something boring like 'hey how's your day'.",
                "I spend most weekends playing video games or hanging with the same 3 guy friends. I rarely go anywhere I'd actually meet women.",
                "I tell myself I need to get in better shape or make more money before I start dating, but I'm not really working on either consistently.",
                "I've been 'working on myself' for 2 years but it's mostly just an excuse to avoid the scary part of actually putting myself out there."
            ],
            "start a business": [
                "I have like 20 business ideas saved in my notes app but I've never actually validated any of them with real people.",
                "I spend hours watching entrepreneur podcasts and YouTube videos but I haven't built a single prototype or talked to a potential customer.",
                "I keep waiting for the 'perfect' idea but really I'm just scared of failing publicly or looking stupid to my friends and family.",
                "I tell myself I need more money saved first, but I also spend money on courses and books instead of just starting small.",
                "I've been saying 'this is the year' for 3 years now. My friends probably think I'm all talk at this point."
            ]
        }
        
        # Get appropriate answers for the goal, or use generic ones
        goal_answers = answers_by_goal.get(self.goal.lower(), [
            "I talk about it a lot but don't take consistent action.",
            "I keep finding excuses and delaying the hard parts.",
            "I consume content about it instead of actually doing it.",
            "I've been 'preparing' for months without real progress.",
            "I know what to do but struggle with follow-through."
        ])
        
        if question_num <= len(goal_answers):
            return goal_answers[question_num - 1]
        else:
            return goal_answers[-1]  # Use last answer as fallback
    
    def answer_question_and_analyze(self, question_num: int):
        """Answer a question and get AI analysis"""
        self.print_section(f"ANSWERING QUESTION {question_num}")
        
        # Simulate user typing answer
        answer = self.simulate_answer(question_num)
        self.answers.append(answer)
        
        print(f"💭 User Answer: {answer}")
        print("\nAnalyzing response...")
        
        # Get analysis
        payload = {
            "prompt": self.goal,
            "questions": self.questions,
            "answers": self.answers,
            "current_answer": answer,
            "model": self.model
        }
        
        response = requests.post(
            f"{API_BASE}/api/analyze-answer-bro",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            analysis = response.json()["analysis"]
            self.analyses.append(analysis)
            print(f"🔥 AI Analysis: {analysis}")
            return True
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            return False
    
    def generate_next_question(self, question_num: int):
        """Generate the next question based on previous answers"""
        if question_num >= 5:
            return True
            
        self.print_section(f"GENERATING QUESTION {question_num + 1}")
        
        payload = {
            "prompt": self.goal,
            "questions": self.questions,
            "answers": self.answers,
            "model": self.model
        }
        
        response = requests.post(
            f"{API_BASE}/api/generate-next-question-bro",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            question = response.json()["question"]
            self.questions.append(question)
            print(f"✅ Next question generated!")
            print(f"🤔 {question}")
            return True
        else:
            print(f"❌ Next question generation failed: {response.status_code}")
            return False
    
    def generate_final_roast(self):
        """Generate the final cosmic analysis"""
        self.print_section("GENERATING FINAL COSMIC ROAST")
        
        payload = {
            "prompt": self.goal,
            "questions": self.questions,
            "answers": self.answers,
            "model": self.model
        }
        
        response = requests.post(
            f"{API_BASE}/api/generate-final-roast",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            final_analysis = response.json()
            print(f"✅ Final analysis generated!")
            print(f"\n🎭 {final_analysis.get('title', 'The Reality Check Report')}")
            print(f"\n📊 Summary: {final_analysis.get('summary', 'Analysis complete')}")
            
            insights = final_analysis.get('insights', [])
            if insights:
                print(f"\n💡 Key Insights:")
                for i, insight in enumerate(insights, 1):
                    print(f"   {i}. {insight}")
            
            return True
        else:
            print(f"❌ Final analysis failed: {response.status_code}")
            print(response.text)
            return False
    
    def run_full_journey(self):
        """Run the complete user journey simulation"""
        self.print_section("STARTING LIFE EVALUATION JOURNEY", f"Goal: {self.goal}")
        
        # Test models endpoint
        if not self.test_models_endpoint():
            return False
        
        time.sleep(1)
        
        # Generate first question
        if not self.generate_first_question():
            return False
            
        # Answer 5 questions
        for i in range(5):
            time.sleep(1)
            
            # Answer current question and get analysis
            if not self.answer_question_and_analyze(i + 1):
                return False
            
            time.sleep(1)
            
            # Generate next question (unless we're on the last one)
            if i < 4:
                if not self.generate_next_question(i + 1):
                    return False
        
        time.sleep(1)
        
        # Generate final analysis
        if not self.generate_final_roast():
            return False
        
        self.print_section("JOURNEY COMPLETE!", "🎉 Successfully tested the entire user flow!")
        return True
    
    def print_summary(self):
        """Print a summary of the entire session"""
        self.print_section("SESSION SUMMARY")
        print(f"🎯 Goal: {self.goal}")
        print(f"🤖 Model: {self.model}")
        print(f"❓ Questions: {len(self.questions)}")
        print(f"💬 Answers: {len(self.answers)}")
        print(f"🔍 Analyses: {len(self.analyses)}")
        
        print(f"\n📝 Q&A Summary:")
        for i, (q, a) in enumerate(zip(self.questions, self.answers), 1):
            print(f"\nQ{i}: {q}")
            print(f"A{i}: {a}")
            if i <= len(self.analyses):
                print(f"Analysis: {self.analyses[i-1]}")

def main():
    # Test scenarios
    test_scenarios = [
        "get jacked",
        "get a girlfriend", 
        "start a business"
    ]
    
    print("🚀 Life Evaluation API Testing Script")
    print("Choose a scenario to test:")
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"  {i}. {scenario}")
    
    try:
        choice = int(input(f"\nEnter choice (1-{len(test_scenarios)}): ")) - 1
        if 0 <= choice < len(test_scenarios):
            goal = test_scenarios[choice]
        else:
            goal = input("Enter custom goal: ")
    except (ValueError, KeyboardInterrupt):
        goal = "get jacked"  # Default
    
    # Choose model
    print(f"\nChoose model:")
    models = ["gpt-4.1-nano", "gpt-4.1-mini", "gpt-4.1"]
    for i, model in enumerate(models, 1):
        print(f"  {i}. {model}")
    
    try:
        model_choice = int(input(f"Enter choice (1-{len(models)}): ")) - 1
        if 0 <= model_choice < len(models):
            model = models[model_choice]
        else:
            model = "gpt-4.1-nano"
    except (ValueError, KeyboardInterrupt):
        model = "gpt-4.1-nano"
    
    # Run the test
    tester = LifeEvaluationTester(goal, model)
    
    try:
        success = tester.run_full_journey()
        if success:
            tester.print_summary()
        else:
            print("❌ Journey failed at some point")
    except KeyboardInterrupt:
        print("\n\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()