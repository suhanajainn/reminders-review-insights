"""Check Haiku's theme labels against an independent second rater.

Draws a fixed random sample from data/classified_reviews.csv, has a stronger
model assign a theme to each review using the same themes.md codebook and
prompt (without seeing Haiku's label), and writes agreement statistics and
the most common disagreements to outputs/validation_results.md. The second
rater's labels are saved to outputs/second_rater_labels.csv.

The sample uses the same seed as data/validation_sample.csv, so it covers the
same 100 reviews you can label by hand.

Usage:
    python scripts/second_rater.py
"""

import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import anthropic
import pandas as pd
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent))
from classify import INSTRUCTIONS, MODEL as FIRST_MODEL, classify, load_themes, output_schema  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = ROOT / "data" / "classified_reviews.csv"
OUTPUT_DIR = ROOT / "outputs"
REPORT_PATH = OUTPUT_DIR / "validation_results.md"
LABELS_PATH = OUTPUT_DIR / "second_rater_labels.csv"

SECOND_MODEL = "claude-sonnet-5-5"
SAMPLE_SIZE = 100
SEED = 42
WORKERS = 5
MAX_RETRIES = 8
TOP_DISAGREEMENTS = 5
EXAMPLES_PER_DISAGREEMENT = 2


def cohens_kappa(a, b):
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    expected = sum(ca[k] * cb[k] for k in ca) / (n * n)
    return (observed - expected) / (1 - expected) if expected < 1 else 1.0


def excerpt(text, limit=220):
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def build_report(sample, themes):
    first, second = sample["theme"].tolist(), sample["second_theme"].tolist()
    n = len(sample)
    agree = sum(x == y for x, y in zip(first, second))
    kappa = cohens_kappa(first, second)

    lines = [
        "# Theme validation: second rater",
        "",
        f"A random sample of {n} reviews from `data/classified_reviews.csv` (seed {SEED}) was "
        f"re-labeled by `{SECOND_MODEL}` using the same `themes.md` codebook and prompt as the "
        f"original `{FIRST_MODEL}` run. The second rater did not see the first label.",
        "",
        "## Agreement",
        "",
        f"- **Agreement rate:** {agree}/{n} ({agree / n:.0%})",
        f"- **Cohen's kappa:** {kappa:.2f} (agreement corrected for chance)",
        "",
        "## By theme",
        "",
        f"| Theme | {FIRST_MODEL} | {SECOND_MODEL} | Both agree |",
        "|---|---|---|---|",
    ]
    cf, cs = Counter(first), Counter(second)
    both = Counter(x for x, y in zip(first, second) if x == y)
    for theme in themes:
        if cf[theme] or cs[theme]:
            lines.append(f"| {theme} | {cf[theme]} | {cs[theme]} | {both[theme]} |")

    disagreements = sample[sample["theme"] != sample["second_theme"]]
    pairs = Counter(zip(disagreements["theme"], disagreements["second_theme"]))
    lines += ["", "## Most common disagreements", ""]
    if not pairs:
        lines.append("None: the two raters agreed on every review.")
    for (a, b), count in pairs.most_common(TOP_DISAGREEMENTS):
        lines += [f"### {FIRST_MODEL}: `{a}` → {SECOND_MODEL}: `{b}` ({count})", ""]
        rows = disagreements[(disagreements["theme"] == a) & (disagreements["second_theme"] == b)]
        for row in rows.head(EXAMPLES_PER_DISAGREEMENT).itertuples():
            lines.append(
                f"> **{row.rating}★ · {excerpt(row.title, 80)}**: {excerpt(row.text)} "
                f"(`{row.review_id}`)"
            )
            lines.append("")
    remaining = len(pairs) - min(len(pairs), TOP_DISAGREEMENTS)
    if remaining > 0:
        lines.append(
            f"{remaining} other disagreement pair(s) not shown; "
            f"see `{LABELS_PATH.relative_to(ROOT)}`."
        )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    load_dotenv(ROOT / ".env")
    client = anthropic.Anthropic(max_retries=MAX_RETRIES)

    codebook, themes = load_themes()
    system = INSTRUCTIONS.format(codebook=codebook)
    schema = output_schema(themes)

    data = pd.read_csv(INPUT_PATH, dtype=str, keep_default_na=False)
    sample = data.sample(n=SAMPLE_SIZE, random_state=SEED).reset_index(drop=True)
    # Send only the raw review fields so the second rater can't see Haiku's labels.
    reviews = sample[["review_id", "rating", "title", "text"]].to_dict("records")

    print(f"Labeling {len(reviews)} reviews with {SECOND_MODEL}")
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
    REPORT_PATH.write_text(build_report(sample, themes), encoding="utf-8")

    agree = (sample["theme"] == sample["second_theme"]).mean()
    print(f"Agreement: {agree:.0%}. Report written to {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
