# Memo: What App Store reviews say to fix first in Reminders

**To:** Apple Reminders product team · **From:** Suhana Jain · **Date:** October 12, 2026

## Context
We analyzed **1,950 App Store reviews** (US, UK, Canada, Australia; Jan 2024–Oct 2026) from Apple's public review feed. Claude Haiku 5.5 labeled each review's theme, sentiment, severity, and whether it requests a feature. A second model (Claude Sonnet 5.5) re-labeled 100 random reviews and agreed on the theme 90% of the time (κ = 0.85).

## Key insight: prioritize by harm, not volume
Organization and sorting is the most common specific theme (158 reviews), but it's mild: 3.8★ average and 11% 1★. **Data loss and bugs, missed alerts, and intrusive pop-ups make up 14% of reviews but half of all 1★ ratings (102 of 204).** Star ratings come from users, so this doesn't rely on our labels.

## Top 3 recommendations
**1. Stop losing people's reminders.** Bugs: 112 reviews · 2.1★ · 47% are 1★. On reading every candidate, **18 describe actual data loss**. Seven tie it to an iOS update, two to turning on iCloud, the rest to no clear cause. *Recommend:* treat update migration and the iCloud enable/Merge flow as zero-loss paths, and make deleted reminders recoverable. *Metric:* no new data-loss reviews for two releases; internally, item-loss incidents.

**2. Close the remaining gaps in Urgent.** Urgent alarms shipped in iOS 26.2 (Dec 2025); iOS 26.4 (Mar 2026) added an Urgent smart list and a long-press "Mark as Urgent" shortcut. Alarm and notification requests haven't dropped significantly: 4.2% of non-US reviews before 26.2, 4.3% in 26.2–26.3, and 2.7% since 26.4 (p = 0.36; small samples). Of the 31 such requests since 26.4:
- **9 ask for an alarm-like alert**, which Urgent already provides (one says it's hard to reach).
- **7 want snooze** or a quick "move to today/tomorrow".
- **3 want to set Urgent from Siri or Apple Watch.**

*Recommend:* suggest Urgent when someone creates a time-critical reminder (medication, bills), add Siri and Watch support, and offer quick snooze lengths (10, 15, 30 min). *Metric:* these requests fall from 3.2% of reviews since 26.4 to under 1.5%; internally, Urgent use on time-critical reminders.

**3. Respect "no" in pop-ups.** 31 reviews · 1.8★ · 68% are 1★, the lowest-rated theme. Reviewers describe:
- **Interrupted mid-task (14):** asked to rate or review the app while in the middle of something.
- **Repeat prompts after declining (9):** prompts to turn on alarms (5), share precise location (3), or re-enable a setting they had switched off (1).
- **Stuck prompts (6, across themes):** an alarm setup prompt that couldn't be dismissed and blocked the app, all after iOS 26.2 (Dec 2025–Jul 2026).

The Urgent rollout caused part of this, so promoting Urgent (#2) must not rely on repeat prompts. *Recommend:* remember "Never" permanently, make every prompt dismissible, and never interrupt while someone is editing. *Metric:* zero re-prompts after "Never" (internal); these reviews fall toward zero.

## Later: organization requests
Common asks: manual order that stays put, top-or-bottom placement for new items, color-coding, turning off grocery auto-categories, and Calendar visibility. Frequent but low harm.

## RICE (illustrative)
| Initiative | Reach (reviews) | Impact (est.) | Confidence (est.) | Effort (est., person-months) | Score |
|---|---:|---:|---:|---:|---:|
| Close Urgent gaps | 122 | 2 | 60% | 2 | 73 |
| Stop data loss | 112 | 3 | 80% | 4 | 67 |
| Pop-ups respect "no" | 31 | 1 | 90% | 0.5 | 56 |
| Organization requests | 158 | 0.5 | 60% | 4 | 12 |

*Reach comes from the data; Impact, Confidence and Effort are my estimates. RICE favors Urgent because it only needs extending; data loss still leads because it's irreversible.*

## Limitations
- **500-review cap:** Apple's feed returns only the ~500 most recent reviews per country, so the US covers only Aug–Oct 2026.
- **Unhappy users review more:** these reviews average 4.2★, against 4.8★ across ~1M App Store ratings.
- **Reviews only:** we have no usage data, so Reach counts reviews, not affected users.
- **Validation method:** only a second AI model checked the labels. That shows consistency, not correctness. It agreed on 90% of 100 random reviews, mostly praise. A targeted check of 10 reviews per priority theme agreed on 28 of 30 (bugs 10/10, alerts 9/10, pop-ups 9/10). Hand-labeling is still pending. iOS periods are inferred from review dates and app versions.
