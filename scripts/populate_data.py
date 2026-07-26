"""
Populate Database with Percy Jackson Data
"""
import sys
sys.path.append('..')

from datetime import date
from models import SessionLocal
from models.character import Character
from models.god import God
from models.all_models import (
    Cabin, Monster, Location, Quest, Book,
    Weapon, Prophecy, Power, CharacterPower,
    QuestParticipant, QuestMonster
)

def populate_database():
    """Populate database with sample Percy Jackson data"""
    db = SessionLocal()
    
    try:
        print("Populating database with Percy Jackson data...")
        
        # 1. Create Gods
        print("\n1. Creating Gods...")
        gods = [
            God(name="Zeus", roman_name="Jupiter", title="King of the Gods", 
                domain="Sky, Thunder, Lightning", symbol="Lightning Bolt",
                description="King of the gods and ruler of Mount Olympus"),
            God(name="Poseidon", roman_name="Neptune", title="God of the Sea", 
                domain="Sea, Earthquakes, Horses", symbol="Trident",
                description="God of the sea, earthquakes, and horses"),
            God(name="Hades", roman_name="Pluto", title="God of the Underworld", 
                domain="Underworld, Death, Riches", symbol="Helm of Darkness",
                description="God of the underworld and the dead"),
            God(name="Athena", roman_name="Minerva", title="Goddess of Wisdom", 
                domain="Wisdom, Battle Strategy, Crafts", symbol="Owl",
                description="Goddess of wisdom and strategic warfare"),
            God(name="Ares", roman_name="Mars", title="God of War", 
                domain="War, Violence, Bloodshed", symbol="Spear and Shield",
                description="God of war and violence"),
            God(name="Apollo", roman_name="Apollo", title="God of the Sun", 
                domain="Sun, Music, Poetry, Prophecy, Healing", symbol="Lyre and Bow",
                description="God of the sun, music, and prophecy"),
            God(name="Artemis", roman_name="Diana", title="Goddess of the Hunt", 
                domain="Hunt, Moon, Wilderness", symbol="Bow and Arrows",
                description="Goddess of the hunt and the moon"),
            God(name="Hermes", roman_name="Mercury", title="Messenger of the Gods", 
                domain="Travel, Thieves, Commerce, Communication", symbol="Caduceus",
                description="Messenger god and god of travelers and thieves"),
        ]
        db.add_all(gods)
        db.commit()
        print(f"  ✓ Created {len(gods)} gods")
        
        # Refresh to get IDs
        for god in gods:
            db.refresh(god)
        
        # 2. Create Cabins
        print("\n2. Creating Cabins...")
        cabins = [
            Cabin(cabin_number=1, patron_god_id=gods[0].id, description="Zeus's cabin", color_scheme="White and Blue"),
            Cabin(cabin_number=3, patron_god_id=gods[1].id, description="Poseidon's cabin", color_scheme="Blue and Green"),
            Cabin(cabin_number=6, patron_god_id=gods[3].id, description="Athena's cabin", color_scheme="Gray and Blue"),
            Cabin(cabin_number=11, patron_god_id=gods[7].id, description="Hermes's cabin", color_scheme="Brown and Orange"),
            Cabin(cabin_number=7, patron_god_id=gods[5].id, description="Apollo's cabin", color_scheme="Gold and Yellow"),
        ]
        db.add_all(cabins)
        db.commit()
        print(f"  ✓ Created {len(cabins)} cabins")
        
        # 3. Create Characters
        print("\n3. Creating Characters...")
        characters = [
            Character(name="Percy Jackson", age=16, gender="Male", 
                     parent_god_id=gods[1].id, cabin_id=cabins[1].id,
                     description="Son of Poseidon, main protagonist",
                     status="alive", first_appearance="The Lightning Thief"),
            Character(name="Annabeth Chase", age=16, gender="Female",
                     parent_god_id=gods[3].id, cabin_id=cabins[2].id,
                     description="Daughter of Athena, architect and strategist",
                     status="alive", first_appearance="The Lightning Thief"),
            Character(name="Grover Underwood", age=28, gender="Male",
                     description="Satyr, Percy's best friend and protector",
                     status="alive", first_appearance="The Lightning Thief"),
            Character(name="Luke Castellan", age=23, gender="Male",
                     parent_god_id=gods[7].id, cabin_id=cabins[3].id,
                     description="Son of Hermes, former counselor turned antagonist",
                     status="deceased", first_appearance="The Lightning Thief"),
            Character(name="Thalia Grace", age=15, gender="Female",
                     parent_god_id=gods[0].id, cabin_id=cabins[0].id,
                     description="Daughter of Zeus, Hunter of Artemis",
                     status="alive", first_appearance="The Sea of Monsters"),
            Character(name="Nico di Angelo", age=14, gender="Male",
                     parent_god_id=gods[2].id,
                     description="Son of Hades, Ghost King",
                     status="alive", first_appearance="The Titan's Curse"),
            Character(name="Clarisse La Rue", age=16, gender="Female",
                     parent_god_id=gods[4].id,
                     description="Daughter of Ares, tough and aggressive warrior",
                     status="alive", first_appearance="The Lightning Thief"),
        ]
        db.add_all(characters)
        db.commit()
        print(f"  ✓ Created {len(characters)} characters")
        
        # 4. Create Weapons
        print("\n4. Creating Weapons...")
        weapons = [
            Weapon(name="Riptide", weapon_type="Sword", material="Celestial Bronze",
                  owner_id=characters[0].id,
                  description="Percy's legendary sword that always returns to his pocket",
                  special_abilities="Returns to owner, deadly to monsters"),
            Weapon(name="Annabeth's Dagger", weapon_type="Dagger", material="Celestial Bronze",
                  owner_id=characters[1].id,
                  description="A gift from Luke, used for close combat",
                  special_abilities="Balanced for throwing and close combat"),
            Weapon(name="Backbiter", weapon_type="Sword", material="Half Steel, Half Celestial Bronze",
                  owner_id=characters[3].id,
                  description="Luke's deadly blade that can harm both mortals and immortals",
                  special_abilities="Can harm mortals and immortals"),
        ]
        db.add_all(weapons)
        db.commit()
        print(f"  ✓ Created {len(weapons)} weapons")
        
        # 5. Create Powers
        print("\n5. Creating Powers...")
        powers = [
            Power(name="Hydrokinesis", power_type="Elemental", power_level=10,
                 description="Control over water and related phenomena"),
            Power(name="Strategic Mind", power_type="Mental", power_level=9,
                 description="Enhanced tactical and strategic thinking"),
            Power(name="Swordsmanship", power_type="Physical", power_level=9,
                 description="Master sword fighting ability"),
            Power(name="Lightning Control", power_type="Elemental", power_level=10,
                 description="Control over lightning and electricity"),
            Power(name="Shadow Travel", power_type="Elemental", power_level=8,
                 description="Ability to travel through shadows"),
            Power(name="Communication with Horses", power_type="Mental", power_level=7,
                 description="Can speak with and understand horses"),
        ]
        db.add_all(powers)
        db.commit()
        print(f"  ✓ Created {len(powers)} powers")
        
        # 6. Create Character-Power relationships
        print("\n6. Creating Character-Power relationships...")
        character_powers = [
            CharacterPower(character_id=characters[0].id, power_id=powers[0].id, 
                          proficiency_level=10),
            CharacterPower(character_id=characters[0].id, power_id=powers[2].id, 
                          proficiency_level=9),
            CharacterPower(character_id=characters[0].id, power_id=powers[5].id, 
                          proficiency_level=8),
            CharacterPower(character_id=characters[1].id, power_id=powers[1].id, 
                          proficiency_level=10),
            CharacterPower(character_id=characters[4].id, power_id=powers[3].id, 
                          proficiency_level=9),
            CharacterPower(character_id=characters[5].id, power_id=powers[4].id, 
                          proficiency_level=8),
        ]
        db.add_all(character_powers)
        db.commit()
        print(f"  ✓ Created {len(character_powers)} character-power relationships")
        
        # 7. Create Books
        print("\n7. Creating Books...")
        books = [
            Book(title="The Lightning Thief", book_number=1, 
                publication_date=date(2005, 7, 1), page_count=377,
                isbn="9780786838653",
                summary="Percy discovers he is a demigod and goes on a quest to prevent a war between the gods"),
            Book(title="The Sea of Monsters", book_number=2,
                publication_date=date(2006, 4, 1), page_count=279,
                isbn="9780786856862",
                summary="Percy and friends embark on a quest to save Camp Half-Blood"),
            Book(title="The Titan's Curse", book_number=3,
                publication_date=date(2007, 5, 1), page_count=312,
                isbn="9781423101451",
                summary="Percy must rescue Annabeth and the goddess Artemis"),
            Book(title="The Battle of the Labyrinth", book_number=4,
                publication_date=date(2008, 5, 6), page_count=361,
                isbn="9781423101468",
                summary="Percy navigates the Labyrinth to prevent Luke's army from invading Camp Half-Blood"),
            Book(title="The Last Olympian", book_number=5,
                publication_date=date(2009, 5, 5), page_count=381,
                isbn="9781423101475",
                summary="The final battle for Olympus as Percy fulfills the Great Prophecy"),
        ]
        db.add_all(books)
        db.commit()
        print(f"  ✓ Created {len(books)} books")
        
        # 8. Create Locations
        print("\n8. Creating Locations...")
        locations = [
            Location(name="Camp Half-Blood", location_type="Camp",
                    description="Training facility for Greek demigods on Long Island",
                    realm="Mortal", coordinates="40.8°N, 72.8°W"),
            Location(name="Mount Olympus", location_type="Divine Palace",
                    description="Home of the Olympian gods, located on the 600th floor of the Empire State Building",
                    realm="Olympus"),
            Location(name="Underworld", location_type="Divine Realm",
                    description="Realm of the dead ruled by Hades",
                    realm="Underworld"),
            Location(name="Lotus Hotel and Casino", location_type="Trap",
                    description="Magical casino where time moves differently",
                    realm="Mortal", coordinates="Las Vegas, NV"),
        ]
        db.add_all(locations)
        db.commit()
        print(f"  ✓ Created {len(locations)} locations")
        
        # 9. Create Monsters
        print("\n9. Creating Monsters...")
        monsters = [
            Monster(name="Minotaur", species="Bull-man hybrid", threat_level="high",
                   description="Half-man, half-bull creature",
                   weaknesses="Can be defeated by demigods with proper training",
                   abilities="Superhuman strength, enhanced senses"),
            Monster(name="Medusa", species="Gorgon", threat_level="extreme",
                   description="Snake-haired woman who turns people to stone",
                   weaknesses="Reflective surfaces, can be beheaded",
                   abilities="Petrifying gaze, snake hair"),
            Monster(name="Chimera", species="Hybrid beast", threat_level="extreme",
                   description="Lion-goat-snake hybrid that breathes fire",
                   weaknesses="Celestial bronze weapons",
                   abilities="Fire breathing, venomous tail, multiple forms of attack"),
            Monster(name="Hellhound", species="Demon dog", threat_level="high",
                   description="Massive dogs from the Underworld",
                   weaknesses="Celestial bronze",
                   abilities="Shadow travel, superhuman speed and strength"),
        ]
        db.add_all(monsters)
        db.commit()
        print(f"  ✓ Created {len(monsters)} monsters")
        
        # 10. Create Prophecies
        print("\n10. Creating Prophecies...")
        prophecies = [
            Prophecy(title="The Great Prophecy",
                    text="A half-blood of the eldest gods, shall reach sixteen against all odds. And see the world in endless sleep, the hero's soul, cursed blade shall reap. A single choice shall end his days, Olympus to preserve or raze.",
                    speaker="The Oracle of Delphi",
                    date_spoken=date(1993, 1, 1),
                    fulfilled=True,
                    interpretation="Percy Jackson's destiny to save or destroy Olympus"),
        ]
        db.add_all(prophecies)
        db.commit()
        print(f"  ✓ Created {len(prophecies)} prophecies")
        
        # 11. Create Quests
        print("\n11. Creating Quests...")
        quests = [
            Quest(title="Retrieve Zeus's Master Bolt", 
                 description="Find and return Zeus's stolen lightning bolt",
                 objective="Prevent war between Zeus and Poseidon",
                 start_date=date(2005, 6, 15), end_date=date(2005, 6, 30),
                 status="completed", difficulty_level=9,
                 start_location_id=locations[0].id, end_location_id=locations[1].id,
                 book_id=books[0].id, prophecy_id=prophecies[0].id),
            Quest(title="Save Camp Half-Blood",
                 description="Find the Golden Fleece to heal Thalia's tree",
                 objective="Restore the camp's magical barrier",
                 start_date=date(2006, 7, 1), end_date=date(2006, 7, 15),
                 status="completed", difficulty_level=8,
                 start_location_id=locations[0].id, book_id=books[1].id),
            Quest(title="Rescue Artemis and Annabeth",
                 description="Save the goddess and Percy's friend from the Titans",
                 objective="Prevent Artemis from being held hostage",
                 start_date=date(2007, 12, 15), end_date=date(2007, 12, 25),
                 status="completed", difficulty_level=9,
                 book_id=books[2].id),
        ]
        db.add_all(quests)
        db.commit()
        print(f"  ✓ Created {len(quests)} quests")
        
        # 12. Create Quest Participants
        print("\n12. Creating Quest Participants...")
        quest_participants = [
            QuestParticipant(quest_id=quests[0].id, character_id=characters[0].id, 
                           role="Leader", joined_date=date(2005, 6, 15)),
            QuestParticipant(quest_id=quests[0].id, character_id=characters[1].id, 
                           role="Strategist", joined_date=date(2005, 6, 15)),
            QuestParticipant(quest_id=quests[0].id, character_id=characters[2].id, 
                           role="Protector", joined_date=date(2005, 6, 15)),
            QuestParticipant(quest_id=quests[1].id, character_id=characters[0].id, 
                           role="Leader", joined_date=date(2006, 7, 1)),
            QuestParticipant(quest_id=quests[1].id, character_id=characters[1].id, 
                           role="Member", joined_date=date(2006, 7, 1)),
            QuestParticipant(quest_id=quests[2].id, character_id=characters[0].id, 
                           role="Leader", joined_date=date(2007, 12, 15)),
        ]
        db.add_all(quest_participants)
        db.commit()
        print(f"  ✓ Created {len(quest_participants)} quest participants")
        
        # 13. Create Quest-Monster encounters
        print("\n13. Creating Quest-Monster encounters...")
        quest_monsters = [
            QuestMonster(quest_id=quests[0].id, monster_id=monsters[0].id,
                       encounter_description="Percy fights the Minotaur to save his mother",
                       defeated=True),
            QuestMonster(quest_id=quests[0].id, monster_id=monsters[1].id,
                       encounter_description="Encounter with Medusa at her garden emporium",
                       defeated=True),
            QuestMonster(quest_id=quests[0].id, monster_id=monsters[2].id,
                       encounter_description="Battle with the Chimera at the St. Louis Arch",
                       defeated=True),
        ]
        db.add_all(quest_monsters)
        db.commit()
        print(f"  ✓ Created {len(quest_monsters)} quest-monster encounters")
        
        print("\n" + "="*50)
        print("✓ Database population complete!")
        print("="*50)
        print("\nDatabase Statistics:")
        print(f"  Gods: {len(gods)}")
        print(f"  Cabins: {len(cabins)}")
        print(f"  Characters: {len(characters)}")
        print(f"  Weapons: {len(weapons)}")
        print(f"  Powers: {len(powers)}")
        print(f"  Books: {len(books)}")
        print(f"  Locations: {len(locations)}")
        print(f"  Monsters: {len(monsters)}")
        print(f"  Prophecies: {len(prophecies)}")
        print(f"  Quests: {len(quests)}")
        print(f"  Character-Power relationships: {len(character_powers)}")
        print(f"  Quest Participants: {len(quest_participants)}")
        print(f"  Quest-Monster encounters: {len(quest_monsters)}")
        print(f"\n  Total records: {len(gods) + len(cabins) + len(characters) + len(weapons) + len(powers) + len(books) + len(locations) + len(monsters) + len(prophecies) + len(quests) + len(character_powers) + len(quest_participants) + len(quest_monsters)}")
        
    except Exception as e:
        print(f"\n✗ Error populating database: {e}")
        db.rollback()
        return False
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    success = populate_database()
    if not success:
        sys.exit(1)
