"""Second-model consistency check on the memo's three priority themes.

Draws 10 random reviews (fixed seed) from each of bugs_and_reliability,
notifications_and_alarms and intrusive_prompts in data/classified_reviews.csv,
has a second model assign a theme using the same themes.md codebook and prompt
(without seeing the original label), and reports agreement per theme.

This checks consistency between two models, not correctness: it is not human
validation. Results are written to their own section of
outputs/validation_results.md (replaced on rerun) and the labels to
outputs/priority_check_labels.csv.

Usage:
    python scripts/priority_check.py
"""

import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import anthropic
import pandas as pd
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent))
from classify import INSTRUCTIONS, MODEL as FIRST_MODEL, classify, load_themes, output_schema  # noqa: E402
from second_rater import SECOND_MODEL, excerpt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = ROOT / "data" / "classified_reviews.csv"
OUTPUT_DIR = ROOT / "outputs"
REPORT_PATH = OUTPUT_DIR / "validation_results.md"
LABELS_PATH = OUTPUT_DIR / "priority_check_labels.csv"

PRIORITY_THEMES = ["bugs_and_reliability", "notifications_and_alarms", "intrusive_prompts"]
PER_THEME = 10
SEED = 42
WORKERS = 5
MAX_RETRIES = 8

SECTION_START = "<!-- priority-check:start -->"
SECTION_END = "<!-- priority-check:end -->"


def build_section(sample):
    n = len(sample)
    agree = (sample["theme"] == sample["second_theme"]).sum()
    lines = [
        SECTION_START,
        "## Priority themes: second-model consistency check",
        "",
        f"**This is a consistency check between two AI models, not human validation.** "
        f"{PER_THEME} random reviews (seed {SEED}) from each of the memo's three priority themes were "
        f"re-labeled by `{SECOND_MODEL}` with the same `themes.md` codebook and prompt as the original "
        f"`{FIRST_MODEL}` labels, without seeing them. Agreement means the two models read the review "
        "the same way; it does not show the label is correct.",
        "",
        f"**Overall:** {agree}/{n} ({agree / n:.0%}) agree.",
        "",
        f"| {FIRST_MODEL} theme | Agree | {SECOND_MODEL} chose instead |",
        "|---|---:|---|",
    ]
    for theme in PRIORITY_THEMES:
        rows = sample[sample["theme"] == theme]
        theme_agree = (rows["second_theme"] == theme).sum()
        others = rows.loc[rows["second_theme"] != theme, "second_theme"].value_counts()
        instead = ", ".join(f"`{t}` ({c})" for t, c in others.items()) or "-"
        lines.append(f"| {theme} | {theme_agree}/{len(rows)} | {instead} |")

    disagreements = sample[sample["theme"] != sample["second_theme"]]
    lines += ["", "### Disagreements", ""]
    if disagreements.empty:
        lines.append("None: the two models agreed on every review.")
    for row in disagreements.itertuples():
        lines.append(
            f"> **`{row.theme}` → `{row.second_theme}`** · {row.rating}★ · "
            f"**{excerpt(row.title, 80)}**: {excerpt(row.text, 300)} (`{row.review_id}`)"
        )
        lines.append("")
    lines.append(SECTION_END)
    return "\n".join(lines).rstrip() + "\n"


def write_section(section):
    """Add or replace this check's section in validation_results.md."""
    existing = REPORT_PATH.read_text(encoding="utf-8") if REPORT_PATH.exists() else ""
    pattern = re.compile(re.escape(SECTION_START) + r".*?" + re.escape(SECTION_END) + r"\n?", re.S)
    if pattern.search(existing):
        updated = pattern.sub(lambda _: section, existing)
    else:
        updated = existing.rstrip() + "\n\n" + section if existing else section
    REPORT_PATH.write_text(updated, encoding="utf-8")


def main():
    load_dotenv(ROOT / ".env")
    client = anthropic.Anthropic(max_retries=MAX_RETRIES)

    codebook, themes = load_themes()
    system = INSTRUCTIONS.format(codebook=codebook)
    schema = output_schema(themes)

    data = pd.read_csv(INPUT_PATH, dtype=str, keep_default_na=False)
    sample = pd.concat(
        data[data["theme"] == theme].sample(n=PER_THEME, random_state=SEED)
        for theme in PRIORITY_THEMES
    ).reset_index(drop=True)
    # Send only the raw review fields so the second model can't see the original label.
    reviews = sample[["review_id", "rating", "title", "text"]].to_dict("records")

    print(f"Labeling {len(reviews)} priority-theme reviews with {SECOND_MODEL}")
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        results = list(executor.map(
            lambda r: classify(client, system, schema, r, model=SECOND_MODEL, max_tokens=8000),
            reviews,
        ))
    sample["second_theme"] = [r["theme"] for r in results]

    OUTPUT_DIR.mkdir(exist_ok=True)
    sample[["review_id", "rating", "title", "text", "theme", "second_theme"]].rename(
        columns={"theme": "first_theme"}
    ).to_csv(LABELS_PATH, index=False)
    write_section(build_section(sample))

    for theme in PRIORITY_THEMES:
        rows = sample[sample["theme"] == theme]
        print(f"  {theme}: {(rows['second_theme'] == theme).sum()}/{len(rows)} agree")
    print(f"Section written to {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
