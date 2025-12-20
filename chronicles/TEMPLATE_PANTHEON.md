# Chronicle Template: Pantheon

This template documents the gods, worship patterns, and religious structures of a civilization.

---

## How to Use This Template

1. Copy this template to a new file (e.g., `pantheon_the_bewildering_nation.md`)
2. Use lookup scripts to gather deity data:
   ```bash
   # Find deities by checking figures with "primordial" birth
   python3 scripts/lookup_figure.py --race <race> --limit 100 | grep -E "deity|primordial"

   # Get full deity details
   python3 scripts/lookup_figure.py <deity_id>

   # Find religious entities
   python3 scripts/lookup_entity.py --list | grep religion

   # Check worship patterns in figure data
   python3 scripts/lookup_figure.py <worshipper_id>  # Shows deity links with strength
   ```
3. Cross-reference `world/parsed/entities/entities_plus.xml` for temple data
4. Check `world/parsed/events/by_type/` for religious events (ceremonies, etc.)

---

# Pantheon of [CIVILIZATION NAME]

> *"[Optional epigraph about the gods or faith]"*

## Overview

| Field | Value |
|-------|-------|
| **Civilization** | [Name] (Entity #X) |
| **Race** | |
| **Number of Deities** | |
| **Primary Faith** | Polytheistic / Monotheistic / Henotheistic |
| **Religious Organizations** | [List any formal religions] |

### Theological Summary
A 2-3 sentence summary of the civilization's religious character. What themes dominate their pantheon? Are their gods benevolent, indifferent, or dark?

---

## The Deities

### Primary Gods
The most widely worshipped deities, those central to the civilization's identity.

#### [Deity Name] (Figure #X)

| Attribute | Value |
|-----------|-------|
| **Race** | |
| **Sex** | |
| **Spheres** | |
| **Epithets** | "The [Title]" |
| **Secrets Known** | [List if any] |
| **Worship Strength** | High / Medium / Low (based on follower data) |

**Description:**
Brief description of this deity's role, personality, or significance.

**Notable Worshippers:**
- [Figure name] - strength [X]
- [Figure name] - strength [X]

---

#### [Repeat for each primary deity]

---

### Secondary Gods
Lesser deities or those with more specialized portfolios.

| Deity | ID | Spheres | Epithets | Notes |
|-------|-----|---------|----------|-------|
| | | | | |

---

### Foreign Gods
Deities from other pantheons that some members worship (e.g., through cultural exchange or corruption).

| Deity | Origin | Spheres | Who Worships | Why |
|-------|--------|---------|--------------|-----|
| | | | | |

---

## Divine Domains

### Spheres of Influence

Group the deities by their domains of power:

#### Life & Creation
| Deity | Spheres |
|-------|---------|
| | |

#### Death & Destruction
| Deity | Spheres |
|-------|---------|
| | |

#### Nature & Elements
| Deity | Spheres |
|-------|---------|
| | |

#### Civilization & Order
| Deity | Spheres |
|-------|---------|
| | |

#### War & Conflict
| Deity | Spheres |
|-------|---------|
| | |

#### Knowledge & Mystery
| Deity | Spheres |
|-------|---------|
| | |

---

## Sacred Knowledge

### Secrets of the Gods
Deities who possess forbidden or arcane knowledge:

| Deity | Secrets Known | Significance |
|-------|---------------|--------------|
| | SECRET_1, SECRET_2, ... | [Interpretation if known] |

---

## Religious Organizations

### Formal Religions
Organized religious bodies within the civilization:

| Entity | ID | Deity Served | Notes |
|--------|-----|--------------|-------|
| | | | |

### Temples & Holy Sites
Structures dedicated to worship:

| Site | Location | Deity/Purpose | Notes |
|------|----------|---------------|-------|
| | | | |

---

## Worship Patterns

### By Population
Analysis of which deities are most commonly worshipped:

| Deity | Worshippers | Avg. Strength | Notes |
|-------|-------------|---------------|-------|
| | X figures | XX | Most popular |
| | X figures | XX | |

### Corrupted Worship
Former members now monsters who still worship these gods:

| Monster | Former Identity | Still Worships | Theological Implications |
|---------|-----------------|----------------|-------------------------|
| | | | |

---

## Religious Events & Practices

### Known Ceremonies
Documented religious events from the legends:

| Event Type | Year | Location | Description |
|------------|------|----------|-------------|
| ceremony | | | |
| procession | | | |

### Festivals & Occasions
Regular celebrations (if documented):

| Occasion | Frequency | Associated Deity | Activities |
|----------|-----------|------------------|------------|
| | | | |

---

## Theological Themes

### Dominant Motifs
What themes emerge from this pantheon's spheres?

- [ ] **Light vs Dark** - Deities of day/night, truth/deception
- [ ] **Order vs Chaos** - Law, oaths vs. chaos, nightmares
- [ ] **Life vs Death** - Creation, fertility vs. death, sacrifice
- [ ] **Nature vs Civilization** - Wild elements vs. crafts, fortresses
- [ ] **War & Conflict** - Explicit war deities, revenge

### Theological Tensions
Apparent contradictions or conflicts within the faith:

- [Example: A god of "truth" in a civilization plagued by night creature deception]
- [Example: A god of "sacrifice" worshipped by the same people as a god of "peace"]

### Dark Elements
Troubling aspects of the pantheon:

| Deity | Dark Sphere | Implications |
|-------|-------------|--------------|
| | deformity | |
| | sacrifice | |
| | thralldom | |

---

## Comparison to Other Pantheons

| Aspect | This Pantheon | [Other Civ] | [Other Civ] |
|--------|---------------|-------------|-------------|
| Number of Gods | | | |
| Dominant Theme | | | |
| Death Deity | | | |
| War Deity | | | |
| Unique Spheres | | | |

---

## Research Notes

### Data Sources
- `world/parsed/figures/by_race/[race].xml` - Deity figures
- `world/parsed/entities/entities_plus.xml` - Religious organizations
- `world/parsed/events/by_type/ceremony.xml` - Religious events

### Gaps in Knowledge
- [ ] Specific worship rituals
- [ ] Mythology and creation stories
- [ ] Relationships between deities
- [ ] Priesthood structures

### Cross-References
- Chronicle: [Link to civilization chronicle]
- Related pantheons: [Links]

---

*Chronicle compiled: [Date]*
*Last updated: [Date]*
