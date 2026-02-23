from pawpal_system import Task, Pet, Owner, Scheduler


# --- Helpers ---

def make_owner(*pets):
    owner = Owner(name="Jordan", available_minutes=60)
    for pet in pets:
        owner.add_pet(pet)
    return owner


# --- Existing tests ---

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


# --- Sorting tests ---

def test_sort_by_time_orders_shortest_first():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Long task",   duration_minutes=30, priority=1))
    pet.add_task(Task(title="Short task",  duration_minutes=5,  priority=2))
    pet.add_task(Task(title="Medium task", duration_minutes=15, priority=3))
    scheduler = Scheduler(owner=make_owner(pet))
    result = scheduler.sort_by_time(pet.tasks)
    durations = [t.duration_minutes for t in result]
    assert durations == sorted(durations)


def test_sort_by_time_does_not_modify_original_list():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Walk",      duration_minutes=20, priority=3))
    pet.add_task(Task(title="Breakfast", duration_minutes=5,  priority=3))
    original_order = [t.title for t in pet.tasks]
    scheduler = Scheduler(owner=make_owner(pet))
    scheduler.sort_by_time(pet.tasks)
    assert [t.title for t in pet.tasks] == original_order


# --- Recurring task tests ---

def test_recurring_daily_task_creates_next_occurrence():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Walk", duration_minutes=20, priority=3,
                      frequency="daily", date="2026-02-23"))
    owner = make_owner(pet)
    scheduler = Scheduler(owner=owner)
    walk = pet.tasks[0]
    scheduler.mark_task_complete(walk)
    assert len(pet.tasks) == 2
    assert pet.tasks[1].date == "2026-02-24"


def test_recurring_weekly_task_creates_next_occurrence():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Bath", duration_minutes=15, priority=2,
                      frequency="weekly", date="2026-02-23"))
    owner = make_owner(pet)
    scheduler = Scheduler(owner=owner)
    bath = pet.tasks[0]
    scheduler.mark_task_complete(bath)
    assert len(pet.tasks) == 2
    assert pet.tasks[1].date == "2026-03-02"


def test_non_recurring_task_does_not_create_next_occurrence():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="One-time groom", duration_minutes=10, priority=2))
    owner = make_owner(pet)
    scheduler = Scheduler(owner=owner)
    scheduler.mark_task_complete(pet.tasks[0])
    assert len(pet.tasks) == 1


def test_completed_recurring_task_is_marked_done():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Walk", duration_minutes=20, priority=3,
                      frequency="daily", date="2026-02-23"))
    owner = make_owner(pet)
    scheduler = Scheduler(owner=owner)
    walk = pet.tasks[0]
    scheduler.mark_task_complete(walk)
    assert walk.completed is True


# --- Conflict detection tests ---

def test_detect_conflicts_finds_same_time_slot():
    mochi = Pet(name="Mochi", species="dog")
    luna  = Pet(name="Luna",  species="cat")
    mochi.add_task(Task(title="Walk",        duration_minutes=20, priority=3, time="09:00"))
    luna.add_task( Task(title="Litter box",  duration_minutes=5,  priority=2, time="09:00"))
    scheduler = Scheduler(owner=make_owner(mochi, luna))
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    titles = {conflicts[0][0].title, conflicts[0][1].title}
    assert titles == {"Walk", "Litter box"}


def test_detect_conflicts_returns_empty_when_no_overlap():
    mochi = Pet(name="Mochi", species="dog")
    luna  = Pet(name="Luna",  species="cat")
    mochi.add_task(Task(title="Walk",       duration_minutes=20, priority=3, time="09:00"))
    luna.add_task( Task(title="Litter box", duration_minutes=5,  priority=2, time="10:00"))
    scheduler = Scheduler(owner=make_owner(mochi, luna))
    assert scheduler.detect_conflicts() == []


def test_detect_conflicts_ignores_tasks_without_time():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Walk",      duration_minutes=20, priority=3))
    pet.add_task(Task(title="Breakfast", duration_minutes=5,  priority=3))
    scheduler = Scheduler(owner=make_owner(pet))
    assert scheduler.detect_conflicts() == []
