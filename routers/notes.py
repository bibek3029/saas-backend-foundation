from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from routers.auth import get_current_user

from database.database import get_db
from models.user import User
from models.note import Note
from schemas import NoteSchema
from core.security import verify_access_token, hash_password, create_access_token


router = APIRouter()
# Note table endpoints
@router.post("/notes")
def create_note(note: NoteSchema,current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_note = Note(title=note.title, content=note.content, user_id=current_user.id)
    #save note
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {"message": "note created successfully", "note": new_note}
    
@router.get("/notes")
def get_notes(note: NoteSchema,current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notes = db.query(Note).filter(Note.user_id == current_user.id).all()
    return notes

@router.put("/notes/{note_id}")
def update_note(note_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="note not found")
    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="not authorized to update this note")
    db.commit()
    db.refresh(note)
    return {"message": "note updated successfully", "note": note}
@router.delete("/notes/{note_id}")
def delete_note(note_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="note not found")
    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="not authorized to delete this note")
    db.delete(note)
    db.commit()
    
    return {"message": "note deleted successfully"}
