from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.db.session import get_db
from backend.models.user import UserCreate, UserUpdate, UserResponse
from backend.db.models import User as UserDB
from backend.utils.security import hash_password


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserDB).filter(UserDB.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered."
        )

    hashed_password = hash_password(user.password)
    new_user = UserDB(
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.get("/{user_id:uuid}", response_model=UserResponse)
async def read_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(UserDB).filter(UserDB.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


@router.put("/{user_id:uuid}", response_model=UserResponse)
async def update_user(user_id: UUID, user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserDB).filter(UserDB.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    if user_update.email:
        user.email = user_update.email

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id:uuid}", response_model=dict)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserDB).filter(UserDB.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    await db.delete(user)
    await db.commit()
    return {"message": "User deleted successfully."}
