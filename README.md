# 🧮 Math Agent - Advanced AI-Powered Math Tutoring System

A sophisticated math tutoring system that leverages Google's Gemini AI, CrewAI framework, and advanced knowledge management to provide comprehensive mathematical assistance. The system features intelligent routing, human-in-the-loop feedback, and robust quality control mechanisms.

## 🌟 What This Project Does

This is an enterprise-grade intelligent math tutor that:
- **Answers complex math questions** using Google's Gemini AI with CrewAI orchestration
- **Intelligently routes queries** through knowledge base, web search, or human feedback
- **Provides step-by-step solutions** with educational explanations
- **Maintains an advanced knowledge base** with JEE Advanced and IMO-level problems
- **Implements human-in-the-loop feedback** for quality assurance
- **Features comprehensive guardrails** for input validation and output sanitization
- **Offers a modern React frontend** with question history and real-time interaction
- **Includes benchmarking capabilities** for performance evaluation

## 🏗️ System Architecture

For detailed architecture information, component relationships, and technical specifications, see the comprehensive [ARCHITECTURE.md](ARCHITECTURE.md) document.

### Quick Overview
The system follows a modular architecture with these key layers:
- **Frontend**: React application for user interaction
- **API Layer**: FastAPI server handling requests
- **AI Engine**: CrewAI orchestration with Gemini AI
- **Knowledge Base**: ChromaDB for semantic search
- **Quality Control**: Multi-layer validation and human feedback
- **External Integration**: MCP protocol for web search

## 🔄 System Workflow

### Query Processing Pipeline

```
1. User Input → Frontend Validation
2. API Request → FastAPI Server
3. Input Guardrails → Mathematical Content Validation
4. Knowledge Base Search → ChromaDB Vector Search
   ├─ If Found: Use KB Answer
   └─ If Not Found: Trigger Web Search
5. Web Search → MCP Client → Educational Websites
6. AI Processing → Gemini AI → Step-by-Step Solution
7. Output Guardrails → Content Sanitization & Validation
8. Quality Evaluation → Score Assessment (Accuracy/Clarity)
   ├─ If Score ≥ 8: Return Solution
   └─ If Score < 8: Trigger Human Feedback Loop
9. Human Feedback → Expert Refinement → KB Update
10. Response Delivery → Frontend Display
```

### Intelligent Routing Logic

The system employs a sophisticated routing mechanism:

1. **Input Validation**: Ensures mathematical content and minimum length
2. **Knowledge Base Priority**: Checks ChromaDB for existing solutions
3. **Web Search Fallback**: Uses MCP protocol for external resources
4. **Quality Assurance**: Evaluates response quality with scoring
5. **Human-in-the-Loop**: Triggers expert review for low-quality responses
6. **Continuous Learning**: Updates knowledge base with improved solutions

## 📁 Project Structure

```
math-agent-project/
├── 📄 main.py                    # AI orchestration engine (CrewAI + Gemini)
├── 📄 app.py                     # FastAPI web server
├── 📄 knowledge_base.py          # ChromaDB knowledge base with JEE/IMO problems
├── 📄 human_feedback.py          # Human-in-the-loop feedback system
├── 📄 mcp_client.py              # MCP protocol web search client
├── 📄 output_guardrails.py       # Input/output validation and sanitization
├── 📄 jee_benchmark.py           # Performance benchmarking system
├── 📄 dspy_optimizer.py          # DSPy optimization utilities
├── 📄 mcp_server_simulator.py    # MCP server simulation for testing
├── 📄 test_full_system.py        # Comprehensive system testing
├── 📄 quick_test.py              # Quick functionality tests
├── 📄 requirements.txt           # Python dependencies
├── 📄 README.md                  # This documentation
├── 📁 env/                       # Python virtual environment
├── 📁 frontend/                  # React frontend application
│   ├── 📄 package.json           # Frontend dependencies
│   ├── 📁 src/
│   │   ├── 📄 App.js             # Main React component
│   │   ├── 📄 App.css             # Styling
│   │   └── 📄 index.js            # React entry point
│   └── 📁 public/
│       └── 📄 index.html          # HTML template
└── 📄 jee_benchmark_results.txt  # Benchmark test results
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js 16+ (for frontend)
- A Google Gemini API key (free from Google AI Studio)

### Step 1: Backend Setup
```bash
# Navigate to the project folder
cd math-agent-project

# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Environment Configuration
1. Get a free Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a `.env` file in the project folder:
```bash
# Create the .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```
Replace `your_api_key_here` with your actual API key.

### Step 3: Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install frontend dependencies
npm install

# Start the React development server
npm start
```

### Step 4: Start the Backend Server
```bash
# In the main project directory
python app.py
```

The API server will start on `http://localhost:8000`
The React frontend will be available at `http://localhost:3000`

### Step 5: Test the System
```bash
# Test the API directly
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is the derivative of x squared?"}'

# Run comprehensive tests
python test_full_system.py

# Run JEE benchmark
python jee_benchmark.py
```

## 🧪 Testing & Benchmarking

### Comprehensive Testing
```bash
# Run full system tests
python test_full_system.py

# Quick functionality test
python quick_test.py

# Test individual components
python main.py  # Test AI agent
python human_feedback.py  # Test feedback system
```

### Performance Benchmarking
```bash
# Run JEE Advanced benchmark
python jee_benchmark.py

# View benchmark results
cat jee_benchmark_results.txt
```

### Frontend Testing
```bash
cd frontend
npm test  # Run React tests
npm run build  # Build for production
```

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### MCP Server Configuration (Optional)
The system can search the web using an MCP (Model Context Protocol) server:
- Default URL: `http://localhost:3001`
- If not running, the system will work with just the AI and knowledge base
- Test MCP server: `python mcp_server_simulator.py`

### Knowledge Base Customization
- Edit `knowledge_base.py` to add custom math problems
- Categories: `algebra`, `geometry`, `calculus`, `jee_advanced`, `imo`
- Difficulty levels: `easy`, `medium`, `hard`, `advanced`, `expert`

## 📚 API Documentation

### POST `/ask`
Submit a mathematical question and receive a comprehensive solution.

**Request:**
```json
{
  "question": "What is the derivative of sin(x) + cos(x)?"
}
```

**Response:**
```json
{
  "answer": "The derivative of sin(x) + cos(x) is cos(x) - sin(x). Here's the step-by-step solution:\n\nStep 1: Apply the sum rule for derivatives...\nStep 2: Find derivative of sin(x) = cos(x)\nStep 3: Find derivative of cos(x) = -sin(x)\nStep 4: Combine results: cos(x) - sin(x)"
}
```

### GET `/`
Health check endpoint.

**Response:**
```json
{
  "message": "Math Professor Agent API is running!"
}
```

### Error Responses
```json
{
  "detail": "Error message describing what went wrong"
}
```

## 🛠️ Troubleshooting

### Common Issues

1. **"API key not found"**
   - Ensure `.env` file exists with `GEMINI_API_KEY=your_key`
   - Verify the API key is valid and has sufficient quota

2. **"MCP server not available"**
   - This is normal if you don't have an MCP server running
   - The system will still work with just the AI and knowledge base
   - Test with: `python mcp_server_simulator.py`

3. **"Import errors"**
   - Ensure virtual environment is activated: `source env/bin/activate`
   - Reinstall dependencies: `pip install -r requirements.txt`

4. **"Port already in use"**
   - Backend: Change port in `app.py` or kill process using port 8000
   - Frontend: Change port in `frontend/package.json` or kill process using port 3000

5. **"ChromaDB errors"**
   - Delete `chroma_db` folder and restart to rebuild knowledge base
   - Ensure sufficient disk space for vector embeddings

6. **"Frontend not connecting to backend"**
   - Verify backend is running on port 8000
   - Check CORS settings in `app.py`
   - Ensure both servers are running simultaneously

## 🔮 Future Enhancements

- [x] ✅ Modern React frontend with question history
- [x] ✅ Advanced knowledge base with JEE/IMO problems
- [x] ✅ Human-in-the-loop feedback system
- [x] ✅ Comprehensive benchmarking and testing
- [x] ✅ MCP protocol integration for web search
- [x] ✅ Output guardrails and input validation
- [ ] Support for image-based math problems (OCR integration)
- [ ] LaTeX rendering for mathematical expressions
- [ ] Multi-language support for international students
- [ ] Integration with learning management systems (LMS)
- [ ] Advanced analytics and learning progress tracking
- [ ] Mobile app version (React Native)
- [ ] Voice input/output capabilities
- [ ] Collaborative problem-solving features
- [ ] Integration with graphing calculators and visualization tools

## 🏆 Key Features & Capabilities

### Advanced AI Integration
- **CrewAI Framework**: Orchestrates multiple AI agents for complex problem-solving
- **Google Gemini AI**: Powers the core mathematical reasoning engine
- **Vector Embeddings**: ChromaDB for semantic search and similarity matching

### Quality Assurance
- **Multi-layer Validation**: Input guardrails, output sanitization, educational content verification
- **Human-in-the-Loop**: Expert review system for low-quality responses
- **Continuous Learning**: Knowledge base updates with improved solutions

### Performance & Scalability
- **Async Processing**: Non-blocking operations for better performance
- **Benchmarking**: JEE Advanced standards for accuracy assessment
- **Modular Architecture**: Easy to extend and maintain

### User Experience
- **Modern Frontend**: React 18 with hooks and responsive design
- **Real-time Interaction**: Live question submission and answer display
- **Question History**: Track previous queries and solutions

## 🤝 Contributing

We welcome contributions to improve this advanced math tutoring system! Here are areas where help is particularly valuable:

### Development Areas
- **Frontend Enhancement**: React components, UI/UX improvements, accessibility
- **AI Integration**: Prompt engineering, model optimization, new AI providers
- **Knowledge Base**: Adding more math problems, curriculum alignment, difficulty scaling
- **Testing**: Unit tests, integration tests, performance optimization
- **Documentation**: API docs, tutorials, educational content

### Contribution Guidelines
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Code Standards
- Follow PEP 8 for Python code
- Use TypeScript for React components
- Include tests for new features
- Update documentation for API changes

## 📄 License

This project is open source and available under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for the powerful language model and mathematical reasoning capabilities
- **CrewAI Framework** for AI agent orchestration and multi-agent systems
- **ChromaDB** for vector database and semantic search capabilities
- **FastAPI** for the high-performance web framework
- **React** for the modern frontend framework
- **MCP Protocol** for standardized AI tool integration
- **The open-source community** for various tools, libraries, and educational resources

## 📊 Performance Metrics

Based on JEE Advanced benchmarking:
- **Average Response Time**: < 3 seconds
- **Knowledge Base Hit Rate**: ~70% for common problems
- **Accuracy Rate**: >85% for standard mathematical problems
- **Human Feedback Trigger Rate**: <15% of responses

---

**Happy Learning! 🎓📚**

For questions, issues, or contributions, please open an issue or reach out to the development team!