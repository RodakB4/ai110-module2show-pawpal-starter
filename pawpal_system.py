from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: int          # 1 = low, 2 = medium, 3 = high
    id: str = ""
    category: str = ""     # e.g. "exercise", "feeding", "meds", "grooming", "enrichment"
    notes: str = ""

    def is_high_priority(self) -> bool:
        pass

    def to_dict(self) -> dict:
        pass


@dataclass
class Pet:
    name: str
    species: str           # "dog", "cat", "other"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_id: str) -> None:
        pass

    def get_tasks_by_priority(self, priority: int) -> List[Task]:
        pass

    def get_all_tasks(self) -> List[Task]:
        pass


class Scheduler:
    def __init__(self, tasks: List[Task], available_minutes: int):
        self.tasks = tasks
        self.available_minutes = available_minutes
        self.schedule: List[Task] = []

    def build_schedule(self) -> None:
        pass

    def explain(self) -> List[str]:
        # Returns a list of strings for now.
        # Could be improved to return structured objects per scheduled task.
        pass

    def get_unscheduled(self) -> List[Task]:
        pass
