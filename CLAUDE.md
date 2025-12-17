# CLAUDE.md

This project extracts and transforms Dwarf Fortress legends data into readable narratives and story documents.

## Project Structure

```
df-claude-legends/
├── world/                        # Dwarf Fortress world data
│   ├── SilMamgoz/                # Raw DF save files (do not touch)
│   ├── *-legends.xml             # Standard legends export from DF
│   ├── *-legends_plus.xml        # Extended legends export from DFHack
│   └── parsed/                   # Split XML files (see below)
├── stories/                      # Generated narratives and character studies
│   └── {character}/              # Per-character story folders
├── scripts/                      # Utility scripts
│   └── parse_legends.py          # XML splitter script
└── README.md
```

## Folder Guidelines

### `world/SilMamgoz/`
Raw Dwarf Fortress save data. **Leave this alone.** Contains compressed game data.

### `world/*.xml`
The original monolithic legends XML files. Keep as source of truth but **prefer using parsed/ files** for lookups.

### `world/parsed/` (Preferred for lookups)
Pre-split XML files organized by category. **Use these instead of the monolithic XMLs** to avoid loading unnecessary data.

```
parsed/
├── world_info.xml              # World name: "Sil Måmgoz" (The Plane of Dragons)
├── geography/                  # Regions, rivers, mountains, underground
├── entities/                   # Civilizations, sites, populations
├── figures/                    # Historical figures
│   ├── historical_figures_all.xml      # Complete (2.2 MB)
│   ├── historical_figures_plus.xml     # Extended data from DFHack
│   └── by_race/                        # Split by race for targeted lookups
│       ├── dwarf.xml (434 figures, 1 MB)
│       ├── human.xml (264 figures, 620 KB)
│       ├── kobold.xml (28 figures)
│       ├── elf.xml (19 figures)
│       └── ... (100+ race files)
├── events/                     # Historical events (17,224 total)
│   ├── by_type/                        # Split by event type
│   │   ├── hf_died.xml (1,006 deaths)
│   │   ├── hf_simple_battle_event.xml (5,573 battles)
│   │   ├── creature_devoured.xml (4,810 events)
│   │   └── ... (60+ event types)
│   ├── by_year/                        # Split by 50-year ranges
│   │   ├── years_0000-0049.xml
│   │   ├── years_0050-0099.xml
│   │   └── ...
│   ├── event_collections.xml           # War/battle groupings
│   └── event_relationships.xml         # Figure relationship events
├── culture/                    # Artifacts, writings, music, poetry, dance
└── reference/                  # Creature definitions, historical eras
```

See `world/parsed/INDEX.md` for complete file listing with sizes.

### `stories/`
Contains narrative documents crafted from the legends data. Organized by subject (character, civilization, event, etc.).

## Working with This Project

### Quick Lookups (use parsed/ files)
1. **Find a figure by race**: Check `parsed/figures/by_race/{race}.xml`
2. **Find death events**: Check `parsed/events/by_type/hf_died.xml`
3. **Find events in a time period**: Check `parsed/events/by_year/years_XXXX-XXXX.xml`
4. **Get civilization info**: Check `parsed/entities/entities_plus.xml`

### Regenerating Parsed Files
If the source legends XMLs are updated, regenerate with:
```bash
python3 scripts/parse_legends.py
```

### Creating Narratives
1. Identify subject (figure, site, event, etc.)
2. Load relevant parsed XML files
3. Cross-reference IDs between files (e.g., figure's entity_link → entities file)
4. Transform historical records into readable narrative
5. Store output in `stories/{subject}/`
