# Placeholder rules/optimizer hooks.
# Replace with your real constraints (5/24, issuer spacing, region rules) and OR-Tools optimizer if needed.

def optimize_stack(goals: dict, constraints: dict):
    # Demo: return a simple, deterministic stack for testing
    sequence = [
        {"issuer":"Amex", "card":"Blue Business Plus", "rank":1, "why":"Pairs with business spend; 2x MR"},
        {"issuer":"Chase", "card":"Ink Business Unlimited", "rank":2, "why":"High instant-approval propensity"},
        {"issuer":"Capital One", "card":"Spark Cash Select", "rank":3, "why":"Diversify bureaus; solid SUB"},
        {"issuer":"Citi", "card":"Custom Cash", "rank":4, "why":"Category optimization; beginner-friendly"},
    ]
    total = 180000
    return sequence, total
