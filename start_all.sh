echo "Stopping old servers..."

pkill -f uvicorn
pkill -f streamlit

sleep 2

echo "Starting AI Business Intelligence system..."

# NLP
(cd nlp && python3 -m uvicorn teamB.api.main:app --port 8001 &)

# ML
(cd ml && python3 -m uvicorn teamA.api.main:app --port 8002 &)

# RAG
(cd rag && python3 -m uvicorn teamC.api.main:app --port 8003 &)

# CV
(cd cv && python3 -m uvicorn teamA.api.main:app --port 8004 &)

# Agent
(cd agent && python3 -m uvicorn teamA.app:app --port 8005 &)

# Backend
(cd backend && python3 -m uvicorn main:app --port 8000 &)

# Frontend
(cd frontend && streamlit run app.py &)

echo "--------------------------------"
echo "All services started"
echo "Frontend: http://localhost:8501"
echo "Backend:  http://127.0.0.1:8000/docs"
echo "--------------------------------"
