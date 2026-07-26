"""
Create Database Tables
Run this script to create all tables in the database
"""
import sys
sys.path.append('..')

from models import Base, engine
from models.character import Character
from models.god import God
from models.all_models import (
    Cabin, Monster, Location, Quest, Book, 
    Weapon, Prophecy, Power, CharacterPower, 
    QuestParticipant, QuestMonster
)

def create_tables():
    """Create all tables in the database"""
    print("Creating database tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✓ All tables created successfully!")
        
        print("\nCreated tables:")
        for table_name in Base.metadata.tables.keys():
            print(f"  - {table_name}")
            
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = create_tables()
    if success:
        print("\n✓ Database initialization complete!")
    else:
        print("\n✗ Database initialization failed!")
        sys.exit(1)
