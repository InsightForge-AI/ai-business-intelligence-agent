from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CalcRequest(BaseModel):
    a: float
    b: float
    c: str  # operation: "add", "sub", "mul", "div"

OPERATIONS = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
    "mul": lambda a, b: a * b,
    "div": lambda a, b: a / b,
}

@app.post("/calculator")
async def calculate(req: CalcRequest):
    if req.c not in OPERATIONS:
        return {"error": "Invalid operation. Use 'add', 'sub', 'mul', 'div'."}

    result = OPERATIONS[req.c](req.a, req.b)
    return {"result": result}


