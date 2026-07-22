# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Core actions:
1. Add owner + pet information
2. Create and edit pet care tasks
3. Generate and view a daily care schedule

For my initial UML design, I will have four classes: Owner, Pet, Task, and Schedule. The Owner class will store the owner's information, such as their name and available time for pet care. The Pet class will store information about the pet, including its name, species, and age. The Task class will represent individual pet care tasks, such as feeding, walking, or meds, along with each task's duration, priority, and completion status. Finally, the Schedule class will organize tasks, generate a daily schedule based on priorities and time constraints, and display the schedule to the user.

Owner: Attributes: name, available_time; Methods: update_info(), set_available_time().

Pet: Attributes: name, species, age; Methods: update_info(), display_info().

Task: Attributes: task_name, duration, priority, completed; Methods: mark_complete(), edit_task().

Schedule: Attributes: tasks, total_time; Methods: add_task(), generate_schedule(), display_schedule().


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, after asking AI to review the skeleton logic, there were some missing relationships. I added bidirectional relationships between Owner, Pet, Task, and Schedule to establish ownership and assignment. Task now knows which pet it's for. Owner tracks their pets. Pet tracks the owner. Schedule references the owner and holds one master task list across all pets. 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

Constraints: The scheduler considers scheduled time (when tasks happen), available time (owner's daily limit), task frequency, and which pet each task is for.

Why time mattered most: I prioritized when tasks are scheduled over their priority level because the owner needs to know what to do when, not just what's important. Available time is checked with warnings rather than blocking, so owners can see if they're overbooked but still choose to proceed.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Tradeoff: Manual Time Scheduling vs. Automatic Conflict Avoidance
 The scheduler requires users to manually specify when each task occurs rather than auto-calculating times. This means users gain control over realistic scheduling but must manage the risk of conflicts themselves as the system detects conflicts with warnings but doesn't prevent them.

Why reasonable: Pet care is tied to the owner's availability and pet routine preferences. Auto-calculated times would ignore actual availability and create schedule that may not be feasible for the owner. Manual scheduling respects real constraints while keeping owner in control.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used Claude throughout the entire project, from initial system design through final UI implementation and refinement. Claude helped me design and translate the UML design into working code by implementing the class logic, then integrating those classes into a functional Streamlit interface. When I encountered issues or bugs Claude helped me debug and refactor the code. I also iterated on features based on user needs, asking Claude to add capabilities like custom available time, task time scheduling, and conflict detection. The most useful interactions were system design questions when creating initial UML and then specific feature requests and bug fixes as the system evolved.

These type of prompts helped:
System design questions ("how should X retrieve data from Y?")
Specific feature requests ("add ability to mark tasks complete after adding")
Error diagnosis ("why isn't the button showing?")
Code refinement ("this logic isn't needed, remove it")


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When Claude suggested adding add_task() and remove_task() methods to the Pet class code, I questioned the design choice. I checked the UML diagram and realized Pet shouldn't manage tasks, Schedule does. The UML showed that tasks are assigned TO pets, not the 
other way around. This makes sense because Schedule needs to see all tasks together to sort by priority, detect conflicts, and generate the overall schedule. Pet is just 
a data model for pet information, not a task manager. This verification helped me catch the mistake and ask Claude to remove the logic.


---

## 4. Testing and Verification

**a. What you tested**
- What behaviors did you test?
- Why were these tests important?

I tested three core behaviors: 
1. sorting (tasks display chronologically by scheduled_time even when added out of order, with edge cases like empty lists and same-time stability)
2. recurrence (completing a daily task creates a next-day instance and weekly creates next-week) 
3. conflict detection (multiple tasks at the same time are flagged with warnings; multiple conflicts at different times handled separately). 

These tests were important because owners need schedules in the correct order to follow them, recurrence automation saves users from manually recreating daily/weekly tasks, and conflict detection prevents impossible double-bookings that would make the schedule unusable.

**b. Confidence**

- How confident are you that your scheduler works correctly? 

Very confident. The core scheduler behaviors such as sorting, recurrence, and conflict detection all have comprehensive test coverage including edge cases.

- What edge cases would you test next if you had more time? 

I would test filtering logic: filter by pet name (case-insensitive), filter by completion status, and filter with both conditions combined.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with the class implementation from UML design to skeleton code to building out the classes and methods. It was really satisfying because the design translated directly into working code and used to implement the UI. I discovered and fixed actual issues during implementation, verified AI suggestions rather than accepting them blindly, and the iterative refinement process made the code better each time. The system actually works and the tests prove it. The full process from design to working, tested code was very satisfying.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would definitely redesign the UI. The schedule is too busy with multiple tabs; I'd consolidate it into one view with filter buttons instead. I'd also add a real-time task progress bar and let users check off tasks directly on the schedule display, instead of in the task list section.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The most important thing I learned is that designing systems with AI is fundamentally iterative. AI likely won't nail it on the first try, and neither will your initial system design and that's okay. I discovered missing relationships during implementation, added features like task frequency and scheduled times as I realized what the scheduler actually needed, and rethought how tasks relate to pets. Rather than trying to perfect the UML upfront, the better approach is to start with the basics, code it, test it, and refine based on what you learn. The design evolves with the implementation. 
