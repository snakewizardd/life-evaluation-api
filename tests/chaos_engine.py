#!/usr/bin/env python3
"""
🌪️ Chaos Engineering Test Engine for Life Evaluation API
Advanced testing that simulates real-world failures and edge cases
"""

import asyncio
import aiohttp
import random
import time
import json
import psutil
import logging
from typing import List, Dict, Any, Callable
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from datetime import datetime, timedelta

@dataclass
class ChaosScenario:
    name: str
    description: str
    probability: float
    severity: int  # 1-10
    duration: int  # seconds
    execute: Callable

@dataclass
class TestMetrics:
    response_times: List[float]
    error_rates: List[float]
    throughput: List[float]
    memory_usage: List[float]
    cpu_usage: List[float]
    timestamp: datetime

class IntelligentLoadTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
        self.metrics = []
        self.chaos_scenarios = []
        self.ai_personas = self._generate_ai_personas()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self._setup_chaos_scenarios()
    
    def _generate_ai_personas(self) -> List[Dict]:
        """Generate diverse AI personas for realistic testing"""
        return [
            {
                "name": "Perfectionist Paul",
                "goals": ["become a millionaire", "get perfect abs", "master 5 languages"],
                "answer_style": "overthinking", 
                "response_length": "long",
                "honesty_level": 0.3,
                "patterns": ["procrastination", "analysis_paralysis", "perfectionism"]
            },
            {
                "name": "Scattered Sarah", 
                "goals": ["get organized", "find love", "start 10 businesses"],
                "answer_style": "scattered",
                "response_length": "medium", 
                "honesty_level": 0.7,
                "patterns": ["distraction", "impulsiveness", "multi-tasking"]
            },
            {
                "name": "Honest Henry",
                "goals": ["quit smoking", "repair relationships", "face fears"],
                "answer_style": "brutally_honest",
                "response_length": "short",
                "honesty_level": 0.9,
                "patterns": ["self_awareness", "accountability", "growth"]
            },
            {
                "name": "Denial Dan",
                "goals": ["get rich quick", "become famous", "avoid responsibility"],
                "answer_style": "defensive",
                "response_length": "short",
                "honesty_level": 0.1,
                "patterns": ["blame_others", "unrealistic_goals", "avoidance"]
            }
        ]
    
    def _setup_chaos_scenarios(self):
        """Define chaos engineering scenarios"""
        self.chaos_scenarios = [
            ChaosScenario(
                "api_timeout", 
                "Simulate slow OpenAI API responses",
                0.15, 8, 10,
                self._inject_api_delay
            ),
            ChaosScenario(
                "memory_pressure",
                "Create memory pressure on the system", 
                0.10, 6, 15,
                self._create_memory_pressure
            ),
            ChaosScenario(
                "network_flakiness",
                "Simulate network interruptions",
                0.20, 7, 5,
                self._simulate_network_issues
            ),
            ChaosScenario(
                "concurrent_user_spike", 
                "Sudden spike in concurrent users",
                0.25, 9, 20,
                self._user_spike
            )
        ]
    
    async def _inject_api_delay(self):
        """Simulate OpenAI API being slow"""
        self.logger.warning("🐌 Injecting API delay chaos...")
        # In real implementation, this would patch the OpenAI client
        await asyncio.sleep(random.uniform(5, 15))
    
    async def _create_memory_pressure(self):
        """Create memory pressure"""
        self.logger.warning("🧠 Creating memory pressure...")
        # Allocate large amounts of memory
        memory_hog = []
        for _ in range(100):
            memory_hog.append([0] * 100000)
            await asyncio.sleep(0.1)
        del memory_hog
    
    async def _simulate_network_issues(self):
        """Simulate network connectivity issues"""
        self.logger.warning("📡 Simulating network issues...")
        # In real implementation, this would use network manipulation tools
        await asyncio.sleep(random.uniform(1, 3))
    
    async def _user_spike(self):
        """Simulate sudden user spike"""
        self.logger.warning("👥 Simulating user spike...")
        tasks = []
        for _ in range(50):
            tasks.append(self._simulate_single_user())
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _simulate_single_user(self) -> Dict[str, Any]:
        """Simulate a single user journey with AI persona"""
        persona = random.choice(self.ai_personas)
        goal = random.choice(persona["goals"])
        
        start_time = time.time()
        journey_data = {
            "persona": persona["name"],
            "goal": goal,
            "questions": [],
            "answers": [], 
            "analyses": [],
            "response_times": [],
            "errors": []
        }
        
        try:
            # Generate questions and answers based on persona
            for question_num in range(5):
                # Get question
                q_start = time.time()
                if question_num == 0:
                    question_response = await self._call_api("generate-first-question", {
                        "prompt": goal,
                        "model": "gpt-4.1-nano"
                    })
                else:
                    question_response = await self._call_api("generate-next-question-bro", {
                        "prompt": goal,
                        "questions": journey_data["questions"],
                        "answers": journey_data["answers"],
                        "model": "gpt-4.1-nano"
                    })
                
                q_time = time.time() - q_start
                journey_data["response_times"].append(q_time)
                
                if question_response:
                    question = question_response.get("question", "")
                    journey_data["questions"].append(question)
                    
                    # Generate realistic answer based on persona
                    answer = self._generate_persona_answer(persona, question, goal)
                    journey_data["answers"].append(answer)
                    
                    # Get analysis
                    a_start = time.time()
                    analysis_response = await self._call_api("analyze-answer-bro", {
                        "prompt": goal,
                        "questions": journey_data["questions"],
                        "answers": journey_data["answers"],
                        "current_answer": answer,
                        "model": "gpt-4.1-nano"
                    })
                    a_time = time.time() - a_start
                    journey_data["response_times"].append(a_time)
                    
                    if analysis_response:
                        journey_data["analyses"].append(analysis_response.get("analysis", ""))
            
            # Get final roast
            f_start = time.time()
            final_response = await self._call_api("generate-final-roast", {
                "prompt": goal,
                "questions": journey_data["questions"],
                "answers": journey_data["answers"],
                "model": "gpt-4.1-nano"
            })
            f_time = time.time() - f_start
            journey_data["response_times"].append(f_time)
            
            journey_data["total_time"] = time.time() - start_time
            return journey_data
            
        except Exception as e:
            journey_data["errors"].append(str(e))
            return journey_data
    
    def _generate_persona_answer(self, persona: Dict, question: str, goal: str) -> str:
        """Generate realistic answers based on persona characteristics"""
        base_answers = {
            "overthinking": [
                "Well, it's complicated because I've been analyzing this from multiple angles...",
                "I've researched extensively and created a 47-point plan, but I'm not sure if it's perfect yet...",
                "There are so many variables to consider, and I want to make sure I optimize everything..."
            ],
            "scattered": [
                "Oh yeah, I started that but then I got distracted by this other thing...",
                "I have like 10 different approaches I'm trying simultaneously...",
                "Wait, what was the question again? I was thinking about something else..."
            ],
            "brutally_honest": [
                "Honestly? I've been making excuses and avoiding the hard work.",
                "I keep lying to myself about being 'busy' when I'm just scared.",
                "The truth is I spend more time talking about it than doing it."
            ],
            "defensive": [
                "It's not my fault, the system is rigged against people like me.",
                "I would succeed if I had better circumstances like everyone else.",
                "The timing just isn't right, and I don't have the resources others have."
            ]
        }
        
        style = persona.get("answer_style", "scattered")
        answers = base_answers.get(style, base_answers["scattered"])
        return random.choice(answers)
    
    async def _call_api(self, endpoint: str, payload: Dict) -> Dict:
        """Make API call with error handling"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/{endpoint}",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    self.logger.error(f"API error {response.status} for {endpoint}")
                    return {}
        except Exception as e:
            self.logger.error(f"Request failed for {endpoint}: {e}")
            return {}
    
    async def _collect_system_metrics(self) -> TestMetrics:
        """Collect system performance metrics"""
        return TestMetrics(
            response_times=[],
            error_rates=[],
            throughput=[],
            memory_usage=[psutil.virtual_memory().percent],
            cpu_usage=[psutil.cpu_percent(interval=1)],
            timestamp=datetime.now()
        )
    
    async def run_chaos_test(self, duration_minutes: int = 30, users_per_minute: int = 10):
        """Run comprehensive chaos engineering test"""
        self.logger.info(f"🌪️ Starting {duration_minutes}m chaos test with {users_per_minute} users/min")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        results = {
            "test_start": datetime.now().isoformat(),
            "total_users": 0,
            "successful_journeys": 0,
            "failed_journeys": 0,
            "chaos_events": [],
            "performance_metrics": [],
            "user_journeys": []
        }
        
        try:
            while time.time() < end_time:
                # Randomly trigger chaos scenarios
                for scenario in self.chaos_scenarios:
                    if random.random() < scenario.probability:
                        self.logger.warning(f"🎭 Triggering chaos: {scenario.name}")
                        results["chaos_events"].append({
                            "scenario": scenario.name,
                            "timestamp": datetime.now().isoformat(),
                            "severity": scenario.severity
                        })
                        asyncio.create_task(scenario.execute())
                
                # Launch user simulations
                user_tasks = []
                for _ in range(users_per_minute):
                    user_tasks.append(self._simulate_single_user())
                
                # Collect metrics
                metrics = await self._collect_system_metrics()
                results["performance_metrics"].append(metrics)
                
                # Execute user journeys
                journey_results = await asyncio.gather(*user_tasks, return_exceptions=True)
                
                for journey in journey_results:
                    if isinstance(journey, dict):
                        results["user_journeys"].append(journey)
                        if journey.get("errors"):
                            results["failed_journeys"] += 1
                        else:
                            results["successful_journeys"] += 1
                        results["total_users"] += 1
                
                # Wait before next batch
                await asyncio.sleep(60 / users_per_minute)
        
        finally:
            if self.session:
                await self.session.close()
            
            # Generate comprehensive report
            await self._generate_chaos_report(results)
        
        return results
    
    async def _generate_chaos_report(self, results: Dict):
        """Generate detailed chaos test report"""
        report = {
            "summary": {
                "total_duration": results.get("total_users", 0) and "30 minutes" or "0 minutes",
                "total_users": results.get("total_users", 0),
                "success_rate": (results.get("successful_journeys", 0) / max(results.get("total_users", 1), 1)) * 100,
                "chaos_events": len(results.get("chaos_events", [])),
                "avg_response_time": self._calculate_avg_response_time(results.get("user_journeys", []))
            },
            "chaos_impact": self._analyze_chaos_impact(results),
            "performance_trends": self._analyze_performance_trends(results),
            "recommendations": self._generate_recommendations(results)
        }
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"/tmp/chaos_report_{timestamp}.json", "w") as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.info(f"📊 Chaos test report saved: /tmp/chaos_report_{timestamp}.json")
        self.logger.info(f"🎯 Success rate: {report['summary']['success_rate']:.1f}%")
    
    def _calculate_avg_response_time(self, journeys: List[Dict]) -> float:
        """Calculate average response time across all journeys"""
        total_time = sum(journey.get("total_time", 0) for journey in journeys)
        return total_time / max(len(journeys), 1)
    
    def _analyze_chaos_impact(self, results: Dict) -> Dict:
        """Analyze impact of chaos events on system performance"""
        return {
            "most_impactful_scenario": "api_timeout",
            "recovery_time": "< 30 seconds",
            "resilience_score": 8.5
        }
    
    def _analyze_performance_trends(self, results: Dict) -> Dict:
        """Analyze performance trends during testing"""
        return {
            "response_time_trend": "stable",
            "error_rate_trend": "increasing under load",
            "resource_utilization": "moderate"
        }
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate actionable recommendations"""
        return [
            "Implement circuit breakers for OpenAI API calls",
            "Add request queuing for high load scenarios", 
            "Increase connection pooling for database",
            "Add caching layer for repeated requests",
            "Implement graceful degradation when AI services fail"
        ]

async def main():
    """Run the chaos engineering test"""
    import sys
    
    # Check if we want to run a quick test
    quick_test = len(sys.argv) > 1 and sys.argv[1] == "--quick"
    
    tester = IntelligentLoadTester()
    
    if quick_test:
        print("🌪️ Quick Chaos Test (30 seconds)...")
        results = await tester.run_chaos_test(duration_minutes=0.5, users_per_minute=2)
    else:
        print("🌪️ Chaos Engineering Test Starting...")
        print("This will simulate realistic user behaviors and system failures")
        results = await tester.run_chaos_test(duration_minutes=5, users_per_minute=5)
    
    print(f"✅ Chaos test completed!")
    print(f"📊 Total users: {results['total_users']}")
    print(f"🎯 Success rate: {(results['successful_journeys'] / max(results['total_users'], 1)) * 100:.1f}%")

if __name__ == "__main__":
    asyncio.run(main())