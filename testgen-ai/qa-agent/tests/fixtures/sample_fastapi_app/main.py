
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(
    title="Sample FastAPI App",
    description="A tiny FastAPI application with CRUD operations for demonstration.",
    version="1.0.0",
)

class Item(BaseModel):
    id: int
    name: str
    description: str | None = None

items_db: Dict[int, Item] = {}

@app.get("/items/", response_model=List[Item])
async def read_items():
    """Retrieve a list of all items."""
    return list(items_db.values())

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    """Retrieve a single item by its ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.post("/items/", response_model=Item, status_code=201)
async def create_item(item: Item):
    """Create a new item."""
    if item.id in items_db:
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items_db[item.id] = item
    return item

@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    """Delete an item by its ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": "Item deleted"}
