from typing import List
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session
from database import get_db_context
from schemas.task import Task
from models.task import TaskModel, TaskViewModel
from schemas.user import User
from schemas.company import Company
from services.auth import token_interceptor
from uuid import UUID
from .common import item_not_found_exception, access_denied_exception
from datetime import datetime

router = APIRouter(prefix="/tasks", tags=["Task"])

@router.get("")
async def get_tasks(
    db: Session = Depends(get_db_context),
    user: User = Depends(token_interceptor),
    ) -> List[TaskViewModel]:
    task_query = db.query(Task). \
        join(User).\
        join(Company). \
        filter(Company.id == user.company_id)

    if user.is_admin:
        return task_query.all()
    else :
        return task_query.filter(Task.owner_id == user.id).all()

@router.get("/{task_id}")
async def get_task_by_id(
    task_id: UUID, 
    db: Session = Depends(get_db_context),
    user: User = Depends(token_interceptor),
    )-> TaskViewModel:
    task = db.query(Task)\
                        .filter(Task.id == task_id)\
                        .first()
    # only allow to view if user is owner or admin
    
    if task is not None:
        if task.owner_id == user.id or user.is_admin:
            return task
        else:
            raise access_denied_exception()
    else:
        raise item_not_found_exception()
        

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskModel, 
    db: Session = Depends(get_db_context),
    user: User = Depends(token_interceptor),
    ) -> None:

    if user is None:
        raise access_denied_exception() 
    
    #validate user
    owner = db.query(User).filter(User.id == request.owner_id).first()
    if owner is None:
        raise item_not_found_exception() 
    
    task = Task(**request.dict())
    task.created_at = datetime.utcnow()

    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.put("/{task_id}")
async def update_task(
    task_id: UUID, 
    request: TaskModel, 
    db: Session = Depends(get_db_context),
    user: User = Depends(token_interceptor),
    ):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise item_not_found_exception()
    
    # only allow to edit if user is owner or admin
    if task.owner_id == user.id or user.is_admin:
        task.summary = request.summary
        task.description = request.description
        task.status = request.status
        task.priority = request.priority

        db.add(task)
        db.commit()
        db.refresh(task)

        return task
    else:
        raise access_denied_exception()
    

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID, 
    db: Session = Depends(get_db_context),
    user: User = Depends(token_interceptor)
    ):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise item_not_found_exception()
    
    # only allow to delete if user is owner or admin
    if task.owner_id == user.id or user.is_admin:
        db.delete(task)
        db.commit()
    else:
        raise access_denied_exception