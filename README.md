# Automated Final Song Title & Version Extraction Script

## Overview
This Python script takes a spreadsheet of song titles to automatically guess the "final" song title for entries that are missing one. It also generates version numbers based on song title. It is designed for music archives where many songs have multiple versions or variations in their names (e.g., live dates, BPM tags, version numbers).

- Standardise titles for better matching using regex cleaning
- Guess missing final titles using fuzzy matching against known entries.
- Extracts and compares version numbers from song titles.
- Provide multiple comparison columns to evaluate and verify automated results with archivist entries.

The script **does not overwrite existing archivist-provided titles** but fills in blanks where possible.  
It is intended to **assist** archivists, and **all results should be checked manually**.
It was written using a spreadsheet containing a subset of songs in which all fields had a value in the 'version' column. It would need to be tested/tweaked for songs that do not have multiple version (e.g. to return blank value). 

---

## Input Columns

The CSV you load must contain at least:

| Column Name        | Description |
|--------------------|-------------|
| `title`            | Raw song title from source (may include BPMs, version numbers, etc.). |
| `Final song title` | Archivist's finalised title, if known. |
| `version`          | Archivist's recorded version number |

The Script can be modified to pull from a google spreadsheet API
---

## Output Columns

The script generates a new CSV with additional columns:

| Column Name             | Description |
|-------------------------|-------------|
| `title_stripped`        | Title after cleaning (lowercased, brackets removed, BPMs and version markers stripped). Used for matching and helps check regex behaviour. |
| `automatedFinalTitle`      | Script’s guessed final title. |
| `finalTitleComparison`    | Compares `automatedFinalTitle` to `Final song title`:<br>• `Match` – same title<br>• `Different` – titles differ<br>• `Previously missing` – no archivist title but script guessed one<br>• `No guess` – no archivist title and no script guess |
| `automatedVersion`      | Version number extracted automatically from `title` (integer only). |
| `versionComparison`     | Compares `version` (archivist) with `automatedVersion`:<br>• `Match` – both numbers match<br>• `Different` – both present but do not match<br>• `Previously missing` – archivist version blank, AI found one<br>• `no version` – neither has a version number |

---

## Manual Checking

While the script can fill in many missing titles and version numbers automatically, **human verification is essential**:

- **Check `title_stripped`** to ensure the regex is removing the intended parts of titles.
- **Review `finalTitleComparison`** to evaluate fuzzy match accuracy.
- **Review `versionComparison`** to see whether version detection aligns with archivist records.

The script’s output is a *starting point* for correction, not a final authoritative list.
It fails on version numbers where numerical values are in the song title itself. It also returned "Ad" as the final song title for "Adventure". Could be tweaked in the script, or just manually edited. 

---

## Output File

The script saves a CSV named:song_titles_with_automation.csv
Script could be modified to populate a google spreadsheet. 
