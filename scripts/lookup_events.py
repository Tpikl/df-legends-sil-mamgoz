#!/usr/bin/env python3
"""
Look up events from parsed legends data.

Usage:
    python3 lookup_events.py --figure 123        # Events involving figure #123
    python3 lookup_events.py --site 45           # Events at site #45
    python3 lookup_events.py --type hf_died      # Events of a specific type
    python3 lookup_events.py --year 100-150      # Events in year range
    python3 lookup_events.py --list-types        # List all event types

Combine filters:
    python3 lookup_events.py --figure 123 --type hf_died  # Deaths of/by figure 123
"""

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PARSED_DIR = Path(__file__).parent.parent / "world" / "parsed"
EVENTS_DIR = PARSED_DIR / "events"


def get_child_text(elem, tag, default=""):
    """Get text content of a child element."""
    child = elem.find(tag)
    return child.text if child is not None and child.text else default


def event_involves_figure(event, figure_id):
    """Check if an event involves a specific figure."""
    fid = str(figure_id)

    # Check common figure-related fields
    figure_fields = [
        'hfid', 'slayer_hfid', 'changer_hfid', 'changee_hfid',
        'group_hfid', 'hist_fig_id', 'attacker_hfid', 'defender_hfid',
        'snatcher_hfid', 'victim_hfid', 'abductor_hfid', 'target_hfid',
        'hfid_target', 'hfid_1', 'hfid_2', 'woundee_hfid', 'wounder_hfid',
        'doer_hfid', 'trickster_hfid'
    ]

    for field in figure_fields:
        if get_child_text(event, field) == fid:
            return True

    return False


def event_at_site(event, site_id):
    """Check if an event occurred at a specific site."""
    return get_child_text(event, 'site_id') == str(site_id)


def event_in_year_range(event, start_year, end_year):
    """Check if an event occurred in a year range."""
    year_str = get_child_text(event, 'year', '0')
    try:
        year = int(year_str)
        return start_year <= year <= end_year
    except ValueError:
        return False


def format_event(event):
    """Format an event for display."""
    event_id = get_child_text(event, 'id')
    year = get_child_text(event, 'year', '?')
    event_type = get_child_text(event, 'type', 'unknown')

    # Build a basic description based on event type
    lines = [f"Event #{event_id} (Year {year}) - {event_type.replace('_', ' ').title()}"]

    # Add relevant details based on type
    detail_fields = {
        'hf died': ['hfid', 'slayer_hfid', 'cause', 'site_id'],
        'changed creature type': ['changee_hfid', 'changer_hfid', 'old_race', 'new_race'],
        'hf simple battle event': ['group_hfid', 'subtype', 'site_id'],
        'add hf hf link': ['hfid_1', 'hfid_2', 'link_type'],
        'remove hf hf link': ['hfid_1', 'hfid_2', 'link_type'],
        'add hf entity link': ['hfid', 'civ_id', 'link_type', 'position_id'],
        'hf learns secret': ['student_hfid', 'teacher_hfid', 'secret_text'],
        'artifact created': ['hfid', 'artifact_id', 'site_id'],
        'created site': ['site_id', 'civ_id', 'site_civ_id'],
        'hf wounded': ['woundee_hfid', 'wounder_hfid', 'site_id'],
        'creature devoured': ['victim_hfid', 'eater_hfid', 'site_id'],
        'hf abducted': ['target_hfid', 'snatcher_hfid', 'site_id'],
    }

    fields_to_show = detail_fields.get(event_type, [])
    if not fields_to_show:
        # Show all non-empty fields for unknown types
        for child in event:
            if child.text and child.tag not in ['id', 'year', 'type', 'seconds72']:
                lines.append(f"  {child.tag}: {child.text}")
    else:
        for field in fields_to_show:
            value = get_child_text(event, field)
            if value and value != '-1':
                lines.append(f"  {field}: {value}")

    return '\n'.join(lines)


def load_events_by_type(event_type):
    """Load events from a specific type file."""
    type_file = EVENTS_DIR / "by_type" / f"{event_type.lower().replace(' ', '_')}.xml"
    if not type_file.exists():
        return []

    tree = ET.parse(type_file)
    root = tree.getroot()
    return root.findall('.//historical_event')


def load_events_by_year_range(start_year, end_year):
    """Load events from year range files."""
    events = []
    year_dir = EVENTS_DIR / "by_year"

    if not year_dir.exists():
        return []

    for year_file in sorted(year_dir.glob("years_*.xml")):
        # Parse range from filename (years_0000-0049.xml)
        filename = year_file.stem
        parts = filename.replace('years_', '').split('-')
        try:
            file_start = int(parts[0])
            file_end = int(parts[1])
        except (ValueError, IndexError):
            continue

        # Check if this file's range overlaps with our target range
        if file_end < start_year or file_start > end_year:
            continue

        tree = ET.parse(year_file)
        root = tree.getroot()
        for event in root.findall('.//historical_event'):
            if event_in_year_range(event, start_year, end_year):
                events.append(event)

    return events


def load_all_event_types():
    """List all available event types."""
    type_dir = EVENTS_DIR / "by_type"
    if not type_dir.exists():
        return []

    types = []
    for type_file in sorted(type_dir.glob("*.xml")):
        tree = ET.parse(type_file)
        root = tree.getroot()
        count = len(root.findall('.//historical_event'))
        types.append((type_file.stem, count))

    return types


def search_events(figure_id=None, site_id=None, event_type=None, year_range=None, limit=50):
    """Search events with combined filters."""
    events = []

    # Determine which files to search
    if event_type:
        events = load_events_by_type(event_type)
    elif year_range:
        start, end = year_range
        events = load_events_by_year_range(start, end)
    else:
        # Need to search all - use year files as they're organized
        events = load_events_by_year_range(0, 9999)

    # Apply filters
    results = []
    for event in events:
        if figure_id and not event_involves_figure(event, figure_id):
            continue
        if site_id and not event_at_site(event, site_id):
            continue
        if year_range:
            start, end = year_range
            if not event_in_year_range(event, start, end):
                continue

        results.append(event)
        if len(results) >= limit:
            break

    # Sort by year
    results.sort(key=lambda e: int(get_child_text(e, 'year', '0')))

    return results


def main():
    parser = argparse.ArgumentParser(description='Look up historical events')
    parser.add_argument('--figure', '-f', type=int, help='Find events involving this figure ID')
    parser.add_argument('--site', '-s', type=int, help='Find events at this site ID')
    parser.add_argument('--type', '-t', help='Filter by event type')
    parser.add_argument('--year', '-y', help='Year or year range (e.g., "100" or "100-200")')
    parser.add_argument('--list-types', action='store_true', help='List all event types')
    parser.add_argument('--limit', '-l', type=int, default=50, help='Limit results (default: 50)')

    args = parser.parse_args()

    if args.list_types:
        types = load_all_event_types()
        print("Event types:")
        print("-" * 50)
        for type_name, count in sorted(types, key=lambda x: -x[1]):
            print(f"  {type_name}: {count} events")
        return 0

    if not any([args.figure, args.site, args.type, args.year]):
        parser.print_help()
        return 1

    # Parse year range
    year_range = None
    if args.year:
        if '-' in args.year:
            parts = args.year.split('-')
            year_range = (int(parts[0]), int(parts[1]))
        else:
            year = int(args.year)
            year_range = (year, year)

    results = search_events(
        figure_id=args.figure,
        site_id=args.site,
        event_type=args.type,
        year_range=year_range,
        limit=args.limit
    )

    if not results:
        print("No events found matching the criteria.")
        return 1

    print(f"Found {len(results)} event(s):\n")
    for event in results:
        print(format_event(event))
        print()

    if len(results) == args.limit:
        print(f"(Limited to {args.limit} results. Use --limit to see more.)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
