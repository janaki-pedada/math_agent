import React, { useState } from 'react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const askQuestion = async () => {
    if (!question.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question.trim() }),
      });
      
      const data = await response.json();
      setAnswer(data.answer);
      
      // Add to history
      setHistory(prev => [...prev, {
        question: question.trim(),
        answer: data.answer,
        timestamp: new Date().toLocaleTimeString()
      }]);
      
    } catch (error) {
      setAnswer('Error connecting to the math tutor. Please make sure the server is running.');
    }
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      askQuestion();
    }
  };

  return (
    <div className="App">
      <header className="header">
        <h1>🧮 Math Professor AI Tutor</h1>
        <p>Ask any mathematics question and get step-by-step solutions</p>
      </header>

      <div className="main-container">
        <div className="input-section">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a math question (e.g., How to solve quadratic equations?)"
            rows="3"
            disabled={loading}
            className="question-input"
          />
          <button 
            onClick={askQuestion} 
            disabled={loading || !question.trim()}
            className="ask-button"
          >
            {loading ? 'Thinking...' : 'Ask Question'}
          </button>
        </div>

        {answer && (
          <div className="answer-section">
            <h3>Solution:</h3>
            <div className="answer-content">
              {answer.split('\n').map((line, i) => (
                <p key={i}>{line}</p>
              ))}
            </div>
          </div>
        )}

        {history.length > 0 && (
          <div className="history-section">
            <h3>Question History</h3>
            <div className="history-list">
              {history.slice().reverse().map((item, index) => (
                <div key={index} className="history-item">
                  <div className="history-question">
                    <strong>Q: {item.question}</strong>
                    <span className="history-time">{item.timestamp}</span>
                  </div>
                  <div className="history-answer">
                    {item.answer.substring(0, 100)}...
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;