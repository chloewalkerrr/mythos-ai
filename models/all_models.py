"""
Additional Models for Percy Jackson Database
"""

import enum

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from models.base import Base


# Enums for type safety
class QuestStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class MonsterThreatLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


class Cabin(Base):
    """Cabins at Camp Half-Blood"""

    __tablename__ = "cabins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cabin_number = Column(Integer, nullable=False, unique=True)
    patron_god_id = Column(Integer, ForeignKey("gods.id", ondelete="CASCADE"), nullable=False)
    description = Column(Text)
    color_scheme = Column(String(100))

    # Relationships
    patron_god = relationship("God", back_populates="cabin")
    members = relationship("Character", back_populates="cabin")

    __table_args__ = (
        CheckConstraint("cabin_number >= 1 AND cabin_number <= 20", name="check_cabin_number"),
    )

    def __repr__(self):
        return f"<Cabin(number={self.cabin_number})>"


class Monster(Base):
    """Mythological monsters and creatures"""

    __tablename__ = "monsters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    species = Column(String(100))  # e.g., "Minotaur", "Cyclops"
    threat_level = Column(String(20))  # low, medium, high, extreme
    description = Column(Text)
    weaknesses = Column(Text)
    abilities = Column(Text)

    # Relationships
    quest_encounters = relationship("QuestMonster", back_populates="monster")

    __table_args__ = (
        Index("idx_monster_name", "name"),
        CheckConstraint(
            "threat_level IN ('low', 'medium', 'high', 'extreme')", name="check_threat_level"
        ),
    )

    def __repr__(self):
        return f"<Monster(name='{self.name}', threat_level='{self.threat_level}')>"


class Location(Base):
    """Important locations in the series"""

    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, unique=True)
    location_type = Column(String(50))  # camp, city, underworld, olympus, etc.
    description = Column(Text)
    coordinates = Column(String(100))  # Optional: real-world coordinates
    realm = Column(String(50))  # mortal, olympus, underworld, etc.

    # Relationships
    quests_starting_here = relationship(
        "Quest", foreign_keys="[Quest.start_location_id]", back_populates="start_location"
    )
    quests_ending_here = relationship(
        "Quest", foreign_keys="[Quest.end_location_id]", back_populates="end_location"
    )

    def __repr__(self):
        return f"<Location(name='{self.name}', type='{self.location_type}')>"


class Quest(Base):
    """Adventures and missions"""

    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    objective = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(20), default="pending")
    difficulty_level = Column(
        Integer, CheckConstraint("difficulty_level >= 1 AND difficulty_level <= 10")
    )

    # Locations
    start_location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"))
    end_location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"))

    # Related book
    book_id = Column(Integer, ForeignKey("books.id", ondelete="SET NULL"))

    # Prophecy
    prophecy_id = Column(Integer, ForeignKey("prophecies.id", ondelete="SET NULL"))

    # Relationships
    start_location = relationship(
        "Location", foreign_keys=[start_location_id], back_populates="quests_starting_here"
    )
    end_location = relationship(
        "Location", foreign_keys=[end_location_id], back_populates="quests_ending_here"
    )
    book = relationship("Book", back_populates="quests")
    prophecy = relationship("Prophecy", back_populates="related_quest")
    participants = relationship(
        "QuestParticipant", back_populates="quest", cascade="all, delete-orphan"
    )
    monsters_encountered = relationship(
        "QuestMonster", back_populates="quest", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_quest_status", "status"),
        CheckConstraint(
            "status IN ('pending', 'in_progress', 'completed', 'failed')", name="check_quest_status"
        ),
    )

    def __repr__(self):
        return f"<Quest(id={self.id}, title='{self.title}', status='{self.status}')>"


class Book(Base):
    """Books in the Percy Jackson series"""

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, unique=True)
    book_number = Column(Integer, nullable=False)
    publication_date = Column(Date)
    isbn = Column(String(20), unique=True)
    page_count = Column(Integer)
    summary = Column(Text)

    # Relationships
    quests = relationship("Quest", back_populates="book")

    __table_args__ = (
        CheckConstraint("book_number >= 1", name="check_book_number"),
        CheckConstraint("page_count > 0", name="check_page_count"),
    )

    def __repr__(self):
        return f"<Book(title='{self.title}', number={self.book_number})>"


class Weapon(Base):
    """Magical weapons and artifacts"""

    __tablename__ = "weapons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    weapon_type = Column(String(50))  # sword, bow, shield, etc.
    material = Column(String(100))  # Celestial Bronze, Imperial Gold, etc.
    description = Column(Text)
    special_abilities = Column(Text)

    # Ownership
    owner_id = Column(Integer, ForeignKey("characters.id", ondelete="SET NULL"))

    # Relationships
    owner = relationship("Character", back_populates="weapons")

    def __repr__(self):
        return f"<Weapon(name='{self.name}', type='{self.weapon_type}')>"


class Prophecy(Base):
    """Important prophecies"""

    __tablename__ = "prophecies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200))
    text = Column(Text, nullable=False)
    speaker = Column(String(100))  # Who delivered it (e.g., "The Oracle")
    date_spoken = Column(Date)
    interpretation = Column(Text)
    fulfilled = Column(Boolean, default=False)

    # Relationships
    related_quest = relationship("Quest", back_populates="prophecy", uselist=False)

    def __repr__(self):
        return f"<Prophecy(id={self.id}, title='{self.title}', fulfilled={self.fulfilled})>"


class Power(Base):
    """Abilities and powers"""

    __tablename__ = "powers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    power_type = Column(String(50))  # elemental, physical, mental, etc.
    power_level = Column(Integer, CheckConstraint("power_level >= 1 AND power_level <= 10"))

    # Relationships
    character_powers = relationship("CharacterPower", back_populates="power")

    def __repr__(self):
        return f"<Power(name='{self.name}', type='{self.power_type}')>"


# Junction Tables


class CharacterPower(Base):
    """Many-to-many relationship between Characters and Powers"""

    __tablename__ = "character_powers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False)
    power_id = Column(Integer, ForeignKey("powers.id", ondelete="CASCADE"), nullable=False)
    proficiency_level = Column(
        Integer, CheckConstraint("proficiency_level >= 1 AND proficiency_level <= 10")
    )
    acquired_date = Column(Date)

    # Relationships
    character = relationship("Character", back_populates="powers")
    power = relationship("Power", back_populates="character_powers")

    __table_args__ = (Index("idx_character_power", "character_id", "power_id"),)

    def __repr__(self):
        return f"<CharacterPower(character_id={self.character_id}, power_id={self.power_id})>"


class QuestParticipant(Base):
    """Many-to-many relationship between Characters and Quests"""

    __tablename__ = "quest_participants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quest_id = Column(Integer, ForeignKey("quests.id", ondelete="CASCADE"), nullable=False)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(100))  # leader, member, support, etc.
    joined_date = Column(Date)

    # Relationships
    quest = relationship("Quest", back_populates="participants")
    character = relationship("Character", back_populates="quest_participations")

    __table_args__ = (Index("idx_quest_participant", "quest_id", "character_id"),)

    def __repr__(self):
        return (
            f"<QuestParticipant("
            f"quest_id={self.quest_id}, "
            f"character_id={self.character_id}, "
            f"role='{self.role}')>"
        )


class QuestMonster(Base):
    """Monsters encountered during quests"""

    __tablename__ = "quest_monsters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quest_id = Column(Integer, ForeignKey("quests.id", ondelete="CASCADE"), nullable=False)
    monster_id = Column(Integer, ForeignKey("monsters.id", ondelete="CASCADE"), nullable=False)
    encounter_description = Column(Text)
    defeated = Column(Boolean, default=False)

    # Relationships
    quest = relationship("Quest", back_populates="monsters_encountered")
    monster = relationship("Monster", back_populates="quest_encounters")

    def __repr__(self):
        return f"<QuestMonster(quest_id={self.quest_id}, monster_id={self.monster_id})>"
