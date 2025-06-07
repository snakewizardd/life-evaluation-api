#!/usr/bin/env python3
"""
Simple chaos test to verify the system works without overwhelming it
"""

import asyncio
import aiohttp
import time
import random

async def test_single_user_journey():
    """Test a single user journey"""
    async with aiohttp.ClientSession() as session:
        try:
            # Test first question generation
            start_time = time.time()
            async with session.post(
                "http://localhost:8000/api/generate-first-question",
                json={"prompt": "get better at coding", "model": "gpt-4.1-nano"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    question = data.get("question", "")
                    print(f"✅ Generated question: {question[:50]}...")
                    
                    # Test answer analysis
                    async with session.post(
                        "http://localhost:8000/api/analyze-answer-bro",
                        json={
                            "prompt": "get better at coding",
                            "questions": [question],
                            "answers": ["I watch tutorials but don't practice"],
                            "current_answer": "I watch tutorials but don't practice",
                            "model": "gpt-4.1-nano"
                        }
                    ) as analysis_response:
                        if analysis_response.status == 200:
                            analysis_data = await analysis_response.json()
                            analysis = analysis_data.get("analysis", "")
                            print(f"✅ Got analysis: {analysis[:50]}...")
                            
                            elapsed = time.time() - start_time
                            print(f"⏱️  Journey time: {elapsed:.2f}s")
                            return True
                        else:
                            print(f"❌ Analysis failed: {analysis_response.status}")
                            return False
                else:
                    print(f"❌ Question generation failed: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Journey failed: {e}")
            return False

async def simple_load_test(concurrent_users=3, duration_seconds=10):
    """Run a simple load test"""
    print(f"🧪 Running simple load test: {concurrent_users} users for {duration_seconds}s")
    
    start_time = time.time()
    successful_journeys = 0
    failed_journeys = 0
    
    while time.time() - start_time < duration_seconds:
        # Launch concurrent user journeys
        tasks = []
        for _ in range(concurrent_users):
            tasks.append(test_single_user_journey())
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if result is True:
                successful_journeys += 1
            else:
                failed_journeys += 1
        
        # Small delay between batches
        await asyncio.sleep(2)
    
    total_users = successful_journeys + failed_journeys
    success_rate = (successful_journeys / total_users * 100) if total_users > 0 else 0
    
    print(f"📊 Results:")
    print(f"   Total users: {total_users}")
    print(f"   Successful: {successful_journeys}")
    print(f"   Failed: {failed_journeys}")
    print(f"   Success rate: {success_rate:.1f}%")
    
    return success_rate > 70  # 70% success rate threshold

async def main():
    print("🔥 Simple Chaos Test - Verifying system handles moderate load")
    success = await simple_load_test()
    
    if success:
        print("✅ System passed simple load test!")
    else:
        print("❌ System failed under moderate load")

if __name__ == "__main__":
    asyncio.run(main())