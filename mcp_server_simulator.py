#!/usr/bin/env python3
"""
Simple MCP server simulator for testing
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="MCP Server Simulator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CallRequest(BaseModel):
    function: str
    arguments: dict

@app.post("/call")
async def call_function(request: CallRequest):
    """Simulate MCP server call"""
    if request.function == "search":
        query = request.arguments.get("query", "")
        max_results = request.arguments.get("max_results", 3)
        
        # Simulate search results
        simulated_results = [
            {
                "title": f"Math Solution for: {query}",
                "content": f"This is a simulated search result for the mathematical query: {query}. In a real implementation, this would come from actual web search results from educational math websites.",
                "url": "https://example.com/math-solution"
            },
            {
                "title": "Related Mathematical Concept",
                "content": f"Related information about {query}. Mathematical concepts often build upon each other, so understanding fundamentals is important.",
                "url": "https://example.com/math-concepts"
            }
        ]
        
        return {
            "content": simulated_results[:max_results],
            "isError": False
        }
    
    return {"error": f"Unknown function: {request.function}"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "MCP Server Simulator"}

if __name__ == "__main__":
    print("🚀 Starting MCP Server Simulator on http://localhost:3001")  
    uvicorn.run(app, host="0.0.0.0", port=3001)  