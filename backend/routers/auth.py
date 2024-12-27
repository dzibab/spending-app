from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.db.session import get_db
from backend.db.models import User as UserDB
from backend.models.auth import TokenResponse
from backend.utils.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


async def authenticate_user(db: AsyncSession, username: str, password: str):
    result = await db.execute(select(UserDB).filter(UserDB.email == username))
    user = result.scalars().first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
