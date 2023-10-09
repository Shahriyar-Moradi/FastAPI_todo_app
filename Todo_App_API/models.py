
from sqlalchemy import Column , Integer , String,Float
from database import Base
from pydantic import BaseModel

class Item(Base):
    __tablename__="items"
    id = Column(Integer, primary_key=True)
    task=Column(Integer)

class TaskItem(BaseModel):
    task:str
