# 🏗️ Math Agent System Architecture

This document provides a comprehensive overview of the Math Agent system architecture, including component relationships, data flow, and technical specifications.

## 📋 Table of Contents
- [System Overview](#system-overview)
- [Architecture Flowchart](#architecture-flowchart)
- [Component Details](#component-details)
- [Data Flow Sequence](#data-flow-sequence)
- [Technology Stack](#technology-stack)
- [Deployment Architecture](#deployment-architecture)

## 🎯 System Overview

The Math Agent is a sophisticated AI-powered tutoring system that combines multiple technologies to provide comprehensive mathematical assistance. The system employs intelligent routing, quality assurance, and continuous learning mechanisms.

### Key Architectural Principles
- **Modular Design**: Each component has a specific responsibility
- **Async Processing**: Non-blocking operations for better performance
- **Quality Assurance**: Multi-layer validation and human-in-the-loop feedback
- **Scalability**: Designed to handle multiple concurrent users
- **Extensibility**: Easy to add new features and integrations

## 🏗️ Architecture Flowchart

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           MATH AGENT SYSTEM ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │   FastAPI Server │    │   MCP Server    │
│   (Port 3000)   │◄──►│   (Port 8000)   │◄──►│   (Port 3001)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  User Interface │    │  API Endpoints  │    │  Web Search     │
│  - Question Input│    │  - POST /ask    │    │  - Khan Academy │
│  - Answer Display│    │  - GET /         │    │  - Wolfram      │
│  - History      │    │  - CORS Support  │    │  - Math Sites   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │   AI Orchestration      │
                    │   Engine (main.py)      │
                    │   - CrewAI Framework     │
                    │   - Gemini AI           │
                    │   - Async Processing    │
                    └─────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │ Input Guardrails│ │ Knowledge Base  │ │ Output Guardrails│
    │ - Math Content  │ │ - ChromaDB      │ │ - Sanitization  │
    │ - Length Check  │ │ - Vector Search │ │ - Validation    │
    │ - Keyword Match │ │ - JEE/IMO Data  │ │ - Educational   │
    └─────────────────┘ └─────────────────┘ └─────────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │  Quality Evaluation    │
                    │  - Accuracy Scoring    │
                    │  - Clarity Assessment  │
                    │  - Threshold Check     │
                    └─────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
        ┌─────────────────┐    ┌─────────────────┐
        │ Score ≥ 8       │    │ Score < 8       │
        │ Return Solution  │    │ Human Feedback  │
        └─────────────────┘    └─────────────────┘
                                        │
                                        ▼
                            ┌─────────────────────────┐
                            │ Human-in-the-Loop       │
                            │ - Expert Review         │
                            │ - Answer Refinement     │
                            │ - KB Update            │
                            └─────────────────────────┘
```

## 🔄 Data Flow Sequence

### 1. User Interaction Layer
```
User Input → Frontend Validation → API Request
```

### 2. Input Processing Layer
```
API Request → Input Guardrails → Mathematical Content Check
```

### 3. Knowledge Retrieval Layer
```
Knowledge Base Search → ChromaDB Vector Similarity
├─ If KB Hit: Use Stored Answer
└─ If No KB Hit: Trigger MCP Web Search
```

### 4. AI Processing Layer
```
AI Processing → Gemini AI → Step-by-Step Solution
```

### 5. Quality Assurance Layer
```
Output Guardrails → Content Sanitization
Quality Evaluation → Score Assessment
├─ If High Score (≥8): Return Solution
└─ If Low Score (<8): Human Feedback Loop
```

### 6. Response Delivery Layer
```
Response Delivery → Frontend Display → History Storage
```

## 🧩 Component Details

### Frontend Components (React)
```
frontend/
├── src/
│   ├── App.js          # Main component with state management
│   ├── App.css         # Styling and responsive design
│   └── index.js        # React entry point
├── public/
│   └── index.html      # HTML template
└── package.json        # Dependencies and scripts
```

### Backend Components (Python)
```
math-agent-project/
├── main.py                    # AI orchestration with CrewAI + Gemini
├── app.py                     # FastAPI server with async endpoints
├── knowledge_base.py          # ChromaDB with JEE/IMO problems
├── human_feedback.py          # Expert review system
├── mcp_client.py              # Web search integration
├── output_guardrails.py      # Content validation
├── jee_benchmark.py          # Performance testing
├── dspy_optimizer.py         # DSPy optimization utilities
├── mcp_server_simulator.py   # MCP server simulation
├── test_full_system.py       # Comprehensive system testing
└── quick_test.py             # Quick functionality tests
```

### External Services
```
External Integrations:
├── Google Gemini AI           # Core mathematical reasoning
├── ChromaDB                   # Vector database for semantic search
├── MCP Protocol               # Standardized web search
└── Educational Websites       # Khan Academy, Wolfram, etc.
```

## 🛠️ Technology Stack

### Frontend Technologies
- **React 18**: Modern UI framework with hooks
- **JavaScript ES6+**: Modern JavaScript features
- **CSS3**: Responsive design and styling
- **Fetch API**: HTTP client for API communication

### Backend Technologies
- **Python 3.8+**: Core programming language
- **FastAPI**: High-performance web framework
- **CrewAI**: AI agent orchestration framework
- **Google Gemini AI**: Large language model
- **ChromaDB**: Vector database for embeddings
- **aiohttp**: Async HTTP client
- **python-dotenv**: Environment variable management

### Data Storage
- **ChromaDB**: Vector embeddings and semantic search
- **Local Files**: Configuration and temporary data
- **In-Memory**: Session data and caching

### External APIs
- **Google Gemini API**: AI model inference
- **MCP Protocol**: Web search integration
- **Educational Websites**: External math resources

## 🚀 Deployment Architecture

### Development Environment
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Dev     │    │   Python Dev    │    │   MCP Simulator │
│   Server        │    │   Server        │    │   (Optional)    │
│   :3000         │    │   :8000         │    │   :3001         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Production Environment (Recommended)
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx         │    │   FastAPI       │    │   MCP Server    │
│   Reverse Proxy │    │   Application   │    │   Production    │
│   :80/:443      │    │   :8000         │    │   :3001         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Static Files  │    │   ChromaDB      │    │   External APIs │
│   (React Build) │    │   Database      │    │   (Gemini, etc.)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 Performance Characteristics

### Response Time Targets
- **Knowledge Base Hit**: < 1 second
- **Web Search Fallback**: < 3 seconds
- **Human Feedback Loop**: < 10 seconds
- **Overall System**: < 5 seconds average

### Scalability Metrics
- **Concurrent Users**: 100+ (with proper deployment)
- **Questions per Minute**: 50+ (depending on complexity)
- **Knowledge Base Size**: 10,000+ problems
- **Memory Usage**: < 2GB per instance

### Quality Metrics
- **Accuracy Rate**: >85% for standard problems
- **Knowledge Base Hit Rate**: ~70%
- **Human Feedback Trigger Rate**: <15%
- **User Satisfaction**: Based on response quality scores

## 🔧 Configuration Management

### Environment Variables
```bash
# Required
GEMINI_API_KEY=your_gemini_api_key

# Optional
MCP_SERVER_URL=http://localhost:3001
CHROMA_DB_PATH=./chroma_db
LOG_LEVEL=INFO
MAX_RESPONSE_TIME=30
```

### Port Configuration
- **Frontend**: 3000 (development), 80/443 (production)
- **Backend API**: 8000 (development), 8000 (production)
- **MCP Server**: 3001 (optional)

## 🔒 Security Considerations

### Input Validation
- Mathematical content verification
- Length and format checks
- Injection attack prevention

### Output Sanitization
- Content filtering and validation
- Educational appropriateness checks
- Harmful content removal

### API Security
- CORS configuration
- Rate limiting (recommended for production)
- Input validation and sanitization

## 📈 Monitoring and Observability

### Key Metrics to Monitor
- Response times per component
- Knowledge base hit rates
- Human feedback trigger rates
- Error rates and types
- User satisfaction scores

### Logging Strategy
- Structured logging with timestamps
- Component-level logging
- Error tracking and alerting
- Performance metrics collection

---

**Last Updated**: December 2024  
**Version**: 1.0  
**Maintainer**: Math Agent Development Team