from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI(
    title="Sample FastAPI App",
    description="A minimal FastAPI application demonstrating CRUD operations, ready for Docker/Kubernetes deployment.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# In-memory store (replace with a real DB in production)
# ---------------------------------------------------------------------------
items: dict[str, dict] = {}


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class Item(ItemCreate):
    id: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "FastAPI app is running"}


@app.get("/health", tags=["Health"])
def health_check():
    """Kubernetes liveness / readiness probe endpoint."""
    return {"status": "healthy"}


@app.get("/items", response_model=list[Item], tags=["Items"])
def list_items():
    return list(items.values())


@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
def get_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.post("/items", response_model=Item, status_code=201, tags=["Items"])
def create_item(body: ItemCreate):
    item_id = str(uuid.uuid4())
    item = Item(id=item_id, **body.model_dump())
    items[item_id] = item.model_dump()
    return item


@app.patch("/items/{item_id}", response_model=Item, tags=["Items"])
def update_item(item_id: str, body: ItemUpdate):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    stored = items[item_id]
    updates = body.model_dump(exclude_unset=True)
    stored.update(updates)
    items[item_id] = stored
    return stored


@app.delete("/items/{item_id}", status_code=204, tags=["Items"])
def delete_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
