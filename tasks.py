"""
tasks.py

This module defines the full list of household tasks used by the Mental Load Helper.
I've expanded and annotated the task catalogue so it can be filtered by household
context (children, pets, vehicles, employment status) and grouped by pillar.

Do not change task IDs casually — they're used as stable keys in session state and
CSV exports.
"""

from typing import List, Dict
from models import Task

TASKS: list[Task] = [
    # Anticipation pillar — tasks that involve planning and thinking ahead
    
    Task(
        id="meal_planning",
        name="Meal planning & grocery list",
        pillar="anticipation",
        definition=(
            "By meal planning & prep we mean the *whole* flow — not just cooking, "
            "but deciding what to eat, checking what's low, building the list, and "
            "sequencing the week so food actually happens."
        ),
        what_counts=[
            "Noticing what's low / planning the week's meals",
            "Creating or updating the grocery list / booking delivery/pick-up",
            "Remembering dietary needs, timings, after-school or late-work days",
            "Prepping ahead (marinating, batch cooking) so the week runs",
        ],
        note="Answer for the 'invisible' work here (planning/organising); the cooking task itself is separate.",
        example="If one partner mostly plans and manages the list, set Responsibility nearer their side (e.g., 70–90).",
    ),
    
    Task(
        id="household_supplies",
        name="Household supplies & consumables",
        pillar="anticipation",
        definition=(
            "Noticing when household items are running low and ensuring they're restocked before you run out."
        ),
        what_counts=[
            "Tracking toilet paper, cleaning products, toiletries",
            "Noticing when bins need new bags, dishwasher needs tablets",
            "Ordering or buying replacements before they run out",
            "Remembering what brands/types each person prefers",
        ],
        example="If one partner notices and orders everything, Responsibility ~80-100 to them.",
    ),
    
    Task(
    id="holiday_planning",
    name="Holiday & vacation planning",
    pillar="anticipation",
    definition=(
        "Planning family holidays and vacations - researching, booking, and coordinating all the details."
    ),
    what_counts=[
        "Researching holiday destinations and accommodation",
        "Booking flights, hotels, activities",
        "Planning itineraries and packing lists",
        "Coordinating time off work and school holidays",
        "Managing travel documents (passports, visas, insurance)",
    ],
    example="If one partner does most of the holiday research and booking, Responsibility ~80-100.",
),

    
    Task(
        id="birthday_gifts",
        name="Gifts, cards & social obligations",
        pillar="anticipation",
        definition=(
            "Remembering birthdays, anniversaries, and social occasions, and organising cards, gifts, or RSVPs."
        ),
        what_counts=[
            "Remembering family/friends' birthdays and important dates",
            "Choosing, buying, wrapping gifts",
            "Sending cards or organising celebrations",
            "Tracking RSVPs and social commitments",
        ],
        example="If one partner manages the family calendar of social obligations, Responsibility ~70-100.",
    ),
    
    Task(
        id="seasonal_prep",
        name="Seasonal & future planning",
        pillar="anticipation",
        definition=(
            "Thinking ahead to seasonal needs, holidays, and future household requirements."
        ),
        what_counts=[
            "Planning for holidays, school breaks, seasons changing",
            "Preparing for birthdays, Christmas, summer holidays",
            "Anticipating when kids need new clothes/shoes/school supplies",
            "Thinking ahead about home repairs or maintenance",
        ],
        example="If one partner does most of the forward-thinking, Responsibility ~70-90.",
    ),
    
    # Identification pillar — visible tasks and noticing what needs doing
    
    Task(
        id="cooking",
        name="Cooking (the visible bit)",
        pillar="identification",
        definition=(
            "This is the *doing* part — cooking the meals. It doesn't include deciding "
            "what to cook or building the shopping list (covered in Meal planning)."
        ),
        what_counts=[
            "Cooking on weekdays/weekends",
            "Warming/prepping for kids or different mealtimes",
            "Tidying as you go (if part of your norm)",
        ],
        note="If you alternate days, that's shared — use ~50.",
        example="If one partner cooks most weeknights, Responsibility might sit ~70–80.",
    ),
    
    Task(
        id="cleaning",
        name="Cleaning (routine)",
        pillar="identification",
        definition=(
            "Regular cleaning tasks and the *system* behind them (not occasional deep cleans unless that's your norm)."
        ),
        what_counts=[
            "Weekly surfaces, bathrooms, floors",
            "Small resets (dishes, counters, bins)",
            "Remembering consumables (sponges, sprays, bags)",
            "A loose rota/checklist if you use one",
        ],
        note="If one person sets the standard and nudges others, that's part of the load.",
        example="If you split weekends but one partner owns the standard, Responsibility ~60–70 to them.",
    ),
    
    Task(
        id="tidying",
        name="Tidying & decluttering",
        pillar="identification",
        definition=(
            "Noticing mess, clutter, and items out of place, and putting things back where they belong."
        ),
        what_counts=[
            "Picking up clothes, toys, items left around",
            "Putting things back in their proper places",
            "Decluttering surfaces and common areas",
            "Organising storage and cupboards",
        ],
        example="If one partner is constantly tidying up after everyone, Responsibility ~70-100.",
    ),
    
    Task(
        id="laundry",
        name="Laundry flow",
        pillar="identification",
        definition=(
            "Everything from noticing the hamper's full to finishing clean clothes in drawers. "
            "We're focusing on the *flow ownership* (who keeps it moving) rather than who folds once."
        ),
        what_counts=[
            "Noticing when to run loads; sorting/whites/darks",
            "Keeping machines cycling; moving wet clothes promptly",
            "Folding/hanging; putting away or delegating it",
            "Remembering school kits/sports days/uniforms",
        ],
        note="If one partner 'keeps it spinning' even if others help sometimes, weight toward that person.",
        example="If A notices and runs everything and B folds occasionally, Responsibility ~70–90 to A.",
    ),
    
    Task(
        id="home_maintenance",
        name="Home repairs & maintenance",
        pillar="identification",
        definition=(
            "Noticing when things break or need maintenance, and organising repairs or fixes."
        ),
        what_counts=[
            "Spotting broken items, leaks, things that need fixing",
            "Calling repair people, getting quotes",
            "Scheduling and coordinating home maintenance",
            "DIY repairs or organising someone to do them",
        ],
        example="If one partner notices and coordinates all repairs, Responsibility ~80-100.",
    ),
    Task(
    id="pet_care",
    name="Pet care & management",
    pillar="identification",
    requires_pets=True,  # conditional flag: only include when household has pets
    definition=(
        "Daily pet care and the mental load of remembering vet appointments, food, medication, and pet needs."
    ),
    what_counts=[
        "Feeding, walking, grooming pets",
        "Remembering vet appointments and vaccinations",
        "Noticing when pet food or supplies are running low",
        "Coordinating pet care when away from home",
        "Managing pet health issues and medication",
    ],
    example="If one partner manages all pet schedules and needs, Responsibility ~80-100.",
),
    # Decision pillar — tasks that require choosing, organising or deciding
    
    Task(
        id="bills_admin",
        name="Bills & admin",
        pillar="decision",
        definition=(
            "Staying on top of finances and life admin so things don't lapse or get stressful."
        ),
        what_counts=[
            "Paying rent/mortgage, utilities, subscriptions",
            "Switching providers, renewals, comparisons",
            "Budgeting, expense tracking, filing receipts",
            "Chasing missing refunds/claims",
        ],
        note="Think 'headspace ownership' — who ensures this stays under control?",
        example="If one partner runs the calendar, reminders and switches, Responsibility ~70–100.",
    ),
    
    Task(
        id="appointments_health",
        name="Appointments & health",
        pillar="decision",
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
        id="social_calendar",
        name="Social calendar & coordination",
        pillar="decision",
        definition=(
            "Managing the household's social life, coordinating schedules, and making social plans."
        ),
        what_counts=[
            "Coordinating family/couple social plans",
            "Managing conflicting schedules between household members",
            "Deciding on weekend plans or activities",
            "Organising when to see friends and family",
        ],
        example="If one partner coordinates most social planning, Responsibility ~70-90.",
    ),
    
    Task(
        id="kids_activities",
        name="Children's activities & hobbies",
        pillar="decision",
        requires_children=True,
        definition=(
            "Researching, choosing, and enrolling children in activities, hobbies, and clubs."
        ),
        what_counts=[
            "Researching options for activities/clubs/sports",
            "Deciding what children should participate in",
            "Enrolling and managing registrations",
            "Coordinating schedules and transport",
        ],
        example="If one partner researches and enrolls children in activities, Responsibility ~80-100.",
    ),
    Task(
    id="tech_troubleshooting",
    name="Tech support & troubleshooting",
    pillar="decision",
    definition=(
        "Being the household tech support - fixing issues, managing devices, and keeping digital life running."
    ),
    what_counts=[
        "Fixing wifi/computer/phone problems",
        "Managing subscriptions and accounts (Netflix, utilities apps, etc.)",
        "Setting up new devices and software",
        "Troubleshooting when tech doesn't work",
        "Managing passwords, security, backups",
        "Being the person everyone asks when tech breaks",
    ],
    note="This is executive function work - requires problem-solving and staying calm under pressure.",
    example="If one partner is the default tech troubleshooter, Responsibility ~70-100.",
),
    # Monitoring pillar — keeping track, following up, and coordinating
    
    Task(
        id="kids_school",
        name="Children: school & schoolwork",
        pillar="monitoring",
        requires_children=True,
        definition=(
            "The orchestration behind school life — not the single pickup, but who keeps the whole system moving."
        ),
        what_counts=[
            "Remembering non-uniform days, forms, trips, fees",
            "Tracking homework and school projects",
            "Parent-teacher communication, emails, portals",
            "Monitoring children's academic progress",
        ],
        note="If you don't have children, this won't show.",
        example="If one partner is the default 'school admin', Responsibility tends to be high (e.g., 80–100).",
    ),
    
    Task(
        id="kids_health",
        name="Children's health & development",
        pillar="monitoring",
        requires_children=True,
        definition=(
            "Tracking children's health, development milestones, and medical needs."
        ),
        what_counts=[
            "Booking and attending children's health appointments",
            "Tracking vaccinations and health records",
            "Monitoring developmental milestones",
            "Noticing if children seem unwell or struggling",
        ],
        example="If one partner monitors and coordinates children's health, Responsibility ~80-100.",
    ),
    
    Task(
        id="household_calendar",
        name="Household calendar & coordination",
        pillar="monitoring",
        definition=(
            "Being the keeper of the family schedule and ensuring everyone knows where they need to be."
        ),
        what_counts=[
            "Maintaining the shared calendar",
            "Reminding others about upcoming appointments/events",
            "Coordinating who's picking up kids, who's cooking, etc.",
            "Ensuring conflicting commitments are resolved",
        ],
        example="If one partner is the 'calendar keeper', Responsibility ~80-100.",
    ),
    
    Task(
        id="food_waste",
        name="Food waste & leftovers",
        pillar="monitoring",
        definition=(
            "Tracking what food is in the fridge, using up leftovers, and preventing waste."
        ),
        what_counts=[
            "Checking what's in the fridge before it goes off",
            "Planning meals around leftovers",
            "Remembering to use ingredients before they expire",
            "Managing food storage and organisation",
        ],
        example="If one partner always knows what's in the fridge, Responsibility ~70-90.",
    ),
    
    Task(
        id="work_life_coordination",
        name="Work-life coordination",
        pillar="monitoring",
        requires_employment=True,
        definition=(
            "Managing the household around work schedules and coordinating when conflicts arise."
        ),
        what_counts=[
            "Tracking both partners' work schedules",
            "Adjusting household plans around work commitments",
            "Coordinating childcare/pickups when work runs late",
            "Managing household when one partner travels for work",
        ],
        example="If one partner does most of the 'work schedule tetris', Responsibility ~70-90.",
    ),
    Task(
    id="vehicle_maintenance",
    name="Car/vehicle maintenance",
    pillar="monitoring",
    requires_vehicle=True,  # conditional flag: only include when household has a vehicle
    definition=(
        "Tracking car servicing, MOT, insurance, and ensuring the vehicle stays roadworthy."
    ),
    what_counts=[
        "Remembering MOT and service due dates",
        "Booking and arranging car maintenance",
        "Managing car insurance renewals",
        "Noticing when car needs attention (tyres, fluids, issues)",
        "Coordinating repairs and dealing with mechanics",
    ],
    example="If one partner tracks and arranges all vehicle maintenance, Responsibility ~80-100.",
),

    # Emotional pillar — the emotional and relational work that keeps a home well
    
    Task(
        id="kids_emotional",
        name="Children's emotional wellbeing",
        pillar="emotional",
        requires_children=True,
        definition=(
            "Noticing and responding to children's emotional needs, worries, and struggles."
        ),
        what_counts=[
            "Checking in with children about their feelings",
            "Noticing when children seem upset or struggling",
            "Providing emotional support and reassurance",
            "Managing bedtime routines, soothing upsets",
        ],
        example="If one partner does most emotional check-ins, Responsibility ~80-100.",
    ),
    
    Task(
        id="relationship_maintenance",
        name="Relationship maintenance",
        pillar="emotional",
        definition=(
            "The work of maintaining your relationship - planning couple time, checking in emotionally."
        ),
        what_counts=[
            "Suggesting date nights or couple time",
            "Initiating conversations about the relationship",
            "Noticing when the relationship needs attention",
            "Remembering anniversaries and special occasions",
        ],
        example="If one partner usually suggests couple time, Responsibility ~70-90.",
    ),
    
    Task(
        id="family_relationships",
        name="Extended family relationships",
        pillar="emotional",
        definition=(
            "Managing relationships with extended family - remembering to call, organising visits, managing expectations."
        ),
        what_counts=[
            "Remembering to call/message parents, in-laws, relatives",
            "Organising family visits and gatherings",
            "Managing family expectations and conflicts",
            "Keeping family members updated on household news",
        ],
        example="If one partner manages most family communications, Responsibility ~80-100.",
    ),
    
    Task(
        id="household_mood",
        name="Household mood & atmosphere",
        pillar="emotional",
        definition=(
            "Managing the emotional atmosphere of the home - smoothing conflicts, creating positive moments."
        ),
        what_counts=[
            "Noticing when household tension is high",
            "Mediating conflicts between household members",
            "Creating positive moments (family activities, treats)",
            "Being the 'emotional thermostat' of the home",
        ],
        example="If one partner is the emotional manager, Responsibility ~80-100.",
    ),
    
    Task(
        id="partner_support",
        name="Partner emotional support",
        pillar="emotional",
        definition=(
            "Providing emotional support to your partner - listening, remembering their needs, checking in."
        ),
        what_counts=[
            "Remembering what's stressing your partner",
            "Asking how their day/work/life is going",
            "Providing emotional support and encouragement",
            "Noticing when your partner needs extra support",
        ],
        example="If one partner does most emotional checking-in, Responsibility ~70-90.",
    ),
]


TASK_LOOKUP: Dict[str, Task] = {t.id: t for t in TASKS}

def get_filtered_tasks(children: int, both_employed: bool, has_pets: bool, has_vehicle: bool) -> List[Task]:
    """
    Filter tasks based on household context.
    
    Args:
        children: Number of children
        both_employed: Whether both partners are employed
        has_pets: Whether household has pets
        has_vehicle: Whether household has a car/vehicle
    """
    out: List[Task] = []
    for t in TASKS:
        # Skip child-related tasks if no children
        if t.requires_children and children <= 0:
            continue
        # Skip employment tasks if not both employed
        if t.requires_employment and not both_employed:
            continue
        # Skip pet tasks if no pets
        if t.requires_pets and not has_pets:
            continue
        # Skip vehicle tasks if no vehicle
        if t.requires_vehicle and not has_vehicle:
            continue
        out.append(t)
    return out


def group_by_pillar(tasks: List[Task]) -> Dict[str, List[Task]]:
    d: Dict[str, List[Task]] = {}
    for t in tasks:
        d.setdefault(t.pillar, []).append(t)
    return d