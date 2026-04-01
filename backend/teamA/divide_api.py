from fastapi import APIRouter
router = APIRouter()

@router.get("/divide")
def divide(a:float,b:float):
    if b ==0:
        return{"error":"cannot divide by zero"}
    return{
        "Operation":"Division",
        "Result": a/b
    }