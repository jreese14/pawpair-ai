import streamlit as st
from pawpal_system import Owner, Pet, Task, Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = None

if "schedule" not in st.session_state:
    st.session_state.schedule = None

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    available_time = st.number_input("Available time (minutes)", min_value=10, max_value=1440, value=120)

if st.button("Create Owner"):
    st.session_state.owner = Owner(name=owner_name, available_time=available_time, pets=[])
    st.session_state.tasks = []
    st.success(f"Owner '{owner_name}' created!")
    st.rerun()

if st.session_state.owner:
    st.write(f"**Current Owner:** {st.session_state.owner.name}")

    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])

    if st.button("Add Pet"):
        pet = Pet(name=pet_name, species=species, age=1, owner=st.session_state.owner)
        st.session_state.owner.add_pet(pet)
        st.success(f"Pet '{pet_name}' added!")

    if st.session_state.owner.pets:
        st.write(f"**Pets:** {[pet.name for pet in st.session_state.owner.pets]}")

    st.markdown("### Tasks")
    st.caption("Add tasks for your pet(s).")

    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    if st.session_state.owner and st.session_state.owner.pets:
        col1, col2, col3 = st.columns(3)
        with col1:
            task_title = st.text_input("Task title", value="Morning walk")
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col3:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

        col1, col2, col3 = st.columns(3)
        with col1:
            frequency = st.selectbox("Frequency", ["daily", "weekly", "once"], index=0)
        with col2:
            selected_pet = st.selectbox("Pet", [pet.name for pet in st.session_state.owner.pets])
        with col3:
            scheduled_time = st.time_input("Scheduled time", value=None)

        if st.button("Add task", use_container_width=True):
            pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet)
            task = Task(
                task_name=task_title,
                duration=int(duration),
                priority=priority,
                frequency=frequency,
                completed=False,
                owner=st.session_state.owner,
                pet=pet,
                scheduled_time=scheduled_time.strftime("%H:%M") if scheduled_time else None
            )
            st.session_state.tasks.append(task)
            st.success(f"Task '{task_title}' added to {selected_pet}!")

        if st.session_state.tasks:
            st.write("Current tasks:")
            for i, task in enumerate(st.session_state.tasks):
                col1, col2, col3 = st.columns([0.5, 3, 0.5])
                with col1:
                    is_done = st.checkbox("Done", value=task.completed, key=f"task_{i}")
                    if is_done != task.completed:
                        task.completed = is_done
                with col2:
                    status = "✓" if task.completed else "○"
                    st.write(f"{status} {task.task_name} ({task.duration}min, Priority: {task.priority}, Freq: {task.frequency}) - {task.pet.name}")
                with col3:
                    if st.button("Remove", key=f"remove_{i}"):
                        st.session_state.tasks.pop(i)
                        st.rerun()
        else:
            st.info("No tasks yet. Add one above.")
    else:
        st.info("Add a pet first.")

st.divider()

st.subheader("📅 Schedule & Analysis")

if st.button("Generate schedule", use_container_width=True):
    if st.session_state.owner and st.session_state.tasks:
        st.session_state.schedule = Schedule(owner=st.session_state.owner, tasks=st.session_state.tasks)
        st.success("Schedule generated!")
    else:
        st.warning("Please create an owner and add at least one task first.")

if st.session_state.schedule:
    schedule = st.session_state.schedule

    # Check for conflicts
    scheduled_tasks = [t for t in schedule.tasks if t.scheduled_time]
    conflicts = schedule.detect_scheduling_conflicts(scheduled_tasks)

    if conflicts:
        st.warning("⚠️ Scheduling Conflicts Detected:")
        for conflict in conflicts:
            st.warning(conflict)
    else:
        st.success("✅ No scheduling conflicts!")

    # Check available time
    total_time = sum(task.duration for task in scheduled_tasks)
    if total_time > schedule.owner.available_time:
        st.warning(f"⚠️ Tasks exceed available time: {total_time} min scheduled vs {schedule.owner.available_time} min available")
    else:
        st.info(f"✓ Tasks fit within available time: {total_time} min of {schedule.owner.available_time} min")

    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Full Schedule", "🔍 Filter by Pet", "✓ Completion Status", "📊 Analysis"])

    with tab1:
        st.subheader("Timeline View")
        if scheduled_tasks:
            sorted_tasks = schedule.sort_by_time(scheduled_tasks)
            schedule_data = []
            for task in sorted_tasks:
                status = "✓ Done" if task.completed else "⏳ Pending"
                schedule_data.append({
                    "Time": task.scheduled_time or "—",
                    "Task": task.task_name,
                    "Pet": task.pet.name,
                    "Duration": f"{task.duration}min",
                    "Priority": task.priority.upper(),
                    "Status": status
                })
            st.table(schedule_data)
        else:
            st.info("No tasks with scheduled times yet.")

    with tab2:
        st.subheader("Filter by Pet")
        pet_names = [pet.name for pet in schedule.owner.pets]
        selected_pet = st.selectbox("Select pet", pet_names, key="filter_pet")

        filtered = schedule.filter_tasks(pet_name=selected_pet)
        if filtered:
            filtered_data = []
            for task in schedule.sort_by_time(filtered):
                status = "✓" if task.completed else "⏳"
                filtered_data.append({
                    "Time": task.scheduled_time or "—",
                    "Task": task.task_name,
                    "Duration": f"{task.duration}min",
                    "Priority": task.priority,
                    "Status": status
                })
            st.table(filtered_data)
            st.caption(f"{len(filtered)} task(s) for {selected_pet}")
        else:
            st.info(f"No tasks for {selected_pet}")

    with tab3:
        st.subheader("Task Completion Status")
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Completed**")
            completed = schedule.filter_tasks(completed=True)
            if completed:
                for task in completed:
                    st.success(f"✓ {task.task_name} ({task.pet.name})")
            else:
                st.info("No completed tasks yet")

        with col2:
            st.write("**Pending**")
            incomplete = schedule.filter_tasks(completed=False)
            if incomplete:
                for task in incomplete:
                    st.warning(f"⏳ {task.task_name} ({task.pet.name})")
            else:
                st.info("All tasks complete!")

    with tab4:
        st.subheader("Schedule Analysis")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Tasks", len(schedule.tasks))
        with col2:
            st.metric("Scheduled Time", f"{total_time}min")
        with col3:
            remaining = schedule.owner.available_time - total_time
            st.metric("Time Remaining", f"{remaining}min")

        st.divider()
        st.write("**Summary**")
        if scheduled_tasks:
            earliest = min(t.scheduled_time for t in scheduled_tasks if t.scheduled_time)
            latest = max(t.scheduled_time for t in scheduled_tasks if t.scheduled_time)
            st.write(f"Schedule runs from **{earliest}** to **{latest}**")

        completion_pct = (len(schedule.filter_tasks(completed=True)) / len(schedule.tasks) * 100) if schedule.tasks else 0
        st.progress(completion_pct / 100, text=f"Completion: {completion_pct:.0f}%")
