from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.db.session import get_db
from backend.models.user import UserCreate, UserUpdate, UserResponse
from backend.db.models import User as UserDB
from backend.utils.security import hash_password, get_current_user

router = APIRouter(prefix="/users", tags=["users"])


async def get_user_by_id(user_id: UUID, db: AsyncSession):
    result = await db.execute(select(UserDB).filter(UserDB.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


async def get_user_by_email(email: str, db: AsyncSession):
    result = await db.execute(select(UserDB).filter(UserDB.email == email))
    return result.scalars().first()


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(user.email, db)
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


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserDB = Depends(get_current_user)):
    return current_user


@router.get("/{user_id:uuid}", response_model=UserResponse)
async def read_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(user_id, db)
    return user


@router.put("/{user_id:uuid}", response_model=UserResponse)
async def update_user(user_id: UUID, user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(user_id, db)

    if user_update.email:
        user.email = user_update.email

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id:uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(user_id, db)
    await db.delete(user)
    await db.commit()
