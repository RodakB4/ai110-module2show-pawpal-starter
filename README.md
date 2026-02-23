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

## Smarter Scheduling

Beyond basic priority sorting, the scheduler includes several additional features:

- **Priority filtering** — `Owner.filter_by_priority(n)` returns all tasks across all pets at a given priority level (1 = low, 2 = medium, 3 = high), making it easy to surface only the most critical items.
- **Sort by duration** — `Scheduler.sort_by_time(tasks)` reorders any task list shortest-first, useful for filling remaining time gaps after high-priority tasks are placed.
- **Recurring tasks** — Tasks can be marked as `"daily"` or `"weekly"`. Calling `Scheduler.mark_task_complete(task)` marks the task done and automatically creates the next occurrence using Python's `timedelta`, adding it back to the correct pet.
- **Conflict detection** — `Scheduler.detect_conflicts()` scans all tasks with an assigned `time` field and returns every pair that shares the same time slot, so the owner can resolve clashes before the day starts.

## Testing PawPal+

Run the full test suite with:

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover

| Area | Tests |
|---|---|
| **Task completion** | Verifies `mark_complete()` flips `completed` from `False` to `True` |
| **Pet task management** | Verifies `add_task()` correctly grows a pet's task list |
| **Sorting** | Verifies `sort_by_time()` returns tasks shortest-first and does not mutate the original list |
| **Recurring tasks** | Verifies daily tasks schedule the next day, weekly tasks schedule 7 days out, one-time tasks do not recur, and the completed flag is set on the original |
| **Conflict detection** | Verifies overlapping time slots are flagged, non-overlapping slots return no conflicts, and tasks without a time field are ignored |

### Confidence Level

⭐⭐⭐⭐ (4 / 5)

The core scheduling behaviors — priority ordering, time budgeting, recurring task generation, and conflict detection — are all covered and passing. One star is held back because edge cases like an empty pet list, zero available minutes, or two pets with the same name are not yet tested. Those would be the next tests to write.

---

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
