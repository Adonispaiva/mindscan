from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.database.base import Base


class MindscanReport(Base):
    __tablename__ = "mindscan_reports"

    id = Column(Integer, primary_key=True, index=True)

    test_id = Column(
        Integer,
        ForeignKey("mindscan_tests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    path = Column(String(512), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    test = relationship("MindscanTest", back_populates="reports")

    def __repr__(self) -> str:
        return f"<MindscanReport id={self.id} test_id={self.test_id} path={self.path}>"
