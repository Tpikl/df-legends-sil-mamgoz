# CLAUDE.md

This project extracts and transforms Dwarf Fortress legends data into readable narratives and story documents.

## Project Structure

```
df-claude-legends/
├── world/                    # Dwarf Fortress world data
│   ├── SilMamgoz/            # Raw DF save files (compressed, do not touch)
│   ├── *-legends.xml         # Standard legends export from DF
│   └── *-legends_plus.xml    # Extended legends export from DFHack
├── stories/                  # Generated narratives and character studies
│   └── {character}/          # Per-character story folders
└── README.md
```

## Folder Guidelines

### `world/SilMamgoz/`
Raw Dwarf Fortress save data. **Leave this alone.** Contains compressed game data. Only reference if you need to verify data missing from XML exports (unlikely).

### `world/*.xml`
The legends XML files exported via Dwarf Fortress and DFHack. These are the primary data sources:
- `legends.xml` - Standard export containing historical figures, events, artifacts, sites
- `legends_plus.xml` - DFHack extended export with additional relationship and event data

### `stories/`
Contains narrative documents crafted from the legends data. Organized by subject (character, civilization, event, etc.).

## Working with This Project

1. Parse XML files to extract relevant historical data
2. Cross-reference between legends and legends_plus for complete information
3. Transform dry historical records into readable narratives
4. Store outputs in appropriate `stories/` subfolders
