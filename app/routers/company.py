from fastapi import APIRouter, Depends
from models.company import CompanyModel, CompanyViewModel
from sqlalchemy.orm import Session
from database import get_db_context
from schemas.company import Company
from uuid import UUID
from starlette import status
from datetime import datetime
from .common import item_not_found_exception, access_denied_exception
from schemas.user import User
from services.auth import token_interceptor

router = APIRouter(prefix="/companies", tags =["Company"])

@router.get("", response_model=list[CompanyViewModel])
async def get_all_companies(
    db: Session = Depends(get_db_context),
    user: User = Depends(token_interceptor),
    ):
    if not user.is_admin:
        raise access_denied_exception()
    return db.query(Company).all()

@router.get("/{company_id}")
async def get_company_by_id(
    company_id: UUID, 
    db: Session = Depends(get_db_context),
    user: User = Depends(token_interceptor),
    )-> CompanyViewModel:
    if not user.is_admin:
        raise access_denied_exception()
    
    company = db.query(Company)\
                    .filter(Company.id == company_id)\
                    .first()
    if company is not None:
        return company
    raise item_not_found_exception()

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_company(
    request: CompanyModel, 
    db: Session = Depends(get_db_context),
    user: User = Depends(token_interceptor),
    ) -> None:
    if not user.is_admin:
        raise access_denied_exception()
    
    company = Company(**request.dict())
    company.created_at = datetime.utcnow()

    db.add(company)
    db.commit()
    db.refresh(company)
    return company

@router.put("/{company_id}")
async def update_company(
    company_id: UUID, 
    request: CompanyModel, 
    db: Session = Depends(get_db_context),
    user: User = Depends(token_interceptor),
    ):
    if not user.is_admin:
        raise access_denied_exception()
    
    company = db.query(Company).filter(Company.id == company_id).first()

    if company is None:
        raise item_not_found_exception()
    
    company.name = request.name if request.name else company.name
    company.description = request.description if request.description else company.description
    company.mode = request.mode if request.mode else company.mode
    company.rating = request.rating if request.rating else company.rating
    company.updated_at = datetime.utcnow()

    db.add(company)
    db.commit()
    db.refresh(company)

    return company

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: UUID, 
    db: Session = Depends(get_db_context),
    user: User = Depends(token_interceptor),
    ):
    if not user.is_admin:
        raise access_denied_exception()
    
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise item_not_found_exception()
    
    db.delete(company)
    db.commit()
