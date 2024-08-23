#Modern web frameworks use routes or endpoints as a part of URL instead of file-based URLs. 
#This helps the user to remember the application URLs more effectively. 
# In FastAPI, it is termed a path. A path or route is the part of the URL trailing after the first ‘/’.

"""
For example, in the following URL,

http://localhost:8000/hello/TutorialsPoint
the path or the route would be

/hello/TutorialsPoint
"""
#In FastAPI, such a path string is given as a parameter to the operation decorator.

from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def index():
    return {"message":"Hello World"}


@app.get("/hello/{name}")
async def hello(name):
    return {"name":name}