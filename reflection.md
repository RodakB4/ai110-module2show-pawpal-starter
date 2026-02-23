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

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
