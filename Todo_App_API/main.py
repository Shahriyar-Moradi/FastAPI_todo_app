
from fastapi import FastAPI, Depends
import models
from database import Base , SessionLocal , engine
from sqlalchemy.orm import Session
import asyncio
import uvicorn
import json
import time



Base.metadata.create_all(engine)

# create function to give us access to database 
def get_db():
    session=SessionLocal()
    try:
        yield session
    finally:
        session.close_all()

app=FastAPI()

ObjectDatabase={
    1:{'task':'learn fast api'},
    2:{'task':'call sanaz'},
    3:{'task':'continue ci/cd'},
}

@app.get("/")
def getItems(db:Session=Depends(get_db)):
    items=db.query(models.Item).all()
    return items
    # return ['Item1','Item2','Item3','Item4']
    # return ObjectDatabase

# first way with object data
# @app.get("/{id}")
# def getItem(id:int):
#     return ObjectDatabase[id]

async def simulate_async_processing():
    await asyncio.sleep(5)  # Simulate a time-consuming task
    return "Async processing complete"

@app.get("/async")
async def root():
    result = await simulate_async_processing()
    return {"message": result}

@app.get("/{id}")
def getItem(id:int,db:Session=Depends(get_db)):
    item=db.query(models.Item).get(id)
    return item
    

# first and simple  
# @app.post("/")
# def addItem(task:str):
#     # return ObjectDatabase.update({4:{'task':'learn fast api 2'}})
#     newId=len(ObjectDatabase.keys())+1
#     ObjectDatabase[newId]={'task':task}
#     return ObjectDatabase

# Second way with structured data format from our models
# @app.post("/")
# def addItem(item:modelss.Item):
#     newId=len(ObjectDatabase.keys())+1
#     ObjectDatabase[newId]={'task':item.task}
#     return ObjectDatabase

#thrid way with using databas db
@app.post("/")
def addItem(item:models.TaskItem,db:Session=Depends(get_db)):
    # update task variable in Item Class that's why task=
    item=models.Item(task=item.task)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# @app.put("/{id}")
# def updateItem(id:int,item:models.TaskItem):
#     ObjectDatabase[id]['task']=item.task
#     return ObjectDatabase

@app.put("/{id}")
def updateItem(id:int,item:models.TaskItem,db:Session=Depends(get_db)):
    updated_item=db.query(models.Item).get(id)
    updated_item.task=item.task
    db.commit()
    # db.refresh(item)
    return updated_item


# @app.delete("/{id}")
# def deleteItem(id:int):
#     del ObjectDatabase[id]
#     return ObjectDatabase

@app.delete("/{id}")
def deleteItem(id:int,db:Session=Depends(get_db)):
    deleted_item=db.query(models.Item).get(id)
    db.delete(deleted_item)
    db.commit()
    db.close()
    return deleted_item


def get_data_from_database():
    # Replace this with your actual database retrieval logic
    # For simplicity, let's assume we're just returning dummy data
    data = [
        {"id": 1, "name": "John"},
        {"id": 2, "name": "Jane"},
        {"id": 3, "name": "Alice"}
    ]
    return data

@app.get("/data")
def get_live_data():
    data = get_data_from_database()
    return data

@app.get("/live-data")
def get_live_data_dynamic():
    while True:
        data = get_data_from_database()
        yield json.dumps(data)
        time.sleep(60)  # Sleep for 60 seconds before fetching new data




# Run the application
# if __name__ == "__main__":
#     Base.metadata.create_all(bind=engine)
#     uvicorn.run(app, host="0.0.0.0", port=8000)