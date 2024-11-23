from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.db.session import get_db
from backend.models.user import UserResponse
from backend.utils.security import verify_password, create_access_token
from backend.db.models import User as UserDB

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=UserResponse)
async def login_for_access_token(email: str, password: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserDB).filter(UserDB.email == email))
    user = result.scalars().first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
