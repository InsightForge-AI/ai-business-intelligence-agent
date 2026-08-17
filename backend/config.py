AGENT_API_URL = "http://127.0.0.1:8005/agent/analyze"

NLP_API_URL = "http://127.0.0.1:8001/nlp/analyze"

ML_API_URL = "http://127.0.0.1:8002/ml/analyze"

RAG_API_URL = "http://127.0.0.1:8003/rag/query"

CV_API_URL = "http://127.0.0.1:8004/cv/analyze"

# Bounds every outbound call to a downstream module, and doubles as the
# budget execute_with_timeout() gives each module in backend/app/api/analyze.py.
REQUEST_TIMEOUT = 5