#!/usr/bin/env python3
"""
Parse Dwarf Fortress legends XML files into organized smaller files.

This script splits the monolithic legends.xml and legends_plus.xml files
into smaller, categorized XML files for easier consumption.
"""

import os
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path


# Configuration
WORLD_DIR = Path(__file__).parent.parent / "world"
LEGENDS_FILE = WORLD_DIR / "SilMamgoz-00500-01-01-legends.xml"
LEGENDS_PLUS_FILE = WORLD_DIR / "SilMamgoz-00500-01-01-legends_plus.xml"
OUTPUT_DIR = WORLD_DIR / "parsed"

# Year range size for event splitting
YEAR_RANGE_SIZE = 50


def ensure_dir(path: Path):
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


def write_xml_file(filepath: Path, root_tag: str, elements: list, source_file: str = None):
    """Write elements to an XML file with proper formatting."""
    ensure_dir(filepath.parent)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        if source_file:
            f.write(f'<!-- Extracted from {source_file} -->\n')
        f.write(f'<{root_tag}>\n')
        for elem in elements:
            xml_str = ET.tostring(elem, encoding='unicode')
            # Add indentation
            indented = '\n'.join('  ' + line if line.strip() else line
                                  for line in xml_str.split('\n'))
            f.write(indented + '\n')
        f.write(f'</{root_tag}>\n')

    print(f"  Written: {filepath.relative_to(WORLD_DIR)} ({len(elements)} items)")


def extract_section(root: ET.Element, section_name: str) -> list:
    """Extract all elements from a section."""
    section = root.find(section_name)
    if section is None:
        return []
    return list(section)


def get_child_text(elem: ET.Element, tag: str, default: str = "") -> str:
    """Get text content of a child element."""
    child = elem.find(tag)
    return child.text if child is not None and child.text else default


def parse_legends_file(filepath: Path) -> ET.Element:
    """Parse an XML file, handling encoding issues."""
    print(f"Parsing {filepath.name}...")

    # Read and fix encoding declaration if needed
    with open(filepath, 'rb') as f:
        content = f.read()

    # Replace CP437 encoding declaration with UTF-8
    content = content.replace(b"encoding='CP437'", b"encoding='UTF-8'")

    # Decode, replacing problematic characters
    text = content.decode('utf-8', errors='replace')

    return ET.fromstring(text)


def split_figures_by_race(figures: list) -> dict:
    """Group historical figures by race."""
    by_race = defaultdict(list)

    for fig in figures:
        race = get_child_text(fig, 'race', 'UNKNOWN').lower()
        # Normalize race names
        race = race.replace(' ', '_')
        by_race[race].append(fig)

    return dict(by_race)


def split_events_by_type(events: list) -> dict:
    """Group events by type."""
    by_type = defaultdict(list)

    for event in events:
        event_type = get_child_text(event, 'type', 'unknown')
        # Normalize type names for filenames
        type_key = event_type.replace(' ', '_').lower()
        by_type[type_key].append(event)

    return dict(by_type)


def split_events_by_year(events: list, range_size: int = YEAR_RANGE_SIZE) -> dict:
    """Group events by year ranges."""
    by_year_range = defaultdict(list)

    for event in events:
        year_str = get_child_text(event, 'year', '0')
        try:
            year = int(year_str)
        except ValueError:
            year = 0

        # Calculate range
        range_start = (year // range_size) * range_size
        range_end = range_start + range_size - 1
        range_key = f"{range_start:04d}-{range_end:04d}"
        by_year_range[range_key].append(event)

    return dict(by_year_range)


def process_geography(legends_root: ET.Element, legends_plus_root: ET.Element):
    """Extract geography-related sections."""
    print("\nProcessing geography...")
    geo_dir = OUTPUT_DIR / "geography"

    # From legends.xml
    sections = ['regions', 'underground_regions']
    for section in sections:
        elements = extract_section(legends_root, section)
        if elements:
            write_xml_file(geo_dir / f"{section}.xml", section, elements, "legends.xml")

    # From legends_plus.xml (has additional geo data)
    plus_sections = ['landmasses', 'mountain_peaks', 'rivers', 'regions', 'underground_regions']
    for section in plus_sections:
        elements = extract_section(legends_plus_root, section)
        if elements:
            write_xml_file(geo_dir / f"{section}_plus.xml", section, elements, "legends_plus.xml")


def process_entities(legends_root: ET.Element, legends_plus_root: ET.Element):
    """Extract entity-related sections."""
    print("\nProcessing entities...")
    ent_dir = OUTPUT_DIR / "entities"

    # From legends.xml
    for section in ['entities', 'entity_populations', 'sites']:
        elements = extract_section(legends_root, section)
        if elements:
            write_xml_file(ent_dir / f"{section}.xml", section, elements, "legends.xml")

    # From legends_plus.xml (richer entity data)
    for section in ['entities', 'entity_populations', 'sites']:
        elements = extract_section(legends_plus_root, section)
        if elements:
            write_xml_file(ent_dir / f"{section}_plus.xml", section, elements, "legends_plus.xml")


def process_figures(legends_root: ET.Element, legends_plus_root: ET.Element):
    """Extract and split historical figures by race."""
    print("\nProcessing historical figures...")
    fig_dir = OUTPUT_DIR / "figures"

    # From legends.xml - split by race
    figures = extract_section(legends_root, 'historical_figures')
    if figures:
        # Write complete file
        write_xml_file(fig_dir / "historical_figures_all.xml", "historical_figures",
                       figures, "legends.xml")

        # Split by race
        by_race = split_figures_by_race(figures)
        race_dir = fig_dir / "by_race"
        for race, race_figures in sorted(by_race.items(), key=lambda x: -len(x[1])):
            write_xml_file(race_dir / f"{race}.xml", "historical_figures",
                          race_figures, "legends.xml")

    # From legends_plus.xml
    figures_plus = extract_section(legends_plus_root, 'historical_figures')
    if figures_plus:
        write_xml_file(fig_dir / "historical_figures_plus.xml", "historical_figures",
                       figures_plus, "legends_plus.xml")

    # Identities (legends_plus only)
    identities = extract_section(legends_plus_root, 'identities')
    if identities:
        write_xml_file(fig_dir / "identities.xml", "identities", identities, "legends_plus.xml")


def process_events(legends_root: ET.Element, legends_plus_root: ET.Element):
    """Extract and split historical events."""
    print("\nProcessing historical events...")
    evt_dir = OUTPUT_DIR / "events"

    # Event collections (not splitting these - they're structural)
    collections = extract_section(legends_root, 'historical_event_collections')
    if collections:
        write_xml_file(evt_dir / "event_collections.xml", "historical_event_collections",
                       collections, "legends.xml")

    # Event relationships from legends_plus
    relationships = extract_section(legends_plus_root, 'historical_event_relationships')
    if relationships:
        write_xml_file(evt_dir / "event_relationships.xml", "historical_event_relationships",
                       relationships, "legends_plus.xml")

    rel_suppl = extract_section(legends_plus_root, 'historical_event_relationship_supplements')
    if rel_suppl:
        write_xml_file(evt_dir / "event_relationship_supplements.xml",
                       "historical_event_relationship_supplements", rel_suppl, "legends_plus.xml")

    # Historical events from legends.xml - split by type AND year
    events = extract_section(legends_root, 'historical_events')
    if events:
        print(f"  Total events: {len(events)}")

        # Split by type
        by_type = split_events_by_type(events)
        type_dir = evt_dir / "by_type"
        for event_type, type_events in sorted(by_type.items(), key=lambda x: -len(x[1])):
            write_xml_file(type_dir / f"{event_type}.xml", "historical_events",
                          type_events, "legends.xml")

        # Split by year range
        by_year = split_events_by_year(events)
        year_dir = evt_dir / "by_year"
        for year_range, year_events in sorted(by_year.items()):
            write_xml_file(year_dir / f"years_{year_range}.xml", "historical_events",
                          year_events, "legends.xml")


def process_culture(legends_root: ET.Element, legends_plus_root: ET.Element):
    """Extract culture-related sections."""
    print("\nProcessing culture...")
    culture_dir = OUTPUT_DIR / "culture"

    sections = ['artifacts', 'written_contents', 'musical_forms', 'poetic_forms', 'dance_forms']

    for section in sections:
        # From legends.xml
        elements = extract_section(legends_root, section)
        if elements:
            write_xml_file(culture_dir / f"{section}.xml", section, elements, "legends.xml")

        # From legends_plus.xml (if different/richer)
        elements_plus = extract_section(legends_plus_root, section)
        if elements_plus and len(elements_plus) != len(elements):
            write_xml_file(culture_dir / f"{section}_plus.xml", section,
                          elements_plus, "legends_plus.xml")


def process_reference(legends_root: ET.Element, legends_plus_root: ET.Element):
    """Extract reference/metadata sections."""
    print("\nProcessing reference data...")
    ref_dir = OUTPUT_DIR / "reference"

    # Historical eras
    eras = extract_section(legends_root, 'historical_eras')
    if eras:
        write_xml_file(ref_dir / "historical_eras.xml", "historical_eras", eras, "legends.xml")

    # Creature raw (legends_plus only)
    creatures = extract_section(legends_plus_root, 'creature_raw')
    if creatures:
        write_xml_file(ref_dir / "creature_raw.xml", "creature_raw", creatures, "legends_plus.xml")

    # World constructions (legends_plus only)
    constructions = extract_section(legends_plus_root, 'world_constructions')
    if constructions:
        write_xml_file(ref_dir / "world_constructions.xml", "world_constructions",
                       constructions, "legends_plus.xml")


def process_world_info(legends_plus_root: ET.Element):
    """Extract world-level metadata."""
    print("\nProcessing world info...")

    # Get world name and altname from legends_plus
    name = legends_plus_root.find('name')
    altname = legends_plus_root.find('altname')

    filepath = OUTPUT_DIR / "world_info.xml"
    ensure_dir(filepath.parent)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<!-- World metadata extracted from legends_plus.xml -->\n')
        f.write('<world_info>\n')
        if name is not None:
            f.write(f'  <name>{name.text}</name>\n')
        if altname is not None:
            f.write(f'  <altname>{altname.text}</altname>\n')
        f.write('</world_info>\n')

    print(f"  Written: {filepath.relative_to(WORLD_DIR)}")


def create_index():
    """Create an index file listing all parsed files."""
    print("\nCreating index...")

    index_path = OUTPUT_DIR / "INDEX.md"

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("# Parsed Legends Data Index\n\n")
        f.write("This directory contains Dwarf Fortress legends data split into smaller files.\n\n")
        f.write("## Directory Structure\n\n")

        for category in ['geography', 'entities', 'figures', 'events', 'culture', 'reference']:
            cat_dir = OUTPUT_DIR / category
            if cat_dir.exists():
                f.write(f"### {category.title()}\n\n")
                for xml_file in sorted(cat_dir.rglob("*.xml")):
                    rel_path = xml_file.relative_to(OUTPUT_DIR)
                    size_kb = xml_file.stat().st_size // 1024
                    f.write(f"- `{rel_path}` ({size_kb} KB)\n")
                f.write("\n")

    print(f"  Written: {index_path.relative_to(WORLD_DIR)}")


def main():
    """Main entry point."""
    print("=" * 60)
    print("Dwarf Fortress Legends XML Parser")
    print("=" * 60)

    # Check source files exist
    if not LEGENDS_FILE.exists():
        print(f"ERROR: {LEGENDS_FILE} not found")
        return 1
    if not LEGENDS_PLUS_FILE.exists():
        print(f"ERROR: {LEGENDS_PLUS_FILE} not found")
        return 1

    # Clean output directory
    if OUTPUT_DIR.exists():
        import shutil
        shutil.rmtree(OUTPUT_DIR)
    ensure_dir(OUTPUT_DIR)

    # Parse source files
    legends_root = parse_legends_file(LEGENDS_FILE)
    legends_plus_root = parse_legends_file(LEGENDS_PLUS_FILE)

    # Process each category
    process_world_info(legends_plus_root)
    process_geography(legends_root, legends_plus_root)
    process_entities(legends_root, legends_plus_root)
    process_figures(legends_root, legends_plus_root)
    process_events(legends_root, legends_plus_root)
    process_culture(legends_root, legends_plus_root)
    process_reference(legends_root, legends_plus_root)

    # Create index
    create_index()

    print("\n" + "=" * 60)
    print("Done! Parsed files written to: world/parsed/")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
