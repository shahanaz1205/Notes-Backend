from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database import Base

class PDFUpload(Base):
    __tablename__ = "pdf_uploads"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)

    filepath = Column(String, nullable=False)

    summary = Column(Text)

    user_id = Column(Integer, ForeignKey("users.id"))