"""Chart and summarize the classified App Store reviews.

Reads data/classified_reviews.csv and produces two breakdowns:
  - all:      every review
  - problems: negative and neutral reviews, excluding general_praise

For each breakdown it saves five interactive charts (HTML) to
outputs/charts/<breakdown>/. The combined summary in outputs/summary.md also
covers theme shifts by app/iOS version, reviews that mention competitors, and
the most common specific feature requests.

Usage:
    python scripts/analyze.py
"""

import math
import re
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = ROOT / "data" / "classified_reviews.csv"
OUTPUT_DIR = ROOT / "outputs"
CHARTS_DIR = OUTPUT_DIR / "charts"
SUMMARY_PATH = OUTPUT_DIR / "summary.md"

# Chart styling (reference palette from the dataviz guidelines).
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
SERIES = "#2a78d6"
FONT = 'system-ui, -apple-system, "Segoe UI", sans-serif'

# Specific feature requests, matched as whole words against Claude's one-line
# summary of each feature-request review. A review can match more than one.
SPECIFIC_REQUESTS = {
    "Alarm-style alerts (louder, keep ringing, bypass silent)": r"alarms?|ring|ringing|loud|louder"
    r"|audible|sound|noticeable|dramatic|full-screen|persistent|hard-to-dismiss|nag|nagging"
    r"|vibration|vibrate|quiet",
    "Show reminders in Calendar, or choose which appear": r"calendars?",
    "Color-code reminders, more color choices": r"colou?r\w*",
    "Widget and lock-screen options": r"widgets?|lock screen|wake screen|wallpaper",
    "Snooze or quick postpone": r"snooze|move to tomorrow|move-to-next-day|to today|to tomorrow|delay\w*",
    "Choose where new items go, manual order that sticks": r"top of|to the top|bottom|insertion"
    r"|reorder\w*|rearrang\w*|manually arrange|switch the order|drag-and-drop ordering|drag day tasks",
    "Better search": r"search\w*",
    "Subtask improvements": r"sub ?tasks?|nested|bullet points?|hierarchical",
    "Attach photos, PDFs or files": r"pdfs?|pictures?|photos?|images?|finder files",
    "Turn emails into reminders, link Mail": r"e?mails?",
    "Sort alphabetically or by date": r"alphabetic\w*|date order|by date|chronological\w*|time order",
    "More repeat options (hourly, specific days, custom intervals)": r"hourly|hour-based|hours"
    r"|specific days|selected days|third thursday|fortnightly|30-day|minute-based|monthly on"
    r"|repeat-in-hours|fixed date",
    "Keep completed items visible, reset lists": r"completed today|stay visible|visible until"
    r"|incomplete|reset an entire list|unmarked|keep checked-off|strikethrough|hidden until the next day",
    "Outlook, Google, Windows or web access": r"outlook|google|windows|linux|web app|caldav|asana|notion",
    "Templates and reusable lists": r"templates?|reusable|permanent shopping|copyable",
    "Repeat from completion date": r"completion date|repeat-on-completion",
    "Habit tracking": r"habits?",
}

# App version -> the iOS release it shipped with, inferred from when each
# version's first reviews appear in the data.
APP_VERSIONS = {
    "1.7": "iOS 17", "1.8": "iOS 18", "1.9.1": "iOS 26", "2.0": "iOS 26.2", "2.6": "iOS 27",
}
# Reviews that name a specific iOS release, or blame a recent update in general.
IOS_MENTION = r"\bios ?(1[5-9]|2[0-7])(\.\d+)?\b|\b(1[78]|2[67])\.\d\b|\bliquid glass\b"
UPDATE_BLAME = (r"\b(since|after) (the )?(latest |last |new |recent )?(ios )?update"
                r"|\bupdate (broke|ruined|messed)|\b(new|latest|last) update\b")

# Competitor apps and platforms, matched against the review title and text.
# "Things" is case-sensitive and needs context, since it is also a common word.
COMPETITORS = {
    "Microsoft To Do / Outlook": r"(?i)\bmicrosoft to ?do\b|\bms to ?do\b|\bto ?do app\b|\bwunderlist\b|\boutlook\b",
    "Google Tasks / Keep / Calendar": r"(?i)\bgoogle (tasks?|keep|calendar)\b",
    "Todoist": r"(?i)\btodoist\b",
    "Samsung / Android": r"(?i)\b(samsung|android)\b",
    "Notion / Asana / Trello": r"(?i)\b(notion|asana|trello)\b",
    "Things": r"\bThings ?3\b|[‘'\"]Things[’'\"]|\bThings,",
    "TickTick": r"(?i)\btick ?tick\b",
    "OmniFocus": r"(?i)\bomni ?focus\b",
    "Fantastical": r"(?i)\bfantastical\b",
}

BREAKDOWNS = {
    "all": "All reviews",
    "problems": "Negative and neutral reviews, excluding general_praise",
}


def load():
    df = pd.read_csv(INPUT_PATH, dtype={"version": str})
    df["date"] = pd.to_datetime(df["date"], utc=True)
    df["month"] = df["date"].dt.strftime("%Y-%m")
    return df


def subsets(df):
    problems = df[df["sentiment"].isin(["negative", "neutral"]) & (df["theme"] != "general_praise")]
    return {"all": df, "problems": problems}


def theme_table(df):
    grouped = df.groupby("theme")
    table = pd.DataFrame({
        "reviews": grouped.size(),
        "avg_rating": grouped["rating"].mean(),
        "one_star_share": grouped["rating"].apply(lambda r: (r == 1).mean()),
        "feature_requests": grouped["is_feature_request"].sum(),
    })
    table["share"] = table["reviews"] / len(df)
    return table.sort_values("reviews", ascending=False)


def request_topics(df):
    requests = df[df["is_feature_request"]]
    summaries = requests["summary"].str.lower()
    counts = {
        topic: int(summaries.str.contains(rf"\b(?:{pattern})\b", regex=True).sum())
        for topic, pattern in SPECIFIC_REQUESTS.items()
    }
    return pd.Series(counts).sort_values(ascending=False), len(requests)


# --- Charts -------------------------------------------------------------------

def style(fig, title, subtitle, height):
    fig.update_layout(
        title={"text": f"{title}<br><sup style='color:{INK_SECONDARY}'>{subtitle}</sup>",
               "x": 0, "xanchor": "left", "font": {"size": 18, "color": INK}},
        font={"family": FONT, "color": INK_SECONDARY, "size": 13},
        paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
        height=height, margin={"l": 20, "r": 30, "t": 90, "b": 50},
        showlegend=False, barcornerradius=4, bargap=0.35,
        hoverlabel={"bgcolor": "white", "bordercolor": GRID, "font": {"color": INK, "family": FONT}},
    )
    fig.update_xaxes(gridcolor=GRID, zeroline=False, linecolor=BASELINE, tickfont={"color": INK_MUTED})
    fig.update_yaxes(gridcolor=GRID, zeroline=False, linecolor=BASELINE, tickfont={"color": INK_SECONDARY})
    return fig


def hbar(labels, values, hover, title, subtitle, x_title, tickformat=None, x_range=None):
    # Largest at the top: plotly draws the first category at the bottom.
    fig = go.Figure(go.Bar(
        x=values[::-1], y=labels[::-1], orientation="h", marker_color=SERIES,
        customdata=hover[::-1], hovertemplate="%{customdata}<extra></extra>",
    ))
    style(fig, title, subtitle, height=120 + 38 * len(labels))
    fig.update_xaxes(title_text=x_title, tickformat=tickformat, range=x_range, showgrid=True)
    fig.update_yaxes(showgrid=False, ticksuffix="  ")
    return fig


def chart_theme_share(table, label):
    hover = [f"<b>{r.Index}</b><br>{r.share:.1%} of reviews ({r.reviews:,})" for r in table.itertuples()]
    return hbar(list(table.index), list(table["share"]), hover,
                "Share of reviews by theme", label, "Share of reviews", tickformat=".0%")


def chart_avg_rating(table, label):
    table = table.sort_values("avg_rating")
    hover = [f"<b>{r.Index}</b><br>Average {r.avg_rating:.2f}★ across {r.reviews:,} reviews"
             for r in table.itertuples()]
    labels, values = list(table.index), list(table["avg_rating"])
    # A dot plot: the rating scale starts at 1, so bars from zero would mislead.
    fig = go.Figure(go.Scatter(
        x=values[::-1], y=labels[::-1], mode="markers",
        marker={"color": SERIES, "size": 11, "line": {"color": SURFACE, "width": 2}},
        customdata=hover[::-1], hovertemplate="%{customdata}<extra></extra>",
    ))
    style(fig, "Average star rating by theme", f"{label} · lowest rated at the top",
          height=120 + 38 * len(labels))
    fig.update_xaxes(title_text="Average rating (1–5★)", range=[0.9, 5.1], dtick=1)
    fig.update_yaxes(showgrid=True, ticksuffix="  ")
    return fig


def chart_one_star(table, label):
    table = table.sort_values("one_star_share", ascending=False)
    hover = [f"<b>{r.Index}</b><br>{r.one_star_share:.0%} are 1★ ({round(r.one_star_share * r.reviews)}"
             f" of {r.reviews:,})" for r in table.itertuples()]
    return hbar(list(table.index), list(table["one_star_share"]), hover,
                "Share of 1-star reviews by theme", label, "Share of the theme's reviews that are 1★",
                tickformat=".0%", x_range=[0, 1])


def chart_by_month(df, table, label):
    themes = list(table.index)
    months = sorted(df["month"].unique())
    counts = df.groupby(["theme", "month"]).size().unstack(fill_value=0).reindex(columns=months, fill_value=0)
    cols = 2
    rows = -(-len(themes) // cols)
    fig = make_subplots(rows=rows, cols=cols, subplot_titles=themes, shared_xaxes=True,
                        vertical_spacing=0.06, horizontal_spacing=0.06)
    for i, theme in enumerate(themes):
        fig.add_trace(go.Scatter(
            x=months, y=counts.loc[theme].tolist(), mode="lines",
            line={"color": SERIES, "width": 2},
            hovertemplate=f"<b>{theme}</b><br>%{{x}}: %{{y}} reviews<extra></extra>",
        ), row=i // cols + 1, col=i % cols + 1)
    style(fig, "Reviews per month by theme",
          f"{label} · each panel has its own scale · counts mostly reflect feed coverage: US reviews start Aug 2026, "
          "GB/CA late 2024, AU Jan 2024", height=110 + 170 * rows)
    fig.update_annotations(font={"size": 13, "color": INK})
    # Each panel gets its own labeled y-scale: on a shared scale general_praise
    # flattens every other theme.
    fig.update_yaxes(rangemode="tozero", showticklabels=True, nticks=4)
    fig.update_xaxes(tickangle=0, nticks=6)
    if len(themes) % cols:
        # The right column ends a row early, so give its last panel date labels too.
        fig.update_xaxes(showticklabels=True, row=rows - 1, col=cols)
    fig.update_layout(hovermode="x")
    return fig


def chart_requests(topics, n_requests, label):
    hover = [f"<b>{t}</b><br>{c} of {n_requests} feature-request reviews ({c / n_requests:.0%})"
             for t, c in topics.items()]
    return hbar(list(topics.index), list(topics.values), hover, "Most common specific feature requests",
                f"{label} · {n_requests} reviews flagged as feature requests; one review can ask for several",
                "Reviews asking for it")


# --- Summary ------------------------------------------------------------------

def markdown_tables(name, label, df, table, topics, n_requests):
    lines = [
        f"## {label}",
        "",
        f"{len(df):,} reviews · average rating {df['rating'].mean():.2f}★ · "
        f"{(df['rating'] == 1).mean():.0%} are 1★ · {n_requests} feature requests. "
        f"Charts: `outputs/charts/{name}/`.",
        "",
        "| Theme | Reviews | Share | Avg ★ | 1★ share | Feature requests |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for r in table.itertuples():
        lines.append(f"| {r.Index} | {r.reviews:,} | {r.share:.1%} | {r.avg_rating:.2f} | "
                     f"{r.one_star_share:.0%} | {int(r.feature_requests)} |")
    lines += ["", "**Most common specific feature requests**", "",
              "| Request | Reviews | Share of requests |",
              "|---|---:|---:|"]
    for topic, count in topics.items():
        lines.append(f"| {topic} | {count} | {count / n_requests:.0%} |")
    return lines


def two_proportion_p(x1, n1, x2, n2):
    """Two-sided p-value for a difference between two proportions (z-test)."""
    pooled = (x1 + x2) / (n1 + n2)
    se = math.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    if se == 0:
        return 1.0
    z = (x1 / n1 - x2 / n2) / se
    return math.erfc(abs(z) / math.sqrt(2))


def share_list(series, total):
    return ", ".join(f"{k} {v / total:.0%}" for k, v in series.items())


def version_section(df):
    # The US only appears from version 2.0 on, so leave it out to keep the
    # country mix the same across versions.
    data = df[df["country"] != "us"]
    versions = [v for v in APP_VERSIONS if v in set(data["version"])]
    counts = pd.crosstab(data["theme"], data["version"]).reindex(columns=versions, fill_value=0)
    totals = counts.sum()
    counts = counts.loc[counts.sum(axis=1).sort_values(ascending=False).index]

    lines = [
        "## Theme shifts by app version",
        "",
        "Share of each theme's reviews per app version, excluding US reviews (the US only appears "
        "from version 2.0, when Apple's feed starts covering it). The iOS release for each version "
        "is inferred from when its first reviews appear.",
        "",
        "| Theme | " + " | ".join(f"{v} ({APP_VERSIONS[v]})" for v in versions) + " |",
        "|---|" + "---:|" * len(versions),
    ]
    for theme, row in counts.iterrows():
        lines.append(f"| {theme} | " + " | ".join(f"{row[v] / totals[v]:.1%}" for v in versions) + " |")
    lines.append("| *reviews* | " + " | ".join(f"*{totals[v]:,}*" for v in versions) + " |")

    shifts = []
    for prev, cur in zip(versions, versions[1:]):
        for theme, row in counts.iterrows():
            p = two_proportion_p(row[cur], totals[cur], row[prev], totals[prev])
            if p < 0.05:
                shifts.append(f"- **{theme}**, {prev} → {cur}: {row[prev] / totals[prev]:.1%} → "
                              f"{row[cur] / totals[cur]:.1%} (p = {p:.3f})")
    lines += ["", "Changes from one version to the next that pass a two-proportion z-test at "
              "p < 0.05 (uncorrected for the number of comparisons):", ""]
    lines += shifts or ["- None. No theme's share changed more than chance would explain."]
    small = [f"{v} ({totals[v]} reviews)" for v in versions if totals[v] < 100]
    if small:
        lines += ["", f"Treat these with caution: with {len(counts) * (len(versions) - 1)} comparisons, "
                  "a few will pass by chance, and small versions swing easily: " + ", ".join(small) + "."]

    text = (df["title"].fillna("") + " " + df["text"].fillna("")).str.lower()
    mentions = df[text.str.contains(IOS_MENTION, regex=True)]
    blames = df[text.str.contains(UPDATE_BLAME, regex=True)]
    problems = subsets(df)["problems"]
    lines += [
        "",
        f"**Reviews naming a specific iOS release ({len(mentions)}):** "
        + share_list(mentions["theme"].value_counts(), len(mentions)) + ".",
        "",
        f"**Reviews blaming a recent update ({len(blames)}):** "
        + share_list(blames["theme"].value_counts(), len(blames))
        + f". For comparison, bugs_and_reliability is "
        f"{(problems['theme'] == 'bugs_and_reliability').mean():.0%} of all negative and neutral reviews.",
    ]
    return lines


def competitor_section(df):
    text = df["title"].fillna("") + " " + df["text"].fillna("")
    hits = pd.DataFrame({name: text.str.contains(p, regex=True) for name, p in COMPETITORS.items()})
    mentioned = df[hits.any(axis=1)]
    n = len(mentioned)
    lines = [
        "## Reviews mentioning competitors",
        "",
        f"{n} reviews ({n / len(df):.1%}) name a competing app or platform · average rating "
        f"{mentioned['rating'].mean():.2f}★ · {mentioned['is_feature_request'].mean():.0%} are "
        "feature requests. Matches are keyword-based, so treat counts as approximate.",
        "",
        "| Competitor | Reviews |",
        "|---|---:|",
    ]
    for name, count in hits.sum().sort_values(ascending=False).items():
        if count:
            lines.append(f"| {name} | {count} |")
    theme_n = mentioned["theme"].value_counts()
    all_share = df["theme"].value_counts(normalize=True)
    lines += ["", "| Theme | Competitor reviews | Share | Share of all reviews |", "|---|---:|---:|---:|"]
    for theme, count in theme_n.items():
        lines.append(f"| {theme} | {count} | {count / n:.0%} | {all_share[theme]:.0%} |")
    return lines


def main():
    df = load()
    lines = [
        "# Review analysis summary",
        "",
        f"Source: `data/classified_reviews.csv` ({len(df):,} reviews, "
        f"{df['date'].min():%b %Y} to {df['date'].max():%b %Y}). Themes, sentiment and "
        "feature-request flags come from `scripts/classify.py`.",
        "",
        "**Caveats.** Apple's feed returns only the ~500 most recent reviews per country, so the "
        "US sample covers just Aug to Oct 2026 while AU goes back to Jan 2024; monthly counts "
        "reflect that coverage, not real changes in volume. Feature-request topics are keyword "
        "matches on Claude's one-line summaries, so treat them as approximate.",
        "",
    ]
    for name, data in subsets(df).items():
        label = BREAKDOWNS[name]
        table = theme_table(data)
        topics, n_requests = request_topics(data)
        out = CHARTS_DIR / name
        out.mkdir(parents=True, exist_ok=True)
        charts = {
            "1_theme_share": chart_theme_share(table, label),
            "2_avg_rating": chart_avg_rating(table, label),
            "3_one_star_share": chart_one_star(table, label),
            "4_theme_by_month": chart_by_month(data, table, label),
            "5_feature_requests": chart_requests(topics, n_requests, label),
        }
        for filename, fig in charts.items():
            fig.write_html(out / f"{filename}.html", include_plotlyjs="cdn",
                           config={"displaylogo": False})
        lines += markdown_tables(name, label, data, table, topics, n_requests) + [""]
        print(f"{label}: {len(data):,} reviews, charts in {out.relative_to(ROOT)}")

    lines += version_section(df) + [""] + competitor_section(df) + [""]
    SUMMARY_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Summary written to {SUMMARY_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
