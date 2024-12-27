from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.db.session import get_db
from backend.db.models import Category
from backend.models.category import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/category", tags=["category"])


async def get_category_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(Category).where(Category.name == name))
    return result.scalars().first()


async def get_category_by_id(db: AsyncSession, category_id: UUID):
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalars().first()


@router.get("/", response_model=list[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    categories = result.scalars().all()
    if not categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No categories found")
    return [CategoryResponse.model_validate(category, from_attributes=True) for category in categories]


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    existing_category = await get_category_by_name(db, category.name)
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists"
        )

    new_category = Category(name=category.name.capitalize())
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return CategoryResponse.model_validate(new_category, from_attributes=True)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: UUID, db: AsyncSession = Depends(get_db)):
    category = await get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    await db.delete(category)
    await db.commit()
