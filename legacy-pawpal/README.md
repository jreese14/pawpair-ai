# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
==================================================
Today's Schedule
==================================================

=== Schedule for Alice ===
Available time: 120 minutes

08:00 — ○ Feed Buddy (Pet: Buddy, 10min) [priority: high]
08:10 — ✓ Groom Whiskers (Pet: Whiskers, 25min) [priority: high]
08:35 — ○ Play with Buddy (Pet: Buddy, 30min) [priority: medium]
09:05 — ○ Clean Whiskers' litter box (Pet: Whiskers, 15min) [priority: low]

Total scheduled time: 80 minutes
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest tests/test_pawpal.py -v
```

The test suite includes **20 comprehensive tests** covering:

- **Sorting Correctness**: Tasks sorted chronologically by scheduled_time, handling empty lists, single tasks, same-time stability, and None values
- **Recurrence Logic**: Daily/weekly tasks create next-day/next-week instances; non-recurring tasks return None; property preservation across task chains
- **Conflict Detection**: Multiple tasks at same time flagged with pet names; multiple conflicts at different times handled separately; unscheduled tasks ignored

Output:
```
============================= test session starts ==============================
platform darwin -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0 -- /Users/Nae/ai110-module2show-pawpal-starter/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/Nae/ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collecting ... collected 20 items

tests/test_pawpal.py::TestTaskCompletion::test_mark_complete PASSED      [  5%]
tests/test_pawpal.py::TestTaskAddition::test_add_task_to_schedule PASSED [ 10%]
tests/test_pawpal.py::TestTaskAddition::test_pet_task_retrieval PASSED   [ 15%]
tests/test_pawpal.py::TestSortingCorrectness::test_sort_by_time_chronological_order PASSED [ 20%]
tests/test_pawpal.py::TestSortingCorrectness::test_sort_empty_list PASSED [ 25%]
tests/test_pawpal.py::TestSortingCorrectness::test_sort_single_task PASSED [ 30%]
tests/test_pawpal.py::TestSortingCorrectness::test_sort_tasks_same_time PASSED [ 35%]
tests/test_pawpal.py::TestSortingCorrectness::test_sort_with_none_times PASSED [ 40%]
tests/test_pawpal.py::TestRecurrenceLogic::test_daily_task_creates_next_day_instance PASSED [ 45%]
tests/test_pawpal.py::TestRecurrenceLogic::test_multiple_recurring_task_chain PASSED [ 50%]
tests/test_pawpal.py::TestRecurrenceLogic::test_non_recurring_task_returns_none PASSED [ 55%]
tests/test_pawpal.py::TestRecurrenceLogic::test_recurring_task_preserves_properties PASSED [ 60%]
tests/test_pawpal.py::TestRecurrenceLogic::test_weekly_task_creates_next_week_instance PASSED [ 65%]
tests/test_pawpal.py::TestConflictDetection::test_detect_conflict_empty_list PASSED [ 70%]
tests/test_pawpal.py::TestConflictDetection::test_detect_conflict_mixed_scheduled_unscheduled PASSED [ 75%]
tests/test_pawpal.py::TestConflictDetection::test_detect_conflict_no_scheduled_times PASSED [ 80%]
tests/test_pawpal.py::TestConflictDetection::test_detect_conflict_three_tasks_same_time PASSED [ 85%]
tests/test_pawpal.py::TestConflictDetection::test_detect_conflict_two_tasks_same_time PASSED [ 90%]
tests/test_pawpal.py::TestConflictDetection::test_detect_multiple_conflict_times PASSED [ 95%]
tests/test_pawpal.py::TestConflictDetection::test_detect_no_conflict_different_times PASSED [100%]

============================== 20 passed in 0.03s ==============================
```
Confidence Level: 5

## 📐 Smarter Scheduling

The scheduler organizes tasks by user-specified time slots and provides filtering, conflict detection, and automatic recurring task management.

| Feature | Method(s) | Description |
|---------|-----------|-------------|
| **Task Sorting** | `Schedule.sort_by_time()` | Sorts tasks chronologically by `scheduled_time`. |
| **Filtering** | `Schedule.filter_tasks(completed, pet_name)` | Filters tasks by completion status and/or pet name. |
| **Conflict Detection** | `Schedule.detect_scheduling_conflicts()` | Detects multiple tasks at the same time slot and returns warning message. |
| **Recurring Tasks** | `Schedule.complete_task()` | Marks a task complete and auto-creates next occurrence for daily/weekly tasks using `timedelta`. Daily +1 day, weekly +7 days. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Enter owner name and available time, then click "Create Owner"
2. Add a pet by entering its name, selecting species, then click "Add Pet"
3. Create a task: enter title, duration, priority, and frequency, scheduled time and assign the task to a pet
4. Click "Generate Schedule" to see the organized plan
5. View the schedule across four tabs: full timeline, filter by pet, completion status, and analysis metrics

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
