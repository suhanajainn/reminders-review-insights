# Review analysis summary

Source: `data/classified_reviews.csv` (1,950 reviews, Jan 2024 to Oct 2026). Themes, sentiment and feature-request flags come from `scripts/classify.py`.

**Caveats.** Apple's feed returns only the ~500 most recent reviews per country, so the US sample covers just Aug to Oct 2026 while AU goes back to Jan 2024; monthly counts reflect that coverage, not real changes in volume. Feature-request topics are keyword matches on Claude's one-line summaries, so treat them as approximate.

## All reviews

1,950 reviews · average rating 4.16★ · 10% are 1★ · 333 feature requests. Charts: `outputs/charts/all/`.

| Theme | Reviews | Share | Avg ★ | 1★ share | Feature requests |
|---|---:|---:|---:|---:|---:|
| general_praise | 1,004 | 51.5% | 4.92 | 0% | 6 |
| organization_and_sorting | 158 | 8.1% | 3.77 | 11% | 76 |
| other | 124 | 6.4% | 3.89 | 16% | 1 |
| notifications_and_alarms | 122 | 6.3% | 2.98 | 23% | 59 |
| app_integrations | 121 | 6.2% | 4.06 | 11% | 52 |
| bugs_and_reliability | 112 | 5.7% | 2.11 | 47% | 3 |
| missing_features | 105 | 5.4% | 3.73 | 9% | 103 |
| ease_of_use_and_design | 94 | 4.8% | 3.21 | 23% | 25 |
| sharing_and_sync | 79 | 4.1% | 3.30 | 23% | 7 |
| intrusive_prompts | 31 | 1.6% | 1.77 | 68% | 1 |

**Most common specific feature requests**

| Request | Reviews | Share of requests |
|---|---:|---:|
| Alarm-style alerts (louder, keep ringing, bypass silent) | 44 | 13% |
| Show reminders in Calendar, or choose which appear | 39 | 12% |
| Color-code reminders, more color choices | 26 | 8% |
| Widget and lock-screen options | 20 | 6% |
| Snooze or quick postpone | 17 | 5% |
| Choose where new items go, manual order that sticks | 17 | 5% |
| Better search | 14 | 4% |
| Subtask improvements | 14 | 4% |
| Turn emails into reminders, link Mail | 12 | 4% |
| Attach photos, PDFs or files | 12 | 4% |
| Sort alphabetically or by date | 11 | 3% |
| More repeat options (hourly, specific days, custom intervals) | 10 | 3% |
| Keep completed items visible, reset lists | 10 | 3% |
| Outlook, Google, Windows or web access | 9 | 3% |
| Templates and reusable lists | 5 | 2% |
| Repeat from completion date | 5 | 2% |
| Habit tracking | 4 | 1% |

## Negative and neutral reviews, excluding general_praise

569 reviews · average rating 2.47★ · 36% are 1★ · 181 feature requests. Charts: `outputs/charts/problems/`.

| Theme | Reviews | Share | Avg ★ | 1★ share | Feature requests |
|---|---:|---:|---:|---:|---:|
| bugs_and_reliability | 105 | 18.5% | 1.95 | 50% | 2 |
| notifications_and_alarms | 89 | 15.6% | 2.38 | 31% | 41 |
| other | 77 | 13.5% | 3.35 | 26% | 0 |
| organization_and_sorting | 73 | 12.8% | 2.73 | 25% | 40 |
| ease_of_use_and_design | 57 | 10.0% | 2.26 | 39% | 15 |
| missing_features | 52 | 9.1% | 2.94 | 17% | 50 |
| app_integrations | 43 | 7.6% | 2.60 | 30% | 28 |
| sharing_and_sync | 43 | 7.6% | 2.02 | 42% | 4 |
| intrusive_prompts | 30 | 5.3% | 1.67 | 70% | 1 |

**Most common specific feature requests**

| Request | Reviews | Share of requests |
|---|---:|---:|
| Alarm-style alerts (louder, keep ringing, bypass silent) | 29 | 16% |
| Show reminders in Calendar, or choose which appear | 19 | 10% |
| Widget and lock-screen options | 10 | 6% |
| Snooze or quick postpone | 10 | 6% |
| Sort alphabetically or by date | 10 | 6% |
| More repeat options (hourly, specific days, custom intervals) | 9 | 5% |
| Choose where new items go, manual order that sticks | 8 | 4% |
| Better search | 8 | 4% |
| Turn emails into reminders, link Mail | 8 | 4% |
| Keep completed items visible, reset lists | 8 | 4% |
| Outlook, Google, Windows or web access | 7 | 4% |
| Color-code reminders, more color choices | 7 | 4% |
| Subtask improvements | 7 | 4% |
| Attach photos, PDFs or files | 5 | 3% |
| Templates and reusable lists | 3 | 2% |
| Habit tracking | 3 | 2% |
| Repeat from completion date | 2 | 1% |

## Theme shifts by app version

Share of each theme's reviews per app version, excluding US reviews (the US only appears from version 2.0, when Apple's feed starts covering it). The iOS release for each version is inferred from when its first reviews appear.

| Theme | 1.7 (iOS 17) | 1.8 (iOS 18) | 1.9.1 (iOS 26) | 2.0 (iOS 26.2) | 2.6 (iOS 27) |
|---|---:|---:|---:|---:|---:|
| general_praise | 53.4% | 48.3% | 49.5% | 47.8% | 58.4% |
| organization_and_sorting | 9.6% | 7.9% | 5.4% | 8.6% | 9.1% |
| bugs_and_reliability | 4.1% | 6.0% | 8.6% | 7.3% | 1.3% |
| notifications_and_alarms | 3.4% | 7.2% | 4.8% | 6.6% | 9.1% |
| app_integrations | 8.2% | 7.2% | 4.8% | 6.2% | 0.0% |
| other | 5.5% | 6.8% | 4.8% | 5.9% | 9.1% |
| missing_features | 6.8% | 5.3% | 8.6% | 5.3% | 5.2% |
| ease_of_use_and_design | 4.8% | 5.3% | 6.5% | 5.3% | 1.3% |
| sharing_and_sync | 3.4% | 4.7% | 5.4% | 5.0% | 5.2% |
| intrusive_prompts | 0.7% | 1.3% | 1.6% | 2.0% | 1.3% |
| *reviews* | *146* | *530* | *186* | *561* | *77* |

Changes from one version to the next that pass a two-proportion z-test at p < 0.05 (uncorrected for the number of comparisons):

- **bugs_and_reliability**, 2.0 → 2.6: 7.3% → 1.3% (p = 0.046)
- **app_integrations**, 2.0 → 2.6: 6.2% → 0.0% (p = 0.024)

Treat these with caution: with 40 comparisons, a few will pass by chance, and small versions swing easily: 2.6 (77 reviews).

**Reviews naming a specific iOS release (20):** bugs_and_reliability 35%, general_praise 20%, app_integrations 15%, organization_and_sorting 10%, ease_of_use_and_design 10%, other 5%, intrusive_prompts 5%.

**Reviews blaming a recent update (19):** bugs_and_reliability 53%, organization_and_sorting 11%, sharing_and_sync 11%, general_praise 11%, ease_of_use_and_design 5%, missing_features 5%, app_integrations 5%. For comparison, bugs_and_reliability is 18% of all negative and neutral reviews.

## Alarm and notification requests around Apple's Urgent changes

Urgent alarms shipped in iOS 26.2 (Dec 2025); iOS 26.4 (Mar 24, 2026) added an Urgent smart list and a long-press "Mark as Urgent" shortcut. A review counts as an alarm or notification request if it is a feature request in the notifications_and_alarms theme or its summary asks for alarm-style alerts or snooze. Periods use the app version (2.0 shipped with iOS 26.2) and, within it, the review date. The US only appears from iOS 26.4 on, so compare periods on non-US reviews.

| Countries | Period | Reviews | Alarm/notification requests | Share of reviews | Share of feature requests |
|---|---|---:|---:|---:|---:|
| All | Before iOS 26.2 | 862 | 36 | 4.2% | 21% |
| All | iOS 26.2–26.3 | 117 | 5 | 4.3% | 21% |
| All | iOS 26.4 and later | 971 | 31 | 3.2% | 23% |
| Non-US | Before iOS 26.2 | 862 | 36 | 4.2% | 21% |
| Non-US | iOS 26.2–26.3 | 117 | 5 | 4.3% | 21% |
| Non-US | iOS 26.4 and later | 521 | 14 | 2.7% | 19% |
| US | iOS 26.4 and later | 450 | 17 | 3.8% | 27% |

Change in share of reviews for iOS 26.4 and later (non-US), two-proportion z-test:

- vs Before iOS 26.2: 4.2% → 2.7% (p = 0.15)
- vs iOS 26.2–26.3: 4.3% → 2.7% (p = 0.36)

## Reviews mentioning competitors

30 reviews (1.5%) name a competing app or platform · average rating 3.87★ · 60% are feature requests. Matches are keyword-based, so treat counts as approximate.

| Competitor | Reviews |
|---|---:|
| Microsoft To Do / Outlook | 10 |
| Google Tasks / Keep / Calendar | 8 |
| Todoist | 6 |
| Samsung / Android | 4 |
| Notion / Asana / Trello | 3 |
| Things | 2 |
| TickTick | 1 |
| OmniFocus | 1 |
| Fantastical | 1 |

| Theme | Competitor reviews | Share | Share of all reviews |
|---|---:|---:|---:|
| app_integrations | 10 | 33% | 6% |
| missing_features | 8 | 27% | 5% |
| general_praise | 7 | 23% | 51% |
| ease_of_use_and_design | 2 | 7% | 5% |
| bugs_and_reliability | 1 | 3% | 6% |
| organization_and_sorting | 1 | 3% | 8% |
| notifications_and_alarms | 1 | 3% | 6% |
