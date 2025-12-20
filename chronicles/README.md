# Chronicles

Structured historical documents for civilizations, entities, and major world events in Sil Måmgoz.

## Purpose

Unlike the narrative `stories/` folder, chronicles are **factual reference documents** that compile and organize legends data into readable historical records. They serve as:

1. **Reference material** for writing narratives
2. **World-building documentation** for understanding the setting
3. **Reusable templates** that can be applied to any civilization

## Files

| File | Description |
|------|-------------|
| `TEMPLATE_CIVILIZATION.md` | Master template for documenting any civilization |
| `TEMPLATE_PANTHEON.md` | Template for documenting a civilization's gods and religion |
| `the_bewildering_nation.md` | Chronicle of the human civilization |
| `pantheon_the_bewildering_nation.md` | Gods and religion of the humans |

## Template System

### Available Templates

- **TEMPLATE_CIVILIZATION.md** - For documenting civilizations (dwarf, human, elf, kobold, etc.)
- **TEMPLATE_PANTHEON.md** - For documenting pantheons, deities, and religious practices

### Planned Templates

- `TEMPLATE_MEGABEAST.md` - For titans, forgotten beasts, and rocs
- `TEMPLATE_SITE.md` - For fortresses, hamlets, lairs
- `TEMPLATE_WAR.md` - For military conflicts between entities
- `TEMPLATE_ARTIFACT.md` - For notable items and their histories

## Usage

1. Copy the relevant template
2. Use lookup scripts to gather data:
   ```bash
   python3 scripts/lookup_entity.py <ID>
   python3 scripts/lookup_figure.py --race <race>
   python3 scripts/lookup_events.py --site <ID>
   python3 scripts/figure_history.py <ID>
   ```
3. Fill in sections systematically
4. Mark unknowns as `[TO RESEARCH]`
5. Add cross-references to related chronicles and stories

## Civilizations to Chronicle

Priority civilizations for future documentation:

| Entity | Race | ID | Status |
|--------|------|-----|--------|
| The Bewildering Nation | Human | #32 | **Completed** |
| The Tombs-Roads of Equivalence | Dwarf | #26 | Pending |
| The Unswerving Fells | Elf | #30 | Pending |
| Faybin | Kobold | #28 | Pending |

## Pantheons to Chronicle

| Civilization | Deity Count | Notable Features | Status |
|--------------|-------------|------------------|--------|
| Human (Bewildering Nation) | 10 | Dark spheres (deformity, thralldom), corrupted worship | **Completed** |
| Dwarf (Tombs-Roads) | 6+ | Craft/war focus, organized religions | Pending |
| Elf (Unswerving Fells) | 1 | Monotheistic (Famime - unknown race) | Pending |

### Known Deities Quick Reference

**Human Gods:** Tunem (#84), Nasnok (#85), Osman (#86), Islas (#87), Agwa (#88), Pabat (#89), Thab (#90), Luthi (#91), Iguk (#92), Ulet (#93)

**Dwarf Gods:** Reg (#44), Nar (#45), Risen (#46), Atir (#48), Onget (#49)

**Elf God:** Famime (#73)

## Relationship to Stories

Chronicles provide the **factual backbone** that stories embellish:

```
chronicles/               stories/
  the_bewildering_nation.md  →  slibtu_trussmoments/
  (facts, dates, figures)       (narrative, dialog, themes)
```

When writing a story, consult the relevant chronicle first to ensure accuracy.
