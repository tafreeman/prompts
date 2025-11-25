#!/usr/bin/env python3
"""
Main test execution script for the prompt testing framework
"""

import asyncio
import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional
import logging
from datetime import datetime

# Add framework to path
sys.path.insert(0, str(Path(__file__).parent))

from framework.core.test_runner import PromptTestRunner, TestType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'test_run_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)
logger = logging.getLogger(__name__)


class TestOrchestrator:
    """Orchestrate test execution across multiple suites"""
    
    def __init__(self):
        self.runner = PromptTestRunner()
        self.results = {}
    
    async def run_suite(self, suite_path: str, **kwargs) -> dict:
        """Run a single test suite"""
        logger.info(f"Loading test suite: {suite_path}")
        self.runner.load_test_suite(suite_path)
        
        suite_name = Path(suite_path).stem
        results = await self.runner.run_test_suite(
            suite_name,
            **kwargs
        )
        
        self.results[suite_name] = results
        return results
    
    async def run_multiple_suites(self, suite_paths: List[str], **kwargs) -> dict:
        """Run multiple test suites"""
        all_results = {}
        
        for suite_path in suite_paths:
            try:
                results = await self.run_suite(suite_path, **kwargs)
                all_results[Path(suite_path).stem] = results
            except Exception as e:
                logger.error(f"Failed to run suite {suite_path}: {e}")
                all_results[Path(suite_path).stem] = {
                    "error": str(e),
                    "status": "failed"
                }
        
        return all_results
    
    def print_summary(self, results: dict):
        """Print test execution summary"""
        print("\n" + "=" * 80)
        print("TEST EXECUTION SUMMARY")
        print("=" * 80)
        
        total_tests = 0
        total_passed = 0
        total_failed = 0
        total_errors = 0
        
        for suite_name, suite_results in results.items():
            if "error" in suite_results:
                print(f"\n❌ Suite: {suite_name} - FAILED TO RUN")
                print(f"   Error: {suite_results['error']}")
                continue
            
            summary = suite_results.get("summary", {})
            total_tests += summary.get("total_tests", 0)
            total_passed += summary.get("passed", 0)
            total_failed += summary.get("failed", 0)
            total_errors += summary.get("errors", 0)
            
            print(f"\n📊 Suite: {suite_name}")
            print(f"   Total Tests: {summary.get('total_tests', 0)}")
            print(f"   ✅ Passed: {summary.get('passed', 0)}")
            print(f"   ❌ Failed: {summary.get('failed', 0)}")
            print(f"   💥 Errors: {summary.get('errors', 0)}")
            print(f"   ⏭️  Skipped: {summary.get('skipped', 0)}")
            print(f"   ⏱️  Timeouts: {summary.get('timeouts', 0)}")
            print(f"   Pass Rate: {summary.get('pass_rate', '0.00%')}")
            print(f"   Execution Time: {summary.get('execution_time', '0.00s')}")
            print(f"   Total Cost: {summary.get('total_cost', '$0.0000')}")
        
        print("\n" + "-" * 80)
        print("OVERALL SUMMARY")
        print("-" * 80)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Total Passed: {total_passed}")
        print(f"❌ Total Failed: {total_failed}")
        print(f"💥 Total Errors: {total_errors}")
        
        if total_tests > 0:
            overall_pass_rate = (total_passed / total_tests) * 100
            print(f"Overall Pass Rate: {overall_pass_rate:.2f}%")
            
            if overall_pass_rate >= 95:
                print("\n🎉 EXCELLENT - All tests are passing!")
            elif overall_pass_rate >= 80:
                print("\n✨ GOOD - Most tests are passing")
            elif overall_pass_rate >= 60:
                print("\n⚠️  WARNING - Several tests are failing")
            else:
                print("\n🚨 CRITICAL - Many tests are failing")
        
        print("=" * 80 + "\n")
    
    def save_results(self, output_path: str):
        """Save test results to file"""
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        logger.info(f"Results saved to {output_path}")


async def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Run prompt testing framework"
    )
    
    parser.add_argument(
        "suites",
        nargs="*",
        default=["test_suites/example_test_suite.yaml"],
        help="Test suite files to run"
    )
    
    parser.add_argument(
        "--parallel",
        action="store_true",
        default=True,
        help="Run tests in parallel"
    )
    
    parser.add_argument(
        "--max-workers",
        type=int,
        default=5,
        help="Maximum parallel workers"
    )
    
    parser.add_argument(
        "--filter-tags",
        nargs="+",
        help="Filter tests by tags"
    )
    
    parser.add_argument(
        "--filter-type",
        choices=["unit", "integration", "regression", "performance", "safety", "quality", "benchmark"],
        help="Filter tests by type"
    )
    
    parser.add_argument(
        "--output",
        default=f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        help="Output file for results"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run - don't execute tests"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Print header
    print("\n" + "=" * 80)
    print("PROMPT TESTING FRAMEWORK")
    print("=" * 80)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Test Suites: {', '.join(args.suites)}")
    print(f"Parallel Execution: {args.parallel}")
    print(f"Max Workers: {args.max_workers}")
    
    if args.filter_tags:
        print(f"Filter Tags: {', '.join(args.filter_tags)}")
    if args.filter_type:
        print(f"Filter Type: {args.filter_type}")
    
    print("=" * 80 + "\n")
    
    if args.dry_run:
        print("DRY RUN MODE - Tests will not be executed")
        return
    
    # Run tests
    orchestrator = TestOrchestrator()
    
    try:
        # Prepare kwargs
        kwargs = {
            "parallel": args.parallel,
            "max_workers": args.max_workers
        }
        
        if args.filter_tags:
            kwargs["filter_tags"] = args.filter_tags
        
        # Run suites
        if len(args.suites) == 1:
            results = await orchestrator.run_suite(args.suites[0], **kwargs)
            orchestrator.results = {Path(args.suites[0]).stem: results}
        else:
            results = await orchestrator.run_multiple_suites(args.suites, **kwargs)
            orchestrator.results = results
        
        # Print summary
        orchestrator.print_summary(orchestrator.results)
        
        # Save results
        orchestrator.save_results(args.output)
        
        # Determine exit code
        total_failed = sum(
            r.get("summary", {}).get("failed", 0) + r.get("summary", {}).get("errors", 0)
            for r in orchestrator.results.values()
            if "summary" in r
        )
        
        sys.exit(0 if total_failed == 0 else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Test execution failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())