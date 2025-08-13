import pandas as pd
from rapidfuzz import fuzz, process
import re

# Load spreadsheet, to be adapted for google sheet API 
df = pd.read_csv("song_titles.csv")

# Make a copy to not overwrite original columns
df_out = df.copy()

# Keep only rows with known final titles from archivist
known_rows = df_out[df_out["Final song title"].notna()]

# Function to clean song titles for better matching
def clean_title(t):
    if pd.isna(t):
        return ""
    t = t.lower()
    t = re.sub(r"\(.*?\)", "", t)           # remove parentheses
    t = re.sub(r"[vV].*$", "", t)           # remove everything from 'v' onwards  
    t = re.sub(r"\bv\d+\b", "", t)          # remove 'v10'
    t = re.sub(r"@\d+", "", t)              # remove '@95'
    t = re.sub(r"\s\d.*$", "", t)           # remoive space + numer and everything after it. Consider commenting out if titles have numbers as part of genuine title. 
    t = re.sub(r"[-_]", " ", t)             # replace separators with spaces
    t = re.sub(r"\s+", " ", t)              # collapse multiple spaces
    return t.strip()

# Show cleaned version (stripped) and removed portion for QA
df_out["titleStripped"] = df_out["title"].apply(clean_title)

#df_out["title_removed"] = df_out.apply(
#    lambda row: row["title"].replace(row["title_stripped"], "").strip(),
 #   axis=1
# )
# Function to guess the final title and return both guess + score
# Get unique stripped titles
unique_titles = df_out["titleStripped"].unique()

# Function to find the "canonical" stripped title for a given title
def find_canonical_title(stripped):
    match = process.extractOne(
        stripped,
        unique_titles,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=90  # <-- adjust threshold here
    )
    if match:
        return match[0]  # The canonical title
    return stripped

# Create finalTitleScript using fuzzy grouping
df_out["finalTitleScript"] = df_out["titleStripped"].apply(find_canonical_title)

# Add comparison column
df_out["finalTitleComparison"] = df_out.apply(
    lambda row: (
        "previously missing" if pd.isna(row["Final song title"]) else
        ("Match" if str(row["Final song title"]).strip().lower() ==
                   str(row["finalTitleScript"]).strip().lower()
         else "Different")
    ),
    axis=1
)

# --- Extract automatedVersion ---
def extract_version_number(text):
    if pd.isna(text):
        return None
    # Look for patterns like v3, v3b, 3, 3b, version 4, etc.
    match = re.search(r"(?:v|version\s*)?(\d+)", str(text).lower())
    return int(match.group(1)) if match else None

df_out["automatedVersion"] = df_out["title"].apply(extract_version_number)

# --- Compare archivist version with automated ---
def compare_versions(row):
    v_arch_num = extract_version_number(row["version"])
    v_auto_num = row["automatedVersion"]

    if v_arch_num is None and v_auto_num is not None:
        return "Previously missing"
    if v_arch_num is not None and v_auto_num is not None:
        return "match" if v_arch_num == v_auto_num else "Different"
    return "No version"

df_out["versionComparison"] = df_out.apply(compare_versions, axis=1)

# Save as CSV
df_out.to_csv("song_titles_with_automation.csv", index=False, encoding="utf-8-sig")

print("script-generated titles, scores, and comparison saved to song_titles_with_automation.csv")