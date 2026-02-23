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
    owner_name = st.text_input("Your name", value=owner.name)
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

    if st.button("Add task"):
        selected_pet.add_task(Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=PRIORITY_MAP[priority_label],
        ))
        st.success(f"'{task_title}' added to {selected_pet_name}.")

st.divider()

# --- Current Tasks ---
st.subheader("Current Tasks")
all_tasks = owner.get_all_tasks()
if all_tasks:
    st.table([t.to_dict() for t in all_tasks])
else:
    st.info("No tasks yet. Add some above.")

st.divider()

# --- Generate Schedule ---
st.subheader("Generate Today's Schedule")
st.caption(f"Time budget: {owner.available_minutes} minutes")

if st.button("Generate schedule"):
    if not all_tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(owner=owner)
        scheduler.build_schedule()

        if scheduler.schedule:
            st.success(f"Scheduled {len(scheduler.schedule)} task(s).")
            st.table([t.to_dict() for t in scheduler.schedule])
        else:
            st.warning("No tasks fit within your time budget.")

        unscheduled = scheduler.get_unscheduled()
        if unscheduled:
            st.markdown("**Skipped tasks:**")
            st.table([t.to_dict() for t in unscheduled])

        st.markdown("**Explanations:**")
        for line in scheduler.explain():
            st.markdown(f"- {line}")
