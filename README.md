# Apple Reminders: App Store Review Insights

> 📸 **Screenshot placeholder:** add a dashboard screenshot here (e.g. `docs/dashboard.png`).

**What 1,950 App Store reviews say Apple should fix first in Reminders: an end-to-end product analysis using AI classification, a second-model check, and a severity-first prioritization.**

**🔗 Live dashboard: [suhana-reminders-insights.streamlit.app](https://suhana-reminders-insights.streamlit.app/)** · 📄 [Recommendation memo](memo.md)

---

## The question

Reminders has a 4.8★ App Store rating from about 1 million ratings, so most people are happy. **What are the unhappy users telling Apple, and which of their problems matter most?**

## Approach

| Step | What I did | Output |
|---|---|---|
| **1. Data collection** | Pulled reviews from Apple's public App Store review feed for the US, UK, Canada and Australia (10 pages each), skipped entries that weren't reviews, and removed duplicates. | [`data/raw_reviews.csv`](data/raw_reviews.csv): 1,950 reviews, Jan 2024 – Oct 2026 |
| **2. Theme taxonomy** | Hand-read 400 reviews, drawn from every star rating with extra low ratings, and wrote a codebook of 9 non-overlapping themes plus "other". Each has a one-line definition, a real quote, and rules for reviews that touch several topics. | [`themes.md`](themes.md) |
| **3. AI classification** | Claude Haiku 5.5 labeled every review with a theme, sentiment, severity, whether it requests a feature, and a one-line summary. Structured output limits the theme to the codebook's names. | [`data/classified_reviews.csv`](data/classified_reviews.csv) |
| **4. Second-model validation** | Claude Sonnet 5.5 re-labeled reviews without seeing the original labels: 100 random reviews, plus 10 from each priority theme. | [`outputs/validation_results.md`](outputs/validation_results.md) |
| **5. Analysis** | Theme share, ratings and 1★ share by theme; problem-only breakdowns; specific feature requests; changes by iOS release; competitor mentions. | [`outputs/summary.md`](outputs/summary.md), [dashboard](https://suhana-reminders-insights.streamlit.app/) |
| **6. Recommendations** | A one-page memo for the product team, revised after critiquing it as a skeptical product director. | [`memo.md`](memo.md) |

## Key findings

- **Prioritize by severity, not volume.** Organization and sorting is the most common specific theme (158 reviews), but it's mild: 3.8★ average. **Bugs, missed alerts and intrusive pop-ups make up 14% of reviews but 50% of all 1★ reviews (102 of 204).**
- **Data loss is the worst problem.** Bug reviews average 2.1★, and 47% are 1★. I read every candidate review and **18 describe reminders actually being lost**: 7 after an iOS update, 2 after turning on iCloud.
- **Pop-ups are the lowest-rated theme** (1.8★, 68% 1★). 14 reviewers were asked to rate or review the app in the middle of a task. 9 were prompted again to turn on alarms, location or a setting after they had declined. 6 describe an alarm prompt stuck on screen, blocking the app.
- **Users ask for alarms more than anything else.** Alarm-style alerts are the top specific feature request (44 of 333).

### How the analysis changed my recommendation

My first draft recommended that Apple **"add an opt-in alarm-style alert."** When I critiqued that draft, the reviews turned out to praise a feature called **Urgent**: Apple had already shipped Urgent alarms in **iOS 26.2** and added an Urgent smart list and shortcut in **iOS 26.4**. So I tested whether demand fell after each release:

| Period (non-US reviews) | Alarm/notification requests as share of reviews |
|---|---|
| Before iOS 26.2 | 4.2% |
| iOS 26.2 – 26.3 | 4.3% |
| iOS 26.4 and later | 2.7% (not significant, p = 0.36) |

Demand didn't drop significantly, and 9 of the 31 requests since 26.4 still ask for what Urgent already does. **I changed the recommendation from "build alarms" to "close the remaining gaps in Urgent".** The same review also corrected a keyword-based "1 in 5 bug reviews describe data loss" to the 18 reviews I verified by reading them, and connected the stuck pop-ups to how Urgent was rolled out.

## Top 3 recommendations

| # | Recommendation | Evidence | Success metric |
|---|---|---|---|
| 1 | **Stop losing people's reminders.** Make iOS update migration and the iCloud Merge flow zero-loss, and make deletions recoverable. | 112 reviews · 2.1★ · 18 verified data-loss reviews | No new data-loss reviews for two releases |
| 2 | **Close the remaining gaps in Urgent.** Suggest Urgent when someone creates a time-critical reminder, add Siri and Watch support, and offer quick snooze. | Requests flat after iOS 26.2 and 26.4 | Requests fall from 3.2% of reviews to under 1.5% |
| 3 | **Respect "no" in pop-ups.** Remember "Never" permanently, make every prompt dismissible, and never interrupt while someone is editing. | 31 reviews · 1.8★ · 68% 1★ | Zero re-prompts after "Never" |

**Later:** organization requests (manual ordering, color-coding, grocery auto-categories). They're frequent but low harm.

## Validation

- **100 random reviews:** 90% agreement between Haiku and Sonnet (Cohen's κ = 0.85).
- **10 reviews per priority theme:** 28 of 30 agree (bugs 10/10, alerts 9/10, pop-ups 9/10).
- **What this shows:** these are **consistency checks between two models, not human validation**. A hand-labeling sample is ready in [`data/validation_sample.csv`](data/validation_sample.csv).

## Limitations

- **500-review cap:** Apple's feed returns only the ~500 most recent reviews per country, so the US covers only Aug–Oct 2026.
- **Unhappy users review more:** written reviews average 4.2★, against 4.8★ across ~1M ratings.
- **Reviews only:** there's no usage data, so counts reflect reviews, not the number of affected users.
- **Model-labeled:** theme, sentiment and severity come from an AI model checked by a second model, not by people. Feature-request topics and data-loss candidates use keyword matching.

## Tech stack

- **Python** with `requests` (data collection) and `pandas` (analysis)
- **Anthropic API:** Claude Haiku 5.5 for classification and Claude Sonnet 5.5 as the second rater. Uses structured JSON output, 5 concurrent requests with automatic retry on rate limits, and saves progress so a rerun resumes.
- **Plotly** for charts, **Streamlit** for the dashboard (deployed on Streamlit Community Cloud)

## Run it locally

**Dashboard** (no API key needed):

```bash
git clone https://github.com/suhanajainn/reminders-review-insights.git
cd reminders-review-insights
pip install -r requirements.txt
streamlit run app.py
```

**Full pipeline** (needs an Anthropic API key in `.env` as `ANTHROPIC_API_KEY=...`):

```bash
pip install -r requirements.txt anthropic python-dotenv requests
python scripts/fetch_reviews.py      # 1. pull reviews        -> data/raw_reviews.csv
python scripts/classify.py           # 2. classify (resumable) -> data/classified_reviews.csv
python scripts/second_rater.py       # 3. 100-review second-model check
python scripts/priority_check.py     # 4. priority-theme check
python scripts/analyze.py            # 5. charts + outputs/summary.md
```

## Repo structure

```
app.py                  Streamlit dashboard
memo.md                 One-page recommendation memo
themes.md               Theme codebook
scripts/                Data collection, classification, validation, analysis
data/                   Raw, classified and validation-sample reviews
outputs/                Summary tables, validation results, interactive charts
```
