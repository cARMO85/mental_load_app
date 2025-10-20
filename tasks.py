from typing import List, Dict
from models import Task

TASKS: list[Task] = [
    Task(
        id="meal_planning",
        name="Meal planning & grocery list",
        pillar="anticipation",
        definition=(
            "By meal planning & prep we mean the *whole* flow — not just cooking, "
            "but deciding what to eat, checking what’s low, building the list, and "
            "sequencing the week so food actually happens."
        ),
        what_counts=[
            "Noticing what’s low / planning the week’s meals",
            "Creating or updating the grocery list / booking delivery/pick-up",
            "Remembering dietary needs, timings, after-school or late-work days",
            "Prepping ahead (marinating, batch cooking) so the week runs",
        ],
        note="Answer for the ‘invisible’ work here (planning/organising); the cooking task itself is separate.",
        example="If one partner mostly plans and manages the list, set Responsibility nearer their side (e.g., 70–90).",
    ),

    Task(
        id="cooking",
        name="Cooking (the visible bit)",
        pillar="identification",
        definition=(
            "This is the *doing* part — cooking the meals. It doesn’t include deciding "
            "what to cook or building the shopping list (covered in Meal planning)."
        ),
        what_counts=[
            "Cooking on weekdays/weekends",
            "Warming/prepping for kids or different mealtimes",
            "Tidying as you go (if part of your norm)",
        ],
        note="If you alternate days, that’s shared — use ~50.",
        example="If one partner cooks most weeknights, Responsibility might sit ~70–80.",
    ),

    Task(
        id="laundry",
        name="Laundry flow",
        pillar="monitoring",
        definition=(
            "Everything from noticing the hamper’s full to finishing clean clothes in drawers. "
            "We’re focusing on the *flow ownership* (who keeps it moving) rather than who folds once."
        ),
        what_counts=[
            "Noticing when to run loads; sorting/whites/darks",
            "Keeping machines cycling; moving wet clothes promptly",
            "Folding/hanging; putting away or delegating it",
            "Remembering school kits/sports days/uniforms",
        ],
        note="If one partner ‘keeps it spinning’ even if others help sometimes, weight toward that person.",
        example="If A notices and runs everything and B folds occasionally, Responsibility ~70–90 to A.",
    ),

    Task(
        id="bills_admin",
        name="Bills & admin",
        pillar="decision",
        definition=(
            "Staying on top of finances and life admin so things don’t lapse or get stressful."
        ),
        what_counts=[
            "Paying rent/mortgage, utilities, subscriptions",
            "Switching providers, renewals, comparisons",
            "Budgeting, expense tracking, filing receipts",
            "Chasing missing refunds/claims",
        ],
        note="Think ‘headspace ownership’ — who ensures this stays under control?",
        example="If one partner runs the calendar, reminders and switches, Responsibility ~70–100.",
    ),

    Task(
        id="kids_school",
        name="Kids: school & activities",
        pillar="monitoring",
        requires_children=True,
        definition=(
            "The orchestration behind school life — not the single pickup, but who keeps the whole system moving."
        ),
        what_counts=[
            "Remembering non-uniform days, forms, trips, fees",
            "Tracking activities, kit, pickups/drop-offs",
            "Parent-teacher communication, emails, portals",
            "Termly planning and handovers",
        ],
        note="If you don’t have kids, this won’t show.",
        example="If one partner is the default ‘school admin’, Responsibility tends to be high (e.g., 80–100).",
    ),

    Task(
        id="appointments_health",
        name="Appointments & health",
        pillar="identification",
        definition=(
            "Booking, tracking and following up on healthcare or essential appointments for the household."
        ),
        what_counts=[
            "Booking GP/dentist/optician; tracking reminders",
            "Booking car service/repairs if you own one",
            "Following up on results, prescriptions, referrals",
            "Keeping the household calendar up to date",
        ],
        note="If one person handles most of the coordination, weight toward them.",
        example="If A books and tracks most appointments, Responsibility ~70–90.",
    ),

    Task(
        id="cleaning",
        name="Cleaning (routine)",
        pillar="identification",
        definition=(
            "Regular cleaning tasks and the *system* behind them (not occasional deep cleans unless that’s your norm)."
        ),
        what_counts=[
            "Weekly surfaces, bathrooms, floors",
            "Small resets (dishes, counters, bins)",
            "Remembering consumables (sponges, sprays, bags)",
            "A loose rota/checklist if you use one",
        ],
        note="If one person sets the standard and nudges others, that’s part of the load.",
        example="If you split weekends but one partner owns the standard, Responsibility ~60–70 to them.",
    ),
]


TASK_LOOKUP: Dict[str, Task] = {t.id: t for t in TASKS}

def get_filtered_tasks(children: int, both_employed: bool) -> List[Task]:
    out: List[Task] = []
    for t in TASKS:
        if t.requires_children and children <= 0:
            continue
        if t.requires_employment and not both_employed:
            continue
        out.append(t)
    return out

def group_by_pillar(tasks: List[Task]) -> Dict[str, List[Task]]:
    d: Dict[str, List[Task]] = {}
    for t in tasks:
        d.setdefault(t.pillar, []).append(t)
    return d