from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    content = Column(Text, nullable=False)

    summary = Column(Text)

    user_id = Column(Integer, ForeignKey("users.id"))