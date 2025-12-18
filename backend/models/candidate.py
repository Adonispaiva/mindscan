from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from backend.database.base import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relação com sessões MindScan
    mindscan_tests = relationship(
        "MindscanTest",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Candidate id={self.id} name={self.name}>"
