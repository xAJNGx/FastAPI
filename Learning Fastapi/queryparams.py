"""
A classical method of passing the request data to the server is to append a query string to the URL.
a list of key-value pairs concatenated by the ampersand (&) forms the query string, which is appended to the URL by putting a question mark (?) as a separator. For example −

http://localhost/cgi-bin/hello.py?name=Ravi&age=20

The trailing part of the URL, after (?), is the query string, which is then parsed by the server-side script for further processing.

As mentioned, the query string is a list of parameter=value pairs concatenated by & symbol.
FastAPI automatically treats the part of the endpoint which is not a path parameter as a query string and parses it into parameters and its values. 
These parameters are passed to the function below the operation decorator.

"""

from fastapi import FastAPI, Path, Query


app = FastAPI()

@app.get("/hello")
async def hello (name:str , age:int):
    return{"name":name ,"age":age}

#ex http://127.0.0.1:8000/hello?name=ajng&age=22

@app.get("/hi/{name}")
async def hi (name:str,age:int):
    return {"name":name,"age":age}

#http://127.0.0.1:8000/hi/ajng?age=22


"""
It is possible to apply validation conditions on path parameters as well as query parameters of the URL. 
In order to apply the validation conditions on a path parameter, you need to import the Path class.
"""

@app.get("/hello/{name}")
async def hello(name:str=Path(...,min_length=3,
max_length=10)):
   return {"name": name}


"""
The query parameters can also have the validation rules applied to them.
You have to specify them as the part of arguments of Query class constructor.
Let us add a query parameter called percent in the above function and apply the validation rules as ge=0 (i.e., greater then equal to 0) and lt=100 (less than or equal to 100)
"""
@app.get("/hello/{name}/{age}")
async def hello(*, name: str=Path(...,min_length=3 ,
      max_length=10), \
      age: int = Path(..., ge=1, le=100), \
      percent:float=Query(..., ge=0, le=100)):
   return {"name": name, "age":age, "percent":percent}