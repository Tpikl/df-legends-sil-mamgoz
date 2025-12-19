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
    """Extract structures from a site."""
    structures = []
    struct_section = elem.find('structures')
    if struct_section is not None:
        for struct in struct_section.findall('structure'):
            local_id = get_child_text(struct, 'local_id')
            struct_type = get_child_text(struct, 'type')
            name = get_child_text(struct, 'name', '(unnamed)')
            structures.append({'id': local_id, 'type': struct_type, 'name': name})
    return structures


def format_site(site):
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

    # Structures
    structures = parse_structures(site)
    if structures:
        lines.append(f"\nStructures ({len(structures)}):")
        for struct in structures[:20]:  # Limit display
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

    for site in results:
        if args.brief:
            site_id = get_child_text(site, 'id')
            name = get_child_text(site, 'name', '(unnamed)')
            site_type = get_child_text(site, 'type', 'unknown')
            print(f"#{site_id}: {name.title()} ({site_type})")
        else:
            print(format_site(site))
            print()

    if len(results) == args.limit:
        print(f"(Limited to {args.limit} results. Use --limit to see more.)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
