#!/usr/bin/env python3
"""
Look up entities (civilizations, groups) from parsed legends data.

Usage:
    python3 lookup_entity.py 123              # Find entity by ID
    python3 lookup_entity.py "name pattern"   # Search by name (case-insensitive)
    python3 lookup_entity.py --list           # List all entities with types
"""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PARSED_DIR = Path(__file__).parent.parent / "world" / "parsed"
ENTITIES_DIR = PARSED_DIR / "entities"


def get_child_text(elem, tag, default=""):
    """Get text content of a child element."""
    child = elem.find(tag)
    return child.text if child is not None and child.text else default


def get_all_child_texts(elem, tag):
    """Get all text values for a repeated tag."""
    return [child.text for child in elem.findall(tag) if child.text]


def format_entity(entity, plus_data=None):
    """Format an entity for display."""
    entity_id = get_child_text(entity, 'id')
    name = get_child_text(entity, 'name', '(unnamed)')

    lines = [
        f"{'='*60}",
        f"ENTITY #{entity_id}: {name.title()}",
        f"{'='*60}",
    ]

    # From plus data if available
    if plus_data is not None:
        race = get_child_text(plus_data, 'race', '')
        entity_type = get_child_text(plus_data, 'type', '')
        if race:
            lines.append(f"Race: {race.replace('_', ' ').title()}")
        if entity_type:
            lines.append(f"Type: {entity_type.replace('_', ' ').title()}")

    # Worship
    worship = get_all_child_texts(entity, 'worship_id')
    if worship:
        lines.append(f"Worships: figure(s) #{', #'.join(worship)}")

    # Children entities
    children = get_all_child_texts(entity, 'child')
    if children:
        lines.append(f"Child Entities: #{', #'.join(children[:10])}")
        if len(children) > 10:
            lines.append(f"  ... and {len(children) - 10} more")

    # Entity links
    for link in entity.findall('entity_link'):
        link_type = get_child_text(link, 'type')
        target = get_child_text(link, 'target')
        if link_type and target:
            lines.append(f"Link: {link_type} -> entity #{target}")

    return '\n'.join(lines)


def load_entities():
    """Load entities from the entities file."""
    entities_file = ENTITIES_DIR / "entities.xml"
    if not entities_file.exists():
        print(f"Entities file not found: {entities_file}")
        return []

    tree = ET.parse(entities_file)
    root = tree.getroot()
    return root.findall('.//entity')


def load_entities_plus():
    """Load entities_plus data (has race/type info)."""
    plus_file = ENTITIES_DIR / "entities_plus.xml"
    if not plus_file.exists():
        return {}

    tree = ET.parse(plus_file)
    root = tree.getroot()

    plus_data = {}
    for entity in root.findall('.//entity'):
        entity_id = get_child_text(entity, 'id')
        if entity_id:
            plus_data[entity_id] = entity

    return plus_data


def find_by_id(entity_id):
    """Find an entity by exact ID."""
    for entity in load_entities():
        if get_child_text(entity, 'id') == str(entity_id):
            return entity
    return None


def search_by_name(pattern, limit=20):
    """Search entities by name pattern (case-insensitive)."""
    results = []
    regex = re.compile(pattern, re.IGNORECASE)

    for entity in load_entities():
        name = get_child_text(entity, 'name', '')
        if regex.search(name):
            results.append(entity)
            if len(results) >= limit:
                break

    return results


def list_all_entities():
    """List all entities with their types."""
    entities = load_entities()
    plus_data = load_entities_plus()

    print(f"All entities ({len(entities)}):\n")

    for entity in entities:
        entity_id = get_child_text(entity, 'id')
        name = get_child_text(entity, 'name', '(unnamed)')

        plus = plus_data.get(entity_id)
        if plus:
            race = get_child_text(plus, 'race', '?')
            entity_type = get_child_text(plus, 'type', '?')
            print(f"#{entity_id}: {name.title()} ({race} {entity_type})")
        else:
            print(f"#{entity_id}: {name.title()}")


def main():
    parser = argparse.ArgumentParser(description='Look up entities (civilizations)')
    parser.add_argument('query', nargs='?', help='Entity ID or name pattern to search')
    parser.add_argument('--list', action='store_true', help='List all entities')
    parser.add_argument('--limit', '-l', type=int, default=20, help='Limit results (default: 20)')
    parser.add_argument('--brief', '-b', action='store_true', help='Brief output')

    args = parser.parse_args()

    if args.list:
        list_all_entities()
        return 0

    if not args.query:
        parser.print_help()
        return 1

    results = []

    # Try as ID first
    if args.query.isdigit():
        entity = find_by_id(args.query)
        if entity is not None:
            results = [entity]

    # If no ID match, search by name
    if not results:
        results = search_by_name(args.query, args.limit)

    if not results:
        print(f"No entities found matching: {args.query}")
        return 1

    plus_data = load_entities_plus()

    for entity in results:
        entity_id = get_child_text(entity, 'id')
        if args.brief:
            name = get_child_text(entity, 'name', '(unnamed)')
            plus = plus_data.get(entity_id)
            extra = ""
            if plus:
                race = get_child_text(plus, 'race', '')
                entity_type = get_child_text(plus, 'type', '')
                extra = f" ({race} {entity_type})" if race else ""
            print(f"#{entity_id}: {name.title()}{extra}")
        else:
            print(format_entity(entity, plus_data.get(entity_id)))
            print()

    if len(results) == args.limit:
        print(f"(Limited to {args.limit} results. Use --limit to see more.)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
