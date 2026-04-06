from fastapi import FastAPI

app = FastAPI()

@app.post("/analyze")
def analyze(data: dict):
    query = data["text"]
    sales = data["sales"]

    keywords = ["sales", "drop"]

    found = False
    for word in keywords:
        if word in query.lower():
            found = True

    is_dropping = True
    for i in range(1, len(sales)):
        if sales[i] >= sales[i-1]:
            is_dropping = False
            break

    if found:
        if is_dropping:
            return {"result": "Sales are dropping"}
        else:
            return {"result": "Sales are increasing"}
    else:
        return {"result": "No relevant data found"}