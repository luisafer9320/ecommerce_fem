from fastapi import APIRouter

router = APIRouter ()

@router.get(path="/", tags=["Home"])
def home():
    return {"message": "Ecommerce API FemCoders Madrid P5"}