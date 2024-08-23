from fastapi import FastAPI, Body
from typing import List
from pydantic import BaseModel, Field

app = FastAPI()

class Student(BaseModel):
   id: int
   name :str = Field(None, title="name of student", max_length=10)
   subjects: List[str] = []


@app.post("/students/")
async def student_data(s1: Student):
   return s1

@app.post("/studentswithbody")
async def student_data(name:str = Body(...), marks:int = Body(...)):
   return {"name":name,"marks": marks}