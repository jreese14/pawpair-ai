from pawpal_system import Owner, Pet, Task, Schedule
from datetime import datetime


def main():
    owner = Owner(name="Alice", available_time=120, pets=[])

    dog = Pet(name="Buddy", species="Dog", age=3, owner=owner)
    cat = Pet(name="Whiskers", species="Cat", age=2, owner=owner)

    owner.add_pet(dog)
    owner.add_pet(cat)

    task1 = Task(
        task_name="Feed Buddy",
        duration=10,
        priority="high",
        frequency="daily",
        completed=False,
        owner=owner,
        pet=dog,
        scheduled_time="08:00"
    )

    task2 = Task(
        task_name="Play with Buddy",
        duration=30,
        priority="medium",
        frequency="daily",
        completed=False,
        owner=owner,
        pet=dog,
        scheduled_time="08:20"
    )

    task3 = Task(
        task_name="Clean Whiskers' litter box",
        duration=15,
        priority="low",
        frequency="daily",
        completed=False,
        owner=owner,
        pet=cat,
        scheduled_time="09:00"
    )

    task4 = Task(
        task_name="Groom Whiskers",
        duration=25,
        priority="high",
        frequency="weekly",
        completed=True,
        owner=owner,
        pet=cat,
        scheduled_time="08:50"
    )

    schedule = Schedule(owner=owner, tasks=[])

    # Add tasks out of order to test sorting
    schedule.add_task(task3)
    schedule.add_task(task1)
    schedule.add_task(task4)
    schedule.add_task(task2)

    # Create an additional task
    conflicting_task = Task(
        task_name="Vet checkup for Buddy",
        duration=15,
        priority="high",
        frequency="monthly",
        completed=False,
        owner=owner,
        pet=dog,
        scheduled_time="09:30"
    )
    schedule.add_task(conflicting_task)

    print("\n" + "="*50)
    print("Today's Schedule (sorted by time)")
    print("="*50)
    schedule.display_schedule()

    print("\n" + "="*50)
    print("Completed Tasks Only")
    print("="*50)
    completed_tasks = schedule.filter_tasks(completed=True)
    for task in completed_tasks:
        print(f"  ✓ {task.task_name} (Pet: {task.pet.name})")

    print("\n" + "="*50)
    print("Incomplete Tasks Only")
    print("="*50)
    incomplete_tasks = schedule.filter_tasks(completed=False)
    for task in incomplete_tasks:
        print(f"  ○ {task.task_name} (Pet: {task.pet.name})")

    print("\n" + "="*50)
    print("Tasks for Buddy")
    print("="*50)
    buddy_tasks = schedule.filter_tasks(pet_name="Buddy")
    for task in buddy_tasks:
        status = "✓" if task.completed else "○"
        print(f"  {status} {task.task_name} ({task.duration}min, {task.priority})")

    print("\n" + "="*50)
    print("Incomplete Tasks for Whiskers")
    print("="*50)
    whiskers_incomplete = schedule.filter_tasks(completed=False, pet_name="Whiskers")
    for task in whiskers_incomplete:
        print(f"  ○ {task.task_name} ({task.duration}min, {task.priority})")

    print("\n" + "="*50)
    print("Tasks Sorted by Time")
    print("="*50)
    sorted_by_time = schedule.sort_by_time()
    for task in sorted_by_time:
        status = "✓" if task.completed else "○"
        print(f"  {task.scheduled_time} — {status} {task.task_name} (Pet: {task.pet.name})")

    print("\n" + "="*50)
    print("Completing Recurring Tasks")
    print("="*50)
    print(f"Initial task count: {len(schedule.tasks)}")

    # Complete the "Feed Buddy" daily task
    feed_buddy = next(t for t in schedule.tasks if t.task_name == "Feed Buddy")
    next_feed = schedule.complete_task(feed_buddy)
    print(f"\n✓ Marked 'Feed Buddy' as complete")
    print(f"  Original due date: {feed_buddy.due_date.strftime('%Y-%m-%d')}")
    print(f"  New task created for: {next_feed.due_date.strftime('%Y-%m-%d')} (tomorrow)")

    # Complete the "Play with Buddy" daily task
    play_buddy = next(t for t in schedule.tasks if t.task_name == "Play with Buddy")
    next_play = schedule.complete_task(play_buddy)
    print(f"\n✓ Marked 'Play with Buddy' as complete")
    print(f"  Original due date: {play_buddy.due_date.strftime('%Y-%m-%d')}")
    print(f"  New task created for: {next_play.due_date.strftime('%Y-%m-%d')} (tomorrow)")

    print(f"\nFinal task count: {len(schedule.tasks)}")
    print("\nAll tasks after completing recurring ones:")
    for task in schedule.tasks:
        status = "✓" if task.completed else "○"
        print(f"  {status} {task.task_name} — Due: {task.due_date.strftime('%Y-%m-%d')} (Frequency: {task.frequency})")

    print("\n" + "="*50)
    print("Conflict Detection Demo")
    print("="*50)
    print("\nDemonstrating conflict detection with manually scheduled tasks...\n")

    # Create a separate schedule to demonstrate conflicts
    conflict_schedule = Schedule(owner=owner, tasks=[])

    # Add same tasks but we'll manually set conflicting times
    task_a = Task(
        task_name="Morning walk with Buddy",
        duration=20,
        priority="high",
        frequency="daily",
        completed=False,
        owner=owner,
        pet=dog,
        scheduled_time="08:00"
    )
    task_b = Task(
        task_name="Feeding Buddy",
        duration=10,
        priority="high",
        frequency="daily",
        completed=False,
        owner=owner,
        pet=dog,
        scheduled_time="08:00"
    )
    task_c = Task(
        task_name="Play with Buddy",
        duration=15,
        priority="medium",
        frequency="daily",
        completed=False,
        owner=owner,
        pet=dog,
        scheduled_time="08:00"
    )
    task_d = Task(
        task_name="Groom Whiskers",
        duration=25,
        priority="high",
        frequency="weekly",
        completed=False,
        owner=owner,
        pet=cat,
        scheduled_time="08:30"
    )

    conflict_schedule.add_task(task_a)
    conflict_schedule.add_task(task_b)
    conflict_schedule.add_task(task_c)
    conflict_schedule.add_task(task_d)

    print("Schedule with conflicts detected:\n")
    conflicts = conflict_schedule.detect_scheduling_conflicts()
    if conflicts:
        print("Found scheduling conflicts:")
        for warning in conflicts:
            print(warning)
    else:
        print("No conflicts detected.")


if __name__ == "__main__":
    main()
