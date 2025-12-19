#!/usr/bin/env python3
"""
Generate a complete timeline for a historical figure.

This script compiles all relevant data about a figure:
- Basic biographical info
- Family relationships (with names)
- Entity affiliations (with names)
- Complete event timeline
- Site connections (with names)

Usage:
    python3 figure_history.py 123              # Full history for figure #123
    python3 figure_history.py "name pattern"   # Search and show history
    python3 figure_history.py 123 --brief      # Condensed timeline
"""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PARSED_DIR = Path(__file__).parent.parent / "world" / "parsed"


# Cache for lookups
_figure_cache = {}
_site_cache = {}
_entity_cache = {}
_creature_cache = {}


def get_child_text(elem, tag, default=""):
    """Get text content of a child element."""
    child = elem.find(tag)
    return child.text if child is not None and child.text else default


def load_all_figures():
    """Load all figures into cache."""
    global _figure_cache
    if _figure_cache:
        return _figure_cache

    fig_file = PARSED_DIR / "figures" / "historical_figures_all.xml"
    if fig_file.exists():
        tree = ET.parse(fig_file)
        root = tree.getroot()
        for fig in root.findall('.//historical_figure'):
            fid = get_child_text(fig, 'id')
            if fid:
                _figure_cache[fid] = fig

    return _figure_cache


def load_all_sites():
    """Load all sites into cache."""
    global _site_cache
    if _site_cache:
        return _site_cache

    site_file = PARSED_DIR / "entities" / "sites.xml"
    if site_file.exists():
        tree = ET.parse(site_file)
        root = tree.getroot()
        for site in root.findall('.//site'):
            sid = get_child_text(site, 'id')
            if sid:
                _site_cache[sid] = site

    return _site_cache


def load_all_entities():
    """Load all entities into cache."""
    global _entity_cache
    if _entity_cache:
        return _entity_cache

    ent_file = PARSED_DIR / "entities" / "entities.xml"
    if ent_file.exists():
        tree = ET.parse(ent_file)
        root = tree.getroot()
        for ent in root.findall('.//entity'):
            eid = get_child_text(ent, 'id')
            if eid:
                _entity_cache[eid] = ent

    return _entity_cache


def load_creature_names():
    """Load creature ID to name mapping."""
    global _creature_cache
    if _creature_cache:
        return _creature_cache

    creature_file = PARSED_DIR / "reference" / "creature_raw.xml"
    if creature_file.exists():
        tree = ET.parse(creature_file)
        root = tree.getroot()
        for creature in root.findall('.//creature'):
            cid = get_child_text(creature, 'creature_id')
            name = get_child_text(creature, 'name_singular')
            if cid and name:
                _creature_cache[cid.upper()] = name

    return _creature_cache


def get_figure_name(figure_id):
    """Get a figure's name by ID."""
    figures = load_all_figures()
    fig = figures.get(str(figure_id))
    if fig is not None:
        name = get_child_text(fig, 'name', '(unnamed)')
        return name.title()
    return f"figure #{figure_id}"


def get_site_name(site_id):
    """Get a site's name by ID."""
    sites = load_all_sites()
    site = sites.get(str(site_id))
    if site is not None:
        name = get_child_text(site, 'name', '(unnamed)')
        site_type = get_child_text(site, 'type', '')
        return f"{name.title()} ({site_type})"
    return f"site #{site_id}"


def get_entity_name(entity_id):
    """Get an entity's name by ID."""
    entities = load_all_entities()
    ent = entities.get(str(entity_id))
    if ent is not None:
        return get_child_text(ent, 'name', '(unnamed)').title()
    return f"entity #{entity_id}"


def get_creature_name(race_id):
    """Get creature name from race ID."""
    creatures = load_creature_names()
    name = creatures.get(race_id.upper())
    if name:
        return name
    return race_id.replace('_', ' ').lower()


def find_figure(query):
    """Find a figure by ID or name pattern."""
    figures = load_all_figures()

    # Try as ID first
    if query.isdigit():
        return figures.get(query)

    # Search by name
    regex = re.compile(query, re.IGNORECASE)
    for fid, fig in figures.items():
        name = get_child_text(fig, 'name', '')
        if regex.search(name):
            return fig

    return None


def find_all_events_for_figure(figure_id):
    """Find all events involving a figure."""
    fid = str(figure_id)
    events = []

    # Figure-related fields to check
    figure_fields = [
        'hfid', 'slayer_hfid', 'changer_hfid', 'changee_hfid',
        'group_hfid', 'hist_fig_id', 'attacker_hfid', 'defender_hfid',
        'snatcher_hfid', 'victim_hfid', 'abductor_hfid', 'target_hfid',
        'hfid_target', 'hfid_1', 'hfid_2', 'woundee_hfid', 'wounder_hfid',
        'doer_hfid', 'trickster_hfid', 'student_hfid', 'teacher_hfid',
        'eater_hfid'
    ]

    # Search through all year files
    year_dir = PARSED_DIR / "events" / "by_year"
    if year_dir.exists():
        for year_file in sorted(year_dir.glob("years_*.xml")):
            tree = ET.parse(year_file)
            root = tree.getroot()
            for event in root.findall('.//historical_event'):
                for field in figure_fields:
                    if get_child_text(event, field) == fid:
                        events.append(event)
                        break

    # Sort by year
    events.sort(key=lambda e: (int(get_child_text(e, 'year', '0')),
                               int(get_child_text(e, 'seconds72', '0'))))

    return events


def describe_event(event, subject_id):
    """Create a narrative description of an event relative to a subject."""
    event_type = get_child_text(event, 'type')
    year = get_child_text(event, 'year')
    site_id = get_child_text(event, 'site_id')

    site_str = f" at {get_site_name(site_id)}" if site_id and site_id != '-1' else ""

    # Event-specific descriptions
    if event_type == 'hf died':
        hfid = get_child_text(event, 'hfid')
        slayer = get_child_text(event, 'slayer_hfid')
        cause = get_child_text(event, 'cause', 'unknown causes')

        if hfid == str(subject_id):
            if slayer and slayer != '-1':
                return f"Year {year}: DIED - killed by {get_figure_name(slayer)} ({cause}){site_str}"
            else:
                return f"Year {year}: DIED - {cause}{site_str}"
        else:
            return f"Year {year}: Killed {get_figure_name(hfid)} ({cause}){site_str}"

    elif event_type == 'changed creature type':
        changee = get_child_text(event, 'changee_hfid')
        changer = get_child_text(event, 'changer_hfid')
        old_race = get_creature_name(get_child_text(event, 'old_race'))
        new_race = get_creature_name(get_child_text(event, 'new_race'))

        if changee == str(subject_id):
            return f"Year {year}: TRANSFORMED from {old_race} to {new_race} by {get_figure_name(changer)}"
        else:
            return f"Year {year}: Transformed {get_figure_name(changee)} from {old_race} to {new_race}"

    elif event_type == 'add hf hf link':
        hfid1 = get_child_text(event, 'hfid_1')
        hfid2 = get_child_text(event, 'hfid_2')
        link_type = get_child_text(event, 'link_type', 'relationship')

        other = hfid2 if hfid1 == str(subject_id) else hfid1
        return f"Year {year}: Formed {link_type} with {get_figure_name(other)}"

    elif event_type == 'add hf entity link':
        hfid = get_child_text(event, 'hfid')
        civ_id = get_child_text(event, 'civ_id')
        link_type = get_child_text(event, 'link_type', 'member')

        return f"Year {year}: Became {link_type} of {get_entity_name(civ_id)}"

    elif event_type == 'hf learns secret':
        student = get_child_text(event, 'student_hfid')
        teacher = get_child_text(event, 'teacher_hfid')
        secret = get_child_text(event, 'secret_text', 'a secret')

        if student == str(subject_id):
            return f"Year {year}: Learned {secret} from {get_figure_name(teacher)}"
        else:
            return f"Year {year}: Taught {secret} to {get_figure_name(student)}"

    elif event_type == 'hf simple battle event':
        subtype = get_child_text(event, 'subtype', 'fought')
        return f"Year {year}: {subtype.replace('_', ' ').title()}{site_str}"

    elif event_type == 'creature devoured':
        victim = get_child_text(event, 'victim_hfid')
        eater = get_child_text(event, 'eater_hfid')

        if eater == str(subject_id):
            return f"Year {year}: Devoured {get_figure_name(victim)}{site_str}"
        else:
            return f"Year {year}: DEVOURED by {get_figure_name(eater)}{site_str}"

    elif event_type == 'artifact created':
        artifact_id = get_child_text(event, 'artifact_id')
        return f"Year {year}: Created artifact #{artifact_id}{site_str}"

    elif event_type == 'hf wounded':
        woundee = get_child_text(event, 'woundee_hfid')
        wounder = get_child_text(event, 'wounder_hfid')

        if woundee == str(subject_id):
            return f"Year {year}: Wounded by {get_figure_name(wounder)}{site_str}"
        else:
            return f"Year {year}: Wounded {get_figure_name(woundee)}{site_str}"

    elif event_type == 'hf abducted':
        target = get_child_text(event, 'target_hfid')
        snatcher = get_child_text(event, 'snatcher_hfid')

        if target == str(subject_id):
            return f"Year {year}: Abducted by {get_figure_name(snatcher)}{site_str}"
        else:
            return f"Year {year}: Abducted {get_figure_name(target)}{site_str}"

    # Default
    return f"Year {year}: {event_type.replace('_', ' ').title()}{site_str}"


def generate_history(fig, brief=False):
    """Generate complete history for a figure."""
    figure_id = get_child_text(fig, 'id')
    name = get_child_text(fig, 'name', '(unnamed)')
    race = get_child_text(fig, 'race', 'unknown')
    caste = get_child_text(fig, 'caste', '')
    birth_year = get_child_text(fig, 'birth_year', '?')
    death_year = get_child_text(fig, 'death_year', '-1')

    lines = [
        "=" * 70,
        f"HISTORY OF {name.upper()} (Figure #{figure_id})",
        "=" * 70,
        "",
        "BIOGRAPHICAL DATA",
        "-" * 40,
        f"Race: {get_creature_name(race)}" + (f" ({caste.lower()})" if caste else ""),
    ]

    if birth_year == '-1':
        lines.append("Born: Before recorded history (deity/primordial)")
    else:
        lines.append(f"Born: Year {birth_year}")

    if death_year != '-1':
        if birth_year != '-1':
            try:
                age = int(death_year) - int(birth_year)
                lines.append(f"Died: Year {death_year} (age {age})")
            except ValueError:
                lines.append(f"Died: Year {death_year}")
        else:
            lines.append(f"Died: Year {death_year}")
    else:
        lines.append("Status: Alive or immortal")

    # Deity spheres
    spheres = [child.text for child in fig.findall('sphere') if child.text]
    if spheres:
        lines.append(f"Spheres: {', '.join(spheres)}")

    # Family relationships
    family = []
    for link in fig.findall('hf_link'):
        link_type = get_child_text(link, 'link_type')
        hfid = get_child_text(link, 'hfid')
        if link_type in ['mother', 'father', 'child', 'spouse', 'former spouse']:
            family.append(f"{link_type.title()}: {get_figure_name(hfid)}")
        elif link_type == 'deity':
            family.append(f"Worships: {get_figure_name(hfid)}")

    if family:
        lines.extend(["", "RELATIONSHIPS", "-" * 40])
        lines.extend(family)

    # Entity affiliations
    entities = []
    for link in fig.findall('entity_link'):
        link_type = get_child_text(link, 'link_type')
        entity_id = get_child_text(link, 'entity_id')
        entities.append(f"{link_type.title()}: {get_entity_name(entity_id)}")

    if entities:
        lines.extend(["", "AFFILIATIONS", "-" * 40])
        lines.extend(entities[:10])  # Limit
        if len(entities) > 10:
            lines.append(f"  ... and {len(entities) - 10} more")

    # Site links
    sites = []
    for link in fig.findall('site_link'):
        link_type = get_child_text(link, 'link_type')
        site_id = get_child_text(link, 'site_id')
        sites.append(f"{link_type.title()}: {get_site_name(site_id)}")

    if sites:
        lines.extend(["", "SITES", "-" * 40])
        lines.extend(sites)

    # Skills (top ones)
    skills = []
    for skill in fig.findall('hf_skill'):
        skill_name = get_child_text(skill, 'skill')
        total_ip = get_child_text(skill, 'total_ip', '0')
        try:
            skills.append((skill_name, int(total_ip)))
        except ValueError:
            pass

    if skills:
        skills.sort(key=lambda x: -x[1])
        lines.extend(["", "NOTABLE SKILLS", "-" * 40])
        for skill_name, ip in skills[:8]:
            lines.append(f"{skill_name.replace('_', ' ').title()}: {ip} IP")

    # Event timeline
    events = find_all_events_for_figure(figure_id)

    if events:
        lines.extend(["", "EVENT TIMELINE", "-" * 40])
        if brief:
            # Just show counts by type
            type_counts = {}
            for event in events:
                etype = get_child_text(event, 'type')
                type_counts[etype] = type_counts.get(etype, 0) + 1
            for etype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
                lines.append(f"  {etype}: {count}")
            lines.append(f"\nTotal: {len(events)} events")
        else:
            for event in events:
                lines.append(describe_event(event, figure_id))

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Generate complete history for a figure')
    parser.add_argument('query', help='Figure ID or name pattern')
    parser.add_argument('--brief', '-b', action='store_true', help='Brief timeline (event counts only)')

    args = parser.parse_args()

    fig = find_figure(args.query)

    if fig is None:
        print(f"No figure found matching: {args.query}")

        # Suggest searching
        if not args.query.isdigit():
            print("\nTry: python3 lookup_figure.py --brief \"pattern\"")

        return 1

    print(generate_history(fig, brief=args.brief))
    return 0


if __name__ == "__main__":
    sys.exit(main())
