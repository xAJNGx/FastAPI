from fastapi import FastAPI,Depends,HTTPException

app = FastAPI()

# @app.get("/user/")
# async def user(id: str, name: str, age: int):
#    return {"id": id, "name": name, "age": age}


# @app.get("/admin/")
# async def admin(id: str, name: str, age: int):
#    return {"id": id, "name": name, "age": age

async def dependency(id:str , name:str , age:int):
    return {"id": id, "name": name, "age": age}

@app.get("/user")
async def user(dep: dict = Depends(dependency)):
    return dep

class DependClass:
   def __init__(self, id: str, name: str, age: int):
      self.id = id
      self.name = name
      self.age = age 

@app.get("/admin/")
async def admin(dep: dependency = Depends(DependClass)):
   return dep 

async def validate(dep: dependency = Depends(DependClass)):
   if dep.age > 18:
      raise HTTPException(status_code=400, detail="You are not eligible")
  
@app.get("/checkage",dependencies=[Depends(validate)])
async def checkage():
    return {"message":"You are eligible"}