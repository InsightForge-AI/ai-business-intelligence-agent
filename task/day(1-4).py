from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel, EmailStr
import mysql.connector




# Pydantic model
class signup(BaseModel):
    email: EmailStr
    phone: str
    password: str


app = FastAPI()
@app.get("/")
async def root():
    return{'message':'Hello World'}


@app.get('/posts')
async def post():
    return{'post':'recent post'}

# @app.post('/signup')
# async def join(su:signup):
#     print(su)
#     return {
#         "email":su.email,
#         "phone":su.phone,
#         "password":su.password
#         }

# DB connection function
def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        database="emp_info",
        user="root",
        password="maj33d"
    )


@app.post("/signup")
async def signup_fun(su:signup):
  try:
      conn = get_connection()
      cursor = conn.cursor()
      query = "INSERT INTO users (email, phone, password) VALUES (%s, %s, %s)"
      cursor.execute(query, (su.email, su.phone, su.password))
      conn.commit()
      cursor.close()
      conn.close()
      return {
            "message" : "user stored successfully"
        }
  except Exception as e:
        return {"error": str(e)}
  


@app.get("/getusers")
async def getuser():
  try:
      conn = get_connection()
      cursor = conn.cursor(dictionary=True)
      query = "select id, phone, email from users"
      cursor.execute(query)
      users = cursor.fetchall()
      cursor.close()
      conn.close()
      return {
            "users" : users
        }
  except Exception as e:
        return {"error": str(e)}
  

  
@app.get("/getuser/{id}")
async def getuser(id:int):
  try:
      conn = get_connection()
      cursor = conn.cursor(dictionary=True)
      query = "SELECT id, phone, email FROM users where id=%s"
      cursor.execute(query,(id,))
      users = cursor.fetchone()
      cursor.close()
      conn.close()
      return {
            "users" : users
        }
  except Exception as e:
        return {"error": str(e)}