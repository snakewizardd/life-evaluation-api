#!/usr/bin/env python3
"""
🎨 Psychedelic UI Visual Regression Testing
Advanced visual testing for the cosmic truth scanner interface
"""

import asyncio
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import base64

from playwright.async_api import async_playwright, Page, Browser
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim

@dataclass
class VisualTest:
    name: str
    description: str
    url_path: str
    viewport: Tuple[int, int]
    interactions: List[Dict[str, Any]]
    expected_elements: List[str]
    animation_checks: List[str]
    performance_thresholds: Dict[str, float]

@dataclass
class VisualTestResult:
    test_name: str
    timestamp: datetime
    passed: bool
    screenshot_path: str
    performance_metrics: Dict[str, float]
    visual_diff_score: float
    missing_elements: List[str]
    animation_failures: List[str]
    console_errors: List[str]
    accessibility_issues: List[str]
    recommendations: List[str]

class PsychedelicUITester:
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.test_results_dir = Path("/tmp/visual_tests")
        self.test_results_dir.mkdir(exist_ok=True)
        self.baseline_dir = self.test_results_dir / "baselines"
        self.baseline_dir.mkdir(exist_ok=True)
        self.results_dir = self.test_results_dir / "results"
        self.results_dir.mkdir(exist_ok=True)
        
        self.visual_tests = self._define_visual_tests()
    
    def _define_visual_tests(self) -> List[VisualTest]:
        """Define comprehensive visual tests for the psychedelic UI"""
        return [
            VisualTest(
                name="cosmic_landing_page",
                description="Test the main landing page with cosmic animations",
                url_path="/",
                viewport=(1920, 1080),
                interactions=[
                    {"action": "wait", "selector": ".animate-bounce", "timeout": 3000},
                    {"action": "hover", "selector": "input[type='text']"},
                    {"action": "type", "selector": "input[type='text']", "text": "get jacked"},
                    {"action": "screenshot", "name": "input_filled"}
                ],
                expected_elements=[
                    ".text-9xl.mb-8.animate-bounce",  # Main emoji
                    ".bg-gradient-to-r.from-pink-400",  # Gradient text
                    "input[placeholder*='get a girlfriend']",  # Input field
                    ".bg-gradient-to-r.from-pink-600",  # Start button
                    ".absolute.inset-0",  # Background animations
                ],
                animation_checks=[
                    "cosmic_stars_animation",
                    "floating_geometric_shapes", 
                    "gradient_pulse_effects",
                    "hover_scale_transforms"
                ],
                performance_thresholds={
                    "first_contentful_paint": 2000,
                    "largest_contentful_paint": 3000,
                    "cumulative_layout_shift": 0.1,
                    "first_input_delay": 100
                }
            ),
            VisualTest(
                name="questioning_phase_visuals",
                description="Test the questioning phase with all visual effects",
                url_path="/",
                viewport=(1920, 1080),
                interactions=[
                    {"action": "type", "selector": "input[type='text']", "text": "become a millionaire"},
                    {"action": "click", "selector": "button[class*='bg-gradient-to-r']"},
                    {"action": "wait", "timeout": 5000},  # Wait for question generation
                    {"action": "type", "selector": "textarea", "text": "I spend most of my time watching get-rich-quick videos instead of building skills"},
                    {"action": "click", "selector": "button[class*='LAUNCH INTO TRUTH SPACE']"},
                    {"action": "wait", "timeout": 3000},
                    {"action": "screenshot", "name": "questioning_with_effects"}
                ],
                expected_elements=[
                    ".bg-gradient-to-br.from-slate-900",  # Background
                    "canvas",  # Cosmic canvas
                    ".text-6xl.mb-4.animate-bounce",  # Question emoji
                    ".w-40.h-40.rounded-full",  # Question worlds
                    ".animate-pulse",  # Pulsing elements
                ],
                animation_checks=[
                    "truth_crystals_generation",
                    "particle_galaxy_movement",
                    "morphing_sculpture_animation",
                    "world_floating_animation"
                ],
                performance_thresholds={
                    "animation_frame_rate": 30,
                    "canvas_render_time": 16.67,  # 60fps target
                    "interaction_response": 200
                }
            ),
            VisualTest(
                name="cosmic_effects_stress_test",
                description="Stress test all visual effects simultaneously",
                url_path="/",
                viewport=(1920, 1080),
                interactions=[
                    {"action": "type", "selector": "input[type='text']", "text": "test all effects"},
                    {"action": "click", "selector": "button[class*='bg-gradient-to-r']"},
                    {"action": "wait", "timeout": 5000},
                    # Rapid-fire interactions to trigger multiple effects
                    {"action": "type", "selector": "textarea", "text": "This should trigger contradictions and lightning"},
                    {"action": "click", "selector": "button[class*='LAUNCH']"},
                    {"action": "wait", "timeout": 2000},
                    {"action": "type", "selector": "textarea", "text": "More BS to trigger effects"},
                    {"action": "click", "selector": "button[class*='LAUNCH']"},
                    {"action": "wait", "timeout": 2000},
                    {"action": "screenshot", "name": "effects_stress_test"}
                ],
                expected_elements=[
                    "svg path[stroke='#ff4444']",  # Lightning effects
                    ".absolute.pointer-events-none.z-40",  # Truth crystals
                    ".absolute.pointer-events-none.z-20",  # Heat map
                    ".w-32.h-32",  # Morphing sculpture
                ],
                animation_checks=[
                    "multiple_truth_crystals",
                    "contradiction_lightning_bolts",
                    "emotional_heat_expansion",
                    "sculpture_morphing_rapid"
                ],
                performance_thresholds={
                    "memory_usage_mb": 100,
                    "cpu_usage_percent": 50,
                    "frame_drops": 5
                }
            ),
            VisualTest(
                name="responsive_mobile_design",
                description="Test responsive design on mobile viewports",
                url_path="/",
                viewport=(375, 667),  # iPhone SE
                interactions=[
                    {"action": "screenshot", "name": "mobile_landing"},
                    {"action": "type", "selector": "input[type='text']", "text": "mobile test"},
                    {"action": "click", "selector": "button"},
                    {"action": "wait", "timeout": 3000},
                    {"action": "screenshot", "name": "mobile_questioning"}
                ],
                expected_elements=[
                    ".min-h-screen",  # Full screen usage
                    ".max-w-4xl.mx-auto",  # Responsive container
                    ".text-center",  # Centered content
                ],
                animation_checks=[
                    "mobile_animation_performance",
                    "touch_interaction_feedback"
                ],
                performance_thresholds={
                    "mobile_page_load": 3000,
                    "touch_response": 150
                }
            ),
            VisualTest(
                name="dark_mode_compatibility",
                description="Test visual consistency in different lighting conditions",
                url_path="/",
                viewport=(1920, 1080),
                interactions=[
                    {"action": "emulate_media", "features": [{"name": "prefers-color-scheme", "value": "dark"}]},
                    {"action": "screenshot", "name": "dark_mode"},
                    {"action": "emulate_media", "features": [{"name": "prefers-color-scheme", "value": "light"}]},
                    {"action": "screenshot", "name": "light_mode"}
                ],
                expected_elements=[
                    ".bg-gradient-to-br",  # Background gradients
                    ".text-white",  # White text
                    ".border-purple-500",  # Purple borders
                ],
                animation_checks=[
                    "gradient_visibility_dark",
                    "text_contrast_ratios"
                ],
                performance_thresholds={
                    "contrast_ratio": 4.5  # WCAG AA standard
                }
            )
        ]
    
    async def capture_baseline_screenshots(self, browser: Browser):
        """Capture baseline screenshots for visual regression testing"""
        print("📸 Capturing baseline screenshots...")
        
        for test in self.visual_tests:
            page = await browser.new_page()
            await page.set_viewport_size({"width": test.viewport[0], "height": test.viewport[1]})
            
            try:
                await page.goto(f"{self.base_url}{test.url_path}")
                await page.wait_for_load_state("networkidle")
                
                # Execute interactions
                for interaction in test.interactions:
                    await self._execute_interaction(page, interaction)
                
                # Take final screenshot
                screenshot_path = self.baseline_dir / f"{test.name}_baseline.png"
                await page.screenshot(path=str(screenshot_path), full_page=True)
                print(f"✅ Baseline captured: {test.name}")
                
            except Exception as e:
                print(f"❌ Failed to capture baseline for {test.name}: {e}")
            finally:
                await page.close()
    
    async def _execute_interaction(self, page: Page, interaction: Dict[str, Any]):
        """Execute a single interaction on the page"""
        action = interaction["action"]
        
        if action == "wait":
            if "selector" in interaction:
                await page.wait_for_selector(interaction["selector"], timeout=interaction.get("timeout", 5000))
            else:
                await page.wait_for_timeout(interaction.get("timeout", 1000))
        
        elif action == "click":
            await page.click(interaction["selector"])
        
        elif action == "type":
            await page.fill(interaction["selector"], interaction["text"])
        
        elif action == "hover":
            await page.hover(interaction["selector"])
        
        elif action == "screenshot":
            screenshot_path = self.results_dir / f"{interaction['name']}.png"
            await page.screenshot(path=str(screenshot_path))
        
        elif action == "emulate_media":
            await page.emulate_media(features=interaction["features"])
    
    async def run_visual_test(self, browser: Browser, test: VisualTest) -> VisualTestResult:
        """Run a single visual test and return results"""
        print(f"🧪 Running visual test: {test.name}")
        
        page = await browser.new_page()
        await page.set_viewport_size({"width": test.viewport[0], "height": test.viewport[1]})
        
        # Collect console errors
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        
        result = VisualTestResult(
            test_name=test.name,
            timestamp=datetime.now(),
            passed=True,
            screenshot_path="",
            performance_metrics={},
            visual_diff_score=0.0,
            missing_elements=[],
            animation_failures=[],
            console_errors=[],
            accessibility_issues=[],
            recommendations=[]
        )
        
        try:
            # Navigate and measure performance
            start_time = time.time()
            await page.goto(f"{self.base_url}{test.url_path}")
            await page.wait_for_load_state("networkidle")
            load_time = time.time() - start_time
            
            result.performance_metrics["page_load_time"] = load_time * 1000
            
            # Check for expected elements
            for element in test.expected_elements:
                try:
                    await page.wait_for_selector(element, timeout=5000)
                except:
                    result.missing_elements.append(element)
                    result.passed = False
            
            # Execute interactions
            for interaction in test.interactions:
                await self._execute_interaction(page, interaction)
                await page.wait_for_timeout(500)  # Small delay between interactions
            
            # Capture screenshot for visual comparison
            screenshot_path = self.results_dir / f"{test.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            await page.screenshot(path=str(screenshot_path), full_page=True)
            result.screenshot_path = str(screenshot_path)
            
            # Compare with baseline if exists
            baseline_path = self.baseline_dir / f"{test.name}_baseline.png"
            if baseline_path.exists():
                result.visual_diff_score = self._compare_screenshots(str(baseline_path), str(screenshot_path))
                if result.visual_diff_score > 0.05:  # 5% threshold
                    result.passed = False
                    result.recommendations.append(f"Visual difference detected: {result.visual_diff_score:.3f}")
            
            # Test animations
            for animation in test.animation_checks:
                animation_result = await self._test_animation(page, animation)
                if not animation_result:
                    result.animation_failures.append(animation)
                    result.passed = False
            
            # Performance checks
            await self._check_performance_metrics(page, test, result)
            
            # Accessibility checks
            await self._check_accessibility(page, result)
            
            # Console errors
            result.console_errors = console_errors
            if console_errors:
                result.passed = False
                result.recommendations.append("Console errors detected")
            
        except Exception as e:
            result.passed = False
            result.recommendations.append(f"Test execution failed: {str(e)}")
        
        finally:
            await page.close()
        
        return result
    
    def _compare_screenshots(self, baseline_path: str, current_path: str) -> float:
        """Compare two screenshots and return difference score"""
        try:
            # Load images
            baseline = cv2.imread(baseline_path)
            current = cv2.imread(current_path)
            
            if baseline is None or current is None:
                return 1.0  # Max difference if can't load
            
            # Resize to same dimensions if needed
            if baseline.shape != current.shape:
                current = cv2.resize(current, (baseline.shape[1], baseline.shape[0]))
            
            # Convert to grayscale
            baseline_gray = cv2.cvtColor(baseline, cv2.COLOR_BGR2GRAY)
            current_gray = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
            
            # Calculate SSIM
            ssim_score, _ = ssim(baseline_gray, current_gray, full=True)
            
            # Return difference (1 - similarity)
            return 1.0 - ssim_score
            
        except Exception as e:
            print(f"Screenshot comparison failed: {e}")
            return 1.0
    
    async def _test_animation(self, page: Page, animation_name: str) -> bool:
        """Test specific animation functionality"""
        try:
            if animation_name == "cosmic_stars_animation":
                # Check if stars are animating
                star_elements = await page.query_selector_all(".animate-pulse")
                return len(star_elements) > 50  # Should have many animated stars
            
            elif animation_name == "floating_geometric_shapes":
                # Check for floating shapes
                shapes = await page.query_selector_all("[style*='animation: float']")
                return len(shapes) > 10
            
            elif animation_name == "truth_crystals_generation":
                # Check if crystals appear after interaction
                crystals = await page.query_selector_all(".absolute.pointer-events-none.z-40")
                return len(crystals) > 0
            
            elif animation_name == "particle_galaxy_movement":
                # Check for particle animations
                particles = await page.query_selector_all(".animate-pulse, .animate-spin")
                return len(particles) > 5
            
            # Add more specific animation tests as needed
            return True
            
        except Exception as e:
            print(f"Animation test failed for {animation_name}: {e}")
            return False
    
    async def _check_performance_metrics(self, page: Page, test: VisualTest, result: VisualTestResult):
        """Check performance metrics against thresholds"""
        try:
            # Get Web Vitals using JavaScript
            vitals = await page.evaluate("""
                () => {
                    return new Promise((resolve) => {
                        // Simple performance measurement
                        const timing = performance.timing;
                        resolve({
                            load_time: timing.loadEventEnd - timing.navigationStart,
                            dom_ready: timing.domContentLoadedEventEnd - timing.navigationStart,
                            first_paint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime || 0
                        });
                    });
                }
            """)
            
            result.performance_metrics.update(vitals)
            
            # Check against thresholds
            for metric, threshold in test.performance_thresholds.items():
                if metric in result.performance_metrics:
                    if result.performance_metrics[metric] > threshold:
                        result.passed = False
                        result.recommendations.append(f"Performance threshold exceeded: {metric}")
        
        except Exception as e:
            print(f"Performance check failed: {e}")
    
    async def _check_accessibility(self, page: Page, result: VisualTestResult):
        """Check basic accessibility requirements"""
        try:
            # Check for alt texts on images
            images_without_alt = await page.evaluate("""
                () => {
                    const images = document.querySelectorAll('img');
                    return Array.from(images).filter(img => !img.alt).length;
                }
            """)
            
            if images_without_alt > 0:
                result.accessibility_issues.append(f"{images_without_alt} images missing alt text")
            
            # Check color contrast (simplified)
            low_contrast_elements = await page.evaluate("""
                () => {
                    // Simplified contrast check
                    const elements = document.querySelectorAll('*');
                    let lowContrastCount = 0;
                    
                    Array.from(elements).forEach(el => {
                        const style = window.getComputedStyle(el);
                        const color = style.color;
                        const bgColor = style.backgroundColor;
                        
                        // Basic check for very low contrast combinations
                        if (color && bgColor && color === bgColor) {
                            lowContrastCount++;
                        }
                    });
                    
                    return lowContrastCount;
                }
            """)
            
            if low_contrast_elements > 0:
                result.accessibility_issues.append(f"Potential low contrast elements: {low_contrast_elements}")
        
        except Exception as e:
            print(f"Accessibility check failed: {e}")
    
    async def run_comprehensive_visual_tests(self) -> Dict[str, Any]:
        """Run all visual tests and generate comprehensive report"""
        print("🎨 Starting comprehensive visual regression testing...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            # Capture baselines if they don't exist
            if not any(self.baseline_dir.glob("*_baseline.png")):
                await self.capture_baseline_screenshots(browser)
            
            # Run all tests
            results = []
            for test in self.visual_tests:
                result = await self.run_visual_test(browser, test)
                results.append(result)
                
                # Brief pause between tests
                await asyncio.sleep(2)
            
            await browser.close()
        
        # Generate report
        report = self._generate_visual_report(results)
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.test_results_dir / f"visual_test_report_{timestamp}.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"📊 Visual test report saved: {report_path}")
        return report
    
    def _generate_visual_report(self, results: List[VisualTestResult]) -> Dict[str, Any]:
        """Generate comprehensive visual test report"""
        passed_tests = [r for r in results if r.passed]
        failed_tests = [r for r in results if not r.passed]
        
        report = {
            "summary": {
                "total_tests": len(results),
                "passed": len(passed_tests),
                "failed": len(failed_tests),
                "success_rate": len(passed_tests) / len(results) * 100,
                "timestamp": datetime.now().isoformat()
            },
            "performance_analysis": {
                "avg_load_time": np.mean([r.performance_metrics.get("page_load_time", 0) for r in results]),
                "max_visual_diff": max([r.visual_diff_score for r in results]),
                "total_console_errors": sum([len(r.console_errors) for r in results])
            },
            "accessibility_summary": {
                "total_issues": sum([len(r.accessibility_issues) for r in results]),
                "tests_with_issues": len([r for r in results if r.accessibility_issues])
            },
            "animation_analysis": {
                "total_animation_failures": sum([len(r.animation_failures) for r in results]),
                "most_problematic_animations": self._get_most_failing_animations(results)
            },
            "recommendations": self._consolidate_recommendations(results),
            "detailed_results": [asdict(r) for r in results]
        }
        
        return report
    
    def _get_most_failing_animations(self, results: List[VisualTestResult]) -> List[str]:
        """Identify animations that fail most frequently"""
        animation_failures = {}
        for result in results:
            for animation in result.animation_failures:
                animation_failures[animation] = animation_failures.get(animation, 0) + 1
        
        return sorted(animation_failures.items(), key=lambda x: x[1], reverse=True)[:5]
    
    def _consolidate_recommendations(self, results: List[VisualTestResult]) -> List[str]:
        """Consolidate recommendations from all tests"""
        all_recommendations = []
        for result in results:
            all_recommendations.extend(result.recommendations)
        
        # Count frequency and return most common
        rec_counts = {}
        for rec in all_recommendations:
            rec_counts[rec] = rec_counts.get(rec, 0) + 1
        
        return sorted(rec_counts.items(), key=lambda x: x[1], reverse=True)[:10]

async def main():
    """Run visual regression testing"""
    tester = PsychedelicUITester()
    
    print("🎨 Starting Psychedelic UI Visual Regression Testing")
    report = await tester.run_comprehensive_visual_tests()
    
    print(f"\n📊 Test Summary:")
    print(f"✅ Passed: {report['summary']['passed']}")
    print(f"❌ Failed: {report['summary']['failed']}")
    print(f"🎯 Success Rate: {report['summary']['success_rate']:.1f}%")
    
    if report['summary']['failed'] > 0:
        print(f"\n⚠️  Issues found:")
        for rec, count in report['recommendations'][:5]:
            print(f"  • {rec} ({count} occurrences)")

if __name__ == "__main__":
    asyncio.run(main())