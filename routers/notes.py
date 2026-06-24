from fastapi import APIRouter, Depends

from dependencies import get_current_user
from services.gemini import generate_notes
from database import SessionLocal
from models.note import Note


router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


@router.get("/generate")
def notes_generate(
    topic: str,
    words: int,
    language: str = "English",
    current_user=Depends(get_current_user)
):

    notes = generate_notes(
        topic,
        words,
        language
    )

    summary = generate_notes(
        f"Give a short summary for {topic}",
        100,
        language
    )

    db = SessionLocal()

    new_note = Note(
        title=topic,
        content=notes,
        summary=summary,
        user_id=current_user["id"]
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    db.close()

    return {
        "message": "Notes Generated & Saved Successfully",
        "topic": topic,
        "language": language,
        "notes": notes,
        "summary": summary
    }


@router.get("/my-notes")
def my_notes(
    current_user=Depends(get_current_user)
):

    db = SessionLocal()

    notes = db.query(Note).filter(
        Note.user_id == current_user["id"]
    ).all()

    db.close()

    return notes


@router.get("/{note_id}")
def get_note(
    note_id: int,
    current_user=Depends(get_current_user)
):

    db = SessionLocal()

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user["id"]
    ).first()

    db.close()

    if not note:
        return {
            "message": "Note not found"
        }

    return note


@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    current_user=Depends(get_current_user)
):

    db = SessionLocal()

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user["id"]
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
        "message": "Note Deleted Successfully"
    }