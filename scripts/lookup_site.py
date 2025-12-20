#!/usr/bin/env python3
"""
Look up sites from parsed legends data.

Usage:
    python3 lookup_site.py 123              # Find site by ID
    python3 lookup_site.py "name pattern"   # Search by name (case-insensitive)
    python3 lookup_site.py --type fortress  # List sites by type
    python3 lookup_site.py --list           # List all site types
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


def parse_structures(elem):
    """Extract structures from a site (from plus data)."""
    structures = []
    struct_section = elem.find('structures')
    if struct_section is not None:
        for struct in struct_section.findall('structure'):
            struct_id = get_child_text(struct, 'id')
            struct_type = get_child_text(struct, 'type')
            name = get_child_text(struct, 'name', '(unnamed)')
            name2 = get_child_text(struct, 'name2', '')
            structures.append({'id': struct_id, 'type': struct_type, 'name': name, 'name2': name2})
    return structures


def load_sites_plus():
    """Load sites_plus data (has ownership and structure info)."""
    plus_file = ENTITIES_DIR / "sites_plus.xml"
    if not plus_file.exists():
        return {}

    tree = ET.parse(plus_file)
    root = tree.getroot()

    plus_data = {}
    for site in root.findall('.//site'):
        site_id = get_child_text(site, 'id')
        if site_id:
            plus_data[site_id] = site

    return plus_data


def load_entity_names():
    """Load entity ID to name mapping for display."""
    entities_file = ENTITIES_DIR / "entities.xml"
    if not entities_file.exists():
        return {}

    tree = ET.parse(entities_file)
    root = tree.getroot()

    names = {}
    for entity in root.findall('.//entity'):
        entity_id = get_child_text(entity, 'id')
        name = get_child_text(entity, 'name', '')
        if entity_id and name:
            names[entity_id] = name.title()

    return names


def format_site(site, plus_data=None, entity_names=None):
    """Format a site for display."""
    site_id = get_child_text(site, 'id')
    name = get_child_text(site, 'name', '(unnamed)')
    site_type = get_child_text(site, 'type', 'unknown')
    coords = get_child_text(site, 'coords', '?')
    rectangle = get_child_text(site, 'rectangle', '')

    lines = [
        f"{'='*60}",
        f"SITE #{site_id}: {name.title()}",
        f"{'='*60}",
        f"Type: {site_type.title()}",
        f"Coordinates: {coords}",
    ]

    if rectangle:
        lines.append(f"Rectangle: {rectangle}")

    # Ownership info from plus data
    if plus_data is not None:
        civ_id = get_child_text(plus_data, 'civ_id', '')
        cur_owner_id = get_child_text(plus_data, 'cur_owner_id', '')

        if entity_names is None:
            entity_names = {}

        if civ_id:
            civ_name = entity_names.get(civ_id, f"entity #{civ_id}")
            lines.append(f"Built By: {civ_name} (entity #{civ_id})")

        if cur_owner_id:
            owner_name = entity_names.get(cur_owner_id, f"entity #{cur_owner_id}")
            lines.append(f"Current Owner: {owner_name} (entity #{cur_owner_id})")
            lines.append(f"Status: ACTIVE")
        elif civ_id:
            # Has civ_id but no cur_owner_id = abandoned/ruined
            lines.append(f"Current Owner: NONE")
            lines.append(f"Status: ABANDONED/RUINED")
        else:
            # No civ_id = lair or natural site
            lines.append(f"Status: Unowned (lair/natural)")

        # Structures from plus data (more detailed)
        structures = parse_structures(plus_data)
        if structures:
            lines.append(f"\nStructures ({len(structures)}):")
            for struct in structures[:20]:
                struct_line = f"  [{struct['id']}] {struct['type']}: {struct['name'].title()}"
                if struct['name2']:
                    struct_line += f" ({struct['name2']})"
                lines.append(struct_line)
            if len(structures) > 20:
                lines.append(f"  ... and {len(structures) - 20} more")
    else:
        # Fallback to base structures
        struct_section = site.find('structures')
        if struct_section is not None:
            structures = []
            for struct in struct_section.findall('structure'):
                struct_id = get_child_text(struct, 'local_id')
                struct_type = get_child_text(struct, 'type')
                struct_name = get_child_text(struct, 'name', '(unnamed)')
                structures.append({'id': struct_id, 'type': struct_type, 'name': struct_name})
            if structures:
                lines.append(f"\nStructures ({len(structures)}):")
                for struct in structures[:20]:
                    lines.append(f"  [{struct['id']}] {struct['type']}: {struct['name'].title()}")
                if len(structures) > 20:
                    lines.append(f"  ... and {len(structures) - 20} more")

    return '\n'.join(lines)


def load_sites():
    """Load all sites from the sites file."""
    sites_file = ENTITIES_DIR / "sites.xml"
    if not sites_file.exists():
        print(f"Sites file not found: {sites_file}")
        return []

    tree = ET.parse(sites_file)
    root = tree.getroot()
    return root.findall('.//site')


def find_by_id(site_id):
    """Find a site by exact ID."""
    for site in load_sites():
        if get_child_text(site, 'id') == str(site_id):
            return site
    return None


def search_by_name(pattern, limit=20):
    """Search sites by name pattern (case-insensitive)."""
    results = []
    regex = re.compile(pattern, re.IGNORECASE)

    for site in load_sites():
        name = get_child_text(site, 'name', '')
        if regex.search(name):
            results.append(site)
            if len(results) >= limit:
                break

    return results


def list_by_type(site_type, limit=50):
    """List all sites of a given type."""
    results = []
    target = site_type.lower()

    for site in load_sites():
        stype = get_child_text(site, 'type', '').lower()
        if target in stype or stype in target:
            results.append(site)
            if len(results) >= limit:
                break

    return results


def list_site_types():
    """List all site types with counts."""
    type_counts = {}
    for site in load_sites():
        stype = get_child_text(site, 'type', 'unknown')
        type_counts[stype] = type_counts.get(stype, 0) + 1

    print("Site types:")
    for stype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {stype}: {count}")


def main():
    parser = argparse.ArgumentParser(description='Look up sites')
    parser.add_argument('query', nargs='?', help='Site ID or name pattern to search')
    parser.add_argument('--type', '-t', help='List sites by type')
    parser.add_argument('--list', action='store_true', help='List all site types')
    parser.add_argument('--limit', '-l', type=int, default=20, help='Limit results (default: 20)')
    parser.add_argument('--brief', '-b', action='store_true', help='Brief output (ID and name only)')

    args = parser.parse_args()

    if args.list:
        list_site_types()
        return 0

    if not args.query and not args.type:
        parser.print_help()
        return 1

    results = []

    if args.type:
        results = list_by_type(args.type, args.limit)
    elif args.query:
        # Try as ID first
        if args.query.isdigit():
            site = find_by_id(args.query)
            if site is not None:
                results = [site]

        # If no ID match, search by name
        if not results:
            results = search_by_name(args.query, args.limit)

    if not results:
        print(f"No sites found matching: {args.query or args.type}")
        return 1

    # Load plus data for ownership info
    plus_data = load_sites_plus()
    entity_names = load_entity_names()

    for site in results:
        site_id = get_child_text(site, 'id')
        site_plus = plus_data.get(site_id)

        if args.brief:
            name = get_child_text(site, 'name', '(unnamed)')
            site_type = get_child_text(site, 'type', 'unknown')

            # Add ownership status to brief output
            status = ""
            if site_plus is not None:
                civ_id = get_child_text(site_plus, 'civ_id', '')
                cur_owner_id = get_child_text(site_plus, 'cur_owner_id', '')
                if cur_owner_id:
                    status = " [ACTIVE]"
                elif civ_id:
                    status = " [ABANDONED]"
                else:
                    status = " [unowned]"

            print(f"#{site_id}: {name.title()} ({site_type}){status}")
        else:
            print(format_site(site, site_plus, entity_names))
            print()

    if len(results) == args.limit:
        print(f"(Limited to {args.limit} results. Use --limit to see more.)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
