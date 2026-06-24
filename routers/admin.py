from fastapi import APIRouter, Depends

from dependencies import get_admin_user
from database import SessionLocal

from models.user import User
from models.note import Note

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/users")
def get_all_users(
    current_admin=Depends(get_admin_user)
):

    db = SessionLocal()

    users = db.query(User).all()

    db.close()

    return users


@router.get("/notes")
def get_all_notes(
    current_admin=Depends(get_admin_user)
):

    db = SessionLocal()

    notes = db.query(Note).all()

    db.close()

    return notes


@router.delete("/notes/{note_id}")
def delete_any_note(
    note_id: int,
    current_admin=Depends(get_admin_user)
):

    db = SessionLocal()

    note = db.query(Note).filter(
        Note.id == note_id
    ).first()

    if not note:
        db.close()
        return {
            "message": "Note not found"
        }

    db.delete(note)
    db.commit()

    db.close()

    return {
        "message": "Note deleted by admin"
    }