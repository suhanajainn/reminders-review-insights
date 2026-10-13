# Theme validation: second rater

A random sample of 100 reviews from `data/classified_reviews.csv` (seed 42) was re-labeled by `claude-sonnet-5-5` using the same `themes.md` codebook and prompt as the original `claude-haiku-5-5` run. The second rater did not see the first label.

## Agreement

- **Agreement rate:** 90/100 (90%)
- **Cohen's kappa:** 0.85 (agreement corrected for chance)

## By theme

| Theme | claude-haiku-5-5 | claude-sonnet-5-5 | Both agree |
|---|---|---|---|
| general_praise | 57 | 55 | 53 |
| organization_and_sorting | 7 | 5 | 5 |
| bugs_and_reliability | 5 | 4 | 4 |
| missing_features | 5 | 5 | 4 |
| notifications_and_alarms | 4 | 5 | 4 |
| app_integrations | 2 | 5 | 2 |
| ease_of_use_and_design | 6 | 5 | 5 |
| sharing_and_sync | 4 | 5 | 4 |
| intrusive_prompts | 3 | 3 | 3 |
| other | 7 | 8 | 6 |

## Most common disagreements

### claude-haiku-5-5: `general_praise` → claude-sonnet-5-5: `other` (2)

> **5★ · Omnia dicta fortiora si dicta Latina**: Hoc est programma/productum/ministerium egregium, sed odi cogitare et recensio bona ac diligens semper scribenda est… itaque, callidus, hanc sententiam communem Latino sermone potius scribo. (`14229495816`)

> **5★ · Work**: Could be better but it works (`12580454151`)

### claude-haiku-5-5: `general_praise` → claude-sonnet-5-5: `app_integrations` (2)

> **4★ · Very handy when no paper**: I often think of something that I need to remember to do and being old school still look for something to write on! Now just have to ask my new best friend Siri to put it on the list of to dos (`12004030225`)

> **5★ · Can’t live without it!**: Love the integration and simplicity. I don’t need anything else. This just works. (`14643810764`)

### claude-haiku-5-5: `missing_features` → claude-sonnet-5-5: `app_integrations` (1)

> **4★ · Keeps getting better**: The app is usable since the last update and shines with the calendar integration. Just small things like inability to attach pdf but only photos and bugs in how repeat calendars behave plus the difference in how mac and… (`13361951577`)

### claude-haiku-5-5: `organization_and_sorting` → claude-sonnet-5-5: `general_praise` (1)

> **5★ · The BEST tool to manage your ToDo’s!**: I have categorized all my todo’s into 4 lists: Myself, Money, Maintenance, Miscellaneous. Works very well! (`14464836433`)

### claude-haiku-5-5: `other` → claude-sonnet-5-5: `general_praise` (1)

> **5★ · Good**: Good (`12405162461`)

3 other disagreement pair(s) not shown; see `outputs/second_rater_labels.csv`.

<!-- priority-check:start -->
## Priority themes: second-model consistency check

**This is a consistency check between two AI models, not human validation.** 10 random reviews (seed 42) from each of the memo's three priority themes were re-labeled by `claude-sonnet-5-5` with the same `themes.md` codebook and prompt as the original `claude-haiku-5-5` labels, without seeing them. Agreement means the two models read the review the same way; it does not show the label is correct.

**Overall:** 28/30 (93%) agree.

| claude-haiku-5-5 theme | Agree | claude-sonnet-5-5 chose instead |
|---|---:|---|
| bugs_and_reliability | 10/10 | - |
| notifications_and_alarms | 9/10 | `missing_features` (1) |
| intrusive_prompts | 9/10 | `bugs_and_reliability` (1) |

### Disagreements

> **`notifications_and_alarms` → `missing_features`** · 3★ · **Days**: Would be great if i can choose what days the reminder pops up currently it only works on weekends or weekdays i would like to filter days out (`13294604235`)

> **`intrusive_prompts` → `bugs_and_reliability`** · 5★ · **Alarm**: I cannot open the app due to a banner about alarms blocking the opening of the App (`13560876267`)

<!-- priority-check:end -->
