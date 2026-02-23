from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=20, priority=3)
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task(title="Breakfast", duration_minutes=5, priority=3))
    assert len(pet.tasks) == 1
    pet.add_task(Task(title="Evening walk", duration_minutes=20, priority=2))
    assert len(pet.tasks) == 2
