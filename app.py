"""Streamlit dashboard for the Apple Reminders App Store review analysis.

Reads data/classified_reviews.csv and memo.md only; it makes no API calls.
Theme, request and period definitions come from scripts/analyze.py so the
dashboard matches outputs/summary.md.

Run with:
    streamlit run app.py
"""

import re
import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
import analyze  # noqa: E402

MEMO_PATH = ROOT / "memo.md"
SERIES_2 = "#eb6834"  # second categorical slot, for the US series
PLOTLY_CONFIG = {"displaylogo": False}

st.set_page_config(page_title="Reminders Review Insights", page_icon="✅", layout="wide")


@st.cache_data
def load_reviews():
    return analyze.load()


@st.cache_data
def load_memo():
    return MEMO_PATH.read_text(encoding="utf-8") if MEMO_PATH.exists() else ""


def memo_section(memo, heading):
    """Return (heading line, body) of the memo section whose heading starts with `heading`."""
    match = re.search(rf"^## ({re.escape(heading)}.*?)$\n(.*?)(?=^## |\Z)", memo, re.M | re.S)
    return (match.group(1).strip(), match.group(2).strip()) if match else (None, "")


def parse_recommendations(body):
    """Split the memo's Top 3 section into title, evidence, recommendation and metric."""
    recs = []
    for block in re.split(r"\n(?=\*\*\d+\. )", body):
        title = re.match(r"\*\*(\d+)\. (.+?)\*\*", block)
        if not title:
            continue
        rest = block[title.end():]
        recommend = re.search(r"\*Recommend:\*\s*(.+?)\s*(?=\*Metric:\*|\Z)", rest, re.S)
        metric = re.search(r"\*Metric:\*\s*(.+?)\s*\Z", rest, re.S)
        evidence = rest[: recommend.start()] if recommend else rest
        recs.append({
            "number": title.group(1),
            "title": title.group(2).rstrip("."),
            "evidence": evidence.strip(),
            "recommend": recommend.group(1).strip() if recommend else "",
            "metric": metric.group(1).strip() if metric else "",
        })
    return recs


def show(fig):
    # theme=None keeps the shared chart styling from scripts/analyze.py.
    st.plotly_chart(fig, config=PLOTLY_CONFIG, theme=None)


def alarm_period_chart(df):
    data = analyze.with_alarm_requests(df)
    groups = {"Non-US": (data[data["country"] != "us"], analyze.SERIES),
              "US": (data[data["country"] == "us"], SERIES_2)}
    fig = go.Figure()
    rows = []
    for name, (group, color) in groups.items():
        stats = group.groupby("period").agg(reviews=("review_id", "size"),
                                            requests=("alarm_request", "sum"),
                                            feature_requests=("is_feature_request", "sum"))
        stats = stats.reindex([p for p in analyze.URGENT_PERIODS if p in stats.index])
        if stats.empty:
            continue
        stats["share"] = stats["requests"] / stats["reviews"]
        fig.add_trace(go.Bar(
            name=name, x=list(stats.index), y=list(stats["share"]), marker_color=color,
            customdata=list(zip(stats["requests"], stats["reviews"])),
            hovertemplate=f"<b>{name}</b> · %{{x}}<br>%{{y:.1%}} of reviews "
                          "(%{customdata[0]} of %{customdata[1]:,})<extra></extra>",
        ))
        for period, r in stats.iterrows():
            rows.append({"Countries": name, "Period": period, "Reviews": int(r.reviews),
                         "Alarm/notification requests": int(r.requests),
                         "Share of reviews": r.share,
                         "Share of feature requests": r.requests / r.feature_requests
                         if r.feature_requests else None})
    analyze.style(fig, "Alarm and notification requests by iOS period",
                  "Share of reviews · Urgent shipped in iOS 26.2; iOS 26.4 added the Urgent smart list "
                  "and long-press shortcut", height=420)
    fig.update_layout(showlegend=True, barmode="group", bargap=0.3, bargroupgap=0.08,
                      legend={"orientation": "h", "y": 1.02, "x": 1, "xanchor": "right",
                              "yanchor": "bottom"})
    fig.update_yaxes(tickformat=".0%", title_text="Share of reviews", showgrid=True)
    fig.update_xaxes(showgrid=False)
    return fig, pd.DataFrame(rows)


# --- Data and filters ---------------------------------------------------------

reviews = load_reviews()
memo = load_memo()

with st.sidebar:
    st.header("Filters")
    countries = sorted(reviews["country"].unique())
    picked_countries = st.multiselect(
        "Country", countries, default=countries, format_func=str.upper, key="countries",
    )
    first, last = reviews["date"].min().date(), reviews["date"].max().date()
    picked_dates = st.slider("Review date", min_value=first, max_value=last, value=(first, last),
                             format="MMM YYYY")
    st.caption(
        "Filters apply to every section. Apple's feed returns only the ~500 most recent reviews "
        "per country, so US reviews start in Aug 2026."
    )

in_range = reviews["date"].dt.date.between(*picked_dates)
df = reviews[reviews["country"].isin(picked_countries) & in_range]

# --- Header -------------------------------------------------------------------

st.title("Apple Reminders: App Store Review Insights")
st.caption(
    f"{len(reviews):,} App Store reviews from the US, UK, Canada and Australia "
    f"({reviews['date'].min():%b %Y} – {reviews['date'].max():%b %Y}), classified by Claude into "
    "themes from `themes.md`. Source: `data/classified_reviews.csv`."
)

if df.empty:
    st.warning("No reviews match the current filters.")
    st.stop()

problems = analyze.subsets(df)["problems"]
cols = st.columns(5)
cols[0].metric("Total reviews", f"{len(df):,}")
cols[1].metric("Average rating", f"{df['rating'].mean():.2f} ★")
cols[2].metric("Negative", f"{(df['sentiment'] == 'negative').mean():.0%}")
cols[3].metric("1★ reviews", f"{(df['rating'] == 1).mean():.0%}")
cols[4].metric("Feature requests", f"{int(df['is_feature_request'].sum()):,}")

tabs = st.tabs(["Overview", "Problem themes", "Alarms by iOS period", "Feature requests",
                "Reviews", "Recommendations"])

# --- Overview -----------------------------------------------------------------

with tabs[0]:
    table = analyze.theme_table(df)
    left, right = st.columns(2)
    with left:
        show(analyze.chart_theme_share(table, "All reviews in the current filter"))
    with right:
        show(analyze.chart_avg_rating(table, "All reviews in the current filter"))

# --- Problem themes -----------------------------------------------------------

with tabs[1]:
    st.caption("Negative and neutral reviews only, excluding general_praise: where the product "
               f"problems are. {len(problems):,} reviews in the current filter.")
    if problems.empty:
        st.info("No negative or neutral reviews match the current filters.")
    else:
        label = analyze.BREAKDOWNS["problems"]
        problem_table = analyze.theme_table(problems)
        left, right = st.columns(2)
        with left:
            show(analyze.chart_theme_share(problem_table, label))
        with right:
            show(analyze.chart_one_star(problem_table, label))

# --- Alarms by iOS period -----------------------------------------------------

with tabs[2]:
    fig, period_table = alarm_period_chart(df)
    show(fig)
    st.caption(
        "A review counts as an alarm/notification request if it is a feature request in the "
        "notifications_and_alarms theme or asks for alarm-style alerts or snooze. Compare periods "
        "on non-US reviews: the US only appears from iOS 26.4 on. Outside the US, the drop after "
        "26.4 is not statistically significant (see `outputs/summary.md`)."
    )
    st.dataframe(
        period_table, hide_index=True, width="stretch",
        column_config={
            "Share of reviews": st.column_config.NumberColumn(format="percent"),
            "Share of feature requests": st.column_config.NumberColumn(format="percent"),
        },
    )

# --- Feature requests ---------------------------------------------------------

with tabs[3]:
    scope = st.radio("Reviews", ["All reviews", "Problem reviews only"], horizontal=True,
                     label_visibility="collapsed")
    source = df if scope == "All reviews" else problems
    topics, n_requests = analyze.request_topics(source)
    if n_requests == 0:
        st.info("No feature requests match the current filters.")
    else:
        show(analyze.chart_requests(topics[topics > 0], n_requests, scope))
        st.caption("Specific requests are keyword matches on Claude's one-line summaries of each "
                   "feature-request review; treat counts as approximate.")

# --- Reviews table ------------------------------------------------------------

with tabs[4]:
    themes = sorted(df["theme"].unique())
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    picked_themes = c1.multiselect("Theme", themes, placeholder="All themes")
    picked_sentiment = c2.multiselect("Sentiment", ["positive", "neutral", "negative"],
                                      placeholder="All")
    picked_severity = c3.multiselect("Severity", ["low", "medium", "high"], placeholder="All")
    picked_ratings = c4.multiselect("Rating", [1, 2, 3, 4, 5], placeholder="All")
    c5, c6 = st.columns([3, 1])
    query = c5.text_input("Search title, review text and summary", placeholder="e.g. iCloud, snooze, widget")
    requests_only = c6.toggle("Feature requests only")

    table_df = df
    if picked_themes:
        table_df = table_df[table_df["theme"].isin(picked_themes)]
    if picked_sentiment:
        table_df = table_df[table_df["sentiment"].isin(picked_sentiment)]
    if picked_severity:
        table_df = table_df[table_df["severity"].isin(picked_severity)]
    if picked_ratings:
        table_df = table_df[table_df["rating"].isin(picked_ratings)]
    if requests_only:
        table_df = table_df[table_df["is_feature_request"]]
    if query.strip():
        text = (table_df["title"].fillna("") + " " + table_df["text"].fillna("") + " "
                + table_df["summary"].fillna(""))
        table_df = table_df[text.str.contains(query.strip(), case=False, regex=False)]

    st.caption(f"{len(table_df):,} of {len(df):,} reviews")
    view = table_df.sort_values("date", ascending=False)[
        ["date", "country", "rating", "theme", "sentiment", "severity", "is_feature_request",
         "title", "text", "summary", "version"]
    ].assign(date=lambda d: d["date"].dt.tz_localize(None), country=lambda d: d["country"].str.upper())
    st.dataframe(
        view, hide_index=True, width="stretch", height=520,
        column_config={
            "date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
            "country": "Country",
            "rating": st.column_config.NumberColumn("Rating", format="%d ★"),
            "theme": "Theme",
            "sentiment": "Sentiment",
            "severity": "Severity",
            "is_feature_request": st.column_config.CheckboxColumn("Request"),
            "title": st.column_config.TextColumn("Title", width="medium"),
            "text": st.column_config.TextColumn("Review", width="large"),
            "summary": st.column_config.TextColumn("Claude summary", width="large"),
            "version": "App version",
        },
    )
    st.download_button("Download these reviews (CSV)", table_df.to_csv(index=False).encode("utf-8"),
                        file_name="reminders_reviews_filtered.csv", mime="text/csv")

# --- Recommendations ----------------------------------------------------------

with tabs[5]:
    if not memo:
        st.info("memo.md not found.")
    else:
        st.caption("Summarized from `memo.md`. Numbers there cover all 1,950 reviews and do not "
                   "change with the filters.")
        insight_heading, insight_body = memo_section(memo, "Key insight")
        if insight_heading:
            st.subheader(insight_heading.replace("Key insight: ", "").capitalize())
            st.markdown(insight_body)

        _, recs_body = memo_section(memo, "Top 3 recommendations")
        recs = parse_recommendations(recs_body)
        if recs:
            cols = st.columns(len(recs))
            for col, rec in zip(cols, recs):
                with col.container(border=True):
                    st.markdown(f"#### {rec['number']}. {rec['title']}")
                    st.markdown(f"**Recommend:** {rec['recommend']}")
                    st.markdown(f"**Success metric:** {rec['metric']}")
                    with st.expander("Evidence"):
                        st.markdown(rec["evidence"])
        else:
            st.markdown(recs_body)

        later_heading, later_body = memo_section(memo, "Later")
        if later_heading:
            st.markdown(f"**{later_heading}.** {later_body}")
        _, limitations = memo_section(memo, "Limitations")
        if limitations:
            with st.expander("Limitations"):
                st.markdown(limitations)
