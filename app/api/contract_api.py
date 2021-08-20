from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/contracts",
    tags=["contracts"],
)

@router.get("/{id}")
def get(id):
    return {"id": id}