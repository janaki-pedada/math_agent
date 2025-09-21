import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

math_qa_pairs = [
    {
        "question": "What is the Pythagorean theorem?",
        "answer": "The Pythagorean theorem states that in a right-angled triangle, the square of the hypotenuse is equal to the sum of the squares of the other two sides. Formula: a² + b² = c²",
        "category": "geometry"
    },
    {
        "question": "How to solve a quadratic equation?",
        "answer": "A quadratic equation is solved using the quadratic formula: x = [-b ± √(b² - 4ac)] / (2a). Steps: 1. Identify coefficients a, b, c. 2. Calculate discriminant D = b² - 4ac. 3. Apply formula if D ≥ 0.",
        "category": "algebra"
    },
    {
        "question": "What is the derivative of sin(x)?",
        "answer": "The derivative of sin(x) with respect to x is cos(x). This is a fundamental rule in differential calculus.",
        "category": "calculus"
    },
    {
        "question": "Explain the concept of limits in calculus.",
        "answer": "A limit describes the value that a function approaches as the input approaches some value. Limits are essential to defining derivatives and integrals.",
        "category": "calculus"
    },
    {
        "question": "What is the formula for the area of a circle?",
        "answer": "The area of a circle is given by the formula A = πr², where 'r' is the radius of the circle and 'π' is approximately 3.14159.",
        "category": "geometry"
    }

    # Add this to your knowledge_base.py after the existing math_qa_pairs
]
# JEE Advanced Dataset
jee_advanced_questions = [
    {
        "question": "If the roots of the equation x² - bx + c = 0 are two consecutive integers, then b² - 4c equals?",
        "answer": "Let the roots be n and n+1. Then sum of roots = n + (n+1) = 2n+1 = b. Product of roots = n(n+1) = c. Then b² - 4c = (2n+1)² - 4n(n+1) = 4n² + 4n + 1 - 4n² - 4n = 1. Therefore, b² - 4c = 1.",
        "category": "jee_advanced",
        "difficulty": "hard",
        "tags": ["quadratic equations", "roots", "consecutive integers"]
    },
    {
        "question": "The number of real solutions of the equation sin(e^x) = 5^x + 5^{-x} is?",
        "answer": "Note that 5^x + 5^{-x} ≥ 2 for all real x (by AM-GM inequality). Since sin(e^x) ≤ 1 for all real x, the equation can only hold if both sides equal exactly 2. But 5^x + 5^{-x} = 2 only when x=0, and sin(e^0) = sin(1) ≈ 0.84 ≠ 2. Therefore, there are no real solutions. Answer: 0",
        "category": "jee_advanced",
        "difficulty": "hard",
        "tags": ["exponential equations", "trigonometry", "inequalities"]
    }
]

#  International Math Olympiad (IMO) Problems
imo_questions = [
    {
        "question": "Find all functions f: R → R such that f(x + y) = f(x) + f(y) + 2xy for all real numbers x, y",
        "answer": "Assume f is a polynomial function. Let f(x) = ax² + bx + c. Substitute into the equation: a(x+y)² + b(x+y) + c = (ax²+bx+c) + (ay²+by+c) + 2xy. Simplify: ax² + 2axy + ay² + bx + by + c = ax² + ay² + bx + by + 2c + 2xy. Compare coefficients: 2a = 2 (from xy terms), so a=1. Also c = 2c, so c=0. The equation holds for any b, but checking: f(x) = x² + bx works? (x+y)² + b(x+y) = x²+bx + y²+by + 2xy → works for any b. However, the constant term must be 0. Actually, f(x) = x² is the solution. Verification: (x+y)² = x² + y² + 2xy. Answer: f(x) = x²",
        "category": "imo",
        "difficulty": "expert",
        "tags": ["functional equations", "polynomials", "imo"]
    }
]

# Advanced Calculus Problems
advanced_calculus = [
    {
        "question": "Evaluate the limit: lim(x→0) (sin(x) - x) / x³",
        "answer": "Use L'Hôpital's rule repeatedly. lim(x→0) (sin(x) - x) / x³ = lim(x→0) (cos(x) - 1) / 3x² = lim(x→0) (-sin(x)) / 6x = lim(x→0) (-cos(x)) / 6 = -1/6. Alternatively, use Taylor series: sin(x) = x - x³/6 + x⁵/120 - ... So (sin(x)-x)/x³ = -1/6 + x²/120 - ... → -1/6 as x→0. Answer: -1/6",
        "category": "calculus",
        "difficulty": "advanced",
        "tags": ["limits", "l'hopital's rule", "taylor series"]
    }
]

class MathKnowledgeBase:
    def __init__(self):
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        self.client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            persist_directory="./chroma_db"
        ))
        self.collection = self.client.get_or_create_collection(
            name="math_knowledge",
            embedding_function=self.embedding_function
        )

        if self.collection.count() == 0:
            self._populate_kb()

    def _populate_kb(self):
        """Populate knowledge base with enhanced dataset"""
        # COMBINE ALL QUESTIONS: basic + bonus datasets
        all_questions = math_qa_pairs + jee_advanced_questions + imo_questions + advanced_calculus
        
        documents = []
        metadatas = []
        ids = []
        
        for i, qa in enumerate(all_questions):
            # Create rich document text
            document_text = f"""
            Question: {qa['question']}
            Answer: {qa['answer']}
            Category: {qa.get('category', 'general')}
            Difficulty: {qa.get('difficulty', 'medium')}
            Tags: {', '.join(qa.get('tags', []))}
            """
            
            documents.append(document_text)
            
            # Convert lists to strings for ChromaDB compatibility
            tags = qa.get('tags', [])
            tags_str = ', '.join(tags) if tags else 'none'
            
            metadatas.append({
                "question": qa['question'],
                "category": qa.get('category', 'general'),
                "difficulty": qa.get('difficulty', 'medium'),
                "tags": tags_str,  # Convert list to string
                "source": "enhanced_knowledge_base"
            })
            ids.append(f"math_qa_{i}")
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"✅ Knowledge base populated with {len(documents)} items (including bonus dataset)")
    def search(self, query: str, n_results: int = 2, threshold: float = 0.6):
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["metadatas", "documents", "distances"]
            )
            
            if (results['documents'] and results['documents'][0] and 
                results['distances'] and results['distances'][0] and 
                results['distances'][0][0] < threshold):
                
                best_doc = results['documents'][0][0]
                best_metadata = results['metadatas'][0][0]
                
                return best_metadata.get('question'), {
                    'answer': best_doc,
                    'metadata': best_metadata,
                    'similarity_score': 1 - results['distances'][0][0]
                }
            
            return None, None
            
        except Exception as e:
            print(f"Knowledge base search error: {e}")
            return None, None

    def add_corrected_answer(self, question: str, answer: str, metadata: dict = None):
        document_text = f"Question: {question}. Answer: {answer}"
        
        self.collection.add(
            documents=[document_text],
            metadatas=[metadata or {
                "question": question,
                "source": "human_corrected",
                "corrected": True
            }],
            ids=[f"corrected_{str(uuid.uuid4())[:8]}"]
        )
        print(f"✅ Added corrected answer to knowledge base: {question}")

math_kb = MathKnowledgeBase()