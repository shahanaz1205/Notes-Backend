from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import FileResponse

from dependencies import get_current_user
from database import SessionLocal
from models.note import Note

from services.gemini import summarize_text, ask_pdf_question

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from textwrap import wrap

from pypdf import PdfReader

router = APIRouter(
    prefix="/pdf",
    tags=["PDF"]
)


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    try:
        pdf_path = file.filename

        with open(pdf_path, "wb") as f:
            f.write(await file.read())

        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        if not text.strip():
            return {
                "filename": file.filename,
                "summary": "No readable text found in PDF"
            }

        try:
            summary = summarize_text(text[:5000])

        except Exception:
            summary = (
                "Gemini API unavailable or quota exceeded.\n\n"
                + text[:1000]
            )

        db = SessionLocal()

        new_note = Note(
            title=file.filename,
            content=text[:5000],
            summary=summary,
            user_id=current_user["id"]
        )

        db.add(new_note)
        db.commit()
        db.refresh(new_note)

        note_id = new_note.id

        db.close()

        return {
            "filename": file.filename,
            "summary": summary,
            "note_id": note_id,
            "message": "PDF uploaded and summary saved"
        }

    except Exception as e:
        return {
            "message": "Error processing PDF",
            "error": str(e)
        }


@router.get("/download/{note_id}")
def download_pdf(
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

    pdf_file = f"note_{note_id}.pdf"

    c = canvas.Canvas(pdf_file, pagesize=letter)

    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, note.title)

    c.setFont("Helvetica", 11)

    y = height - 90

    paragraphs = note.content.split("\n")

    for paragraph in paragraphs:

        wrapped_lines = wrap(paragraph, width=90)

        if not wrapped_lines:
            y -= 15

        for line in wrapped_lines:

            c.drawString(50, y, line)

            y -= 15

            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = height - 50

    c.save()

    return FileResponse(
        pdf_file,
        media_type="application/pdf",
        filename=pdf_file
    )


@router.get("/download-summary/{note_id}")
def download_summary_pdf(
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

    pdf_file = f"summary_{note_id}.pdf"

    c = canvas.Canvas(pdf_file, pagesize=letter)

    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Summary - {note.title}")

    c.setFont("Helvetica", 11)

    y = height - 90

    summary_text = (
        note.summary
        if note.summary
        else "No summary available"
    )

    paragraphs = summary_text.split("\n")

    for paragraph in paragraphs:

        wrapped_lines = wrap(paragraph, width=90)

        if not wrapped_lines:
            y -= 15

        for line in wrapped_lines:

            c.drawString(50, y, line)

            y -= 15

            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = height - 50

    c.save()

    return FileResponse(
        pdf_file,
        media_type="application/pdf",
        filename=pdf_file
    )


@router.get("/ask")
def ask_question_from_pdf(
    note_id: int,
    question: str,
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

    answer = ask_pdf_question(
        note.content,
        question
    )

    return {
        "note_id": note_id,
        "question": question,
        "answer": answer
    }