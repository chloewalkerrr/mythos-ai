"""
Character Model - represents demigods and characters
"""

import enum

from sqlalchemy import CheckConstraint, Column, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import relationship

from models.base import Base


class CharacterStatus(enum.Enum):
    ALIVE = "alive"
    DECEASED = "deceased"
    MISSING = "missing"


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # unique name constraint
    name = Column(String(100), nullable=False, unique=True)
    age = Column(Integer)  # check constraint is below in table_args
    gender = Column(String(20))
    description = Column(Text)

    # foreign keys to gods and cabins tables
    parent_god_id = Column(Integer, ForeignKey("gods.id", ondelete="SET NULL"))
    cabin_id = Column(Integer, ForeignKey("cabins.id", ondelete="SET NULL"))

    status = Column(
        Enum(CharacterStatus, values_callable=lambda x: [e.value for e in x]),
        default=CharacterStatus.ALIVE,
    )
    first_appearance = Column(String(100))

    # relationships - sqlalchemy handles the joins
    parent_god = relationship("God", back_populates="children")
    cabin = relationship("Cabin", back_populates="members")
    powers = relationship(
        "CharacterPower", back_populates="character", cascade="all, delete-orphan"
    )
    quest_participations = relationship(
        "QuestParticipant", back_populates="character", cascade="all, delete-orphan"
    )
    weapons = relationship("Weapon", back_populates="owner")

    # constraints and indexes
    # note: had to put check constraint here not in column definition bc mariadb syntax
    __table_args__ = (
        CheckConstraint("age >= 0 AND age <= 150", name="check_age"),
        Index("idx_character_name", "name"),
        Index("idx_character_parent_god", "parent_god_id"),
    )
