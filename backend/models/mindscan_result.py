from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from backend.database.base import Base


class MindscanResult(Base):
    __tablename__ = "mindscan_results"

    id = Column(Integer, primary_key=True, index=True)

    test_id = Column(
        Integer,
        ForeignKey("mindscan_tests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    result = Column(JSON, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    test = relationship("MindscanTest", back_populates="results")

    def __repr__(self) -> str:
        return f"<MindscanResult id={self.id} test_id={self.test_id}>"
