import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Session state init ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Default User", available_minutes=60)

owner = st.session_state.owner

st.title("🐾 PawPal+")

# --- Owner Info ---
st.subheader("Owner Info")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Your name", value="", placeholder="e.g. Default User")
with col2:
    available_minutes = st.number_input(
        "Time available today (minutes)", min_value=1, max_value=480, value=owner.available_minutes
    )
owner.name = owner_name
owner.available_minutes = available_minutes

st.divider()

# --- Add a Pet ---
st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner.add_pet(Pet(name=pet_name, species=species))
    st.success(f"{pet_name} the {species} added!")

if owner.pets:
    st.write("Your pets:", ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a Task ---
st.subheader("Add a Task")

PRIORITY_MAP = {"low": 1, "medium": 2, "high": 3}

if not owner.pets:
    st.warning("Add a pet first before adding tasks.")
else:
    pet_names = [p.name for p in owner.pets]
    selected_pet_name = st.selectbox("Assign to pet", pet_names)
    selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col4, col5 = st.columns(2)
    with col4:
        frequency = st.selectbox("Repeats", ["none", "daily", "weekly"])
    with col5:
        task_time = st.text_input("Time slot (HH:MM, optional)", value="", placeholder="e.g. 09:00")

    if st.button("Add task"):
        selected_pet.add_task(Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=PRIORITY_MAP[priority_label],
            frequency="" if frequency == "none" else frequency,
            time=task_time.strip(),
        ))
        st.success(f"'{task_title}' added to {selected_pet_name}.")

st.divider()

# --- Current Tasks ---
st.subheader("Current Tasks")
all_tasks = owner.get_all_tasks()

if all_tasks:
    col1, col2 = st.columns(2)
    with col1:
        priority_filter = st.selectbox(
            "Filter by priority",
            ["all", "high (3)", "medium (2)", "low (1)"]
        )
    with col2:
        sort_mode = st.selectbox("Sort by", ["priority (default)", "duration (shortest first)"])

    filtered = all_tasks
    if priority_filter == "high (3)":
        filtered = owner.filter_by_priority(3)
    elif priority_filter == "medium (2)":
        filtered = owner.filter_by_priority(2)
    elif priority_filter == "low (1)":
        filtered = owner.filter_by_priority(1)

    if sort_mode == "duration (shortest first)":
        scheduler_preview = Scheduler(owner=owner)
        filtered = scheduler_preview.sort_by_time(filtered)

    priority_labels = {1: "low", 2: "medium", 3: "high"}
    display_rows = [
        {
            "title": t.title,
            "duration (min)": t.duration_minutes,
            "priority": priority_labels.get(t.priority, "?"),
            "repeats": t.frequency or "none",
            "time slot": t.time or "—",
            "done": "✔" if t.completed else "",
        }
        for t in filtered
    ]
    st.table(display_rows)

    # Conflict warning
    conflict_checker = Scheduler(owner=owner)
    conflicts = conflict_checker.detect_conflicts()
    if conflicts:
        st.warning(f"⚠️ {len(conflicts)} time conflict(s) detected:")
        for a, b in conflicts:
            st.markdown(f"- **{a.title}** and **{b.title}** are both scheduled at `{a.time}`")
else:
    st.info("No tasks yet. Add some above.")

st.divider()

# --- Generate Schedule ---
st.subheader("Generate Today's Schedule")
st.caption(f"Time budget: {owner.available_minutes} minutes")

if st.button("Generate schedule"):
    all_tasks = owner.get_all_tasks()
    if not all_tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(owner=owner)
        scheduler.build_schedule()

        if scheduler.schedule:
            total_scheduled = sum(t.duration_minutes for t in scheduler.schedule)
            st.success(
                f"Scheduled {len(scheduler.schedule)} task(s) — "
                f"{total_scheduled} of {owner.available_minutes} minutes used."
            )
            priority_labels = {1: "low", 2: "medium", 3: "high"}
            st.table([
                {
                    "title": t.title,
                    "duration (min)": t.duration_minutes,
                    "priority": priority_labels.get(t.priority, "?"),
                    "repeats": t.frequency or "none",
                    "time slot": t.time or "—",
                }
                for t in scheduler.schedule
            ])
        else:
            st.warning("No tasks fit within your time budget.")

        unscheduled = scheduler.get_unscheduled()
        if unscheduled:
            st.error(f"{len(unscheduled)} task(s) could not be scheduled:")
            st.table([{"title": t.title, "duration (min)": t.duration_minutes} for t in unscheduled])

        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.warning(f"⚠️ {len(conflicts)} time conflict(s) in your task list:")
            for a, b in conflicts:
                st.markdown(f"- **{a.title}** and **{b.title}** overlap at `{a.time}`")

        with st.expander("Scheduling explanations"):
            for line in scheduler.explain():
                st.markdown(f"- {line}")
