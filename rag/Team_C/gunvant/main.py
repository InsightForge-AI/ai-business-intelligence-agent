from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Business Intelligence API - Gunvant")

# ------------------------
# User Model
# ------------------------
class User(BaseModel):
    name: str
    age: int

# ------------------------
# Basic APIs
# ------------------------
@app.get("/")
def home():
    return {"message": "Welcome"}

@app.get("/hello")
def hello():
    return {"message": "Hello World"}

@app.get("/greet")
def greet(name: str):
    return {"message": f"Hello {name}"}

@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}

@app.post("/user")
def create_user(user: User):
    return {"message": f"Hello {user.name}, age {user.age}"}

# ------------------------
# RAG PART
# ------------------------
docs = ["sales dropped", "bad delivery"]

def search(query: str):
    for d in docs:
        if "sales" in query.lower():
            return d
    return "No relevant data found"

@app.post("/rag/query")
def rag_query(data: dict):
    return {"context": search(data["query"])}

# ------------------------
# Extra Calculator APIs
# ------------------------
@app.get("/subtract")
def subtract(a: int, b: int):
    return {"result": a - b}

@app.get("/multiply")
def multiply(a: int, b: int):
    return {"result": a * b}

@app.get("/divide")
def divide(a: int, b: int):
    if b == 0:
        return {"error": "Division by zero"}
    return {"result": a / b}
