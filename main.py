from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(name="Jordan", available_minutes=60)

mochi = Pet(name="Mochi", species="dog")
luna = Pet(name="Luna", species="cat")

# Mochi's tasks
mochi.add_task(Task(title="Morning walk",   duration_minutes=20, priority=3, category="exercise"))
mochi.add_task(Task(title="Breakfast",      duration_minutes=5,  priority=3, category="feeding"))
mochi.add_task(Task(title="Flea treatment", duration_minutes=10, priority=2, category="meds"))

# Luna's tasks
luna.add_task(Task(title="Litter box clean", duration_minutes=5,  priority=2, category="grooming"))
luna.add_task(Task(title="Puzzle feeder",    duration_minutes=15, priority=1, category="enrichment"))

owner.add_pet(mochi)
owner.add_pet(luna)

# --- Schedule ---
scheduler = Scheduler(owner=owner)
scheduler.build_schedule()

# --- Display ---
print(f"=== Today's Schedule for {owner.name} ===")
print(f"Time budget: {owner.available_minutes} minutes\n")

if scheduler.schedule:
    print("Scheduled tasks:")
    for task in scheduler.schedule:
        priority_label = {1: "low", 2: "medium", 3: "high"}.get(task.priority, "?")
        print(f"  - [{priority_label}] {task.title} ({task.duration_minutes} min)")
else:
    print("  No tasks could be scheduled.")

unscheduled = scheduler.get_unscheduled()
if unscheduled:
    print("\nSkipped (not enough time):")
    for task in unscheduled:
        print(f"  - {task.title} ({task.duration_minutes} min)")

print("\nExplanations:")
for line in scheduler.explain():
    print(f"  {line}")

# --- Sorting Test ---
print("\n=== Sorting Test ===")
all_tasks = owner.get_all_tasks()
sorted_tasks = scheduler.sort_by_time(all_tasks)

for t in sorted_tasks:
    print(f"{t.title} — {t.duration_minutes} min — priority {t.priority}")

# --- Filter: High Priority Only ---
print("\n=== Filter: High Priority Only ===")
high_priority = owner.filter_by_priority(3)

for t in high_priority:
    print(f"{t.title} — priority {t.priority}")

# --- Recurring Task Test ---
print("\n=== Recurring Task Test ===")
example_task = mochi.tasks[0]
example_task.frequency = "daily"
example_task.date = "2026-02-23"

new_task = scheduler.handle_recurring(example_task)

print("Original task date:", example_task.date)
print("New recurring task date:", new_task.date)

# --- Conflict Detection ---
print("\n=== Conflict Detection ===")
mochi.tasks[0].time = "09:00"
luna.tasks[0].time = "09:00"

conflicts = scheduler.detect_conflicts()

if conflicts:
    print("Conflicts found:")
    for a, b in conflicts:
        print(f" - {a.title} conflicts with {b.title}")
else:
    print("No conflicts detected.")
