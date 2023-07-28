import uvicorn ##ASGI
from fastapi import FastAPI, Body
from transformers import BertForSequenceClassification
from transformers import BertTokenizer
from routers.routers import router
from db.database import Database
import  db.model   
from db.database import db_class



app = FastAPI()

@app.get('/')
def index():
    return {'message': 'Hello from Classification'}

@app.on_event("startup")
async def startup_event():
    db_class1=Database()
    db.model.Base.metadata.create_all(bind=db_class.engine)

app.include_router(router, prefix="/detection", tags=["detection"])

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=9001, reload=True)
    
#uvicorn app.main:app --reload
