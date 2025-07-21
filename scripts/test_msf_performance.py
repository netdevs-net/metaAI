#!/usr/bin/env python3
"""
Performance Comparison: Basic vs Optimized Metasploit RPC Client

This script demonstrates the performance difference between the basic pymetasploit3
client and our optimized MSFClient wrapper.
"""

import os
import time
import statistics
from typing import Dict, List, Tuple, Any
from pymetasploit3.msfrpc import MsfRpcClient

# Import our optimized client
from scripts.msf_client import msf as optimized_client

def setup_basic_client() -> MsfRpcClient:
    """Set up and return a basic pymetasploit3 client."""
    return MsfRpcClient(
        os.getenv('MSGRPC_PASS', 'Meta2025SecurePass'),
        server=os.getenv('MSF_HOST', 'metasploit'),
        port=int(os.getenv('MSF_PORT', '55552')),
        username=os.getenv('MSF_USER', 'msf'),
        ssl=os.getenv('MSF_SSL', 'false').lower() == 'true'
    )

def time_function(func, *args, **kwargs) -> Tuple[float, Any]:
    """Time a function call and return the duration and result."""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    return (end - start) * 1000, result  # Convert to milliseconds

def test_module_listing(basic_client: MsfRpcClient, num_runs: int = 5) -> Dict[str, List[float]]:
    """Test performance of listing modules."""
    times = {'basic': [], 'optimized': []}
    
    # Test basic client
    for _ in range(num_runs):
        duration, _ = time_function(lambda: basic_client.modules.exploits[:10])
        times['basic'].append(duration)
        time.sleep(0.1)  # Small delay between tests
    
    # Test optimized client
    for _ in range(num_runs):
        duration, _ = time_function(lambda: optimized_client.client.modules.exploits[:10])
        times['optimized'].append(duration)
        time.sleep(0.1)
    
    return times

def test_module_info(basic_client: MsfRpcClient, module_name: str, num_runs: int = 5) -> Dict[str, List[float]]:
    """Test performance of getting module information."""
    times = {'basic': [], 'optimized': []}
    
    # Test basic client
    for _ in range(num_runs):
        duration, _ = time_function(
            lambda: basic_client.modules.use('exploit', module_name)
        )
        times['basic'].append(duration)
        time.sleep(0.1)
    
    # Test optimized client (first run will be slower due to cache miss)
    for _ in range(num_runs):
        duration, _ = time_function(
            lambda: optimized_client.get_module_info('exploit', module_name)
        )
        times['optimized'].append(duration)
        time.sleep(0.1)
    
    return times

def test_search(basic_client: MsfRpcClient, query: str, num_runs: int = 5) -> Dict[str, List[float]]:
    """Test performance of searching modules."""
    times = {'basic': [], 'optimized': []}
    
    # Test basic client
    for _ in range(num_runs):
        duration, _ = time_function(
            lambda: basic_client.modules.search(query)
        )
        times['basic'].append(duration)
        time.sleep(0.1)
    
    # Test optimized client
    for _ in range(num_runs):
        duration, _ = time_function(
            lambda: optimized_client.search_modules(query)
        )
        times['optimized'].append(duration)
        time.sleep(0.1)
    
    return times

def print_results(test_name: str, results: Dict[str, List[float]]):
    """Print formatted test results."""
    print(f"\n{test_name} Test Results:")
    print("-" * 50)
    
    basic_avg = statistics.mean(results['basic'])
    optimized_avg = statistics.mean(results['optimized'])
    improvement = ((basic_avg - optimized_avg) / basic_avg) * 100
    
    print(f"Basic Client: {basic_avg:.2f}ms (avg)")
    print(f"Optimized Client: {optimized_avg:.2f}ms (avg)")
    print(f"Improvement: {improvement:+.2f}%")
    
    if len(results['basic']) > 1 and len(results['optimized']) > 1:
        basic_std = statistics.stdev(results['basic'])
        optimized_std = statistics.stdev(results['optimized'])
        print(f"\nBasic Std Dev: {basic_std:.2f}ms")
        print(f"Optimized Std Dev: {optimized_std:.2f}ms")
    
    print("-" * 50)

def main():
    """Run performance tests and display results."""
    print("Performance Comparison: Basic vs Optimized Metasploit RPC Client")
    print("=" * 70)
    
    try:
        print("Setting up clients...")
        basic_client = setup_basic_client()
        
        # Test 1: Module Listing
        print("\nRunning Module Listing Test...")
        results = test_module_listing(basic_client)
        print_results("Module Listing", results)
        
        # Test 2: Module Information (first run will be slower due to cache miss)
        print("\nRunning Module Information Test (First Run)...")
        module_name = 'multi/handler'  # Common module for testing
        results = test_module_info(basic_client, module_name, num_runs=1)
        print_results("Module Info (First Run)", results)
        
        # Test 3: Module Information (cached)
        print("\nRunning Module Information Test (Cached)...")
        results = test_module_info(basic_client, module_name)
        print_results("Module Info (Cached)", results)
        
        # Test 4: Search
        print("\nRunning Search Test...")
        results = test_search(basic_client, 'ssh')
        print_results("Module Search", results)
        
    except Exception as e:
        print(f"\nError during testing: {e}")
        raise
    finally:
        try:
            basic_client.logout()
        except:
            pass

if __name__ == "__main__":
    main()
