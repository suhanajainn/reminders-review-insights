# Review themes: Apple Reminders

Themes found by reading a sample of 400 reviews from `data/raw_reviews.csv`.

**Sample:** 100 reviews per country (us, gb, ca, au), drawn at random within each star rating: 20 × 1★, 12 × 2★, 15 × 3★, 18 × 4★, 35 × 5★. Low ratings are deliberately oversampled, since they contain most of the complaints and requests. Counts below therefore overstate complaints relative to the full dataset, where 5★ reviews make up 65% of the total.

**Labeling rules:**

- Give each review exactly **one** theme, its primary topic.
- If a review covers several topics, label it with the one the reviewer spends the most words on. If that is a tie, use the one mentioned first.
- A positive review that includes one specific complaint or request gets that complaint's or request's theme, not `general_praise`.
- Missed or late notifications count as `notifications_and_alarms`, even when a bug causes them. Sync failures count as `sharing_and_sync`, not `bugs_and_reliability`.

---

### general_praise
**Definition:** A positive review that names no specific defect, feature request, or particular feature beyond the app's basic job of helping the reviewer remember, organize, or plan (bills, medication, school, groceries).

> "Whenever I have a commitment I instantly enter it into this app. It has kept me on track and on time. I am grateful for this app."

**Count:** ~136 / 400 (34%)

### organization_and_sorting
**Definition:** How reminders are ordered, grouped, categorized, found, or cleared within lists. This covers manual reordering, where new items are inserted, sections, sorting by date or priority, color coding, automatic grocery categories, search, and clearing completed items.

> "I can’t rearrange tasks, they just jump back to the same place even though it’s set to sort manually."

**Count:** ~40 / 400 (10%)

### bugs_and_reliability
**Definition:** The app crashes, freezes, is slow or laggy, loses or duplicates data, records completions incorrectly, or stopped working after an update. Notification and sync failures are excluded; they belong to `notifications_and_alarms` and `sharing_and_sync`.

> "It constantly freezes and it can take up to 2 minutes to be able to add or amend reminders which is frustrating and time consuming."

**Count:** ~39 / 400 (10%)

### missing_features
**Definition:** A request for a task-management capability the app lacks or limits. Examples: richer recurrence rules, subtask behavior, templates, habit tracking, separate due and reminder dates, rich text or attachments, and widget or display options. Alarms, sorting, sharing, and integrations are excluded because they have their own themes.

> "Like this app, but it would get 5 stars if you could repeat from completion date as well as due date."

**Count:** ~33 / 400 (8%)

### notifications_and_alarms
**Definition:** Whether and how reminders alert the user. This covers alerts that don't fire, fire late, or are easy to miss, plus requests for loud or persistent alarms, snooze, and location- or CarPlay-triggered alerts.

> "It’s very basic and far too easy to miss the reminders as the brief tone notification becomes background noise! We need to be able to assign an alarm of some duration, to prioritise certain reminders so they cannot be missed!"

**Count:** ~32 / 400 (8%)

### app_integrations
**Definition:** How Reminders works with other apps, assistants, and platforms (Calendar, Mail, Siri, Apple Watch, iPad, the web), as praise, complaint, or request.

> "I would just like Reminders to talk to Mail and vice versa."

**Count:** ~29 / 400 (7%)

### ease_of_use_and_design
**Definition:** The interface is hard to learn, confusing, cluttered, dated, or takes too many taps, or the reviewer likes or dislikes the visual design. This applies when no single feature is the target of the complaint.

> "I want to like reminders. I really do but it takes too many clicks to get anything done. The UI is very busy at times and it’s hard to see everything without jumping to different sections of the app."

**Count:** ~27 / 400 (7%)

### sharing_and_sync
**Definition:** Sharing lists with other people or keeping reminders in sync across devices, as praise for the feature or complaints that changes don't sync or sharing fails.

> "Partner and I use this app for shared lists like shopping but notice that changes don’t always sync between us. Some items do while others don’t in the same list."

**Count:** ~21 / 400 (5%)

### intrusive_prompts
**Definition:** The app interrupts with prompts the reviewer didn't ask for: requests to rate the app, location-permission pop-ups, unwanted suggestions, or collaboration prompts.

> "Asking for a review, while someone is half way through dragging and dropping a task is poor usability. Expect better from Apple."

**Count:** ~14 / 400 (4%)

### other
**Definition:** The review is off-topic, unintelligible, spam, or too vague to classify (for example "Mid" or "Not too bad").

> "High pressure n Acid"

**Count:** ~29 / 400 (7%)
