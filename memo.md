# Memo: What App Store reviews say to fix first in Reminders

**To:** Apple Reminders product team · **From:** Suhana Jain · **Date:** October 12, 2026

## Context
We analyzed **1,950 App Store reviews** (US, UK, Canada, Australia; Jan 2024–Oct 2026) from Apple's public review feed. Claude Haiku 5.5 labeled each review's theme, sentiment, severity, and whether it requests a feature. A second model (Claude Sonnet 5.5) independently re-labeled 100 random reviews and **agreed on the theme 90% of the time (κ = 0.85)**.

## Key insight: prioritize by severity, not volume
Organization and sorting is the most common specific theme (158 reviews), but it's mild: 3.8★ average and only 3 high-severity reviews. **Bugs, missed alerts and intrusive pop-ups make up 14% of reviews but half of all 1★ reviews (102 of 204) and 86% of high-severity ones (57 of 66).** Counting reviews alone would put the wrong problem first.

## Top 3 recommendations
**1. Stop data loss and update regressions.** 112 reviews · 2.1★ · 47% are 1★ · 34 high severity, the most of any theme. About 1 in 5 describe reminders vanishing. Reviewers name regressions in iOS 26.0.1, 26.2, 26.4 and 26.6. *Recommend:* make reminder integrity a release gate across iOS updates and iCloud merges, and make every deletion recoverable. *Metric:* bugs fall from 26% to under 15% of 1★ reviews within two releases.

**2. Add an opt-in alarm-style alert.** 122 reviews · 3.0★ · 21 high severity (missed medication, bills, appointments). It's the top specific feature request (44 of 333). *Recommend:* a per-reminder option that rings until dismissed, with quick snooze. *Metric:* alarm requests halve, and notification complaints fall from 23% 1★ to under 15%.

**3. Respect "no" in pop-ups.** 31 reviews · 1.8★ · 68% are 1★, the lowest-rated theme. Reviewers describe two problems:
- **Interrupted mid-task:** 14 were asked to rate or review the app while in the middle of something.
- **Repeat prompts after declining:** 9 were repeatedly prompted to turn on alarms, share their precise location or re-enable a setting they had declined. Some banners couldn't be dismissed and blocked the app, mostly reported after iOS 26.2.

*Recommend:* remember "Never" permanently, make every banner dismissible, and never interrupt while someone is editing. *Metric:* these reviews fall from 1.6% to near zero.

## Later: organization requests
Common asks: manual order that stays put, choosing whether new items go at the top or bottom, color-coding, turning off automatic grocery categories, and choosing which reminders show in Calendar. They're frequent but low severity, so they come after the three fixes above.

## RICE
| Initiative | Reach (reviews) | Impact (est.) | Confidence (est.) | Effort (est., person-months) | Score |
|---|---:|---:|---:|---:|---:|
| Data loss and regressions | 112 | 3 | 80% | 4 | 67 |
| Alarm-style alerts | 122 | 2 | 70% | 3 | 57 |
| Pop-ups respect "no" | 31 | 1 | 90% | 0.5 | 56 |
| Organization requests | 158 | 0.5 | 60% | 4 | 12 |

*Reach comes from the data. Impact, Confidence and Effort are my estimates.*

## Limitations
- **500-review cap:** Apple's feed returns only the ~500 most recent reviews per country, so the US covers only Aug–Oct 2026.
- **Unhappy users review more:** these reviews average 4.2★, against 4.8★ across ~1M App Store ratings.
- **Reviews only:** we have no usage data, so Reach counts reviews, not affected users.
- **Validation method:** a second AI model checked the labels, not people. That shows consistency, not correctness. Data-loss and request counts are keyword-based estimates.
