#!/usr/bin/env python3
"""
Look up creature names from creature IDs.

This is essential for generated creatures like NIGHT_CREATURE_3, FORGOTTEN_BEAST_5, etc.

Usage:
    python3 lookup_creature.py NIGHT_CREATURE_3      # Get name for creature ID
    python3 lookup_creature.py night_creature        # List all matching creature IDs
    python3 lookup_creature.py --list-special        # List all special creatures (night, forgotten, titan)
"""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PARSED_DIR = Path(__file__).parent.parent / "world" / "parsed"
REFERENCE_DIR = PARSED_DIR / "reference"


def get_child_text(elem, tag, default=""):
    """Get text content of a child element."""
    child = elem.find(tag)
    return child.text if child is not None and child.text else default


def load_creatures():
    """Load all creatures from creature_raw.xml."""
    creature_file = REFERENCE_DIR / "creature_raw.xml"
    if not creature_file.exists():
        print(f"Creature file not found: {creature_file}")
        return []

    tree = ET.parse(creature_file)
    root = tree.getroot()
    return root.findall('.//creature')


def format_creature(creature):
    """Format a creature for display."""
    creature_id = get_child_text(creature, 'creature_id')
    name_singular = get_child_text(creature, 'name_singular', '(no name)')
    name_plural = get_child_text(creature, 'name_plural', '')

    lines = [f"{creature_id}: {name_singular}"]
    if name_plural and name_plural != name_singular:
        lines[0] += f" (plural: {name_plural})"

    return lines[0]


def find_by_id(creature_id):
    """Find a creature by exact ID (case-insensitive)."""
    target = creature_id.upper()
    for creature in load_creatures():
        cid = get_child_text(creature, 'creature_id', '').upper()
        if cid == target:
            return creature
    return None


def search_creatures(pattern, limit=50):
    """Search creatures by ID pattern."""
    results = []
    regex = re.compile(pattern, re.IGNORECASE)

    for creature in load_creatures():
        creature_id = get_child_text(creature, 'creature_id', '')
        name = get_child_text(creature, 'name_singular', '')

        if regex.search(creature_id) or regex.search(name):
            results.append(creature)
            if len(results) >= limit:
                break

    return results


def list_special_creatures():
    """List all special creatures (night creatures, forgotten beasts, titans)."""
    categories = {
        'Night Creatures': [],
        'Forgotten Beasts': [],
        'Titans': [],
        'Other Uniques': []
    }

    for creature in load_creatures():
        creature_id = get_child_text(creature, 'creature_id', '')
        name = get_child_text(creature, 'name_singular', '(unnamed)')

        if creature_id.startswith('NIGHT_CREATURE'):
            categories['Night Creatures'].append((creature_id, name))
        elif creature_id.startswith('FORGOTTEN_BEAST'):
            categories['Forgotten Beasts'].append((creature_id, name))
        elif creature_id.startswith('TITAN'):
            categories['Titans'].append((creature_id, name))
        elif any(x in creature_id for x in ['DEMON', 'UNIQUE', 'DEVIL']):
            categories['Other Uniques'].append((creature_id, name))

    for category, creatures in categories.items():
        if creatures:
            print(f"\n{category}:")
            print("-" * 40)
            for cid, name in sorted(creatures):
                print(f"  {cid}: {name}")


def main():
    parser = argparse.ArgumentParser(description='Look up creature names from IDs')
    parser.add_argument('query', nargs='?', help='Creature ID or search pattern')
    parser.add_argument('--list-special', action='store_true',
                        help='List all special creatures (night, forgotten, titan)')
    parser.add_argument('--limit', '-l', type=int, default=50, help='Limit results (default: 50)')

    args = parser.parse_args()

    if args.list_special:
        list_special_creatures()
        return 0

    if not args.query:
        parser.print_help()
        return 1

    # Try exact match first
    creature = find_by_id(args.query)
    if creature is not None:
        print(format_creature(creature))
        return 0

    # Search for pattern
    results = search_creatures(args.query, args.limit)

    if not results:
        print(f"No creatures found matching: {args.query}")
        return 1

    for creature in results:
        print(format_creature(creature))

    if len(results) == args.limit:
        print(f"\n(Limited to {args.limit} results. Use --limit to see more.)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
