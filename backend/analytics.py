"""
SkillAdapt - Analytics & Performance Intelligence Module
Computes strength & weakness classification, mastery levels, historical trends,
and actionable pedagogical recommendations for students.
"""

import os
import json
from typing import List, Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ATTEMPTS_FILE = os.path.join(BASE_DIR, "data", "quiz_attempts.json")
USERS_FILE = os.path.join(BASE_DIR, "data", "users.json")
QUESTIONS_FILE = os.path.join(BASE_DIR, "data", "questions.json")
RESOURCES_FILE = os.path.join(BASE_DIR, "data", "learning_resources.json")

def load_attempts() -> List[Dict[str, Any]]:
    if not os.path.exists(ATTEMPTS_FILE):
        return []
    try:
        with open(ATTEMPTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def load_resources() -> List[Dict[str, Any]]:
    if not os.path.exists(RESOURCES_FILE):
        return []
    try:
        with open(RESOURCES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def compute_student_topic_analytics(user_id: str) -> Dict[str, Any]:
    """
    Aggregate student responses across all quiz attempts by topic.
    Returns classified topics: 'Strong', 'Developing', 'Needs Improvement', 'Not enough data'.
    """
    attempts = [a for a in load_attempts() if a.get("user_id") == user_id]
    
    # Map topic -> stats
    topic_data: Dict[str, Dict[str, Any]] = {}

    for attempt in attempts:
        for resp in attempt.get("responses", []):
            topic = resp.get("topic") or attempt.get("topic") or "General"
            subject = resp.get("subject") or attempt.get("subject") or "General"
            
            if topic not in topic_data:
                topic_data[topic] = {
                    "topic": topic,
                    "subject": subject,
                    "total_questions": 0,
                    "correct_answers": 0,
                    "total_marks_earned": 0,
                    "max_marks_possible": 0
                }
            
            topic_data[topic]["total_questions"] += 1
            if resp.get("is_correct"):
                topic_data[topic]["correct_answers"] += 1
            topic_data[topic]["total_marks_earned"] += resp.get("marks_earned", 0)
            topic_data[topic]["max_marks_possible"] += resp.get("max_marks", 1)

    classified_topics = []
    strong_topics = []
    weak_topics = []
    developing_topics = []

    for topic_name, stats in topic_data.items():
        total_q = stats["total_questions"]
        correct_q = stats["correct_answers"]
        accuracy = round((correct_q / total_q) * 100.0, 1) if total_q > 0 else 0.0
        
        # Classification threshold rules:
        # Minimum 3 questions required for an empirical evaluation, otherwise 'Not enough data'
        if total_q < 3:
            classification = "Not enough data"
            recommendation = f"Attempt more practice quizzes on '{topic_name}' (minimum 3 questions needed for assessment)."
        elif accuracy >= 80.0:
            classification = "Strong"
            recommendation = f"Great mastery! Maintain your edge with Hard-level quizzes and explore advanced projects."
            strong_topics.append(topic_name)
        elif accuracy >= 50.0:
            classification = "Developing"
            recommendation = f"Good progress. Review tricky edge cases and take Medium-level quizzes to reach 80%+."
            developing_topics.append(topic_name)
        else:
            classification = "Needs Improvement"
            recommendation = f"Concept revision advised. Revisit foundational guides in the Learning Path and practice Easy questions."
            weak_topics.append(topic_name)

        classified_topics.append({
            "topic": topic_name,
            "subject": stats["subject"],
            "total_questions": total_q,
            "correct_answers": correct_q,
            "accuracy": accuracy,
            "classification": classification,
            "recommendation": recommendation
        })

    # Sort topics by accuracy ascending so weakest topics appear first
    classified_topics.sort(key=lambda t: t["accuracy"])

    return {
        "topics": classified_topics,
        "strong_topics": strong_topics,
        "developing_topics": developing_topics,
        "weak_topics": weak_topics
    }

def get_student_dashboard_metrics(user: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate high-level dashboard indicators from real student data:
    - Overall average score
    - Total quizzes attempted
    - Completed topics count
    - Current learning level
    - Strongest topic
    - Topic requiring most improvement
    - Recent quiz activity
    - Chart data (score progression and topic accuracy)
    """
    user_id = user["id"]
    attempts = [a for a in load_attempts() if a.get("user_id") == user_id]
    
    total_quizzes = len(attempts)
    completed_resources = user.get("completed_resources", [])
    completed_topics_count = len(completed_resources)

    if total_quizzes > 0:
        overall_avg_score = round(sum(a.get("percentage", 0) for a in attempts) / total_quizzes, 1)
    else:
        overall_avg_score = 0.0

    topic_analysis = compute_student_topic_analytics(user_id)
    topics = topic_analysis["topics"]

    # Identify strongest and weakest evaluated topics
    evaluated_topics = [t for t in topics if t["classification"] != "Not enough data"]
    if evaluated_topics:
        # sorted by accuracy
        topic_weakest = evaluated_topics[0]["topic"]
        topic_strongest = evaluated_topics[-1]["topic"]
    else:
        topic_strongest = "Not yet evaluated"
        topic_weakest = "Not yet evaluated"

    # Dynamic learning level determination based on average score and attempted quizzes
    if total_quizzes >= 4 and overall_avg_score >= 80.0:
        learning_level = "Advanced"
    elif total_quizzes >= 2 and overall_avg_score >= 60.0:
        learning_level = "Intermediate"
    else:
        learning_level = "Beginner"

    # Recent quiz history (last 5 attempts sorted newest first)
    sorted_attempts = sorted(attempts, key=lambda a: a.get("completed_at", ""), reverse=True)
    recent_activity = []
    for a in sorted_attempts[:5]:
        recent_activity.append({
            "attempt_id": a["attempt_id"],
            "subject": a.get("subject", "General"),
            "score": a.get("score", 0),
            "max_score": a.get("max_score", 0),
            "percentage": a.get("percentage", 0.0),
            "difficulty_breakdown": a.get("difficulty_breakdown", {}),
            "completed_at": a.get("completed_at", "")
        })

    # Prepare Chart.js data
    # 1. Progression Timeline (chronological order)
    timeline_attempts = sorted(attempts, key=lambda a: a.get("completed_at", ""))
    progress_chart = {
        "labels": [f"Quiz #{i+1} ({a.get('subject', '')})" for i, a in enumerate(timeline_attempts)],
        "scores": [a.get("percentage", 0.0) for a in timeline_attempts]
    }

    # 2. Topic Accuracy Bar Chart
    topic_chart = {
        "labels": [t["topic"] for t in topics[:7]],
        "accuracies": [t["accuracy"] for t in topics[:7]],
        "classifications": [t["classification"] for t in topics[:7]]
    }

    return {
        "username": user["username"],
        "full_name": user.get("full_name", user["username"]),
        "overall_avg_score": overall_avg_score,
        "total_quizzes": total_quizzes,
        "completed_topics_count": completed_topics_count,
        "learning_level": learning_level,
        "strongest_topic": topic_strongest,
        "weakest_topic": topic_weakest,
        "recent_activity": recent_activity,
        "topic_analytics": topics,
        "progress_chart": progress_chart,
        "topic_chart": topic_chart
    }
