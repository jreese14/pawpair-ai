import unittest
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Schedule


class TestTaskCompletion(unittest.TestCase):
    """Test that mark_complete() changes task status."""

    def setUp(self):
        self.owner = Owner(name="Alice", available_time=120, pets=[])
        self.pet = Pet(name="Buddy", species="Dog", age=3, owner=self.owner)

    def test_mark_complete(self):
        task = Task(
            task_name="Feed Buddy",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet
        )
        self.assertFalse(task.completed)
        task.mark_complete()
        self.assertTrue(task.completed)


class TestTaskAddition(unittest.TestCase):
    """Test that adding a task to a schedule for a pet works correctly."""

    def setUp(self):
        self.owner = Owner(name="Alice", available_time=120, pets=[])
        self.pet = Pet(name="Buddy", species="Dog", age=3, owner=self.owner)
        self.owner.add_pet(self.pet)
        self.schedule = Schedule(owner=self.owner, tasks=[])

    def test_add_task_to_schedule(self):
        task = Task(
            task_name="Feed Buddy",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet
        )
        self.assertEqual(len(self.schedule.tasks), 0)
        self.schedule.add_task(task)
        self.assertEqual(len(self.schedule.tasks), 1)

    def test_pet_task_retrieval(self):
        """Verify tasks for a specific pet can be retrieved from schedule."""
        task1 = Task(
            task_name="Feed Buddy",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet
        )
        task2 = Task(
            task_name="Play with Buddy",
            duration=30,
            priority="medium",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet
        )
        self.schedule.add_task(task1)
        self.schedule.add_task(task2)

        pet_tasks = [t for t in self.schedule.tasks if t.pet == self.pet]
        self.assertEqual(len(pet_tasks), 2)


class TestSortingCorrectness(unittest.TestCase):
    """Verify tasks are sorted by scheduled_time in chronological order."""

    def setUp(self):
        self.owner = Owner(name="Alice", available_time=300, pets=[])
        self.pet = Pet(name="Buddy", species="Dog", age=3, owner=self.owner)
        self.owner.add_pet(self.pet)
        self.schedule = Schedule(owner=self.owner, tasks=[])

    def test_sort_by_time_chronological_order(self):
        """Tasks added out of order should be sorted chronologically."""
        task1 = Task(
            task_name="Evening walk",
            duration=30,
            priority="medium",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet,
            scheduled_time="18:00"
        )
        task2 = Task(
            task_name="Morning feed",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet,
            scheduled_time="08:00"
        )
        task3 = Task(
            task_name="Afternoon playtime",
            duration=20,
            priority="medium",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet,
            scheduled_time="14:00"
        )

        self.schedule.add_task(task1)
        self.schedule.add_task(task2)
        self.schedule.add_task(task3)

        sorted_tasks = self.schedule.sort_by_time([task1, task2, task3])

        self.assertEqual(sorted_tasks[0].scheduled_time, "08:00")
        self.assertEqual(sorted_tasks[1].scheduled_time, "14:00")
        self.assertEqual(sorted_tasks[2].scheduled_time, "18:00")
        self.assertEqual(sorted_tasks[0].task_name, "Morning feed")

    def test_sort_empty_list(self):
        """Sorting an empty task list should return an empty list."""
        sorted_tasks = self.schedule.sort_by_time([])
        self.assertEqual(sorted_tasks, [])

    def test_sort_single_task(self):
        """Sorting a single task should return a list with that task."""
        task = Task(
            task_name="Feed",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet,
            scheduled_time="09:00"
        )
        sorted_tasks = self.schedule.sort_by_time([task])
        self.assertEqual(len(sorted_tasks), 1)
        self.assertEqual(sorted_tasks[0], task)

    def test_sort_tasks_same_time(self):
        """Tasks with same scheduled_time should maintain stable order."""
        task1 = Task(
            task_name="Task A",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet,
            scheduled_time="09:00"
        )
        task2 = Task(
            task_name="Task B",
            duration=10,
            priority="medium",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet,
            scheduled_time="09:00"
        )
        sorted_tasks = self.schedule.sort_by_time([task1, task2])
        self.assertEqual(len(sorted_tasks), 2)
        self.assertEqual(sorted_tasks[0].task_name, "Task A")
        self.assertEqual(sorted_tasks[1].task_name, "Task B")

    def test_sort_with_none_times(self):
        """Tasks without scheduled_time should sort to beginning."""
        task_no_time = Task(
            task_name="Unscheduled",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet,
            scheduled_time=None
        )
        task_with_time = Task(
            task_name="Scheduled",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet,
            scheduled_time="09:00"
        )
        sorted_tasks = self.schedule.sort_by_time([task_with_time, task_no_time])
        self.assertEqual(sorted_tasks[0].scheduled_time, None)
        self.assertEqual(sorted_tasks[1].scheduled_time, "09:00")


class TestRecurrenceLogic(unittest.TestCase):
    """Verify recurring tasks create new instances with correct due dates."""

    def setUp(self):
        self.owner = Owner(name="Alice", available_time=300, pets=[])
        self.pet = Pet(name="Buddy", species="Dog", age=3, owner=self.owner)
        self.owner.add_pet(self.pet)
        self.schedule = Schedule(owner=self.owner, tasks=[])
        self.base_date = datetime(2026, 7, 9, 12, 0, 0)

    def test_daily_task_creates_next_day_instance(self):
        """Completing a daily task should create a new task for the next day."""
        task = Task(
            task_name="Feed Buddy",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet,
            due_date=self.base_date
        )
        self.schedule.add_task(task)
        self.assertEqual(len(self.schedule.tasks), 1)

        new_task = self.schedule.complete_task(task)

        self.assertTrue(task.completed)
        self.assertIsNotNone(new_task)
        self.assertEqual(new_task.task_name, "Feed Buddy")
        self.assertEqual(new_task.frequency, "daily")
        self.assertFalse(new_task.completed)
        self.assertEqual(new_task.due_date, self.base_date + timedelta(days=1))
        self.assertEqual(len(self.schedule.tasks), 2)

    def test_weekly_task_creates_next_week_instance(self):
        """Completing a weekly task should create a new task for the next week."""
        task = Task(
            task_name="Groom Buddy",
            duration=30,
            priority="medium",
            frequency="weekly",
            completed=False,
            owner=self.owner,
            pet=self.pet,
            due_date=self.base_date
        )
        self.schedule.add_task(task)

        new_task = self.schedule.complete_task(task)

        self.assertTrue(task.completed)
        self.assertIsNotNone(new_task)
        self.assertEqual(new_task.due_date, self.base_date + timedelta(days=7))
        self.assertEqual(len(self.schedule.tasks), 2)

    def test_non_recurring_task_returns_none(self):
        """Completing a non-recurring task should return None."""
        task = Task(
            task_name="One-time vet visit",
            duration=45,
            priority="high",
            frequency="once",
            completed=False,
            owner=self.owner,
            pet=self.pet,
            due_date=self.base_date
        )
        self.schedule.add_task(task)

        result = self.schedule.complete_task(task)

        self.assertTrue(task.completed)
        self.assertIsNone(result)
        self.assertEqual(len(self.schedule.tasks), 1)

    def test_multiple_recurring_task_chain(self):
        """Completing recurring tasks multiple times should create a chain."""
        task1 = Task(
            task_name="Morning feed",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet,
            due_date=self.base_date
        )
        self.schedule.add_task(task1)

        task2 = self.schedule.complete_task(task1)
        self.assertEqual(len(self.schedule.tasks), 2)
        self.assertEqual(task2.due_date, self.base_date + timedelta(days=1))

        task3 = self.schedule.complete_task(task2)
        self.assertEqual(len(self.schedule.tasks), 3)
        self.assertEqual(task3.due_date, self.base_date + timedelta(days=2))

        task4 = self.schedule.complete_task(task3)
        self.assertEqual(len(self.schedule.tasks), 4)
        self.assertEqual(task4.due_date, self.base_date + timedelta(days=3))

    def test_recurring_task_preserves_properties(self):
        """New recurring task should preserve name, duration, priority, frequency, and pet."""
        task = Task(
            task_name="Afternoon playtime",
            duration=45,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet,
            due_date=self.base_date
        )
        self.schedule.add_task(task)

        new_task = self.schedule.complete_task(task)

        self.assertEqual(new_task.task_name, task.task_name)
        self.assertEqual(new_task.duration, task.duration)
        self.assertEqual(new_task.priority, task.priority)
        self.assertEqual(new_task.frequency, task.frequency)
        self.assertEqual(new_task.pet, task.pet)
        self.assertEqual(new_task.owner, task.owner)


class TestConflictDetection(unittest.TestCase):
    """Verify scheduling conflicts at duplicate times are detected."""

    def setUp(self):
        self.owner = Owner(name="Alice", available_time=300, pets=[])
        self.pet1 = Pet(name="Buddy", species="Dog", age=3, owner=self.owner)
        self.pet2 = Pet(name="Whiskers", species="Cat", age=2, owner=self.owner)
        self.owner.add_pet(self.pet1)
        self.owner.add_pet(self.pet2)
        self.schedule = Schedule(owner=self.owner, tasks=[])

    def test_detect_conflict_two_tasks_same_time(self):
        """Two tasks at the same time should be detected as a conflict."""
        task1 = Task(
            task_name="Feed Buddy",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet1,
            scheduled_time="09:00"
        )
        task2 = Task(
            task_name="Feed Whiskers",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet2,
            scheduled_time="09:00"
        )
        self.schedule.add_task(task1)
        self.schedule.add_task(task2)

        conflicts = self.schedule.detect_scheduling_conflicts([task1, task2])

        self.assertEqual(len(conflicts), 1)
        self.assertIn("09:00", conflicts[0])
        self.assertIn("Feed Buddy (Buddy)", conflicts[0])
        self.assertIn("Feed Whiskers (Whiskers)", conflicts[0])

    def test_detect_no_conflict_different_times(self):
        """Tasks at different times should not be detected as conflicts."""
        task1 = Task(
            task_name="Feed Buddy",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet1,
            scheduled_time="09:00"
        )
        task2 = Task(
            task_name="Feed Whiskers",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet2,
            scheduled_time="14:00"
        )
        self.schedule.add_task(task1)
        self.schedule.add_task(task2)

        conflicts = self.schedule.detect_scheduling_conflicts([task1, task2])

        self.assertEqual(len(conflicts), 0)

    def test_detect_conflict_three_tasks_same_time(self):
        """Three or more tasks at the same time should all be in conflict message."""
        pet3 = Pet(name="Tweety", species="Bird", age=1, owner=self.owner)
        self.owner.add_pet(pet3)

        task1 = Task(
            task_name="Feed Buddy",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet1,
            scheduled_time="09:00"
        )
        task2 = Task(
            task_name="Feed Whiskers",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet2,
            scheduled_time="09:00"
        )
        task3 = Task(
            task_name="Feed Tweety",
            duration=5,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=pet3,
            scheduled_time="09:00"
        )

        conflicts = self.schedule.detect_scheduling_conflicts([task1, task2, task3])

        self.assertEqual(len(conflicts), 1)
        self.assertIn("Feed Buddy (Buddy)", conflicts[0])
        self.assertIn("Feed Whiskers (Whiskers)", conflicts[0])
        self.assertIn("Feed Tweety (Tweety)", conflicts[0])

    def test_detect_multiple_conflict_times(self):
        """Multiple different times with conflicts should each generate a warning."""
        task1 = Task(
            task_name="Task A",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet1,
            scheduled_time="09:00"
        )
        task2 = Task(
            task_name="Task B",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet2,
            scheduled_time="09:00"
        )
        task3 = Task(
            task_name="Task C",
            duration=10,
            priority="medium",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet1,
            scheduled_time="14:00"
        )
        task4 = Task(
            task_name="Task D",
            duration=10,
            priority="medium",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet2,
            scheduled_time="14:00"
        )

        conflicts = self.schedule.detect_scheduling_conflicts([task1, task2, task3, task4])

        self.assertEqual(len(conflicts), 2)
        self.assertTrue(any("09:00" in c for c in conflicts))
        self.assertTrue(any("14:00" in c for c in conflicts))

    def test_detect_conflict_empty_list(self):
        """Detecting conflicts in an empty list should return empty list."""
        conflicts = self.schedule.detect_scheduling_conflicts([])
        self.assertEqual(len(conflicts), 0)

    def test_detect_conflict_no_scheduled_times(self):
        """Tasks without scheduled_time should not trigger conflicts."""
        task1 = Task(
            task_name="Unscheduled task 1",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet1,
            scheduled_time=None
        )
        task2 = Task(
            task_name="Unscheduled task 2",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet2,
            scheduled_time=None
        )

        conflicts = self.schedule.detect_scheduling_conflicts([task1, task2])

        self.assertEqual(len(conflicts), 0)

    def test_detect_conflict_mixed_scheduled_unscheduled(self):
        """Only scheduled tasks should be checked for conflicts."""
        task1 = Task(
            task_name="Scheduled task",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet1,
            scheduled_time="09:00"
        )
        task2 = Task(
            task_name="Unscheduled task",
            duration=10,
            priority="high",
            frequency="daily",
            completed=False,
            owner=self.owner,
            pet=self.pet2,
            scheduled_time=None
        )

        conflicts = self.schedule.detect_scheduling_conflicts([task1, task2])

        self.assertEqual(len(conflicts), 0)


if __name__ == "__main__":
    unittest.main()
