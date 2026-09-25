from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.database import get_session
from app.models.user import User, UserCreate, UserPublic
from app.security import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register", response_model=UserPublic)
def register(
    user: UserCreate,
    session: Session = Depends(get_session)
):

    existing_user = session.exec(
        select(User).where(
            User.username == user.username
        )
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password)
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user



@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):

    user = session.exec(
        select(User).where(
            User.username == form_data.username
        )
    ).first()


    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    if not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    token = create_access_token(
        user.username
    )


    return {
        "access_token": token,
        "token_type": "bearer"
    }