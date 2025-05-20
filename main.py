from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import datetime
from manager import InsightManager
from insight import Insight  # זוהי המחלקה הלוגית שלך
from typing import Optional
from fastapi import HTTPException

app = FastAPI()
manager = InsightManager()
manager.load()


# === מחלקות API ===
class InsightBase(BaseModel):
    title: str
    subtitle: str
    content: str
    tags: Optional[List[str]] = None
    date: Optional[Union[str, datetime]] = None
    connections: Optional[List[int]] = None

class InsightCreate(InsightBase):
    pass

class InsightOut(InsightBase):
    id: int

class InsightUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    date: Optional[datetime] = None
    connections: Optional[List[int]] = None

# === API ===

@app.get("/insights", response_model=List[InsightOut])
async def get_insights():
    insights = manager.list_insights()
    return insights


@app.get("/insights/{insight_id}", response_model=InsightOut)
async def get_insight(insight_id: int):
    insight = manager.get_insight_by_id(insight_id)
    if insight is None:
        raise HTTPException(status_code=404, detail="Insight not found")
    return insight


@app.post("/insights", response_model=InsightOut, status_code=status.HTTP_201_CREATED)
async def create_insight(insight_data: InsightCreate):
    new_insight = Insight(
        title=insight_data.title,
        subtitle=insight_data.subtitle,
        content=insight_data.content,
        tags=insight_data.tags,
        date=insight_data.date,
        connections=insight_data.connections
    )
    manager.add_insight(new_insight)
    manager.save()
    return InsightOut(**new_insight.to_dict())

@app.put("/insights/{insight_id}", response_model=InsightOut, status_code=status.HTTP_200_OK)
async def update_insight(insight_id: int, updated_data: InsightUpdate):
    data_to_update = updated_data.dict(exclude_unset=True)
    if not data_to_update:
        raise HTTPException(status_code=400, detail="No data provided for update")
    manager.update_insight(insight_id, **data_to_update)
    manager.save()

    updated = next((i for i in manager.insights if i.id == insight_id), None)
    if not updated:
        raise HTTPException(status_code=404, detail="Insight not found")
    
    return InsightOut(**updated.to_dict())


@app.delete("/insights/{insight_id}",  status_code=204)
async def delete_insight(insight_id: int):
    insight_to_remove = manager.remove_insight(insight_id)
    if not insight_to_remove:
        raise HTTPException(status_code=404, detail="Insight not found")
        


