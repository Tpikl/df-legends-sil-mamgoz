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
| `dwarf_the_tombs_roads_of_equivalence.md` | Chronicle of the fallen dwarf civilization |
| `dwarf_pantheon_the_tombs_roads_of_equivalence.md` | The six-god dwarf pantheon |
| `human_the_bewildering_nation.md` | Chronicle of the human civilization |
| `human_pantheon_the_bewildering_nation.md` | Gods and religion of the humans |
| `elf_the_unswerving_fells.md` | Chronicle of the elf civilization |
| `elf_pantheon_the_unswerving_fells.md` | The monotheistic worship of Famime |
| `kobold_faybin.md` | Chronicle of the kobold civilization |
| `kobold_pantheon_faybin.md` | The borrowed gods - kobolds with no native deities |

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
| The Tombs-Roads of Equivalence | Dwarf | #26 | **Completed** (Lost - civil war) |
| The Bewildering Nation | Human | #32 | **Completed** (Lost - monster attacks) |
| The Unswerving Fells | Elf | #30 | **Completed** (Lost - titans/night creatures) |
| The Crystalline Knights | Dwarf | #52 | Pending (conquered the Tombs-Roads) |
| Faybin | Kobold | #28 | **Completed** (Subjugated - undead thralls of necromancer) |

**Note:** All three original civilizations (dwarf, human, elf) are marked as "Lost" - their populations survive as homeless refugees but hold no territory. The kobolds (Faybin) are "Subjugated" - their historical figures exist as undead thralls serving a dwarf necromancer. This makes Sil Mamgoz a truly dark world.

## Pantheons to Chronicle

| Civilization | Deity Count | Notable Features | Status |
|--------------|-------------|------------------|--------|
| Dwarf (Tombs-Roads) | 6 | Craft/war focus, 3 organized religions, **civilization lost** | **Completed** |
| Human (Bewildering Nation) | 10 | Dark spheres (deformity, thralldom), **civilization lost** | **Completed** |
| Elf (Unswerving Fells) | 1 | Monotheistic (Famime - nature/rivers), **civilization lost** | **Completed** |
| Kobold (Faybin) | 0 native / 16 adopted | No native gods - borrowed dwarf/human deities | **Completed** |

### Known Deities Quick Reference

**Human Gods:** Tunem (#84), Nasnok (#85), Osman (#86), Islas (#87), Agwa (#88), Pabat (#89), Thab (#90), Luthi (#91), Iguk (#92), Ulet (#93)

**Dwarf Gods:** Reg (#44), Nar (#45), Risen (#46), Idrath (#47), Atir (#48), Onget (#49)

**Elf God:** Famime (#73)

**Kobold Gods:** None native - kobolds worship Onget, Nar, Risen (dwarf) and various human gods

## Relationship to Stories

Chronicles provide the **factual backbone** that stories embellish:

```
chronicles/                        stories/
  human_the_bewildering_nation.md  →  slibtu_trussmoments/
  (facts, dates, figures)       (narrative, dialog, themes)
```

When writing a story, consult the relevant chronicle first to ensure accuracy.
