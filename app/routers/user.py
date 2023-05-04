from typing import List
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session
from database import get_db_context
from schemas.user import User
from models.user import UserViewModel, UserModel, UserCreateModel
from uuid import UUID
from .common import item_not_found_exception, access_denied_exception
from datetime import datetime
from schemas.user import get_password_hash
from services.auth import token_interceptor
from schemas.company import Company

router = APIRouter(prefix="/users", tags=["User"])

@router.get("")
async def get_users(
    db: Session = Depends(get_db_context),
    user: User = Depends(token_interceptor),
    ) -> List[UserViewModel]:
    if not user.is_admin:
        raise access_denied_exception()
    
    return db.query(User).all()

@router.get("/{user_id}")
async def get_user_by_id(
    user_id: UUID, 
    db: Session = Depends(get_db_context),
    user: User = Depends(token_interceptor),
    )-> UserViewModel:
    search_user = db.query(User)\
                    .filter(User.id == user_id)\
                    .first()
    if search_user is not None:
        if user.is_admin:
            return search_user
        else: 
            if user.id == user_id:
                return search_user
            else:
                raise access_denied_exception()
    raise item_not_found_exception()

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    request: UserCreateModel, 
    db: Session = Depends(get_db_context),
    user: User = Depends(token_interceptor)
    ) -> None:

    if not user.is_admin:
        raise access_denied_exception()
    
    user = User(**UserModel(
        email=request.email,
        username=request.username,
        hashed_password=get_password_hash(request.password),
        first_name=request.first_name,
        last_name=request.last_name,
        is_active=request.is_active,
        is_admin=request.is_admin,
        company_id=request.company_id
    ).dict())

    user.created_at = datetime.utcnow()
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.put("/{user_id}")
async def update_user(
    user_id: UUID, 
    request: UserCreateModel, 
    db: Session = Depends(get_db_context),
    user: User = Depends(token_interceptor)
    ):
    if not user.is_admin:
        raise access_denied_exception()
    editUser = db.query(User).filter(User.id == user_id).first()

    if editUser is None:
        raise item_not_found_exception()
    
    editUser.email = request.email
    editUser.first_name = request.first_name
    editUser.last_name = request.last_name
    editUser.hashed_password = get_password_hash(request.password)
    editUser.is_active = request.is_active
    editUser.is_admin = request.is_admin

    #validate company
    company = db.query(Company).filter(Company.id == request.company_id).first()
    if company is None:
        raise item_not_found_exception() 
    editUser.company_id = request.company_id

    db.add(editUser)
    db.commit()
    db.refresh(editUser)

    return editUser

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID, 
    db: Session = Depends(get_db_context),
    user: User = Depends(token_interceptor)
    ):
    if not user.is_admin:
        raise access_denied_exception()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise item_not_found_exception()
    
    db.delete(user)
    db.commit()