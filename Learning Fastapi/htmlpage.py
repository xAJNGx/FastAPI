from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import FastAPI, Request , Form , Cookie
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static",StaticFiles(directory ="static"),name="static")

class User(BaseModel):
   username:str
   password:str

@app.get("/hello/{name}", response_class=HTMLResponse)
async def hello(request: Request, name:str):
    return templates.TemplateResponse("hello.html",{"request":request, "name":name})

@app.get("/login",response_class=HTMLResponse)
async def login(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})

@app.post("/submit",response_model=User)
async def submit(name : str = Form(...), password :str = Form(...)):
    return {"username":name,"password":password}

#In FastAPI, the cookie parameter is set on the response object with the help of set_cookie() method
"""
Here is an example of set_cookie() method. 
We have a JSON response object called content. Call the set_cookie() method on it to set a cookie as key="usrname" and value="admin" −
"""
@app.post("/cookie")
def create_cookie():
    content = {"message":"cookie set"}
    response = JSONResponse(content=content)
    response.set_cookie(key="username",value="ajng")
    return response

@app.get("/readcookie/")
async def read_cookie(username: str = Cookie(None)):
   return {"username": username}