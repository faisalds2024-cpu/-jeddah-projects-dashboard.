import json
import math
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


SEED = 42
TODAY = date(2026, 9, 3)
DATA_DIR = Path("data")

random.seed(SEED)
np.random.seed(SEED)


SECTOR_CONFIG = {
    "Roads & Transportation": {"count": 32, "value": (35_000_000, 800_000_000)},
    "Urban Development": {"count": 26, "value": (25_000_000, 650_000_000)},
    "Buildings": {"count": 22, "value": (8_000_000, 220_000_000)},
    "Stormwater & Drainage": {"count": 20, "value": (20_000_000, 500_000_000)},
    "Utilities": {"count": 16, "value": (12_000_000, 280_000_000)},
    "Public Facilities": {"count": 14, "value": (6_000_000, 180_000_000)},
    "Parks & Landscaping": {"count": 10, "value": (4_000_000, 110_000_000)},
    "Street Lighting": {"count": 10, "value": (3_000_000, 90_000_000)},
}

DISTRICTS = {
    "Al Safa": (21.567, 39.184),
    "Al Zahra": (21.596, 39.141),
    "Al Rawdah": (21.567, 39.155),
    "Al Hamra": (21.533, 39.168),
    "Al Salamah": (21.609, 39.161),
    "Al Naeem": (21.646, 39.168),
    "Al Marwah": (21.617, 39.214),
    "Al Rehab": (21.541, 39.226),
    "Al Faisaliyah": (21.574, 39.203),
    "Al Bawadi": (21.596, 39.185),
    "Al Aziziyah": (21.542, 39.240),
    "Al Naseem": (21.521, 39.258),
    "Al Rawabi": (21.498, 39.235),
    "Al Andalus": (21.556, 39.147),
    "Al Shati": (21.637, 39.108),
    "Al Basateen": (21.665, 39.120),
    "Al Muhammadiyah": (21.673, 39.112),
    "Obhur": (21.742, 39.120),
    "Al Hamdaniyah": (21.786, 39.210),
    "Al Manar": (21.553, 39.256),
    "Al Waha": (21.594, 39.228),
    "Al Rabwah": (21.561, 39.214),
    "Al Samer": (21.589, 39.232),
    "Al Ajwad": (21.640, 39.244),
    "Al Kandarah": (21.500, 39.185),
    "Al Balad": (21.485, 39.186),
    "Al Ruwais": (21.519, 39.169),
    "Al Thaghr": (21.469, 39.241),
    "Al Jamiah": (21.474, 39.227),
    "Al Sanabel": (21.397, 39.262),
    "Prince Fawaz": (21.417, 39.246),
    "Al Baghdadiyah": (21.507, 39.176),
    "Mishrifah": (21.547, 39.197),
    "Al Khalidiyah": (21.561, 39.142),
    "Al Rowais": (21.515, 39.172),
}

CONTRACTORS = [
    ("CONT-001", "Red Sea Infrastructure Ltd.", "excellent", 11),
    ("CONT-002", "Al Binaa Contracting Co.", "good", 10),
    ("CONT-003", "Horizon Construction Group", "excellent", 9),
    ("CONT-004", "Jeddah Urban Works Co.", "mixed", 9),
    ("CONT-005", "Arabian Development Contractors", "good", 8),
    ("CONT-006", "Gulf Engineering & Construction", "mixed", 8),
    ("CONT-007", "Western Projects Company", "weak", 7),
    ("CONT-008", "Al Manar Contracting", "good", 7),
    ("CONT-009", "Future Cities Construction", "excellent", 7),
    ("CONT-010", "Saudi Infrastructure Solutions", "good", 7),
    ("CONT-011", "Corniche Civil Works", "weak", 6),
    ("CONT-012", "Madar Utilities & Build", "mixed", 6),
    ("CONT-013", "Blue Horizon Contractors", "good", 6),
    ("CONT-014", "Desert Line Projects", "weak", 5),
    ("CONT-015", "Alpha Core Construction", "excellent", 5),
    ("CONT-016", "Nesma Urban Contracting", "good", 5),
    ("CONT-017", "Vision Axis Developments", "mixed", 5),
    ("CONT-018", "First Route Engineering", "good", 5),
    ("CONT-019", "Modern Grid Contracting", "weak", 4),
    ("CONT-020", "Prime Gulf Builders", "mixed", 4),
]

PROJECT_MANAGERS = [
    ("PM-001", "Ahmed Alharbi", 15),
    ("PM-002", "Mohammed Alqahtani", 13),
    ("PM-003", "Fahad Alghamdi", 12),
    ("PM-004", "Abdullah Alzahrani", 11),
    ("PM-005", "Khalid Alotaibi", 10),
    ("PM-006", "Saad Alshammari", 10),
    ("PM-007", "Yousef Alsubaie", 9),
    ("PM-008", "Omar Alshehri", 9),
    ("PM-009", "Turki Almutairi", 8),
    ("PM-010", "Bander Alghamdi", 8),
    ("PM-011", "Nawaf Alqahtani", 8),
    ("PM-012", "Majed Alharbi", 7),
    ("PM-013", "Hassan Alzahrani", 7),
    ("PM-014", "Tariq Alotaibi", 7),
]

NOTES_POOL = [
    "",
    "",
    "",
    "Awaiting utility relocation approval.",
    "Additional manpower assigned to recover schedule.",
    "Design revision under review.",
    "Project progressing according to plan.",
    "Contractor submitted recovery plan.",
    "Variation order under evaluation.",
    "Procurement of long-lead items in progress.",
    "Coordination ongoing with traffic management authority.",
    "Final handover documentation under preparation.",
]

NAME_PARTS = {
    "Roads & Transportation": [
        "Road Improvement", "Intersection Upgrade", "Corridor Enhancement",
        "Bridge Rehabilitation", "Mobility Improvement", "Traffic Flow Optimization",
        "Road Widening", "Transport Link Upgrade", "Access Road Development",
    ],
    "Urban Development": [
        "Urban Regeneration", "District Revitalization", "Waterfront Enhancement",
        "Mixed-Use Infrastructure Development", "Public Realm Improvement",
        "Boulevard Development", "Urban Gateway Upgrade", "Neighborhood Renewal",
    ],
    "Buildings": [
        "Municipal Building Renovation", "Administrative Complex Development",
        "Community Center Construction", "Operations Facility Expansion",
        "Service Center Upgrade", "Public Building Rehabilitation",
    ],
    "Stormwater & Drainage": [
        "Stormwater Drainage Upgrade", "Flood Mitigation Program",
        "Drainage Network Expansion", "Water Channel Rehabilitation",
        "Runoff Management Improvement", "Drainage Capacity Enhancement",
    ],
    "Parks & Landscaping": [
        "Public Park Development", "Landscape Enhancement", "Green Corridor Development",
        "Open Space Rehabilitation", "Boulevard Landscaping Project",
    ],
    "Utilities": [
        "Utility Network Upgrade", "Water & Sewer Infrastructure Renewal",
        "Substation Access Improvement", "Distribution Network Enhancement",
        "Service Diversion Project", "Underground Utility Development",
    ],
    "Street Lighting": [
        "Street Lighting Upgrade", "LED Lighting Retrofit",
        "Boulevard Lighting Enhancement", "Pedestrian Lighting Improvement",
        "Smart Lighting Deployment",
    ],
    "Public Facilities": [
        "Public Facilities Upgrade", "Neighborhood Services Improvement",
        "Civic Amenities Development", "Sports Facility Rehabilitation",
        "Emergency Services Facility Enhancement",
    ],
}

AREA_PREFIXES = [
    "Northern Jeddah", "Southern Jeddah", "Eastern Jeddah", "Western Jeddah",
    "Central Jeddah", "Corniche", "Airport District", "Obhur", "Al Balad",
    "King Abdulaziz Road", "Prince Majed Corridor", "Haramain Gateway",
]


@dataclass
class ContractorProfile:
    contractor_id: str
    name: str
    profile: str
    project_slots: int


def weighted_pick(items):
    expanded = []
    for entry in items:
        expanded.extend([entry[0]] * entry[1])
    return expanded


CONTRACTOR_POOL = weighted_pick([(ContractorProfile(*c), c[3]) for c in CONTRACTORS])
PM_POOL = weighted_pick([((pm_id, pm_name), weight) for pm_id, pm_name, weight in PROJECT_MANAGERS])


def clamp(value, low, high):
    return max(low, min(high, value))


def format_date(value):
    if value is None:
        return ""
    return value.isoformat()


def money(value):
    return int(round(value, 0))


def generate_project_names():
    names = []
    seen = set()
    sector_list = []
    for sector, cfg in SECTOR_CONFIG.items():
        sector_list.extend([sector] * cfg["count"])
    district_names = list(DISTRICTS.keys())
    random.shuffle(district_names)
    district_idx = 0
    area_idx = 0

    for sector in sector_list:
        while True:
            area = AREA_PREFIXES[area_idx % len(AREA_PREFIXES)]
            district = district_names[district_idx % len(district_names)]
            suffix = random.choice(NAME_PARTS[sector])
            name = f"{area} {district} {suffix}"
            area_idx += 1
            district_idx += random.randint(1, 3)
            if name not in seen:
                seen.add(name)
                names.append((sector, name))
                break
    return names


def pick_status_buckets():
    statuses = (
        ["Completed"] * 27
        + ["In Progress"] * 75
        + ["Delayed"] * 25
        + ["On Hold"] * 10
        + ["Not Started"] * 13
    )
    random.shuffle(statuses)
    return statuses


def pick_district(sector):
    preferred = {
        "Roads & Transportation": ["Al Safa", "Al Rawdah", "Al Salamah", "Al Bawadi", "Obhur", "Al Hamdaniyah", "Al Samer"],
        "Urban Development": ["Al Balad", "Al Hamra", "Al Shati", "Obhur", "Al Ruwais", "Al Muhammadiyah"],
        "Stormwater & Drainage": ["Al Sanabel", "Al Ajwad", "Al Naseem", "Al Manar", "Al Samer", "Al Waha"],
        "Buildings": ["Al Rawdah", "Al Andalus", "Al Faisaliyah", "Al Rehab", "Al Rabwah"],
        "Utilities": ["Al Marwah", "Al Aziziyah", "Al Naseem", "Al Jamiah", "Al Thaghr"],
        "Street Lighting": ["Al Naeem", "Al Basateen", "Al Zahra", "Al Bawadi", "Al Salamah"],
        "Public Facilities": ["Al Kandarah", "Al Balad", "Al Jamiah", "Al Rehab", "Prince Fawaz"],
        "Parks & Landscaping": ["Al Shati", "Al Basateen", "Al Zahra", "Al Muhammadiyah", "Al Hamra"],
    }
    pool = preferred.get(sector, list(DISTRICTS))
    if random.random() < 0.72:
        return random.choice(pool)
    return random.choice(list(DISTRICTS.keys()))


def contractor_adjustments(profile):
    mapping = {
        "excellent": {"schedule": 8, "budget": -4, "risk": -8},
        "good": {"schedule": 3, "budget": -1, "risk": -3},
        "mixed": {"schedule": -5, "budget": 4, "risk": 4},
        "weak": {"schedule": -12, "budget": 10, "risk": 10},
    }
    return mapping[profile]


def sector_duration_range(sector):
    return {
        "Roads & Transportation": (420, 1200),
        "Urban Development": (540, 1400),
        "Buildings": (300, 900),
        "Stormwater & Drainage": (360, 1100),
        "Parks & Landscaping": (180, 540),
        "Utilities": (240, 780),
        "Street Lighting": (150, 450),
        "Public Facilities": (210, 720),
    }[sector]


def generate_dates(status, duration_days):
    if status == "Completed":
        planned_start = TODAY - timedelta(days=random.randint(duration_days + 30, duration_days + 700))
    elif status == "In Progress":
        planned_start = TODAY - timedelta(days=random.randint(60, max(duration_days - 30, 120)))
    elif status == "Delayed":
        planned_start = TODAY - timedelta(days=random.randint(int(duration_days * 0.45), duration_days + 220))
    elif status == "On Hold":
        planned_start = TODAY - timedelta(days=random.randint(90, max(duration_days // 2, 180)))
    else:
        planned_start = TODAY + timedelta(days=random.randint(10, 420))

    actual_start = planned_start + timedelta(days=random.randint(-20, 45)) if status != "Not Started" else None
    if actual_start and actual_start > TODAY:
        actual_start = planned_start

    planned_end = planned_start + timedelta(days=duration_days)
    return planned_start, actual_start, planned_end


def compute_progress(status, planned_start, actual_start, planned_end, duration_days, adj):
    if status == "Not Started":
        return 0.0, 0.0

    if status == "Completed":
        return 100.0, 100.0

    elapsed_plan = (TODAY - planned_start).days
    planned_progress = clamp((elapsed_plan / duration_days) * 100, 0, 99)

    variance_noise = random.uniform(-6, 6) + adj["schedule"]
    if status == "In Progress":
        actual_progress = clamp(planned_progress + variance_noise, 8, 98)
    elif status == "Delayed":
        actual_progress = clamp(planned_progress - random.uniform(12, 35) + adj["schedule"], 5, 92)
        planned_progress = max(actual_progress + random.uniform(8, 26), planned_progress)
    else:
        actual_progress = clamp(planned_progress - random.uniform(8, 28), 3, 85)

    if actual_start and actual_start > planned_start:
        kickoff_penalty = min((actual_start - planned_start).days * 0.08, 6)
        actual_progress = clamp(actual_progress - kickoff_penalty, 0, 100)

    planned_progress = clamp(planned_progress, 0, 100)
    actual_progress = clamp(actual_progress, 0, 100)
    return round(planned_progress, 2), round(actual_progress, 2)


def compute_financials(status, approved_budget, actual_progress, adj, sector):
    base_ratio = actual_progress / 100 if actual_progress > 0 else 0
    sector_bias = 0.0
    if sector in {"Stormwater & Drainage", "Utilities"}:
        sector_bias = 0.04
    elif sector in {"Parks & Landscaping", "Street Lighting"}:
        sector_bias = -0.02

    spend_ratio = base_ratio + random.uniform(-0.08, 0.10) + sector_bias + (adj["budget"] / 100)

    if status == "Completed":
        spend_ratio = random.uniform(0.92, 1.08)
    elif status == "Delayed" and random.random() < 0.45:
        spend_ratio += random.uniform(0.12, 0.28)
    elif status == "In Progress" and random.random() < 0.18:
        spend_ratio += random.uniform(0.10, 0.22)
    elif status == "In Progress" and random.random() < 0.14:
        spend_ratio -= random.uniform(0.08, 0.18)
    elif status == "On Hold":
        spend_ratio += random.uniform(0.03, 0.16)

    spend_ratio = clamp(spend_ratio, 0, 1.2)
    amount_spent = money(approved_budget * spend_ratio)
    financial_progress = round((amount_spent / approved_budget) * 100, 2) if approved_budget else 0.0
    return amount_spent, financial_progress


def determine_schedule_status(actual_progress, schedule_variance):
    if actual_progress >= 100:
        return "Completed"
    if schedule_variance > 5:
        return "Ahead of Schedule"
    if -5 <= schedule_variance <= 5:
        return "On Track"
    if -10 <= schedule_variance < -5:
        return "Slightly Delayed"
    if -20 <= schedule_variance < -10:
        return "Delayed"
    return "Critical Delay"


def determine_budget_status(financial_progress, actual_progress, amount_spent, approved_budget):
    budget_variance = financial_progress - actual_progress
    if amount_spent > approved_budget:
        return "Over Budget"
    if budget_variance > 18:
        return "Over Budget"
    if budget_variance > 8:
        return "Watch"
    if budget_variance < -8:
        return "Under Budget"
    return "On Budget"


def determine_delay_days(status, planned_end, expected_end, schedule_status):
    if status == "Completed":
        return max((expected_end - planned_end).days, 0)
    if schedule_status in {"On Track", "Ahead of Schedule"} or status in {"Not Started"}:
        return 0
    if status == "On Hold":
        return random.randint(20, 220)
    late = max((expected_end - planned_end).days, 0)
    if late == 0:
        late = random.randint(5, 40) if schedule_status == "Slightly Delayed" else random.randint(30, 220)
    if schedule_status == "Critical Delay":
        late = max(late, random.randint(90, 400))
    return late


def determine_risk(status, schedule_variance, budget_variance, delay_days):
    risk_points = 0
    if status == "On Hold":
        risk_points += 35
    if status == "Delayed":
        risk_points += 20
    if schedule_variance < -20:
        risk_points += 35
    elif schedule_variance < -10:
        risk_points += 20
    elif schedule_variance < -5:
        risk_points += 10
    if budget_variance > 20:
        risk_points += 25
    elif budget_variance > 10:
        risk_points += 12
    elif budget_variance < -15:
        risk_points += 5
    if delay_days > 180:
        risk_points += 20
    elif delay_days > 60:
        risk_points += 10

    if risk_points >= 70:
        return "Critical"
    if risk_points >= 40:
        return "High"
    if risk_points >= 18:
        return "Medium"
    return "Low"


def compute_health(schedule_variance, budget_variance, actual_progress, planned_progress, risk_level, status):
    schedule_score = clamp(100 + min(schedule_variance, 10) * 3, 0, 100)
    if schedule_variance < 0:
        schedule_score = clamp(100 + schedule_variance * 2.8, 0, 100)

    budget_score = clamp(100 - abs(budget_variance) * 3.2, 0, 100)
    if budget_variance < -12:
        budget_score = clamp(86 - abs(budget_variance) * 1.2, 0, 100)

    progress_gap = abs(actual_progress - planned_progress)
    progress_score = clamp(100 - progress_gap * 2.5, 0, 100)
    if status == "Completed":
        progress_score = 100

    risk_score = {"Low": 95, "Medium": 75, "High": 50, "Critical": 25}[risk_level]
    total = (schedule_score * 0.4) + (budget_score * 0.3) + (progress_score * 0.2) + (risk_score * 0.1)
    return round(clamp(total, 0, 100), 2)


def determine_health_status(score):
    if score >= 85:
        return "Healthy"
    if score >= 70:
        return "Monitor"
    if score >= 50:
        return "At Risk"
    return "Critical"


def build_projects():
    project_names = generate_project_names()
    statuses = pick_status_buckets()
    projects = []

    contractor_cycle = CONTRACTOR_POOL.copy()
    pm_cycle = PM_POOL.copy()
    random.shuffle(contractor_cycle)
    random.shuffle(pm_cycle)
    contractor_index = 0
    pm_index = 0

    for idx, ((sector, project_name), status) in enumerate(zip(project_names, statuses), start=1):
        district = pick_district(sector)
        contractor = contractor_cycle[contractor_index % len(contractor_cycle)]
        contractor_index += 1
        pm_id, pm_name = pm_cycle[pm_index % len(pm_cycle)]
        pm_index += 1
        adj = contractor_adjustments(contractor.profile)

        min_val, max_val = SECTOR_CONFIG[sector]["value"]
        contract_value = money(np.exp(np.random.uniform(np.log(min_val), np.log(max_val))))
        approved_budget = money(contract_value * random.uniform(0.95, 1.15))

        dur_low, dur_high = sector_duration_range(sector)
        duration_days = random.randint(dur_low, dur_high)
        planned_start, actual_start, planned_end = generate_dates(status, duration_days)

        planned_progress, actual_progress = compute_progress(
            status, planned_start, actual_start, planned_end, duration_days, adj
        )
        schedule_variance = round(actual_progress - planned_progress, 2)

        if status == "Completed":
            expected_end = planned_end + timedelta(days=random.randint(-20, 75) if contractor.profile != "weak" else random.randint(15, 160))
            actual_end = expected_end + timedelta(days=random.randint(-5, 20))
            actual_progress = 100.0
            planned_progress = 100.0
            schedule_variance = 0.0
        elif status == "Not Started":
            expected_end = planned_end
            actual_end = None
        else:
            if schedule_variance >= -5:
                end_shift = random.randint(-35, 25)
            elif schedule_variance >= -10:
                end_shift = random.randint(10, 70)
            elif schedule_variance >= -20:
                end_shift = random.randint(45, 160)
            else:
                end_shift = random.randint(120, 420)
            if status == "On Hold":
                end_shift = max(end_shift, random.randint(60, 240))
            expected_end = planned_end + timedelta(days=end_shift)
            actual_end = None

        elapsed_days = 0 if not actual_start else max((min(TODAY, actual_end or TODAY) - actual_start).days, 0)
        remaining_days = 0 if actual_end else max((expected_end - TODAY).days, 0)

        amount_spent, financial_progress = compute_financials(status, approved_budget, actual_progress, adj, sector)
        remaining_budget = money(approved_budget - amount_spent)
        budget_variance = round(financial_progress - actual_progress, 2)
        schedule_status = determine_schedule_status(actual_progress, schedule_variance)
        delay_days = determine_delay_days(status, planned_end, expected_end, schedule_status)

        if status == "Completed":
            delay_days = max((actual_end - planned_end).days, 0)

        if status == "In Progress" and schedule_status in {"Delayed", "Critical Delay"}:
            status = "Delayed" if random.random() < 0.65 else "In Progress"

        budget_status = determine_budget_status(financial_progress, actual_progress, amount_spent, approved_budget)
        risk_level = determine_risk(status, schedule_variance, budget_variance, delay_days)
        health_score = compute_health(schedule_variance, budget_variance, actual_progress, planned_progress, risk_level, status)
        health_status = determine_health_status(health_score)

        priority = "Strategic" if contract_value >= 250_000_000 or sector in {"Urban Development", "Roads & Transportation"} and contract_value >= 180_000_000 and random.random() < 0.45 else random.choices(
            ["High", "Medium", "Low"], weights=[4, 8, 3], k=1
        )[0]
        if health_status == "Critical" and priority == "Low":
            priority = "Medium"

        lat, lon = DISTRICTS[district]
        lat = round(clamp(lat + random.uniform(-0.018, 0.018), 21.30, 21.85), 6)
        lon = round(clamp(lon + random.uniform(-0.022, 0.022), 39.05, 39.35), 6)

        last_update = TODAY - timedelta(days=random.randint(0, 9))
        note = random.choice(NOTES_POOL)

        projects.append({
            "Project_ID": f"JED-PROJ-{idx:03d}",
            "Project_Name": project_name,
            "Sector": sector,
            "District": district,
            "Contractor_ID": contractor.contractor_id,
            "Contractor_Name": contractor.name,
            "Project_Manager_ID": pm_id,
            "Project_Manager_Name": pm_name,
            "Contract_Value": contract_value,
            "Approved_Budget": approved_budget,
            "Amount_Spent": amount_spent,
            "Remaining_Budget": remaining_budget,
            "Financial_Progress": round(financial_progress, 2),
            "Planned_Start_Date": format_date(planned_start),
            "Actual_Start_Date": format_date(actual_start),
            "Planned_End_Date": format_date(planned_end),
            "Expected_End_Date": format_date(expected_end),
            "Actual_End_Date": format_date(actual_end),
            "Project_Duration_Days": duration_days,
            "Elapsed_Days": elapsed_days,
            "Remaining_Days": remaining_days,
            "Planned_Progress": round(planned_progress, 2),
            "Actual_Progress": round(actual_progress, 2),
            "Schedule_Variance": round(schedule_variance, 2),
            "Budget_Variance": round(budget_variance, 2),
            "Delay_Days": delay_days,
            "Status": status,
            "Schedule_Status": schedule_status,
            "Budget_Status": budget_status,
            "Risk_Level": risk_level,
            "Project_Health_Score": health_score,
            "Health_Status": health_status,
            "Priority": priority,
            "Latitude": lat,
            "Longitude": lon,
            "Last_Update": format_date(last_update),
            "Notes": note,
        })

    df = pd.DataFrame(projects)
    return rebalance_portfolio(df)


def rebalance_portfolio(df):
    target = {"Completed": 27, "In Progress": 75, "Delayed": 25, "On Hold": 10, "Not Started": 13}

    delayed_surplus = int((df["Status"] == "Delayed").sum() - target["Delayed"])
    if delayed_surplus > 0:
        candidates = df[
            (df["Status"] == "Delayed")
            & (df["Schedule_Status"].isin(["Slightly Delayed", "Delayed"]))
        ].sort_values(["Delay_Days", "Schedule_Variance"], ascending=[True, False])
        for idx in candidates.index[:delayed_surplus]:
            df.loc[idx, "Status"] = "In Progress"

    in_progress_deficit = int(target["In Progress"] - (df["Status"] == "In Progress").sum())
    if in_progress_deficit > 0:
        candidates = df[
            (df["Status"] == "Delayed")
            & (df["Schedule_Status"] != "Critical Delay")
        ].sort_values(["Delay_Days", "Schedule_Variance"], ascending=[True, False])
        for idx in candidates.index[:in_progress_deficit]:
            df.loc[idx, "Status"] = "In Progress"

    on_hold_deficit = int(target["On Hold"] - (df["Status"] == "On Hold").sum())
    if on_hold_deficit > 0:
        candidates = df[
            (df["Status"] == "Delayed")
            & (df["Risk_Level"].isin(["High", "Critical"]))
        ].sort_values(["Delay_Days", "Budget_Variance"], ascending=[False, False])
        for idx in candidates.index[:on_hold_deficit]:
            df.loc[idx, "Status"] = "On Hold"

    not_started_gap = int(target["Not Started"] - (df["Status"] == "Not Started").sum())
    if not_started_gap > 0:
        candidates = df[
            (df["Status"] == "In Progress")
            & (df["Actual_Progress"] <= 5)
            & (df["Actual_Start_Date"] == "")
        ]
        for idx in candidates.index[:not_started_gap]:
            df.loc[idx, "Status"] = "Not Started"

    return df


def build_monthly_progress(projects_df):
    rows = []
    for row in projects_df.to_dict("records"):
        start = datetime.fromisoformat(row["Planned_Start_Date"]).date()
        actual_end = datetime.fromisoformat(row["Actual_End_Date"]).date() if row["Actual_End_Date"] else None
        end = actual_end or TODAY
        if end < start:
            end = start
        dates = list(pd.date_range(start=start, end=end, freq="MS").date)
        if not dates or dates[0] != start:
            dates = [start] + dates
        target_planned = row["Planned_Progress"]
        target_actual = row["Actual_Progress"]
        progress_points = max(len(dates), 2)
        planned_curve = np.linspace(0, target_planned, progress_points)
        base_actual = np.linspace(0, target_actual, progress_points)

        lag_bias = row["Schedule_Variance"] / max(progress_points - 1, 1)
        smoothed_actual = []
        current = 0.0
        for i in range(progress_points):
            step_target = base_actual[i] + lag_bias * i + np.random.uniform(-1.8, 1.8)
            step_target = clamp(step_target, current, 100)
            if i == progress_points - 1:
                step_target = target_actual
            current = round(step_target, 2)
            smoothed_actual.append(current)

        for idx, dt in enumerate(dates):
            planned = round(clamp(planned_curve[idx], 0, 100), 2)
            actual = round(clamp(smoothed_actual[idx], 0, 100), 2)
            if idx == len(dates) - 1:
                planned = row["Planned_Progress"]
                actual = row["Actual_Progress"]
            rows.append({
                "Date": dt.isoformat(),
                "Project_ID": row["Project_ID"],
                "Project_Name": row["Project_Name"],
                "Planned_Progress": planned,
                "Actual_Progress": actual,
                "Progress_Variance": round(actual - planned, 2),
            })
    return pd.DataFrame(rows)


def build_monthly_financials(projects_df, progress_df):
    rows = []
    grouped = progress_df.groupby("Project_ID")
    for row in projects_df.to_dict("records"):
        project_progress = grouped.get_group(row["Project_ID"]).sort_values("Date")
        periods = len(project_progress)
        if periods == 0:
            continue
        cumulative_planned = 0
        cumulative_actual = 0
        prev_planned = 0
        prev_actual = 0
        for idx, (_, prog) in enumerate(project_progress.iterrows()):
            planned_ratio = clamp(prog["Planned_Progress"] / 100, 0, 1.15)
            actual_ratio = clamp(prog["Actual_Progress"] / 100, 0, 1.2)
            cum_plan = money(row["Approved_Budget"] * planned_ratio)
            cum_actual = money(row["Approved_Budget"] * actual_ratio)

            if idx == periods - 1:
                cum_actual = row["Amount_Spent"]
                cum_plan = money(row["Approved_Budget"] * (row["Planned_Progress"] / 100))

            planned_spend = max(cum_plan - prev_planned, 0)
            actual_spend = max(cum_actual - prev_actual, 0)
            rows.append({
                "Date": prog["Date"],
                "Project_ID": row["Project_ID"],
                "Project_Name": row["Project_Name"],
                "Planned_Spend": planned_spend,
                "Actual_Spend": actual_spend,
                "Cumulative_Planned_Spend": cum_plan,
                "Cumulative_Actual_Spend": cum_actual,
                "Financial_Variance": money(cum_actual - cum_plan),
            })
            prev_planned = cum_plan
            prev_actual = cum_actual
    return pd.DataFrame(rows)


def contractor_summary(projects_df):
    agg = projects_df.groupby(["Contractor_ID", "Contractor_Name"]).agg(
        Total_Projects=("Project_ID", "count"),
        Completed_Projects=("Status", lambda s: int((s == "Completed").sum())),
        Active_Projects=("Status", lambda s: int(s.isin(["In Progress", "Delayed"]).sum())),
        Delayed_Projects=("Status", lambda s: int((s == "Delayed").sum())),
        On_Hold_Projects=("Status", lambda s: int((s == "On Hold").sum())),
        Total_Contract_Value=("Contract_Value", "sum"),
        Average_Project_Value=("Contract_Value", "mean"),
        Average_Progress=("Actual_Progress", "mean"),
        Average_Schedule_Variance=("Schedule_Variance", "mean"),
        Average_Delay_Days=("Delay_Days", "mean"),
        Average_Health_Score=("Project_Health_Score", "mean"),
    ).reset_index()

    performance_score = (
        agg["Average_Health_Score"] * 0.45
        + agg["Average_Progress"] * 0.15
        + (100 - agg["Delayed_Projects"] / agg["Total_Projects"] * 100) * 0.2
        + (100 - agg["On_Hold_Projects"] / agg["Total_Projects"] * 100) * 0.05
        + (50 + agg["Average_Schedule_Variance"].clip(-25, 15) * 2) * 0.15
    )
    agg["Contractor_Performance_Score"] = performance_score.round(2)
    agg["Performance_Category"] = pd.cut(
        agg["Contractor_Performance_Score"],
        bins=[-1, 55, 72, 85, 101],
        labels=["Poor", "Needs Attention", "Good", "Excellent"],
    ).astype(str)

    monetary_cols = ["Total_Contract_Value", "Average_Project_Value"]
    for col in monetary_cols:
        agg[col] = agg[col].round(0).astype(int)
    for col in ["Average_Progress", "Average_Schedule_Variance", "Average_Delay_Days", "Average_Health_Score"]:
        agg[col] = agg[col].round(2)
    return agg.sort_values("Total_Contract_Value", ascending=False)


def sector_summary(projects_df):
    agg = projects_df.groupby("Sector").agg(
        Total_Projects=("Project_ID", "count"),
        Total_Contract_Value=("Contract_Value", "sum"),
        Total_Budget=("Approved_Budget", "sum"),
        Total_Spent=("Amount_Spent", "sum"),
        Average_Progress=("Actual_Progress", "mean"),
        Completed_Projects=("Status", lambda s: int((s == "Completed").sum())),
        Delayed_Projects=("Status", lambda s: int((s == "Delayed").sum())),
        Average_Health_Score=("Project_Health_Score", "mean"),
    ).reset_index()
    for col in ["Total_Contract_Value", "Total_Budget", "Total_Spent"]:
        agg[col] = agg[col].round(0).astype(int)
    for col in ["Average_Progress", "Average_Health_Score"]:
        agg[col] = agg[col].round(2)
    return agg.sort_values("Total_Contract_Value", ascending=False)


def district_summary(projects_df):
    agg = projects_df.groupby("District").agg(
        Total_Projects=("Project_ID", "count"),
        Total_Contract_Value=("Contract_Value", "sum"),
        Average_Progress=("Actual_Progress", "mean"),
        Completed_Projects=("Status", lambda s: int((s == "Completed").sum())),
        Delayed_Projects=("Status", lambda s: int((s == "Delayed").sum())),
        Critical_Projects=("Health_Status", lambda s: int((s == "Critical").sum())),
    ).reset_index()
    agg["Total_Contract_Value"] = agg["Total_Contract_Value"].round(0).astype(int)
    agg["Average_Progress"] = agg["Average_Progress"].round(2)
    return agg.sort_values(["Total_Projects", "Total_Contract_Value"], ascending=[False, False])


def pm_summary(projects_df):
    agg = projects_df.groupby(["Project_Manager_ID", "Project_Manager_Name"]).agg(
        Total_Projects=("Project_ID", "count"),
        Completed_Projects=("Status", lambda s: int((s == "Completed").sum())),
        Delayed_Projects=("Status", lambda s: int((s == "Delayed").sum())),
        Total_Project_Value=("Contract_Value", "sum"),
        Average_Progress=("Actual_Progress", "mean"),
        Average_Health_Score=("Project_Health_Score", "mean"),
    ).reset_index()
    agg["Total_Project_Value"] = agg["Total_Project_Value"].round(0).astype(int)
    agg["Average_Progress"] = agg["Average_Progress"].round(2)
    agg["Average_Health_Score"] = agg["Average_Health_Score"].round(2)
    return agg.sort_values("Total_Project_Value", ascending=False)


def dashboard_summary(projects_df):
    summary = {
        "Total_Projects": int(len(projects_df)),
        "Total_Contract_Value": int(projects_df["Contract_Value"].sum()),
        "Total_Approved_Budget": int(projects_df["Approved_Budget"].sum()),
        "Total_Amount_Spent": int(projects_df["Amount_Spent"].sum()),
        "Remaining_Budget": int(projects_df["Remaining_Budget"].sum()),
        "Average_Actual_Progress": round(projects_df["Actual_Progress"].mean(), 2),
        "Average_Planned_Progress": round(projects_df["Planned_Progress"].mean(), 2),
        "Completed_Projects": int((projects_df["Status"] == "Completed").sum()),
        "In_Progress_Projects": int((projects_df["Status"] == "In Progress").sum()),
        "Delayed_Projects": int((projects_df["Status"] == "Delayed").sum()),
        "On_Hold_Projects": int((projects_df["Status"] == "On Hold").sum()),
        "Not_Started_Projects": int((projects_df["Status"] == "Not Started").sum()),
        "Healthy_Projects": int((projects_df["Health_Status"] == "Healthy").sum()),
        "Monitor_Projects": int((projects_df["Health_Status"] == "Monitor").sum()),
        "At_Risk_Projects": int((projects_df["Health_Status"] == "At Risk").sum()),
        "Critical_Projects": int((projects_df["Health_Status"] == "Critical").sum()),
        "Total_Contractors": int(projects_df["Contractor_ID"].nunique()),
        "Total_Sectors": int(projects_df["Sector"].nunique()),
        "Total_Districts": int(projects_df["District"].nunique()),
        "Average_Project_Health": round(projects_df["Project_Health_Score"].mean(), 2),
        "Average_Schedule_Variance": round(projects_df["Schedule_Variance"].mean(), 2),
        "Projects_Over_Budget": int((projects_df["Budget_Status"] == "Over Budget").sum()),
        "Projects_Ahead_Of_Schedule": int((projects_df["Schedule_Status"] == "Ahead of Schedule").sum()),
    }
    return summary


def validate_data(projects_df, contractors_df, summary):
    errors = []
    if projects_df["Project_ID"].duplicated().any():
        errors.append("Duplicate Project_ID found.")
    if (projects_df["Project_Name"].str.strip() == "").any():
        errors.append("Empty Project_Name found.")
    known_contractors = set(projects_df["Contractor_ID"].unique())
    if set(contractors_df["Contractor_ID"]) != known_contractors:
        errors.append("Contractor summary IDs do not match project contractor IDs.")
    if not projects_df["Actual_Progress"].between(0, 100).all():
        errors.append("Actual_Progress outside range.")
    if not projects_df["Planned_Progress"].between(0, 100).all():
        errors.append("Planned_Progress outside range.")

    financial_check = ((projects_df["Amount_Spent"] / projects_df["Approved_Budget"]) * 100).round(2)
    if not np.allclose(financial_check, projects_df["Financial_Progress"], atol=0.02):
        errors.append("Financial_Progress mismatch.")
    if not ((projects_df["Approved_Budget"] - projects_df["Amount_Spent"]).round(0) == projects_df["Remaining_Budget"]).all():
        errors.append("Remaining_Budget mismatch.")
    if not ((projects_df["Actual_Progress"] - projects_df["Planned_Progress"]).round(2) == projects_df["Schedule_Variance"]).all():
        errors.append("Schedule_Variance mismatch.")
    if not (projects_df.loc[projects_df["Status"] == "Completed", "Actual_Progress"] == 100).all():
        errors.append("Completed projects with progress not 100.")
    if (projects_df.loc[projects_df["Status"] == "Completed", "Actual_End_Date"] == "").any():
        errors.append("Completed projects missing Actual_End_Date.")
    if (projects_df.loc[projects_df["Status"] != "Completed", "Actual_End_Date"] != "").any():
        errors.append("Non-completed projects have Actual_End_Date.")

    expected_health = projects_df["Project_Health_Score"].apply(determine_health_status)
    if not (expected_health == projects_df["Health_Status"]).all():
        errors.append("Health_Status mismatch.")
    if not projects_df["Latitude"].between(21.30, 21.85).all():
        errors.append("Latitude outside Jeddah range.")
    if not projects_df["Longitude"].between(39.05, 39.35).all():
        errors.append("Longitude outside Jeddah range.")

    planned_starts = pd.to_datetime(projects_df["Planned_Start_Date"])
    planned_ends = pd.to_datetime(projects_df["Planned_End_Date"])
    if not (planned_ends > planned_starts).all():
        errors.append("Planned_End_Date not after Planned_Start_Date.")

    actual_starts = pd.to_datetime(projects_df["Actual_Start_Date"], errors="coerce")
    actual_ends = pd.to_datetime(projects_df["Actual_End_Date"], errors="coerce")
    if ((actual_starts.notna()) & (actual_ends.notna()) & (actual_starts > actual_ends)).any():
        errors.append("Actual_Start_Date after Actual_End_Date.")
    if (projects_df["Amount_Spent"] < 0).any():
        errors.append("Negative Amount_Spent found.")
    if (projects_df["Contract_Value"] < 0).any():
        errors.append("Negative Contract_Value found.")

    required_columns = [
        "Project_ID", "Project_Name", "Sector", "District", "Contractor_ID", "Contractor_Name",
        "Project_Manager_ID", "Project_Manager_Name", "Contract_Value", "Approved_Budget",
        "Amount_Spent", "Planned_Start_Date", "Planned_End_Date", "Status", "Health_Status",
    ]
    if projects_df[required_columns].isnull().any().any():
        errors.append("Nulls found in required columns.")

    if summary["Total_Projects"] != len(projects_df):
        errors.append("Dashboard summary total projects mismatch.")
    if summary["Total_Contractors"] != projects_df["Contractor_ID"].nunique():
        errors.append("Dashboard summary contractor count mismatch.")

    return errors


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def build_data_dictionary():
    content = """# Data Dictionary

## projects.csv / projects.json

### Project_ID
Unique project identifier.
Type: String
Example: JED-PROJ-001

### Project_Name
Descriptive project title for reporting and dashboard display.
Type: String

### Sector
Project sector classification.
Type: Categorical String
Values: Roads & Transportation, Buildings, Stormwater & Drainage, Parks & Landscaping, Utilities, Street Lighting, Public Facilities, Urban Development

### District
Jeddah district where the project is located.
Type: Categorical String

### Contractor_ID
Unique contractor identifier.
Type: String
Example: CONT-001

### Contractor_Name
Assigned contractor name.
Type: String

### Project_Manager_ID
Unique project manager identifier.
Type: String
Example: PM-001

### Project_Manager_Name
Assigned project manager name.
Type: String

### Contract_Value
Original contract value in SAR.
Type: Integer

### Approved_Budget
Approved working budget in SAR.
Type: Integer

### Amount_Spent
Total spent amount in SAR as of the latest update.
Type: Integer

### Remaining_Budget
Unspent approved budget in SAR.
Type: Integer
Formula: Approved_Budget - Amount_Spent

### Financial_Progress
Spent budget percentage.
Type: Decimal Percentage
Formula: Amount_Spent / Approved_Budget * 100

### Planned_Start_Date
Baseline planned start date.
Type: Date (YYYY-MM-DD)

### Actual_Start_Date
Actual mobilization or construction start date.
Type: Date (YYYY-MM-DD) or Empty

### Planned_End_Date
Baseline planned completion date.
Type: Date (YYYY-MM-DD)

### Expected_End_Date
Current forecast completion date.
Type: Date (YYYY-MM-DD)

### Actual_End_Date
Actual completion date for completed projects only.
Type: Date (YYYY-MM-DD) or Empty

### Project_Duration_Days
Planned baseline duration.
Type: Integer
Formula: Planned_End_Date - Planned_Start_Date

### Elapsed_Days
Elapsed days since actual start until latest update or actual completion.
Type: Integer

### Remaining_Days
Forecast remaining days until expected end for open projects.
Type: Integer

### Planned_Progress
Expected completion percentage by the latest update.
Type: Decimal Percentage

### Actual_Progress
Observed completion percentage by the latest update.
Type: Decimal Percentage

### Schedule_Variance
Difference between actual and planned progress.
Type: Decimal Percentage
Formula: Actual_Progress - Planned_Progress

### Budget_Variance
Difference between financial and physical progress.
Type: Decimal Percentage
Formula: Financial_Progress - Actual_Progress

### Delay_Days
Estimated or realized delay in days for delayed projects.
Type: Integer

### Status
Portfolio execution status.
Type: Categorical String
Values: Not Started, In Progress, Completed, Delayed, On Hold

### Schedule_Status
Schedule performance band.
Type: Categorical String
Values: Ahead of Schedule, On Track, Slightly Delayed, Delayed, Critical Delay, Completed

### Budget_Status
Budget performance band.
Type: Categorical String
Values: Under Budget, On Budget, Watch, Over Budget

### Risk_Level
Overall project risk classification.
Type: Categorical String
Values: Low, Medium, High, Critical

### Project_Health_Score
Composite project health score from 0 to 100.
Type: Decimal
Method: Weighted score using schedule performance, budget performance, progress alignment, and risk level.

### Health_Status
Health category derived from Project_Health_Score.
Type: Categorical String
Values: Healthy, Monitor, At Risk, Critical

### Priority
Management priority classification.
Type: Categorical String
Values: Low, Medium, High, Strategic

### Latitude
Approximate project latitude inside Jeddah.
Type: Decimal

### Longitude
Approximate project longitude inside Jeddah.
Type: Decimal

### Last_Update
Latest reporting date for the record.
Type: Date (YYYY-MM-DD)

### Notes
Short operational note or management remark.
Type: String

## contractors.csv / contractors.json

### Contractor_ID
Unique contractor identifier.
Type: String

### Contractor_Name
Contractor name.
Type: String

### Total_Projects
Number of assigned projects.
Type: Integer

### Completed_Projects
Number of completed projects.
Type: Integer

### Active_Projects
Number of active projects with status In Progress or Delayed.
Type: Integer

### Delayed_Projects
Number of assigned projects with status Delayed.
Type: Integer

### On_Hold_Projects
Number of assigned projects with status On Hold.
Type: Integer

### Total_Contract_Value
Total contract value across assigned projects.
Type: Integer

### Average_Project_Value
Average contract value across assigned projects.
Type: Integer

### Average_Progress
Average actual progress across assigned projects.
Type: Decimal Percentage

### Average_Schedule_Variance
Average schedule variance across assigned projects.
Type: Decimal Percentage

### Average_Delay_Days
Average delay days across assigned projects.
Type: Decimal

### Average_Health_Score
Average project health score across assigned projects.
Type: Decimal

### Contractor_Performance_Score
Composite contractor performance score.
Type: Decimal
Method: Weighted mix of health, progress, schedule, and delayed/on-hold project ratios.

### Performance_Category
Performance band derived from Contractor_Performance_Score.
Type: Categorical String
Values: Excellent, Good, Needs Attention, Poor

## sectors.json

### Sector
Sector name.
Type: String

### Total_Projects
Number of projects in the sector.
Type: Integer

### Total_Contract_Value
Total contract value for the sector.
Type: Integer

### Total_Budget
Total approved budget for the sector.
Type: Integer

### Total_Spent
Total spent amount for the sector.
Type: Integer

### Average_Progress
Average actual progress for sector projects.
Type: Decimal Percentage

### Completed_Projects
Completed projects in the sector.
Type: Integer

### Delayed_Projects
Delayed projects in the sector.
Type: Integer

### Average_Health_Score
Average project health score for the sector.
Type: Decimal

## districts.json

### District
District name in Jeddah.
Type: String

### Total_Projects
Number of projects in the district.
Type: Integer

### Total_Contract_Value
Total contract value in the district.
Type: Integer

### Average_Progress
Average actual progress in the district.
Type: Decimal Percentage

### Completed_Projects
Completed projects in the district.
Type: Integer

### Delayed_Projects
Delayed projects in the district.
Type: Integer

### Critical_Projects
Projects with Health_Status equal to Critical.
Type: Integer

## project_managers.json

### Project_Manager_ID
Unique project manager identifier.
Type: String

### Project_Manager_Name
Project manager name.
Type: String

### Total_Projects
Number of assigned projects.
Type: Integer

### Completed_Projects
Completed assigned projects.
Type: Integer

### Delayed_Projects
Delayed assigned projects.
Type: Integer

### Total_Project_Value
Total assigned contract value.
Type: Integer

### Average_Progress
Average actual progress across assigned projects.
Type: Decimal Percentage

### Average_Health_Score
Average health score across assigned projects.
Type: Decimal

## monthly_progress.csv

### Date
Monthly reporting date.
Type: Date (YYYY-MM-DD)

### Project_ID
Project identifier.
Type: String

### Project_Name
Project name.
Type: String

### Planned_Progress
Planned cumulative progress for the reporting month.
Type: Decimal Percentage

### Actual_Progress
Actual cumulative progress for the reporting month.
Type: Decimal Percentage

### Progress_Variance
Difference between actual and planned cumulative progress.
Type: Decimal Percentage
Formula: Actual_Progress - Planned_Progress

## monthly_financials.csv

### Date
Monthly reporting date.
Type: Date (YYYY-MM-DD)

### Project_ID
Project identifier.
Type: String

### Project_Name
Project name.
Type: String

### Planned_Spend
Planned spend during the month.
Type: Integer

### Actual_Spend
Actual spend during the month.
Type: Integer

### Cumulative_Planned_Spend
Planned cumulative spend by the reporting month.
Type: Integer

### Cumulative_Actual_Spend
Actual cumulative spend by the reporting month.
Type: Integer

### Financial_Variance
Difference between cumulative actual and planned spend.
Type: Integer
Formula: Cumulative_Actual_Spend - Cumulative_Planned_Spend

## dashboard_summary.json

Contains portfolio-level KPIs calculated from projects.csv for direct dashboard initialization.
Type: JSON Object
"""
    return content


def print_summary(projects_df, contractors_df):
    print("DATASET SUMMARY")
    print(f"Projects: {len(projects_df)}")
    print(f"Contractors: {projects_df['Contractor_ID'].nunique()}")
    print(f"Sectors: {projects_df['Sector'].nunique()}")
    print(f"Districts: {projects_df['District'].nunique()}")
    print("\nProjects by Status:")
    print(projects_df["Status"].value_counts().to_string())
    print("\nProjects by Schedule Status:")
    print(projects_df["Schedule_Status"].value_counts().to_string())
    print("\nProjects by Health Status:")
    print(projects_df["Health_Status"].value_counts().to_string())
    print("\nProjects by Risk Level:")
    print(projects_df["Risk_Level"].value_counts().to_string())
    print("\nFinancial Totals:")
    print(f"Total Contract Value: {int(projects_df['Contract_Value'].sum()):,} SAR")
    print(f"Total Approved Budget: {int(projects_df['Approved_Budget'].sum()):,} SAR")
    print(f"Total Amount Spent: {int(projects_df['Amount_Spent'].sum()):,} SAR")
    print(f"Average Planned Progress: {projects_df['Planned_Progress'].mean():.2f}%")
    print(f"Average Actual Progress: {projects_df['Actual_Progress'].mean():.2f}%")
    print(f"Average Health Score: {projects_df['Project_Health_Score'].mean():.2f}")
    print("\nTop 5 Contractors by Contract Value:")
    print(contractors_df.nlargest(5, "Total_Contract_Value")[["Contractor_Name", "Total_Contract_Value"]].to_string(index=False))
    print("\nTop 5 Contractors by Average Progress:")
    print(contractors_df.nlargest(5, "Average_Progress")[["Contractor_Name", "Average_Progress"]].to_string(index=False))
    print("\nTop 10 Most Delayed Projects:")
    print(projects_df.nlargest(10, "Delay_Days")[["Project_ID", "Project_Name", "Delay_Days", "Status"]].to_string(index=False))
    print("\nTop 10 Highest Value Projects:")
    print(projects_df.nlargest(10, "Contract_Value")[["Project_ID", "Project_Name", "Contract_Value", "Sector"]].to_string(index=False))
    high_fin = (projects_df["Financial_Progress"] - projects_df["Actual_Progress"] > 15).sum()
    print(f"\nProjects with Financial Progress > Actual Progress by more than 15%: {int(high_fin)}")


def main():
    DATA_DIR.mkdir(exist_ok=True)
    projects_df = build_projects()
    projects_df = projects_df.sort_values("Project_ID").reset_index(drop=True)

    monthly_progress_df = build_monthly_progress(projects_df)
    monthly_financials_df = build_monthly_financials(projects_df, monthly_progress_df)
    contractors_df = contractor_summary(projects_df)
    sectors_df = sector_summary(projects_df)
    districts_df = district_summary(projects_df)
    managers_df = pm_summary(projects_df)
    summary = dashboard_summary(projects_df)

    errors = validate_data(projects_df, contractors_df, summary)
    if errors:
        raise ValueError("Validation failed:\n- " + "\n- ".join(errors))

    projects_df.to_csv(DATA_DIR / "projects.csv", index=False)
    write_json(DATA_DIR / "projects.json", projects_df.to_dict("records"))
    contractors_df.to_csv(DATA_DIR / "contractors.csv", index=False)
    write_json(DATA_DIR / "contractors.json", contractors_df.to_dict("records"))
    write_json(DATA_DIR / "sectors.json", sectors_df.to_dict("records"))
    write_json(DATA_DIR / "districts.json", districts_df.to_dict("records"))
    write_json(DATA_DIR / "project_managers.json", managers_df.to_dict("records"))
    monthly_progress_df.to_csv(DATA_DIR / "monthly_progress.csv", index=False)
    monthly_financials_df.to_csv(DATA_DIR / "monthly_financials.csv", index=False)
    write_json(DATA_DIR / "dashboard_summary.json", summary)
    (DATA_DIR / "data_dictionary.md").write_text(build_data_dictionary(), encoding="utf-8")

    print_summary(projects_df, contractors_df)
    print("\nGenerated files:")
    for path in sorted(DATA_DIR.iterdir()):
        print(path.resolve())


if __name__ == "__main__":
    main()
