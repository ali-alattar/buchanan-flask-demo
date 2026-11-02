"""Small, deterministic policy derived from the supplied Buchanan assessment.

Points express a prioritisation judgement, never a hiring probability. Keep every
weight here. A missing input is None, not evidence of absence.
"""

from decimal import Decimal, ROUND_HALF_UP


POLICY = {
    "hiring": {
        "label": "Hiring evidence", "weight": 50,
        "factors": {
            "requirement": ("Current hiring requirement", 45),
            "activity": ("Team-specific activity uplift", 20),
            "growth": ("Committed team growth", 15),
            "gap": ("Unfilled replacement gap", 10),
            "timing": ("Confirmed or usable timing", 10),
        },
    },
    "access": {
        "label": "Relationship & access", "weight": 30,
        "factors": {
            "relationship": ("Relevant hiring relationship", 40),
            "route": ("Permitted commercial route", 30),
            "history": ("Relevant delivery history", 20),
            "position": ("Competitive position", 10),
        },
    },
    "delivery": {
        "label": "Candidate readiness", "weight": 20,
        "factors": {
            "supply": ("Engaged, relevant candidates", 45),
            "pay": ("Pay alignment", 25),
            "location": ("Location & qualification fit", 20),
            "availability": ("Availability against timetable", 10),
        },
    },
}
MIN_COMPONENT_COVERAGE = 70


def rounded(value):
    return float(Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def assess(opportunity):
    groups = []
    for key, policy in POLICY.items():
        factors = []
        for factor_id, (label, weight) in policy["factors"].items():
            value, note = opportunity["factors"][key][factor_id]
            if value is not None and not 0 <= value <= 1:
                raise ValueError(f"Invalid factor: {factor_id}")
            factors.append({
                "id": factor_id, "label": label, "weight": weight,
                "value": value, "note": note,
                "lower": rounded(weight * value) if value is not None else 0,
                "upper": rounded(weight * value) if value is not None else weight,
            })
        # No deduction for an unknown. Only independently confirmed contrary
        # pipeline evidence can subtract points; restrictions are a separate gate.
        deduction = opportunity.get("contrary", {}).get("points", 0) if key == "hiring" else 0
        if not 0 <= deduction <= 20:
            raise ValueError("Contrary evidence deduction must be between 0 and 20")
        lower = rounded(max(0, sum(f["lower"] for f in factors) - deduction))
        upper = rounded(max(0, sum(f["upper"] for f in factors) - deduction))
        groups.append({
            "id": key, "label": policy["label"], "weight": policy["weight"],
            "factors": factors, "deduction": deduction,
            "deduction_note": opportunity.get("contrary", {}).get("note") if deduction else None,
            "coverage": sum(f["weight"] for f in factors if f["value"] is not None),
            "lower": lower, "upper": upper,
            "contribution_lower": rounded(lower * policy["weight"] / 100),
            "contribution_upper": rounded(upper * policy["weight"] / 100),
        })
    meaningful = opportunity.get("identity_resolved", True) and all(
        g["coverage"] >= MIN_COMPONENT_COVERAGE for g in groups
    )
    return {
        "groups": groups, "meaningful": meaningful,
        "minimum_coverage": MIN_COMPONENT_COVERAGE,
        "lower": rounded(sum(g["contribution_lower"] for g in groups)),
        "upper": rounded(sum(g["contribution_upper"] for g in groups)),
        "blocked": opportunity.get("restriction") is not None,
    }


def ranked_opportunities(records):
    assessed = [{**record, "assessment": assess(record)} for record in records]
    # A contact restriction takes precedence over every score. Unscored research
    # leads follow assessable opportunities. Stable ID breaks equal-score ties.
    assessed.sort(key=lambda o: (
        o["assessment"]["blocked"], not o["assessment"]["meaningful"],
        -o["assessment"]["lower"] if o["assessment"]["meaningful"] else 0,
        o["id"],
    ))
    return [{**record, "rank": index + 1} for index, record in enumerate(assessed)]


def dashboard_opportunities(records):
    """Expose only fully assessed, scored opportunities that are not on hold.

    Keep the wider research examples intact internally. Filtering at the API
    boundary also keeps their firms, locations and practices out of UI filters.
    """
    eligible = [
        record for record in ranked_opportunities(records)
        if record["assessment"]["meaningful"]
        and not record["assessment"]["blocked"]
        and record["status"] != "paused"
        and all(group["coverage"] == 100 for group in record["assessment"]["groups"])
    ]
    return [{**record, "rank": index + 1} for index, record in enumerate(eligible)]
