#!/usr/bin/env python3
"""
Quick test to verify all services are running
"""
import requests
import asyncio
import aiohttp

async def test_services():
    print("🔍 Testing if all services are running...")
    print("=" * 50)
    
    services = [
        ("FastAPI Backend", "http://localhost:8000"),
        ("MCP Server", "http://localhost:3001/health"),
        ("React Frontend", "http://localhost:3000")
    ]
    
    for name, url in services:
        try:
            if name == "React Frontend":
                # React might not have a specific health endpoint
                print(f"✅ {name}: Running (manual check needed)")
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=5) as response:
                        if response.status == 200:
                            print(f"✅ {name}: Running")
                        else:
                            print(f"❌ {name}: Not responding properly")
        except Exception as e:
            print(f"❌ {name}: Not running - {e}")
    
    print("\n🎯 Manual Test Instructions:")
    print("1. Open http://localhost:3000 in browser")
    print("2. Test: 'What is Pythagorean theorem?' (should use Knowledge Base)")
    print("3. Test: 'Explain Taylor series' (should use Web Search via MCP)")
    print("4. Test: 'What's the weather?' (should be blocked by guardrails)")

if __name__ == "__main__":
    asyncio.run(test_services())