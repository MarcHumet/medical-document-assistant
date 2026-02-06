#!/usr/bin/env python3
"""
Test script for the Medical Document Assistant MCP Server
"""

import json
import subprocess
import sys
import time
from pathlib import Path

def test_mcp_server():
    """Test the MCP server functionality"""
    
    print("🧪 Testing Medical Document Assistant MCP Server...")
    
    # Test 1: CLI Help
    print("\n✅ Test 1: CLI Help")
    try:
        result = subprocess.run(
            [sys.executable, "mcp_server.py", "--help"], 
            capture_output=True, 
            text=True,
            cwd=Path(__file__).parent
        )
        if result.returncode == 0:
            print("   ✅ CLI help works correctly")
        else:
            print(f"   ❌ CLI help failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ CLI help test failed: {e}")
        return False
    
    # Test 2: Server initialization
    print("\n✅ Test 2: Server Initialization")
    try:
        # Start server as subprocess and check if it initializes
        process = subprocess.Popen(
            [sys.executable, "mcp_server.py", "--verbose"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=Path(__file__).parent
        )
        
        # Give it time to initialize
        time.sleep(5)
        
        # Check if process is still running (successful initialization)
        if process.poll() is None:
            print("   ✅ Server started successfully")
            process.terminate()
            process.wait()
        else:
            stdout, stderr = process.communicate()
            print(f"   ❌ Server failed to start: {stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Server initialization test failed: {e}")
        return False
    
    # Test 3: Check configuration file
    print("\n✅ Test 3: Configuration File")
    config_file = Path("mcp_config.json")
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                print(f"   ✅ Configuration loaded: {len(config)} sections")
        except Exception as e:
            print(f"   ❌ Configuration file invalid: {e}")
            return False
    else:
        print("   ❌ Configuration file not found")
        return False
    
    # Test 4: Check MCP setup documentation  
    print("\n✅ Test 4: Documentation")
    setup_file = Path("MCP_SETUP.md")
    if setup_file.exists():
        print("   ✅ MCP setup documentation exists")
    else:
        print("   ⚠️  MCP setup documentation not found")
    
    print("\n🎉 All MCP server tests passed!")
    return True

def test_docker_services():
    """Test that Docker services are still working"""
    
    print("\n🐳 Testing Docker Services...")
    
    # Test API health
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:8000/health"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            health_data = json.loads(result.stdout)
            print(f"   ✅ API Service: {health_data.get('status', 'unknown')}")
        else:
            print("   ❌ API Service not responding")
            return False
    except Exception as e:
        print(f"   ❌ API Service test failed: {e}")
        return False
    
    # Test Streamlit frontend
    try:
        result = subprocess.run(
            ["curl", "-s", "-I", "http://localhost:8501"],
            capture_output=True, 
            text=True,
            timeout=10
        )
        if result.returncode == 0 and "200 OK" in result.stdout:
            print("   ✅ Streamlit Frontend: Running")
        else:
            print("   ❌ Streamlit Frontend not responding")
            return False
    except Exception as e:
        print(f"   ❌ Streamlit Frontend test failed: {e}")
        return False
    
    print("   🎉 Docker services are working correctly!")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Medical Document Assistant - Integration Test")
    print("=" * 60)
    
    # Activate virtual environment first
    print("🔧 Setting up environment...")
    
    all_tests_passed = True
    
    # Test MCP server
    if not test_mcp_server():
        all_tests_passed = False
    
    # Test Docker services
    if not test_docker_services():
        all_tests_passed = False
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED - Both MCP and Docker functionality working!")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED - Check output above")
        sys.exit(1)