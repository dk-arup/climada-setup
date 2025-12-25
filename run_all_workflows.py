#!/usr/bin/env python3
"""
Run All CLIMADA Workflows

This script runs all example workflows in sequence.
Useful for testing and demonstration purposes.

Author: CLIMADA Setup Project
Date: 2025-12-25
"""

import sys
import subprocess
from pathlib import Path
import time


def run_workflow(script_path):
    """
    Run a workflow script and report results.
    
    Args:
        script_path: Path to the workflow script
        
    Returns:
        bool: True if successful, False otherwise
    """
    script_name = script_path.name
    print("\n" + "=" * 70)
    print(f"Running: {script_name}")
    print("=" * 70)
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=script_path.parent,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout per script
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✓ SUCCESS ({elapsed:.1f}s)")
            print("\nOutput:")
            print(result.stdout)
            return True
        else:
            print(f"✗ FAILED ({elapsed:.1f}s)")
            print("\nError output:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        print(f"✗ TIMEOUT ({elapsed:.1f}s)")
        return False
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"✗ ERROR ({elapsed:.1f}s): {e}")
        return False


def main():
    """Run all workflows."""
    print("=" * 70)
    print("CLIMADA Workflows Runner")
    print("=" * 70)
    print("\nThis script will run all example workflows in sequence.")
    print("Note: Workflows require CLIMADA to be installed.")
    
    # Check if CLIMADA is available
    try:
        import climada
        print(f"\n✓ CLIMADA version {climada.__version__} detected")
    except ImportError:
        print("\n⚠ WARNING: CLIMADA not installed")
        print("Workflows will demonstrate error handling but won't produce results.")
        print("\nTo install CLIMADA:")
        print("  mamba env create -f environment.yml")
        print("  mamba activate climada_env")
        
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
    
    # Find all workflow scripts
    workflows_dir = Path(__file__).parent / 'workflows'
    workflows = sorted(workflows_dir.glob('*.py'))
    
    if not workflows:
        print("\nNo workflow scripts found in workflows/ directory.")
        return
    
    print(f"\nFound {len(workflows)} workflow scripts:")
    for wf in workflows:
        print(f"  - {wf.name}")
    
    # Ask for confirmation
    print(f"\nThis may take several minutes to complete.")
    response = input("Continue? (y/n): ")
    if response.lower() != 'y':
        print("Aborted.")
        return
    
    # Run workflows
    results = {}
    start_time = time.time()
    
    for workflow in workflows:
        success = run_workflow(workflow)
        results[workflow.name] = success
    
    total_time = time.time() - start_time
    
    # Summary
    print("\n" + "=" * 70)
    print("WORKFLOW EXECUTION SUMMARY")
    print("=" * 70)
    
    successful = sum(1 for v in results.values() if v)
    failed = len(results) - successful
    
    for workflow_name, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{status}: {workflow_name}")
    
    print(f"\nTotal: {len(results)} workflows")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total time: {total_time:.1f}s ({total_time/60:.1f}m)")
    
    if failed > 0:
        print("\n⚠ Some workflows failed. Check the output above for details.")
        sys.exit(1)
    else:
        print("\n✓ All workflows completed successfully!")
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
