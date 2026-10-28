"""
SkillAdapt - Personalized Learning Path Module
Generates an adaptive, prioritized curriculum based on student quiz weaknesses,
prerequisite dependencies, and tracks persistent resource completion.
"""

import os
import sys
import json
from typing import List, Dict, Any

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from auth import load_users, save_users, find_user_by_id
from analytics import compute_student_topic_analytics
RESOURCES_FILE = os.path.join(BASE_DIR, "data", "learning_resources.json")

def load_all_resources() -> List[Dict[str, Any]]:
    if not os.path.exists(RESOURCES_FILE):
        return []
    try:
        with open(RESOURCES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def get_personalized_learning_path(user: Dict[str, Any]) -> Dict[str, Any]:
    """
    Construct an individualized learning path tailored to the student's weaknesses.
    Priority hierarchy:
      1. Topics classified as 'Needs Improvement' (< 50% accuracy)
      2. Topics classified as 'Developing' (50% - 79% accuracy)
      3. Topics not yet attempted or with insufficient data
      4. Topics classified as 'Strong' (>= 80% accuracy) for enrichment
    """
    user_id = user["id"]
    resources = load_all_resources()
    completed_ids = set(user.get("completed_resources", []))

    topic_analysis = compute_student_topic_analytics(user_id)
    # Map topic name -> classification info
    topic_map = {t["topic"].lower(): t for t in topic_analysis["topics"]}

    ordered_resources = []

    for res in resources:
        topic_name = res.get("topic", "").lower()
        topic_info = topic_map.get(topic_name)

        if topic_info:
            classification = topic_info["classification"]
            accuracy = topic_info["accuracy"]
        else:
            classification = "Not Attempted"
            accuracy = 0.0

        is_completed = (res["resource_id"] in completed_ids)

        # Assign priority weight (lower number = higher study priority)
        # 1: Needs Improvement
        # 2: Developing
        # 3: Not Attempted
        # 4: Strong (already mastered, lowest urgency)
        if classification == "Needs Improvement":
            priority_score = 1
            priority_label = "High Priority"
            reason = "Quiz accuracy below 50%. Foundational review strongly recommended."
        elif classification == "Developing":
            priority_score = 2
            priority_label = "Medium Priority"
            reason = "Quiz accuracy between 50%-79%. Practice recommended to achieve mastery."
        elif classification == "Not Attempted":
            priority_score = 3
            priority_label = "Next Up"
            reason = "Topic not yet assessed in quizzes. Explore fundamentals."
        else: # Strong
            priority_score = 4
            priority_label = "Mastered"
            reason = "Quiz accuracy 80%+. Solid mastery demonstrated."

        # Check prerequisite status
        prereqs = res.get("prerequisites", [])
        prereq_status = "Satisfied"
        for p in prereqs:
            p_lower = p.lower()
            # If prerequisite is in needs improvement, warn student
            if p_lower in topic_map and topic_map[p_lower]["classification"] == "Needs Improvement":
                prereq_status = f"Review Recommended: Prerequisite '{p}' requires improvement first."
                break

        ordered_resources.append({
            "resource_id": res["resource_id"],
            "subject": res["subject"],
            "topic": res["topic"],
            "title": res["title"],
            "description": res["description"],
            "learning_objectives": res.get("learning_objectives", []),
            "estimated_minutes": res.get("estimated_minutes", 30),
            "difficulty": res.get("difficulty", "Beginner"),
            "resource_type": res.get("resource_type", "Concept Guide"),
            "summary_content": res.get("summary_content", ""),
            "reference_url": res.get("reference_url", "#"),
            "prerequisites": prereqs,
            "prerequisite_status": prereq_status,
            "is_completed": is_completed,
            "topic_classification": classification,
            "topic_accuracy": accuracy,
            "priority_score": priority_score,
            "priority_label": priority_label,
            "priority_reason": reason
        })

    # Sort: uncompleted first, then by priority score (High -> Medium -> Next Up -> Mastered)
    ordered_resources.sort(key=lambda r: (1 if r["is_completed"] else 0, r["priority_score"]))

    total_count = len(resources)
    completed_count = len(completed_ids)
    overall_progress_pct = round((completed_count / total_count) * 100.0, 1) if total_count > 0 else 0.0

    return {
        "total_resources": total_count,
        "completed_resources": completed_count,
        "completion_percentage": overall_progress_pct,
        "resources": ordered_resources
    }

def toggle_resource_completion(user_id: str, resource_id: str) -> Dict[str, Any]:
    """Toggle persistent completion status of a learning resource for the student."""
    users = load_users()
    target_user = None
    for u in users:
        if u.get("id") == user_id:
            target_user = u
            break

    if not target_user:
        raise ValueError("User not found.")

    completed_list = target_user.get("completed_resources", [])
    if resource_id in completed_list:
        completed_list.remove(resource_id)
        is_completed = False
    else:
        completed_list.append(resource_id)
        is_completed = True

    target_user["completed_resources"] = completed_list
    save_users(users)

    return {
        "resource_id": resource_id,
        "is_completed": is_completed,
        "total_completed": len(completed_list)
    }
