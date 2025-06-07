#!/usr/bin/env python3
"""
🤖 AI-Powered Test Data Generation & Validation System
Uses LLMs to generate realistic test scenarios and validate AI responses
"""

import asyncio
import json
import openai
import random
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import anthropic
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

@dataclass
class TestScenario:
    goal: str
    persona_type: str
    expected_question_themes: List[str]
    expected_analysis_keywords: List[str]
    difficulty_level: int  # 1-10
    emotional_state: str
    backstory: str
    red_flags: List[str]  # Things that should trigger concern

@dataclass
class ValidationResult:
    test_id: str
    scenario: TestScenario
    questions_generated: List[str]
    answers_given: List[str]
    analyses_received: List[str]
    final_roast: Dict[str, Any]
    quality_scores: Dict[str, float]
    issues_found: List[str]
    recommendations: List[str]
    timestamp: datetime

class AITestValidator:
    def __init__(self, openai_key: str, anthropic_key: Optional[str] = None):
        self.openai_client = openai.OpenAI(api_key=openai_key)
        self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key) if anthropic_key else None
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        
    async def generate_test_scenarios(self, count: int = 50) -> List[TestScenario]:
        """Generate diverse, realistic test scenarios using AI"""
        
        persona_templates = [
            "perfectionist_procrastinator", "optimistic_unrealistic", "depressed_unmotivated",
            "anxious_overthinker", "defensive_blamer", "honest_self_aware", "manic_scattered",
            "cynical_pessimist", "naive_idealist", "traumatized_avoidant", "addictive_personality",
            "workaholic_burnout", "people_pleaser", "narcissistic_entitled", "imposter_syndrome"
        ]
        
        goal_categories = [
            "fitness_health", "relationships_dating", "career_business", "personal_growth", 
            "creativity_arts", "financial_independence", "education_skills", "mental_health",
            "social_confidence", "life_purpose", "addiction_recovery", "family_relationships"
        ]
        
        scenarios = []
        
        for i in range(count):
            persona = random.choice(persona_templates)
            category = random.choice(goal_categories)
            
            scenario_prompt = f"""Generate a realistic test scenario for a brutal honesty life coaching AI.

Create a person with "{persona}" personality trying to achieve something in "{category}".

Return JSON with:
{{
    "goal": "specific, realistic goal statement",
    "persona_type": "{persona}",
    "expected_question_themes": ["list", "of", "themes", "questions", "should", "explore"],
    "expected_analysis_keywords": ["keywords", "that", "should", "appear", "in", "AI", "analysis"],
    "difficulty_level": 1-10,
    "emotional_state": "current emotional state description",
    "backstory": "brief backstory explaining their situation",
    "red_flags": ["concerning", "patterns", "AI", "should", "identify"]
}}

Make it psychologically realistic and diverse."""

            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": scenario_prompt}],
                    temperature=0.8
                )
                
                scenario_data = json.loads(response.choices[0].message.content)
                scenario = TestScenario(**scenario_data)
                scenarios.append(scenario)
                
            except Exception as e:
                print(f"Failed to generate scenario {i}: {e}")
                continue
        
        return scenarios
    
    async def generate_realistic_answers(self, scenario: TestScenario, questions: List[str]) -> List[str]:
        """Generate psychologically consistent answers for a scenario"""
        
        context = f"""
You are roleplaying as someone with these characteristics:
- Goal: {scenario.goal}
- Personality: {scenario.persona_type}
- Emotional state: {scenario.emotional_state}
- Backstory: {scenario.backstory}

Answer each question as this person would, being authentic to their psychology.
Include their defense mechanisms, blind spots, and patterns.
"""
        
        answers = []
        for question in questions:
            answer_prompt = f"""
{context}

Question: {question}

Provide a realistic answer that shows this person's psychology, including:
- Their typical defense mechanisms
- Level of self-awareness
- Communication patterns
- Emotional responses

Answer (1-3 sentences, stay in character):
"""
            
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": answer_prompt}],
                    temperature=0.7,
                    max_tokens=150
                )
                
                answer = response.choices[0].message.content.strip()
                answers.append(answer)
                
            except Exception as e:
                print(f"Failed to generate answer: {e}")
                answers.append("I don't know how to answer that.")
        
        return answers
    
    def validate_question_quality(self, question: str, scenario: TestScenario) -> Tuple[float, List[str]]:
        """Validate if a question is appropriately probing and relevant"""
        issues = []
        score = 0.0
        
        # Check question length
        if len(question.split()) < 5:
            issues.append("Question too short/shallow")
            score -= 0.2
        elif len(question.split()) > 30:
            issues.append("Question too long/complex")
            score -= 0.1
        else:
            score += 0.2
        
        # Check for question themes
        question_lower = question.lower()
        theme_matches = 0
        for theme in scenario.expected_question_themes:
            if theme.lower() in question_lower:
                theme_matches += 1
        
        if theme_matches > 0:
            score += 0.3 * (theme_matches / len(scenario.expected_question_themes))
        else:
            issues.append("Question doesn't explore expected themes")
        
        # Check for brutally honest style
        honesty_indicators = [
            "really", "actually", "honestly", "truth", "reality", "what's",
            "how often", "when was the last", "why do you", "what stops you"
        ]
        
        honesty_score = sum(1 for indicator in honesty_indicators if indicator in question_lower)
        if honesty_score > 0:
            score += 0.3
        else:
            issues.append("Question lacks brutal honesty style")
        
        # Check for specificity
        vague_words = ["better", "more", "improve", "good", "bad"]
        if any(word in question_lower for word in vague_words):
            issues.append("Question too vague, needs more specificity")
            score -= 0.1
        
        # Normalize score
        score = max(0.0, min(1.0, score))
        
        return score, issues
    
    def validate_analysis_quality(self, analysis: str, scenario: TestScenario, answer: str) -> Tuple[float, List[str]]:
        """Validate if analysis appropriately calls out patterns and BS"""
        issues = []
        score = 0.0
        
        analysis_lower = analysis.lower()
        answer_lower = answer.lower()
        
        # Check for keyword relevance
        keyword_matches = 0
        for keyword in scenario.expected_analysis_keywords:
            if keyword.lower() in analysis_lower:
                keyword_matches += 1
        
        if keyword_matches > 0:
            score += 0.3 * (keyword_matches / len(scenario.expected_analysis_keywords))
        else:
            issues.append("Analysis missing expected psychological keywords")
        
        # Check for brutal honesty
        honesty_indicators = [
            "bullshit", "bs", "excuse", "lying", "avoid", "scared", "afraid",
            "pattern", "always", "never", "really", "actually", "truth"
        ]
        
        honesty_score = sum(1 for indicator in honesty_indicators if indicator in analysis_lower)
        if honesty_score > 0:
            score += 0.3
        else:
            issues.append("Analysis lacks brutal honesty")
        
        # Check for emojis (part of the brand)
        emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]'
        if re.search(emoji_pattern, analysis):
            score += 0.1
        else:
            issues.append("Analysis missing emojis (brand style)")
        
        # Check length (should be concise)
        if 20 <= len(analysis.split()) <= 50:
            score += 0.2
        else:
            issues.append("Analysis length not optimal (should be 20-50 words)")
        
        # Check for red flag identification
        red_flag_identified = False
        for red_flag in scenario.red_flags:
            if red_flag.lower() in analysis_lower:
                red_flag_identified = True
                score += 0.1
                break
        
        if scenario.red_flags and not red_flag_identified:
            issues.append("Analysis missed identifying red flags from scenario")
        
        score = max(0.0, min(1.0, score))
        return score, issues
    
    def validate_final_roast(self, roast: Dict[str, Any], scenario: TestScenario) -> Tuple[float, List[str]]:
        """Validate the final analysis quality"""
        issues = []
        score = 0.0
        
        required_fields = ["title", "summary", "insights"]
        for field in required_fields:
            if field not in roast:
                issues.append(f"Missing required field: {field}")
                continue
            
            if not roast[field] or len(str(roast[field]).strip()) < 10:
                issues.append(f"Field '{field}' too short or empty")
                continue
            
            score += 0.2
        
        # Validate insights quality
        insights = roast.get("insights", [])
        if isinstance(insights, list) and len(insights) >= 3:
            score += 0.2
            
            # Check insight quality
            insight_scores = []
            for insight in insights[:5]:  # Check first 5 insights
                insight_score = 0
                insight_lower = insight.lower()
                
                # Check for actionability
                action_words = ["start", "stop", "try", "practice", "focus", "avoid"]
                if any(word in insight_lower for word in action_words):
                    insight_score += 0.5
                
                # Check for specificity
                if len(insight.split()) > 8:  # Detailed insights
                    insight_score += 0.3
                
                # Check for psychological depth
                psych_words = ["pattern", "behavior", "mindset", "belief", "fear", "motivation"]
                if any(word in insight_lower for word in psych_words):
                    insight_score += 0.2
                
                insight_scores.append(insight_score)
            
            avg_insight_score = np.mean(insight_scores)
            score += 0.2 * avg_insight_score
        else:
            issues.append("Insufficient or invalid insights")
        
        # Check title creativity
        title = roast.get("title", "")
        if "report" in title.lower() and any(char in title for char in "🎭🎯📊🔥"):
            score += 0.1
        else:
            issues.append("Title lacks creativity or branding")
        
        score = max(0.0, min(1.0, score))
        return score, issues
    
    async def run_comprehensive_validation(self, api_base: str, scenario: TestScenario) -> ValidationResult:
        """Run complete validation test for a scenario"""
        import aiohttp
        
        test_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000,9999)}"
        
        questions = []
        answers = []
        analyses = []
        quality_scores = {}
        issues_found = []
        
        async with aiohttp.ClientSession() as session:
            try:
                # Generate first question
                async with session.post(
                    f"{api_base}/api/generate-first-question",
                    json={"prompt": scenario.goal, "model": "gpt-4.1-nano"}
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        question = data.get("question", "")
                        questions.append(question)
                        
                        # Validate question
                        q_score, q_issues = self.validate_question_quality(question, scenario)
                        quality_scores["first_question"] = q_score
                        issues_found.extend([f"Q1: {issue}" for issue in q_issues])
                
                # Generate answers and continue journey
                for i in range(min(5, len(questions))):
                    # Generate realistic answer
                    scenario_answers = await self.generate_realistic_answers(scenario, [questions[i]])
                    answer = scenario_answers[0] if scenario_answers else "I don't know."
                    answers.append(answer)
                    
                    # Get analysis
                    async with session.post(
                        f"{api_base}/api/analyze-answer-bro",
                        json={
                            "prompt": scenario.goal,
                            "questions": questions,
                            "answers": answers,
                            "current_answer": answer,
                            "model": "gpt-4.1-nano"
                        }
                    ) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            analysis = data.get("analysis", "")
                            analyses.append(analysis)
                            
                            # Validate analysis
                            a_score, a_issues = self.validate_analysis_quality(analysis, scenario, answer)
                            quality_scores[f"analysis_{i+1}"] = a_score
                            issues_found.extend([f"A{i+1}: {issue}" for issue in a_issues])
                    
                    # Generate next question (if not last)
                    if i < 4:
                        async with session.post(
                            f"{api_base}/api/generate-next-question-bro",
                            json={
                                "prompt": scenario.goal,
                                "questions": questions,
                                "answers": answers,
                                "model": "gpt-4.1-nano"
                            }
                        ) as resp:
                            if resp.status == 200:
                                data = await resp.json()
                                question = data.get("question", "")
                                questions.append(question)
                                
                                # Validate question
                                q_score, q_issues = self.validate_question_quality(question, scenario)
                                quality_scores[f"question_{i+2}"] = q_score
                                issues_found.extend([f"Q{i+2}: {issue}" for issue in q_issues])
                
                # Get final roast
                final_roast = {}
                async with session.post(
                    f"{api_base}/api/generate-final-roast",
                    json={
                        "prompt": scenario.goal,
                        "questions": questions,
                        "answers": answers,
                        "model": "gpt-4.1-nano"
                    }
                ) as resp:
                    if resp.status == 200:
                        final_roast = await resp.json()
                        
                        # Validate final roast
                        f_score, f_issues = self.validate_final_roast(final_roast, scenario)
                        quality_scores["final_roast"] = f_score
                        issues_found.extend([f"Final: {issue}" for issue in f_issues])
            
            except Exception as e:
                issues_found.append(f"API Error: {str(e)}")
        
        # Generate recommendations
        recommendations = self._generate_recommendations(quality_scores, issues_found, scenario)
        
        return ValidationResult(
            test_id=test_id,
            scenario=scenario,
            questions_generated=questions,
            answers_given=answers,
            analyses_received=analyses,
            final_roast=final_roast,
            quality_scores=quality_scores,
            issues_found=issues_found,
            recommendations=recommendations,
            timestamp=datetime.now()
        )
    
    def _generate_recommendations(self, scores: Dict[str, float], issues: List[str], scenario: TestScenario) -> List[str]:
        """Generate actionable recommendations based on test results"""
        recommendations = []
        
        avg_score = np.mean(list(scores.values())) if scores else 0.0
        
        if avg_score < 0.5:
            recommendations.append("Overall AI performance below standards - needs significant improvement")
        
        # Question-specific recommendations
        question_scores = [score for key, score in scores.items() if "question" in key]
        if question_scores and np.mean(question_scores) < 0.6:
            recommendations.append("Improve question generation - add more specificity and brutal honesty")
        
        # Analysis-specific recommendations  
        analysis_scores = [score for key, score in scores.items() if "analysis" in key]
        if analysis_scores and np.mean(analysis_scores) < 0.6:
            recommendations.append("Enhance analysis quality - better pattern recognition and callouts needed")
        
        # Issue-based recommendations
        if any("missing emojis" in issue for issue in issues):
            recommendations.append("Ensure consistent emoji usage in responses for brand consistency")
        
        if any("red flag" in issue for issue in issues):
            recommendations.append("Improve red flag detection for concerning behavioral patterns")
        
        if any("theme" in issue for issue in issues):
            recommendations.append("Better alignment of questions with user's specific goal themes")
        
        return recommendations

async def main():
    """Run AI-powered test generation and validation"""
    import os
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("❌ OPENAI_API_KEY not set")
        return
    
    validator = AITestValidator(openai_key)
    
    print("🤖 Generating AI test scenarios...")
    scenarios = await validator.generate_test_scenarios(count=10)
    
    print(f"✅ Generated {len(scenarios)} test scenarios")
    
    # Run validation on a few scenarios
    for i, scenario in enumerate(scenarios[:3]):
        print(f"\n🧪 Testing scenario {i+1}: {scenario.goal}")
        result = await validator.run_comprehensive_validation("http://localhost:8000", scenario)
        
        print(f"📊 Average quality score: {np.mean(list(result.quality_scores.values())):.2f}")
        print(f"⚠️  Issues found: {len(result.issues_found)}")
        print(f"💡 Recommendations: {len(result.recommendations)}")
        
        # Save detailed results
        with open(f"/tmp/ai_validation_{result.test_id}.json", "w") as f:
            json.dump(asdict(result), f, indent=2, default=str)

if __name__ == "__main__":
    asyncio.run(main())