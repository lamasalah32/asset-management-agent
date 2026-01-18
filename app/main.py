from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from langchain_core.messages import HumanMessage
from llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent

from database import SessionLocal, engine, get_db
from tools import query_assets
import models, schemas, crud
from system_prompt import SYSTEM_PROMPT


models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="AI Asset Management API")

@app.post("/assets", response_model=schemas.AssetOut)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    return crud.create_asset(db, asset)

@app.get("/assets", response_model=list[schemas.AssetOut])
def list_assets(db: Session = Depends(get_db)):
    return crud.get_assets(db)

@app.get("/assets/{asset_id}", response_model=schemas.AssetOut)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = crud.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@app.put("/assets/{asset_id}", response_model=schemas.AssetOut)
def update_asset(asset_id: int, asset: schemas.AssetUpdate, db: Session = Depends(get_db)):
    updated = crud.update_asset(db, asset_id, asset)
    if not updated:
        raise HTTPException(status_code=404, detail="Asset not found")
    return updated

@app.delete("/assets/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_asset(db, asset_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"message": "Asset deleted"}

@app.post("/agent/query", response_model=schemas.AgentResponse)
def query_agent(req: schemas.AgentRequest):
    model = get_llm()
    tools = [query_assets]
    agent = create_agent(
        model,
        tools,
        system_prompt=SYSTEM_PROMPT,
    )

    answer = agent.invoke(
        {
            "messages": [
                HumanMessage(content=req.question)
            ]
        }
    )
    
    final_answer = answer["messages"][-1].content

    return schemas.AgentResponse(
        answer=final_answer or "No answer generated",
        sources=[],
    )

