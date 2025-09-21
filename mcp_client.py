import aiohttp
import asyncio
from typing import List
import json

class MCPClient:
    def __init__(self):
        self.base_url = "http://localhost:3000"
        self.initialized = False
        
    async def initialize(self):
        """Initialize MCP connection - simple version"""
        try:
            # Test connection to MCP server
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health", timeout=5) as response:
                    if response.status == 200:
                        self.initialized = True
                        print("✅ MCP Client connected successfully")
                    else:
                        print("⚠️ MCP Server not responding properly")
                        self.initialized = False
        except Exception as e:
            print(f"❌ MCP Connection failed: {e}")
            self.initialized = False

    async def search(self, query: str, max_results: int = 3) -> List[str]:
        """Perform search using MCP protocol - simplified version"""
        if not self.initialized:
            await self.initialize()
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.base_url}/call',
                    json={
                        "function": "search",
                        "arguments": {
                            "query": f"mathematics {query}",
                            "max_results": max_results,
                            "include_domains": ["khanacademy.org", "mathsisfun.com", "wolfram.com"]
                        }
                    },
                    timeout=10
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        if result and 'content' in result:
                            formatted_results = []
                            for item in result['content']:
                                if isinstance(item, dict):
                                    title = item.get('title', 'No title')
                                    content = item.get('content', 'No content')
                                    formatted_results.append(f"{title}: {content[:150]}...")
                                else:
                                    formatted_results.append(f"{item}")
                            
                            return formatted_results
                    
                    return [f"No relevant web results found for '{query}'"]
                    
        except aiohttp.ClientError as e:
            return [f"MCP connection failed: {str(e)}"]
        except asyncio.TimeoutError:
            return ["MCP search timeout: Server took too long to respond"]
        except Exception as e:
            return [f"MCP search error: {str(e)}"]

    async def close(self):
        """Cleanup MCP connection"""
        pass

# Global MCP client instance
mcp_client_instance = MCPClient()