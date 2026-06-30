from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas import ProductCreate, ProductRead, ProductUpdate
from app.crud import create_product, get_products, get_product, update_product, delete_product

router = APIRouter()

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product_endpoint(product_in: ProductCreate, db: AsyncSession = Depends(get_session)):
    return await create_product(db, product_in)

@router.get("/", response_model=List[ProductRead])
async def list_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    return await get_products(db, skip, limit)

@router.get("/{product_id}", response_model=ProductRead)
async def get_product_endpoint(product_id: int, db: AsyncSession = Depends(get_session)):
    product = await get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductRead)
async def update_product_endpoint(product_id: int, product_in: ProductUpdate, db: AsyncSession = Depends(get_session)):
    product = await get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return await update_product(db, product, product_in)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_endpoint(product_id: int, db: AsyncSession = Depends(get_session)):
    product = await get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await delete_product(db, product)
    return
