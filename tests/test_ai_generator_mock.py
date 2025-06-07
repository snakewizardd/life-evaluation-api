#!/usr/bin/env python3
"""
Mock version of AI test generator that doesn't require OpenAI API key
"""

import asyncio
import json
import random
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Any

@dataclass
class MockTestScenario:
    goal: str
    persona_type: str
    expected_question_themes: List[str]
    expected_analysis_keywords: List[str]
    difficulty_level: int
    emotional_state: str
    backstory: str
    red_flags: List[str]

class MockAITestValidator:
    def __init__(self):
        self.mock_scenarios = self._generate_mock_scenarios()
    
    def _generate_mock_scenarios(self) -> List[MockTestScenario]:
        """Generate realistic mock test scenarios"""
        return [
            MockTestScenario(
                goal="get jacked and build muscle mass",
                persona_type="perfectionist_procrastinator",
                expected_question_themes=["consistency", "excuses", "gym_attendance", "diet"],
                expected_analysis_keywords=["procrastination", "perfectionism", "analysis_paralysis"],
                difficulty_level=7,
                emotional_state="frustrated with lack of progress",
                backstory="Has been 'planning' to start working out for 8 months",
                red_flags=["all_or_nothing_thinking", "chronic_planning_without_action"]
            ),
            MockTestScenario(
                goal="find a girlfriend and improve dating life",
                persona_type="anxious_overthinker",
                expected_question_themes=["social_anxiety", "dating_apps", "real_conversations"],
                expected_analysis_keywords=["overthinking", "anxiety", "avoidance", "fear"],
                difficulty_level=8,
                emotional_state="lonely but scared of rejection",
                backstory="Hasn't been on a date in 14 months, spends hours on dating apps",
                red_flags=["social_isolation", "fear_of_vulnerability", "app_addiction"]
            ),
            MockTestScenario(
                goal="start a successful online business",
                persona_type="optimistic_unrealistic",
                expected_question_themes=["market_research", "customers", "revenue", "execution"],
                expected_analysis_keywords=["unrealistic", "research", "validation", "action"],
                difficulty_level=9,
                emotional_state="excited but naive about challenges",
                backstory="Has 20 business ideas but no customers or revenue",
                red_flags=["shiny_object_syndrome", "lack_of_focus", "no_customer_validation"]
            )
        ]
    
    def generate_mock_answers(self, scenario: MockTestScenario, questions: List[str]) -> List[str]:
        """Generate realistic answers based on persona"""
        persona_answers = {
            "perfectionist_procrastinator": [
                "I've been researching the perfect workout routine for months but haven't started yet.",
                "I need to get my diet completely dialed in before I can start going to the gym.",
                "I'm waiting until I have 2 hours free every day to do this properly.",
            ],
            "anxious_overthinker": [
                "I swipe on dating apps for hours but rarely message anyone because I overthink everything.",
                "I practice conversations in my head but freeze up when talking to attractive women.",
                "I keep telling myself I need to be more confident first before I start dating.",
            ],
            "optimistic_unrealistic": [
                "I have this amazing app idea that's going to disrupt the entire industry!",
                "I'm sure people will love my product once I build it - who wouldn't want this?",
                "I just need to find the right investor who understands my vision.",
            ]
        }
        
        answers = persona_answers.get(scenario.persona_type, [
            "I keep making excuses and not taking action.",
            "I know what to do but struggle with consistency.",
            "I overthink everything instead of just starting."
        ])
        
        return [random.choice(answers) for _ in questions]
    
    def validate_question_quality(self, question: str, scenario: MockTestScenario) -> tuple[float, List[str]]:
        """Mock validation of question quality"""
        issues = []
        score = 0.8  # Start with good score
        
        # Check if question contains brutal honesty indicators
        honesty_words = ["really", "actually", "honestly", "last time", "how often"]
        if any(word in question.lower() for word in honesty_words):
            score += 0.1
        else:
            issues.append("Question lacks brutal honesty style")
            score -= 0.2
        
        # Check for theme relevance
        if any(theme in question.lower() for theme in scenario.expected_question_themes):
            score += 0.1
        else:
            issues.append("Question doesn't explore expected themes")
            score -= 0.1
        
        return max(0.0, min(1.0, score)), issues
    
    def validate_analysis_quality(self, analysis: str, scenario: MockTestScenario) -> tuple[float, List[str]]:
        """Mock validation of analysis quality"""
        issues = []
        score = 0.7  # Start with decent score
        
        # Check for brutally honest language
        brutal_words = ["bs", "bullshit", "excuse", "lying", "reality", "truth"]
        if any(word in analysis.lower() for word in brutal_words):
            score += 0.2
        else:
            issues.append("Analysis lacks brutal honesty")
            score -= 0.1
        
        # Check for emojis
        if any(char in analysis for char in "🔥💀🤔😂"):
            score += 0.1
        else:
            issues.append("Missing brand-style emojis")
        
        return max(0.0, min(1.0, score)), issues

async def test_validation_system():
    """Test the validation system with mock data"""
    print("🤖 Testing AI Validation System (Mock Mode)")
    
    validator = MockAITestValidator()
    
    # Test scenarios
    total_score = 0
    total_tests = 0
    
    for scenario in validator.mock_scenarios:
        print(f"\n🧪 Testing scenario: {scenario.goal}")
        print(f"   Persona: {scenario.persona_type}")
        print(f"   Difficulty: {scenario.difficulty_level}/10")
        
        # Mock questions (simulate what API would generate)
        mock_questions = [
            "How many times have you actually started and given up on this goal?",
            "What's the real reason you haven't made progress yet?",
            "When was the last time you took action instead of just thinking about it?"
        ]
        
        # Generate mock answers
        answers = validator.generate_mock_answers(scenario, mock_questions)
        
        # Mock analysis
        mock_analysis = f"Bro, you're clearly stuck in {scenario.persona_type} patterns 🤔 Time to face the truth!"
        
        # Validate question quality
        q_scores = []
        for question in mock_questions:
            score, issues = validator.validate_question_quality(question, scenario)
            q_scores.append(score)
            if issues:
                print(f"   ⚠️  Question issues: {issues}")
        
        # Validate analysis quality
        a_score, a_issues = validator.validate_analysis_quality(mock_analysis, scenario)
        if a_issues:
            print(f"   ⚠️  Analysis issues: {a_issues}")
        
        avg_score = (sum(q_scores) + a_score) / (len(q_scores) + 1)
        total_score += avg_score
        total_tests += 1
        
        print(f"   📊 Average quality score: {avg_score:.2f}")
        print(f"   🎯 Red flags to detect: {scenario.red_flags}")
    
    overall_score = total_score / total_tests
    print(f"\n📊 Overall Results:")
    print(f"   Average quality score: {overall_score:.2f}")
    print(f"   Tests completed: {total_tests}")
    
    if overall_score > 0.7:
        print("✅ AI validation system working properly!")
        return True
    else:
        print("❌ AI validation system needs improvement")
        return False

async def main():
    success = await test_validation_system()
    
    if success:
        print("\n🎉 Mock AI testing system validated successfully!")
        print("💡 To use with real OpenAI API, set OPENAI_API_KEY environment variable")
    else:
        print("\n❌ Issues found in AI testing system")

if __name__ == "__main__":
    asyncio.run(main())