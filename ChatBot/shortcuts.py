from dataclasses import dataclass

@dataclass
class ShortcutDefinition:
    trigger: str
    expansion: str
    temperature: float
    max_tokens: int

SHORTCUT_REGISTRY = {
    "/budget": ShortcutDefinition(
        trigger="budget",
        expansion="""
Estimate travel budget for this destination.
Include:
- low budget
- medium budget
- luxury budget
- hotel costs
- food costs
- transportation costs
""",
        temperature=0.3,
        max_tokens=500
    ),

    "/weather": ShortcutDefinition(
        trigger="weather",
        expansion="""
Analyze destination weather.
Include:
- expected temperature
- clothing advice
- packing suggestions
""",
        temperature=0.3,
        max_tokens=400
    ),

    "/places": ShortcutDefinition(
        trigger="places",
        expansion="""
Recommend top tourist attractions.
Include:
- famous landmarks
- hidden gems
- best visit times
""",
        temperature=0.5,
        max_tokens=700
    ),

    "/hotel": ShortcutDefinition(
        trigger="hotel",
        expansion="""
Recommend hotels by budget level.
Include:
- budget stay
- medium stay
- luxury stay
""",
        temperature=0.4,
        max_tokens=600
    ),

    "/plan": ShortcutDefinition(
        trigger="plan",
        expansion="""
Create a complete travel itinerary.
Include:
- daily schedule
- attractions
- transportation suggestions
- estimated costs
""",
        temperature=0.6,
        max_tokens=1200
    )
}