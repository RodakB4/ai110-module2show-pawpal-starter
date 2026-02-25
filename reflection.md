# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I organized the design around three classes. `Task` holds everything about a single care activity — its name, how long it takes, and how urgent it is. `Pet` groups the tasks that belong to one animal. `Scheduler` takes a list of tasks and a time budget and decides which tasks fit into the day, returning an ordered plan the UI can display. The three core user actions that shaped this design were: adding pet care tasks, generating a daily schedule based on available time, and viewing today's scheduled tasks with explanations of why each was chosen.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After reviewing the class skeletons, I made several design refinements. First, I added unique IDs to tasks because using the task title for identifying or removing tasks can lead to errors when multiple tasks share the same name. Second, I changed priority from a string to an integer scale (1–3), making comparison and sorting more reliable for the scheduler. I also noted that remove_task() should operate on IDs instead of titles for safety.
Finally, I recognized that the Scheduler could be decoupled from the Pet class to accept a list of tasks directly, which would allow more flexible scheduling in the future. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers two constraints: available time (in minutes) and task priority (an integer from 1 to 3). It sorts all tasks from highest to lowest priority and then greedily adds each one to the schedule only if it fits within the remaining time budget. Priority was treated as the most important constraint because some tasks — like giving medication — cannot be skipped regardless of how long they take. Time came second because it is the hard outer limit that no schedule can exceed.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The greedy approach trades optimality for simplicity. Because tasks are always selected in priority order, a single large high-priority task can consume enough time that several smaller lower-priority tasks get skipped — even though those smaller tasks could have collectively fit in the same window. A smarter algorithm (like a knapsack solver) could pack the day more efficiently, but it would be significantly harder to read, explain, and maintain.

A second smaller tradeoff came up when handling recurring task frequencies. A dictionary lookup (`{"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}`) would be considered more Pythonic, but we kept the `if/elif` chain because it reads more naturally in plain English and has identical performance at only two conditions. Clarity for a human reader was worth more than style points here.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

AI was used across every phase of the project rather than just for writing code. In the design phase it helped brainstorm what attributes and methods each class should carry and pointed out that the initial design was missing an `Owner` class entirely. During implementation it generated class skeletons, filled in method logic, and suggested the `dataclasses.replace()` approach for copying tasks cleanly. In the testing phase it wrote pytest cases from the method signatures alone. The most effective prompts were specific and contextual — for example, asking "based on this class, what edge cases should I test?" consistently produced more useful output than asking for code directly. Asking the AI to compare two approaches (like greedy vs. knapsack scheduling) and explain the tradeoffs was especially helpful for making design decisions with confidence.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When the AI initially designed `Scheduler` to accept a `Pet` directly instead of an `Owner`, I pushed back on it. The suggestion worked for a single-pet scenario but would have broken down the moment a second pet was added, because the scheduler would have no way to see tasks across both animals. I evaluated it by tracing the data flow — "where does `available_minutes` live, and how does the scheduler reach tasks from multiple pets?" — and the answer made it clear that `Owner` was the right entry point. The fix was to pass `Owner` to `Scheduler` and have `Owner.get_all_tasks()` flatten the task list across all pets. I then verified it worked by running `main.py` with two pets and confirming both pets' tasks appeared in the schedule.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

Eleven tests were written across five areas: task completion (`mark_complete()` flipping the completed flag), pet task management (`add_task()` growing the task list), sorting (`sort_by_time()` ordering correctly and not mutating the original list), recurring tasks (daily and weekly next-date generation, one-time tasks not recurring, and the completed flag being set on the original), and conflict detection (overlapping time slots flagged, non-overlapping slots returning empty, and tasks without a time field being ignored). These tests mattered because the scheduler's correctness depends entirely on these lower-level behaviors — if `add_task()` silently fails or `sort_by_time()` modifies the original list, the schedule output becomes unpredictable in ways that are hard to trace from the UI.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

Confidence level: 4 out of 5. The core behaviors are fully tested and all 11 tests pass. The remaining uncertainty comes from untested edge cases: an owner with no pets, a time budget of zero minutes, two pets sharing the same name (which would break the pet selector in the UI), a recurring task with no date set, and a schedule where every task is exactly the same duration and priority. Those cases would be the first tests to add in the next iteration.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The recurring task system came together more cleanly than expected. Connecting `mark_task_complete()` in `Scheduler` to `handle_recurring()` and then back to the correct `Pet` — all in about eight lines — felt like a genuine design win. The separation of concerns paid off here: because `Task` only holds data, `Pet` only manages its list, and `Scheduler` owns the logic, adding recurring behavior required no changes to `Task` or `Pet` at all.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

The `Scheduler` currently uses a simple greedy algorithm that always picks highest priority first. In a real app this causes frustrating situations where one long high-priority task blocks several short tasks that could have fit. I would explore a lightweight knapsack approach that maximizes the number of tasks completed rather than just filling from the top of the priority list. I would also move `available_minutes` out of the flat `Owner` dataclass and into a separate daily schedule object, which would make it easier to plan multiple days without overwriting the same field.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

AI is most useful when you already have a clear enough picture of the system to evaluate what it gives you. Every time I gave the AI a vague prompt I got plausible-looking code that had subtle structural problems — like the `Scheduler` receiving `Pet` instead of `Owner`. Every time I gave it a specific, constrained question the output was accurate and fast to integrate. The real skill in AI-assisted development is not prompting — it is knowing your own design well enough to spot when the AI's suggestion drifts away from it.
