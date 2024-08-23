from fastapi import FastAPI,Depends
from pydantic import BaseModel


from sqlalchemy import create_engine,Column,Integer,String
from typing import List
from sqlalchemy.dialects.sqlite import *
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()

data = []


class Student(BaseModel):
   id: int
   name: str
   grade: int
   addess: str
   
@app.post("/student")
def add_student(student: Student):
   data.append(student.dict())
   return data

@app.get("/list")
def get_students():
   return data

@app.get("/student/{id}")
def get_student(id: int):
   id = id - 1
   return data[id]

@app.put("/student/{id}")
def edit_student(id: int, student: Student):
   data[id-1] = student
   return data

@app.delete("/student/{id}")
def delete_student(id: int):
   data.pop(id-1)
   return data

#using the SQLLIte DB
"""
Since we are going to use SQLite database, we need to create a database engine for our database called test.db
"""
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False})

"""
In order to interact with the database, we need to obtain its handle. A session object is the handle to database. Session class is defined using sessionmaker() − a configurable session factory method which is bound to the engine object.
"""
session = sessionmaker(autoflush=False,autocommit= False, bind=engine)

"""
we need a declarative base class that stores a catalog of classes and mapped tables in the Declarative system.
"""
Base = declarative_base()

#define the data model
class Books(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(50), unique=True)
    author = Column(String(50))
    publisher = Column(String(50))

#to create the table
# This line should be outside the class definition and after all models are defined.
Base.metadata.create_all(bind=engine) #The create_all() method creates the corresponding tables in the database.

#define the schema
class Book(BaseModel):
    id:int
    title:str
    author:str
    publisher:str
    class Config: 
        orm_mode =True #Note the use of orm_mode=True in the config class indicating that it is mapped with the ORM class of SQLAlchemy.
  
#dependency injecttion to get db session       
def get_db():
   db = session()
   try:
      yield db
   finally:
      db.close()     

#CRUD Endpoints
@app.post('/add_new', response_model=Book)
def add_book(b1: Book, db: Session = Depends(get_db)):
   bk=Books(id=b1.id, title=b1.title, author=b1.author,publisher=b1.publisher)
   db.add(bk)
   db.commit()
   db.refresh(bk)
   return Books(**b1.dict())

@app.get('/list', response_model=List[Book])
def get_books(db: Session = Depends(get_db)):
   recs = db.query(Books).all()
   return recs

@app.get('/book/{id}', response_model=Book)
def get_book(id:int, db: Session = Depends(get_db)):
   return db.query(Books).filter(Books.id == id).first()

@app.put('/update/{id}', response_model=Book)
def update_book(id:int, book:Book, db: Session = Depends(get_db)):
   b1 = db.query(Books).filter(Books.id == id).first()
   b1.id=book.id
   b1.title=book.title
   b1.author=book.author
   b1.publisher=book.publisher
   db.commit()
   return db.query(Books).filter(Books.id == id).first()


@app.delete('/delete/{id}')
def del_book(id:int, db: Session = Depends(get_db)):
   try:
      db.query(Books).filter(Books.id == id).delete()
      db.commit()
   except Exception as e:
      raise Exception(e)
   return {"delete status": "success"}