"""
WelfareAI - Predictive Personnel Stress & Welfare Assessment Engine
Designed for Uniformed Forces (Armed Forces, CAPF, State Police).

NOTE: Prototype risk assessment model for operational welfare and fatigue monitoring.
DOES NOT provide medical diagnosis or psychiatric clinical evaluation.
"""

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class AssessmentResult:
    risk_level: str              # "Low", "Moderate", "High"
    risk_color: str              # Hex color or badge string
    risk_badge: str              # Emoji + label
    welfare_index: int           # 0 to 100 (Higher = healthier welfare)
    stress_score: float          # 0.0 to 10.0 calculated risk load
    primary_factors: List[str]   # Explanation bullet points
    factor_breakdown: Dict[str, float]  # Numerical breakdown (0-100 scale for charts)
    recommendations: Dict[str, List[Dict[str, str]]] # Grouped actionable advice
    disclaimer: str

def evaluate_welfare_status(
    sleep_hours: float,
    duty_hours: float,
    workload: int,
    night_duty_count: int,
    rest_days: int,
    stress_level: int
) -> AssessmentResult:
    """
    Evaluates personnel operational inputs and produces an explainable
    welfare & stress risk assessment.
    """
    # 1. Individual Factor Scoring (0 to 100 where 100 represents severe fatigue/stress)
    
    # Sleep Deficit: Optimal is 7-8 hrs. Below 5 is critical.
    if sleep_hours >= 7.5:
        sleep_factor = max(5.0, (8.0 - sleep_hours) * 10)
    elif sleep_hours >= 6.0:
        sleep_factor = 25.0 + (7.5 - sleep_hours) * 20
    elif sleep_hours >= 4.5:
        sleep_factor = 55.0 + (6.0 - sleep_hours) * 25
    else:
        sleep_factor = min(100.0, 85.0 + (4.5 - sleep_hours) * 10)

    # Duty Overload: Normal duty is 8 hrs. >12 hrs causes acute fatigue. >16 hrs is extreme.
    if duty_hours <= 8:
        duty_factor = max(5.0, (duty_hours / 8.0) * 25.0)
    elif duty_hours <= 12:
        duty_factor = 25.0 + ((duty_hours - 8) / 4.0) * 35.0
    elif duty_hours <= 16:
        duty_factor = 60.0 + ((duty_hours - 12) / 4.0) * 25.0
    else:
        duty_factor = min(100.0, 85.0 + ((duty_hours - 16) / 8.0) * 15.0)

    # Circadian Strain (Night duties in past 30 days): Normal <= 3. Heavy > 8. Critical > 12.
    if night_duty_count <= 3:
        night_factor = max(5.0, night_duty_count * 8.0)
    elif night_duty_count <= 7:
        night_factor = 25.0 + (night_duty_count - 3) * 10.0
    elif night_duty_count <= 12:
        night_factor = 65.0 + (night_duty_count - 7) * 5.0
    else:
        night_factor = min(100.0, 90.0 + (night_duty_count - 12) * 1.5)

    # Recovery Deficit (Rest days in past 30 days): Standard ~6-8 days. <4 is severe fatigue risk.
    if rest_days >= 8:
        recovery_factor = 10.0
    elif rest_days >= 5:
        recovery_factor = 25.0 + (8 - rest_days) * 10.0
    elif rest_days >= 2:
        recovery_factor = 55.0 + (5 - rest_days) * 15.0
    else:
        recovery_factor = min(100.0, 85.0 + (2 - rest_days) * 15.0)

    # Workload Intensity & Perceived Stress
    workload_factor = (workload / 10.0) * 100.0
    stress_factor = (stress_level / 10.0) * 100.0

    # 2. Weighted Aggregation (Operational Biometric Model)
    w_sleep = 0.25
    w_duty = 0.22
    w_workload = 0.18
    w_night = 0.15
    w_recovery = 0.10
    w_stress = 0.10

    composite_stress_index = (
        (sleep_factor * w_sleep) +
        (duty_factor * w_duty) +
        (workload_factor * w_workload) +
        (night_factor * w_night) +
        (recovery_factor * w_recovery) +
        (stress_factor * w_stress)
    )

    # Convert to 0 - 10 scale for convenience
    calculated_stress_score = round(composite_stress_index / 10.0, 1)
    
    # Welfare Operational Index (100 is optimum well-being, 0 is depleted)
    welfare_index = int(max(5, min(100, 100 - composite_stress_index)))

    # 3. Categorization into Low, Moderate, or High
    # Incorporates the prototype baseline heuristics plus composite logic
    is_high = (
        composite_stress_index >= 68 or
        stress_level >= 8 or
        (sleep_hours < 5.0 and workload >= 8) or
        (duty_hours >= 14 and sleep_hours < 5.5) or
        (night_duty_count >= 12 and rest_days <= 3)
    )
    is_moderate = (
        composite_stress_index >= 40 or
        stress_level >= 5 or
        sleep_hours < 6.0 or
        duty_hours >= 11 or
        workload >= 7 or
        night_duty_count >= 6
    )

    if is_high:
        risk_level = "High"
        risk_color = "#EF4444"
        risk_badge = "🔴 HIGH RISK"
    elif is_moderate:
        risk_level = "Moderate"
        risk_color = "#F59E0B"
        risk_badge = "🟡 MODERATE RISK"
    else:
        risk_level = "Low"
        risk_color = "#10B981"
        risk_badge = "🟢 LOW RISK"

    # 4. Explainability Engine: Identify Primary Risk Drivers
    factors = []
    if sleep_hours < 5.0:
        factors.append(f"Severe Sleep Deficit: Only {sleep_hours:.1f} hrs of rest (recommended 7-8 hrs for operational alertness).")
    elif sleep_hours < 6.0:
        factors.append(f"Borderline Sleep Duration: {sleep_hours:.1f} hrs of sleep increases reaction-time latency.")

    if duty_hours >= 13:
        factors.append(f"Extended Duty Exposure: {duty_hours} hrs exceeds optimal consecutive operational endurance thresholds.")
    elif duty_hours >= 10:
        factors.append(f"Prolonged Duty Shift: {duty_hours} hrs active duty requiring structured recovery.")

    if workload >= 8:
        factors.append(f"Elevated Workload Intensity: Self-rated workload at {workload}/10 signals elevated cognitive demands.")

    if night_duty_count >= 8:
        factors.append(f"High Circadian Disruption: {night_duty_count} night shifts in 30 days induces chronic sleep phase fatigue.")
    elif night_duty_count >= 5:
        factors.append(f"Moderate Night Shift Load: {night_duty_count} night duties requiring circadian adaptation.")

    if rest_days <= 3:
        factors.append(f"Acute Recovery Deficit: Only {rest_days} rest days in the last month limits physiological recuperation.")

    if stress_level >= 7:
        factors.append(f"High Perceived Stress: Self-reported stress level is {stress_level}/10.")

    if not factors:
        factors.append("Optimal Balance: Sleep, duty duration, and rest day ratios are within healthy operational standards.")

    # 5. Personalized Tailored Recommendations
    recs = {
        "rest": [],
        "workload": [],
        "hydration": [],
        "support": []
    }

    if risk_level == "High":
        recs["rest"].append({
            "title": "Mandatory Recovery Window",
            "desc": "Initiate an unbroken 7-8 hour sleep cycle before the next operational mobilization. Avoid digital screens 45 mins prior to rest."
        })
        recs["rest"].append({
            "title": "20-Minute Tactical Power Nap",
            "desc": "If currently on operational standby, utilize a 20-minute power nap to restore cognitive vigilance."
        })
        recs["workload"].append({
            "title": "Shift Rotation & Duty Reallocation",
            "desc": "Request temporary rotation off continuous night patrols or intense field postings to a stabilizing daytime duty."
        })
        recs["workload"].append({
            "title": "Task Prioritization",
            "desc": "Delegate non-critical administrative duties and focus purely on essential operational directives."
        })
        recs["hydration"].append({
            "title": "Targeted Electrolyte & Fluid Intake",
            "desc": "Target 3.5+ liters of water with oral electrolytes, especially during outdoor patrol duties. Cut caffeine 5 hrs before sleep."
        })
        recs["support"].append({
            "title": "Tactical Box Breathing (4-4-4-4)",
            "desc": "Practice 4 cycles: Inhale 4s, Hold 4s, Exhale 4s, Hold 4s to rapidly calm sympathetic nervous system arousal."
        })
        recs["support"].append({
            "title": "Confidential Peer Welfare Check",
            "desc": "Connect with your designated unit Welfare Officer or peer counselor for proactive debriefing and support."
        })
    elif risk_level == "Moderate":
        recs["rest"].append({
            "title": "Sleep Hygiene Optimization",
            "desc": "Aim for an additional 60-90 minutes of sleep tonight in a dark, cool barracks/quarters environment."
        })
        recs["workload"].append({
            "title": "Pacing & Structured Micro-Breaks",
            "desc": "Incorporate 5-minute physical decompression breaks every 2 hours of stationary or high-focus duty."
        })
        recs["hydration"].append({
            "title": "Hydration Maintenance",
            "desc": "Maintain 2.5 to 3 liters of water intake. Replace energy drinks with natural hydration to prevent energy crashes."
        })
        recs["support"].append({
            "title": "De-escalation & Mental Reset",
            "desc": "Engage in light stretching or a 10-minute quiet walk post-shift to transition out of duty mode."
        })
    else: # Low Risk
        recs["rest"].append({
            "title": "Maintain Consistent Sleep Cycle",
            "desc": "Keep regular sleep and wake times to preserve circadian rhythm resilience for unpredictable duty calls."
        })
        recs["workload"].append({
            "title": "Sustained Operational Readiness",
            "desc": "Workload and fatigue levels are balanced. Continue standard duty pacing and team coordination."
        })
        recs["hydration"].append({
            "title": "Consistent Hydration",
            "desc": "Continue healthy baseline fluid intake (2.5 - 3.0 L/day) and balanced mess nutrition."
        })
        recs["support"].append({
            "title": "Peer Welfare Buddy Support",
            "desc": "You are in a resilient state. Check in on squad mates who may be on heavy night shifts or extended duties."
        })

    factor_breakdown = {
        "Sleep Deficit": round(sleep_factor, 1),
        "Duty Load": round(duty_factor, 1),
        "Workload Pressure": round(workload_factor, 1),
        "Circadian Strain": round(night_factor, 1),
        "Recovery Deficit": round(recovery_factor, 1),
        "Perceived Stress": round(stress_factor, 1)
    }

    disclaimer = (
        "PROTOTYPE RISK ASSESSMENT ONLY: WelfareAI provides an operational fatigue and stress risk assessment "
        "designed solely for personnel welfare and preventive duty management. This assessment is NOT a medical, "
        "clinical, or psychiatric diagnosis, and must not be used for disciplinary actions."
    )

    return AssessmentResult(
        risk_level=risk_level,
        risk_color=risk_color,
        risk_badge=risk_badge,
        welfare_index=welfare_index,
        stress_score=calculated_stress_score,
        primary_factors=factors,
        factor_breakdown=factor_breakdown,
        recommendations=recs,
        disclaimer=disclaimer
    )
