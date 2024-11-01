from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.note import Note
from ..schemas.note import NoteCreate, NoteUpdate, NoteResponse
from ..utils.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=NoteResponse)
async def create_note(
    note: NoteCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新笔记"""
    db_note = Note(**note.model_dump(), user_id=current_user.id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/", response_model=List[NoteResponse])
async def get_notes(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取所有笔记"""
    return db.query(Note).filter(Note.user_id == current_user.id).all()

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取特定笔记"""
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note_update: NoteUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新笔记"""
    db_note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    update_data = note_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_note, field, value)
    
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除笔记"""
    db_note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(db_note)
    db.commit()
    return {"message": "Note deleted successfully"} 