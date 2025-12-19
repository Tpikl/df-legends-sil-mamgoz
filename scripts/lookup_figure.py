#!/usr/bin/env python3
"""
Look up historical figures from parsed legends data.

Usage:
    python3 lookup_figure.py 123              # Find figure by ID
    python3 lookup_figure.py "name pattern"   # Search by name (case-insensitive)
    python3 lookup_figure.py --race dwarf     # List all figures of a race
    python3 lookup_figure.py --race dwarf --limit 10  # Limit results
"""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PARSED_DIR = Path(__file__).parent.parent / "world" / "parsed"
FIGURES_DIR = PARSED_DIR / "figures"


def get_child_text(elem, tag, default=""):
    """Get text content of a child element."""
    child = elem.find(tag)
    return child.text if child is not None and child.text else default


def get_all_child_texts(elem, tag):
    """Get all text values for a repeated tag."""
    return [child.text for child in elem.findall(tag) if child.text]


def parse_hf_links(elem):
    """Extract all hf_link relationships."""
    links = []
    for link in elem.findall('hf_link'):
        link_type = get_child_text(link, 'link_type')
        hfid = get_child_text(link, 'hfid')
        strength = get_child_text(link, 'link_strength', '')
        links.append({'type': link_type, 'hfid': hfid, 'strength': strength})
    return links


def parse_entity_links(elem):
    """Extract all entity_link relationships."""
    links = []
    for link in elem.findall('entity_link'):
        link_type = get_child_text(link, 'link_type')
        entity_id = get_child_text(link, 'entity_id')
        strength = get_child_text(link, 'link_strength', '')
        links.append({'type': link_type, 'entity_id': entity_id, 'strength': strength})
    return links


def parse_site_links(elem):
    """Extract all site_link relationships."""
    links = []
    for link in elem.findall('site_link'):
        link_type = get_child_text(link, 'link_type')
        site_id = get_child_text(link, 'site_id')
        links.append({'type': link_type, 'site_id': site_id})
    return links


def parse_skills(elem):
    """Extract all skills."""
    skills = []
    for skill in elem.findall('hf_skill'):
        skill_name = get_child_text(skill, 'skill')
        total_ip = get_child_text(skill, 'total_ip', '0')
        skills.append({'skill': skill_name, 'total_ip': int(total_ip)})
    # Sort by IP descending
    return sorted(skills, key=lambda x: x['total_ip'], reverse=True)


def format_figure(fig):
    """Format a figure for display."""
    fig_id = get_child_text(fig, 'id')
    name = get_child_text(fig, 'name', '(unnamed)')
    race = get_child_text(fig, 'race', 'unknown')
    caste = get_child_text(fig, 'caste', '')
    birth_year = get_child_text(fig, 'birth_year', '?')
    death_year = get_child_text(fig, 'death_year', '-1')

    # Basic info
    lines = [
        f"{'='*60}",
        f"FIGURE #{fig_id}: {name.title()}",
        f"{'='*60}",
        f"Race: {race.replace('_', ' ').title()}" + (f" ({caste.lower()})" if caste else ""),
    ]

    # Life span
    if birth_year == '-1':
        lines.append("Born: Before time (deity/primordial)")
    else:
        lines.append(f"Born: Year {birth_year}")

    if death_year != '-1':
        lines.append(f"Died: Year {death_year}")
    else:
        lines.append("Status: Alive (or immortal)")

    # Deity info
    if fig.find('deity') is not None:
        spheres = get_all_child_texts(fig, 'sphere')
        if spheres:
            lines.append(f"Deity Spheres: {', '.join(spheres)}")

    # Interaction knowledge (secrets)
    secrets = get_all_child_texts(fig, 'interaction_knowledge')
    if secrets:
        lines.append(f"Secrets Known: {', '.join(secrets)}")

    # Relationships
    hf_links = parse_hf_links(fig)
    if hf_links:
        lines.append("\nRelationships:")
        for link in hf_links:
            strength_str = f" (strength: {link['strength']})" if link['strength'] else ""
            lines.append(f"  - {link['type']}: figure #{link['hfid']}{strength_str}")

    # Entity links
    entity_links = parse_entity_links(fig)
    if entity_links:
        lines.append("\nEntity Affiliations:")
        for link in entity_links:
            strength_str = f" (strength: {link['strength']})" if link['strength'] else ""
            lines.append(f"  - {link['type']}: entity #{link['entity_id']}{strength_str}")

    # Site links
    site_links = parse_site_links(fig)
    if site_links:
        lines.append("\nSite Links:")
        for link in site_links:
            lines.append(f"  - {link['type']}: site #{link['site_id']}")

    # Skills
    skills = parse_skills(fig)
    if skills:
        lines.append("\nSkills (top 10):")
        for skill in skills[:10]:
            skill_name = skill['skill'].replace('_', ' ').title()
            lines.append(f"  - {skill_name}: {skill['total_ip']} IP")

    return '\n'.join(lines)


def find_by_id(figure_id):
    """Find a figure by exact ID."""
    # Search in the all file first
    all_file = FIGURES_DIR / "historical_figures_all.xml"
    if all_file.exists():
        tree = ET.parse(all_file)
        root = tree.getroot()
        for fig in root.findall('.//historical_figure'):
            if get_child_text(fig, 'id') == str(figure_id):
                return fig
    return None


def search_by_name(pattern, limit=20):
    """Search figures by name pattern (case-insensitive)."""
    results = []
    regex = re.compile(pattern, re.IGNORECASE)

    all_file = FIGURES_DIR / "historical_figures_all.xml"
    if all_file.exists():
        tree = ET.parse(all_file)
        root = tree.getroot()
        for fig in root.findall('.//historical_figure'):
            name = get_child_text(fig, 'name', '')
            if regex.search(name):
                results.append(fig)
                if len(results) >= limit:
                    break

    return results


def list_by_race(race, limit=50):
    """List all figures of a given race."""
    race_file = FIGURES_DIR / "by_race" / f"{race.lower().replace(' ', '_')}.xml"

    if not race_file.exists():
        # List available races
        race_dir = FIGURES_DIR / "by_race"
        if race_dir.exists():
            races = sorted([f.stem for f in race_dir.glob("*.xml")])
            print(f"Race '{race}' not found. Available races:")
            for r in races:
                print(f"  - {r}")
        return []

    tree = ET.parse(race_file)
    root = tree.getroot()
    figures = root.findall('.//historical_figure')

    return figures[:limit]


def main():
    parser = argparse.ArgumentParser(description='Look up historical figures')
    parser.add_argument('query', nargs='?', help='Figure ID or name pattern to search')
    parser.add_argument('--race', '-r', help='List figures by race')
    parser.add_argument('--limit', '-l', type=int, default=20, help='Limit results (default: 20)')
    parser.add_argument('--brief', '-b', action='store_true', help='Brief output (ID and name only)')

    args = parser.parse_args()

    if not args.query and not args.race:
        parser.print_help()
        return 1

    results = []

    if args.race:
        results = list_by_race(args.race, args.limit)
    elif args.query:
        # Try as ID first
        if args.query.isdigit():
            fig = find_by_id(args.query)
            if fig is not None:
                results = [fig]

        # If no ID match, search by name
        if not results:
            results = search_by_name(args.query, args.limit)

    if not results:
        print(f"No figures found matching: {args.query or args.race}")
        return 1

    for fig in results:
        if args.brief:
            fig_id = get_child_text(fig, 'id')
            name = get_child_text(fig, 'name', '(unnamed)')
            race = get_child_text(fig, 'race', 'unknown')
            death_year = get_child_text(fig, 'death_year', '-1')
            status = "alive" if death_year == '-1' else f"died {death_year}"
            print(f"#{fig_id}: {name.title()} ({race.lower()}, {status})")
        else:
            print(format_figure(fig))
            print()

    if len(results) == args.limit:
        print(f"(Limited to {args.limit} results. Use --limit to see more.)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
