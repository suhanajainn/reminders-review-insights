# Memo: What App Store reviews say to fix first in Reminders

**To:** Apple Reminders product team · **From:** Suhana Jain · **Date:** October 12, 2026

## Context
We analyzed **1,950 App Store reviews** (US, UK, Canada, Australia; Jan 2024–Oct 2026) from Apple's public review feed. Claude Haiku 5.5 labeled each review's theme, sentiment, severity, and whether it requests a feature. A second model (Claude Sonnet 5.5) re-labeled 100 random reviews and agreed on the theme 90% of the time (κ = 0.85). See Limitations for what that does and doesn't show.

## Key insight: prioritize by harm, not volume
Organization and sorting is the most common specific theme (158 reviews), but it's mild: 3.8★ average and 11% 1★. **Data loss and bugs, missed alerts, and intrusive pop-ups make up 14% of reviews but half of all 1★ ratings (102 of 204).** Star ratings come from users, not our model, so this doesn't depend on how we labeled severity.

## Top 3 recommendations
**1. Stop losing people's reminders.** Bugs: 112 reviews · 2.1★ · 47% are 1★. We read every candidate review: **18 describe actual data loss**. Seven tie it to an iOS update, two to turning on or merging iCloud, and the rest to no clear cause. *Recommend:* treat update migration and the iCloud enable/Merge flow as zero-loss paths, and make deleted reminders recoverable. *Metric:* no new data-loss reviews for two releases; internally, item-loss incidents in migration and merge.

**2. Make the existing Urgent alarm findable.** Urgent alarms shipped around version 2.0 (early 2026), but alarm-style requests barely moved (15% of feature requests before, 12% after). Notification complaints held at about 6% of reviews. Several recent requests ask for exactly what Urgent already does, which points to a discoverability problem, not a missing feature. Others want vibration-only alarms, a level between a normal alert and Urgent, or setting Urgent from Siri or Apple Watch. *Recommend:* offer Urgent when someone creates a time-critical reminder (medication, bills), and add Siri and Watch support. *Metric:* alarm requests fall below 5% of feature requests; internally, Urgent adoption on time-critical reminders.

**3. Respect "no" in pop-ups.** 31 reviews · 1.8★ · 68% are 1★, the lowest-rated theme. Reviewers describe:
- **Interrupted mid-task (14):** asked to rate or review the app while in the middle of something.
- **Repeat prompts after declining (9):** prompts to turn on alarms (5), share precise location (3), or re-enable a setting they had switched off (1).
- **Stuck prompts (6, across themes):** an alarm setup prompt that couldn't be dismissed and blocked the app, all in version 2.0.

The Urgent rollout caused part of this, so promoting Urgent (#2) must not rely on repeat prompts. *Recommend:* remember "Never" permanently, make every prompt dismissible, and never interrupt while someone is editing. *Metric:* zero re-prompts after "Never" (internal); these reviews fall toward zero.

## Later: organization requests
Common asks: manual order that stays put, choosing whether new items go at the top or bottom, color-coding, turning off automatic grocery categories, and choosing which reminders show in Calendar. They're frequent but low harm.

## RICE (illustrative)
| Initiative | Reach (reviews) | Impact (est.) | Confidence (est.) | Effort (est., person-months) | Score |
|---|---:|---:|---:|---:|---:|
| Make Urgent findable | 122 | 2 | 60% | 2 | 73 |
| Stop data loss | 112 | 3 | 80% | 4 | 67 |
| Pop-ups respect "no" | 31 | 1 | 90% | 0.5 | 56 |
| Organization requests | 158 | 0.5 | 60% | 4 | 12 |

*Reach comes from the data. Impact, Confidence and Effort are my estimates. RICE puts Urgent first because it's cheap now that the feature exists. I still lead with data loss because it's irreversible, and review counts understate it.*

## Limitations
- **500-review cap:** Apple's feed returns only the ~500 most recent reviews per country, so the US covers only Aug–Oct 2026.
- **Unhappy users review more:** these reviews average 4.2★, against 4.8★ across ~1M App Store ratings.
- **Reviews only:** we have no usage data, so Reach counts reviews, not affected users. Review-based metrics are noisy at these volumes.
- **Validation method:** a second AI model checked the labels, not people. The 90% agreement is driven by praise: only 3–5 of the 100 checked reviews fell in each priority theme, and hand-labeling is still pending. Version-to-iOS mapping is inferred from review dates.
