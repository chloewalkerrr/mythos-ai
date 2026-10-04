"""
God Model
"""

from sqlalchemy import Column, Index, Integer, String, Text
from sqlalchemy.orm import relationship

from models.base import Base


class God(Base):
    __tablename__ = "gods"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Basic Information
    name = Column(String(100), nullable=False, unique=True)
    roman_name = Column(String(100))
    title = Column(String(200))  # e.g., "God of the Sea"
    domain = Column(String(100))  # e.g., "Sea, Earthquakes, Horses"
    symbol = Column(String(100))  # e.g., "Trident"
    description = Column(Text)

    # Relationships
    children = relationship("Character", back_populates="parent_god")
    cabin = relationship("Cabin", back_populates="patron_god", uselist=False)

    # Index
    __table_args__ = (Index("idx_god_name", "name"),)

    def __repr__(self):
        return f"<God(id={self.id}, name='{self.name}', title='{self.title}')>"
