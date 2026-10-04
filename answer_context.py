"""Small deterministic profiles for gods and characters named in a question."""

import re
from collections import Counter

from sqlalchemy.orm import Session

from models.character import Character
from models.god import God
from schemas.answer import Fact


def database_facts(question: str, db: Session) -> list[Fact]:
    """Match whole names, Roman names, or unambiguous character first names.

    Return at most three named profiles, with at most five powers per character.
    These are selected records, not an exhaustive account of mythology.
    """
    question = question.casefold()

    def mentioned(name: str | None) -> bool:
        return bool(
            name and re.search(r"(?<!\w)" + re.escape(name.casefold()) + r"(?!\w)", question)
        )

    gods = db.query(God).order_by(God.id).all()
    characters = [
        character
        for character in db.query(Character).order_by(Character.id).all()
        if character.name.strip()
    ]
    first_names = Counter(character.name.split()[0].casefold() for character in characters)
    matches = [("god", god) for god in gods if mentioned(god.name) or mentioned(god.roman_name)]
    for character in characters:
        first_name = character.name.split()[0]
        if mentioned(character.name) or (
            first_names[first_name.casefold()] == 1 and mentioned(first_name)
        ):
            matches.append(("character", character))

    facts = []
    for entity_type, entity in matches[:3]:
        fields = {"name": entity.name, "description": entity.description}
        if entity_type == "god":
            fields.update(
                roman_name=entity.roman_name,
                title=entity.title,
                domain=entity.domain,
                symbol=entity.symbol,
            )
        else:
            fields["parent_god"] = entity.parent_god.name if entity.parent_god else None
            for assignment in sorted(entity.powers, key=lambda item: item.power_id)[:5]:
                power = assignment.power
                fields[f"power:{power.id}"] = (
                    f"{power.name}: {power.description}" if power.description else power.name
                )
        facts.extend(
            Fact(
                entity_type=entity_type,
                entity_id=entity.id,
                name=entity.name,
                field=field,
                value=value,
            )
            for field, value in fields.items()
            if value
        )
    return facts
