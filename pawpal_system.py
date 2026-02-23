from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Tuple
from uuid import uuid4


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: int          # 1 = low, 2 = medium, 3 = high
    id: str = field(default_factory=lambda: str(uuid4()))
    category: str = ""     # e.g. "exercise", "feeding", "meds", "grooming", "enrichment"
    notes: str = ""
    completed: bool = False
    frequency: str = ""    # "daily", "weekly", or "" for one-time
    date: str = ""         # "YYYY-MM-DD", e.g. "2026-02-23"
    time: str = ""         # "HH:MM", e.g. "09:00"

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def is_high_priority(self) -> bool:
        """Return True if this task has the highest priority level (3)."""
        return self.priority == 3

    def to_dict(self) -> dict:
        """Return a plain dictionary representation of this task."""
        return {
            "id": self.id,
            "title": self.title,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "category": self.category,
            "notes": self.notes,
        }


@dataclass
class Pet:
    name: str
    species: str           # "dog", "cat", "other"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove the task with the given ID from this pet's task list."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_tasks_by_priority(self, priority: int) -> List[Task]:
        """Return all tasks matching the given priority level."""
        return [t for t in self.tasks if t.priority == priority]

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks sorted from highest to lowest priority."""
        return sorted(self.tasks, key=lambda t: t.priority, reverse=True)


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Collect every task from every pet this owner has."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def filter_by_priority(self, priority: int) -> List[Task]:
        """Return all tasks across all pets matching the given priority level."""
        return [t for t in self.get_all_tasks() if t.priority == priority]


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize the scheduler with an Owner and an empty schedule."""
        self.owner = owner
        self.schedule: List[Task] = []

    def build_schedule(self) -> None:
        """Greedily fill the schedule with highest-priority tasks that fit within the time budget."""
        all_tasks = self.owner.get_all_tasks()
        sorted_tasks = sorted(all_tasks, key=lambda t: t.priority, reverse=True)
        time_remaining = self.owner.available_minutes
        self.schedule = []
        for task in sorted_tasks:
            if task.duration_minutes <= time_remaining:
                self.schedule.append(task)
                time_remaining -= task.duration_minutes

    def mark_task_complete(self, task: Task) -> None:
        """Mark a task complete and auto-schedule the next occurrence if it is recurring."""
        task.mark_complete()
        if task.frequency in ("daily", "weekly"):
            next_task = self.handle_recurring(task)
            for pet in self.owner.pets:
                if task in pet.tasks:
                    pet.add_task(next_task)
                    break

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by duration, shortest first."""
        return sorted(tasks, key=lambda t: t.duration_minutes)

    def handle_recurring(self, task: Task) -> Task:
        """Create and return a new Task instance scheduled for the next recurrence date."""
        if not task.date:
            next_date = date.today()
        else:
            current_date = date.fromisoformat(task.date)
            if task.frequency == "daily":
                next_date = current_date + timedelta(days=1)
            elif task.frequency == "weekly":
                next_date = current_date + timedelta(weeks=1)
            else:
                next_date = current_date + timedelta(days=1)

        return Task(
            title=task.title,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            category=task.category,
            notes=task.notes,
            frequency=task.frequency,
            date=str(next_date),
            time=task.time,
        )

    def detect_conflicts(self) -> List[Tuple[Task, Task]]:
        """Return pairs of tasks that share the same non-empty time slot."""
        all_tasks = self.owner.get_all_tasks()
        timed = [t for t in all_tasks if t.time]
        conflicts = []
        for i, a in enumerate(timed):
            for b in timed[i + 1:]:
                if a.time == b.time:
                    conflicts.append((a, b))
        return conflicts

    def explain(self) -> List[str]:
        """Return a human-readable explanation for each scheduled and skipped task."""
        # Could be improved to return structured objects per scheduled task.
        priority_labels = {1: "low", 2: "medium", 3: "high"}
        explanations = []
        time_used = 0
        for task in self.schedule:
            time_used += task.duration_minutes
            label = priority_labels.get(task.priority, "unknown")
            explanations.append(
                f"'{task.title}' ({task.duration_minutes} min, {label} priority) — "
                f"included because it fits within your time budget. "
                f"Time used so far: {time_used}/{self.owner.available_minutes} min."
            )
        scheduled_ids = {t.id for t in self.schedule}
        skipped = [t for t in self.owner.get_all_tasks() if t.id not in scheduled_ids]
        for task in skipped:
            explanations.append(
                f"'{task.title}' ({task.duration_minutes} min) — skipped: not enough time remaining."
            )
        return explanations

    def get_unscheduled(self) -> List[Task]:
        """Return tasks that were not included in the schedule due to time constraints."""
        scheduled_ids = {t.id for t in self.schedule}
        return [t for t in self.owner.get_all_tasks() if t.id not in scheduled_ids]
