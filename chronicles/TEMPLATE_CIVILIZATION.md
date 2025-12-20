# Chronicle Template: Civilization

This template provides a structured format for documenting the history of any civilization in the legends. It can be applied to dwarven, human, elven, kobold, or any other civilization.

---

## How to Use This Template

1. Copy this template to a new file named after the civilization (e.g., `the_bewildering_nation.md`)
2. Use the lookup scripts to gather data:
   - `python3 scripts/lookup_entity.py <ID>` - Basic entity info
   - `python3 scripts/lookup_entity.py --list` - Find entity IDs
   - `python3 scripts/lookup_site.py --list` - Find sites
   - `python3 scripts/lookup_figure.py --race <race>` - Find historical figures
   - `python3 scripts/lookup_events.py --site <ID>` - Events at a site
3. Cross-reference `world/parsed/entities/entities_plus.xml` for detailed data
4. Fill in each section, marking unknown items with `[UNKNOWN]` or `[TO RESEARCH]`

---

# [CIVILIZATION NAME]

> *"[Optional epigraph or quote that captures the civilization's essence]"*

## Overview

| Field | Value |
|-------|-------|
| **Entity ID** | # |
| **Race** | |
| **Type** | civilization |
| **Founded** | Year [X] or "Before recorded history" |
| **Status** | Active / Fallen / Diminished |
| **Capital** | [Site name] (if applicable) |

### Brief Summary
A 2-3 sentence summary of who this civilization is and their place in world history.

---

## Geography & Territory

### Current Holdings
List of sites currently controlled:

| Site | Type | Coordinates | Governing Entity | Notable Structures |
|------|------|-------------|------------------|-------------------|
| | | | | |

### Lost Holdings
Sites that were destroyed or conquered:

| Site | Type | Years Held | Fate |
|------|------|-----------|------|
| | | | Destroyed by [X] in Year [Y] |

### Territorial Notes
- Geographic region description
- Climate/biome if known
- Strategic significance

---

## Government & Structure

### Leadership Positions
Titles and roles within the civilization:

| Position | Description | Current Holder (if any) |
|----------|-------------|------------------------|
| | | Figure #X |

### Child Entities
Sub-organizations that belong to this civilization:

| Entity | Type | Notes |
|--------|------|-------|
| | sitegovernment | |
| | guild | |
| | religion | |
| | nomadicgroup | |
| | performancetroupe | |

---

## Religion & Culture

### Pantheon Overview

| Field | Value |
|-------|-------|
| **Deity Count** | |
| **Primary Faith** | Polytheistic / Monotheistic |
| **Dominant Themes** | (e.g., war, craft, nature) |

*See [TEMPLATE_PANTHEON.md](TEMPLATE_PANTHEON.md) for full deity documentation.*

### Religious Organizations

| Entity | Type | Deity Served |
|--------|------|--------------|
| | religion | |

### Cultural Practices
- Festivals/occasions observed
- Art forms (music, poetry, dance)
- Notable traditions

### Artifacts
Important items created or held by this civilization:

| Artifact | Type | Creator | Current Location |
|----------|------|---------|-----------------|
| | | | |

---

## Historical Figures

### Rulers & Leaders
Figures who held positions of power:

| Figure | Titles Held | Years Active | Fate |
|--------|------------|--------------|------|
| | | | |

### Heroes & Champions
Notable warriors, adventurers, or defenders:

| Figure | Deeds | Years Active | Fate |
|--------|-------|--------------|------|
| | | | |

### Villains & Traitors
Those who betrayed or harmed the civilization:

| Figure | Crimes/Actions | Fate |
|--------|---------------|------|
| | | |

### The Transformed
Members who became monsters, vampires, or other creatures:

| Figure | Original Identity | Transformed Into | Year | Circumstances |
|--------|------------------|------------------|------|---------------|
| | | | | |

---

## Wars & Conflicts

### Major Wars
Organized conflicts involving this civilization:

| War/Conflict | Years | Opponents | Outcome |
|--------------|-------|-----------|---------|
| | | | Victory / Defeat / Ongoing / Stalemate |

### Beast Attacks
Notable attacks by megabeasts, titans, or forgotten beasts:

| Attacker | Target Site | Year | Outcome |
|----------|-------------|------|---------|
| | | | Repelled / Site Destroyed / Attacker Slain |

### Night Creature Predation
Abductions and attacks by night creatures:

| Predator | Victims | Site | Year | Notes |
|----------|---------|------|------|-------|
| | | | | |

---

## Timeline of Major Events

A chronological listing of significant events:

### Before Year 1 (Mythic Era)
- Foundation events, if known

### Early History (Years 1-50)
- Year X: [Event description]

### Middle History (Years 51-200)
- Year X: [Event description]

### Recent History (Years 201-Present)
- Year X: [Event description]

---

## Current State

### Population
- Estimated figures count: [X] living members
- Notable demographics

### Threats
Current dangers facing the civilization:
- [ ] Active enemy civilizations
- [ ] Monster threats
- [ ] Internal problems

### Prospects
Assessment of the civilization's future:
- Strengths
- Weaknesses
- Likely trajectory

---

## Research Notes

### Data Sources Used
- `world/parsed/entities/entities_plus.xml` - Entity ID #X
- `world/parsed/figures/by_race/[race].xml`
- `world/parsed/events/by_type/[type].xml`

### Gaps in Knowledge
Items that couldn't be determined from available data:
- [ ]
- [ ]

### Cross-References
Related chronicles to consult:
- [Link to related civilization chronicle]
- [Link to related figure story]

---

*Chronicle compiled: [Date]*
*Last updated: [Date]*
