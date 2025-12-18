from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database.base import Base


class MindscanTest(Base):
    __tablename__ = "mindscan_tests"

    id = Column(Integer, primary_key=True, index=True)

    # Relações
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)

    user = relationship("User", back_populates="mindscan_tests")
    candidate = relationship("Candidate", back_populates="mindscan_tests")

    # Estado da sessão
    status = Column(String(50), default="pending", nullable=False)

    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Metadados futuros
    engine_version = Column(String(50), nullable=True)
    report_type = Column(String(50), nullable=True)

    def __repr__(self):
        return (
            f"<MindscanTest id={self.id} "
            f"user_id={self.user_id} "
            f"candidate_id={self.candidate_id} "
            f"status={self.status}>"
        )
