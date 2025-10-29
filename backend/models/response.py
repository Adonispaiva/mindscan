from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer)
    answer = Column(String)
