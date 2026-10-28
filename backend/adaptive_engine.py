"""
SkillAdapt - Adaptive Quiz Engine
Implements the real-time performance-driven question difficulty adaptation,
question selection, attempt persistence, and scoring.
"""

import os
import json
import secrets
import random
from datetime import datetime
from typing import List, Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_FILE = os.path.join(BASE_DIR, "data", "questions.json")
ATTEMPTS_FILE = os.path.join(BASE_DIR, "data", "quiz_attempts.json")
USERS_FILE = os.path.join(BASE_DIR, "data", "users.json")

# In-memory session registry: session_id -> AdaptiveQuizSession
ACTIVE_QUIZZES: Dict[str, Dict[str, Any]] = {}

DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]

def load_questions() -> List[Dict[str, Any]]:
    """Load question bank from questions.json."""
    if not os.path.exists(QUESTIONS_FILE):
        return []
    try:
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def load_attempts() -> List[Dict[str, Any]]:
    """Load all saved quiz attempts."""
    if not os.path.exists(ATTEMPTS_FILE):
        return []
    try:
        with open(ATTEMPTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_attempts(attempts: List[Dict[str, Any]]) -> None:
    """Safely persist quiz attempts to quiz_attempts.json."""
    temp_file = f"{ATTEMPTS_FILE}.tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(attempts, f, indent=2)
    os.replace(temp_file, ATTEMPTS_FILE)

def get_recently_answered_question_ids(user_id: str, limit_attempts: int = 4) -> set:
    """Retrieve IDs of questions recently answered by the student to avoid repeats."""
    attempts = [a for a in load_attempts() if a.get("user_id") == user_id]
    recent_attempts = attempts[-limit_attempts:] if len(attempts) > limit_attempts else attempts
    recent_q_ids = set()
    for att in recent_attempts:
        for resp in att.get("responses", []):
            qid = resp.get("question_id")
            if qid:
                recent_q_ids.add(qid)
    return recent_q_ids

def pick_next_question(
    subject: str,
    target_difficulty: str,
    excluded_ids: set,
    user_id: str
) -> Optional[Dict[str, Any]]:
    """
    Select an optimal next question matching subject and target difficulty,
    avoiding already asked questions and recently attempted ones.
    """
    all_questions = load_questions()
    if not all_questions:
        return None

    # Filter by subject
    if subject and subject.lower() != "all":
        pool = [q for q in all_questions if q.get("subject", "").lower() == subject.lower()]
    else:
        pool = all_questions

    # 1. Exact difficulty match, excluding session and recent questions
    recent_ids = get_recently_answered_question_ids(user_id)
    candidates = [
        q for q in pool 
        if q.get("difficulty") == target_difficulty 
        and q["question_id"] not in excluded_ids 
        and q["question_id"] not in recent_ids
    ]

    # 2. If no fresh candidate found, relax the recent_ids constraint (still exclude current session)
    if not candidates:
        candidates = [
            q for q in pool 
            if q.get("difficulty") == target_difficulty 
            and q["question_id"] not in excluded_ids
        ]

    # 3. If still empty, search adjacent difficulty tiers
    if not candidates:
        adjacent = ["Medium"] if target_difficulty in ["Easy", "Hard"] else ["Easy", "Hard"]
        for adj in adjacent:
            candidates = [
                q for q in pool 
                if q.get("difficulty") == adj and q["question_id"] not in excluded_ids
            ]
            if candidates:
                break

    # 4. Fallback: any remaining question in pool not in current session
    if not candidates:
        candidates = [q for q in pool if q["question_id"] not in excluded_ids]

    if not candidates:
        return None

    # Pick a random candidate from the eligible pool
    return random.choice(candidates)

def sanitize_question(q: Dict[str, Any]) -> Dict[str, Any]:
    """Return question payload without revealing correct_answer or explanation."""
    return {
        "question_id": q["question_id"],
        "subject": q["subject"],
        "topic": q["topic"],
        "question_text": q["question_text"],
        "options": q["options"],
        "difficulty": q["difficulty"],
        "marks": q["marks"]
    }

def start_adaptive_session(user_id: str, subject: str, total_questions: int = 5) -> Dict[str, Any]:
    """
    Initialize an adaptive quiz session. Beginners always start with Easy questions.
    Returns session_id, first sanitized question, and session metadata.
    """
    session_id = f"sess_{secrets.token_hex(8)}"
    initial_difficulty = "Easy"
    
    first_question = pick_next_question(
        subject=subject,
        target_difficulty=initial_difficulty,
        excluded_ids=set(),
        user_id=user_id
    )

    if not first_question:
        raise ValueError(f"No questions available for subject '{subject}'.")

    ACTIVE_QUIZZES[session_id] = {
        "session_id": session_id,
        "user_id": user_id,
        "subject": subject,
        "total_questions": total_questions,
        "current_question_index": 1,
        "current_difficulty": first_question["difficulty"],
        "consecutive_correct": 0,
        "consecutive_wrong": 0,
        "asked_question_ids": [first_question["question_id"]],
        "current_question": first_question,
        "adaptive_path": [first_question["difficulty"]],
        "responses": [],
        "started_at": datetime.now().isoformat()
    }

    return {
        "session_id": session_id,
        "subject": subject,
        "total_questions": total_questions,
        "current_question_index": 1,
        "question": sanitize_question(first_question)
    }

def process_answer_submission(session_id: str, question_id: str, selected_option: str) -> Dict[str, Any]:
    """
    Evaluate user's answer, compute adaptive difficulty adjustments,
    and return detailed feedback + next question (or final completion summary).
    """
    session = ACTIVE_QUIZZES.get(session_id)
    if not session:
        raise KeyError("Quiz session expired or not found. Please start a new quiz.")

    current_q = session.get("current_question")
    if not current_q or current_q["question_id"] != question_id:
        raise ValueError("Submitted question does not match active quiz question.")

    is_correct = (selected_option.strip() == current_q["correct_answer"].strip())
    marks_earned = current_q["marks"] if is_correct else 0
    curr_diff = current_q["difficulty"]

    # --- Adaptive Algorithm ---
    # Difficulty adjustment rules:
    # 1. Easy + Correct -> Escalate to Medium
    # 2. Medium + Correct (2 consecutive) -> Escalate to Hard
    # 3. Hard + Wrong -> De-escalate to Medium
    # 4. Medium + Wrong -> De-escalate to Easy
    if is_correct:
        session["consecutive_correct"] += 1
        session["consecutive_wrong"] = 0
        
        if curr_diff == "Easy":
            next_diff = "Medium"
        elif curr_diff == "Medium":
            if session["consecutive_correct"] >= 2:
                next_diff = "Hard"
            else:
                next_diff = "Medium"
        else: # Already Hard
            next_diff = "Hard"
    else:
        session["consecutive_wrong"] += 1
        session["consecutive_correct"] = 0

        if curr_diff == "Hard":
            next_diff = "Medium"
        elif curr_diff == "Medium":
            next_diff = "Easy"
        else: # Already Easy
            next_diff = "Easy"

    session["current_difficulty"] = next_diff

    # Record response
    response_record = {
        "question_id": current_q["question_id"],
        "subject": current_q["subject"],
        "topic": current_q["topic"],
        "difficulty": current_q["difficulty"],
        "question_text": current_q["question_text"],
        "selected_option": selected_option,
        "correct_answer": current_q["correct_answer"],
        "is_correct": is_correct,
        "marks_earned": marks_earned,
        "max_marks": current_q["marks"],
        "explanation": current_q["explanation"]
    }
    session["responses"].append(response_record)

    # Check if quiz has reached target question limit
    if len(session["responses"]) >= session["total_questions"]:
        # Quiz completed! Persist attempt
        final_summary = finalize_quiz_session(session)
        del ACTIVE_QUIZZES[session_id]
        return {
            "is_completed": True,
            "is_correct": is_correct,
            "correct_answer": current_q["correct_answer"],
            "explanation": current_q["explanation"],
            "marks_earned": marks_earned,
            "summary": final_summary
        }

    # Fetch next question
    next_question = pick_next_question(
        subject=session["subject"],
        target_difficulty=next_diff,
        excluded_ids=set(session["asked_question_ids"]),
        user_id=session["user_id"]
    )

    if not next_question:
        # Fallback if no questions left in DB for this subject
        final_summary = finalize_quiz_session(session)
        del ACTIVE_QUIZZES[session_id]
        return {
            "is_completed": True,
            "is_correct": is_correct,
            "correct_answer": current_q["correct_answer"],
            "explanation": current_q["explanation"],
            "marks_earned": marks_earned,
            "summary": final_summary
        }

    session["current_question_index"] += 1
    session["current_question"] = next_question
    session["asked_question_ids"].append(next_question["question_id"])
    session["adaptive_path"].append(next_question["difficulty"])

    return {
        "is_completed": False,
        "is_correct": is_correct,
        "correct_answer": current_q["correct_answer"],
        "explanation": current_q["explanation"],
        "marks_earned": marks_earned,
        "current_question_index": session["current_question_index"],
        "total_questions": session["total_questions"],
        "next_question": sanitize_question(next_question),
        "adaptive_level": next_diff
    }

def finalize_quiz_session(session: Dict[str, Any]) -> Dict[str, Any]:
    """Compute score metrics and persist attempt to quiz_attempts.json."""
    responses = session["responses"]
    total_q = len(responses)
    correct_count = sum(1 for r in responses if r["is_correct"])
    total_score = sum(r["marks_earned"] for r in responses)
    max_score = sum(r["max_marks"] for r in responses)
    percentage = round((total_score / max_score) * 100.0, 1) if max_score > 0 else 0.0

    diff_breakdown = {"Easy": 0, "Medium": 0, "Hard": 0}
    for r in responses:
        d = r.get("difficulty", "Easy")
        diff_breakdown[d] = diff_breakdown.get(d, 0) + 1

    attempt_id = f"att_{secrets.token_hex(6)}"
    completed_at = datetime.now().isoformat()

    attempt_record = {
        "attempt_id": attempt_id,
        "user_id": session["user_id"],
        "subject": session["subject"],
        "topic": responses[0].get("topic", "General") if responses else "General",
        "total_questions": total_q,
        "correct_answers": correct_count,
        "score": total_score,
        "max_score": max_score,
        "percentage": percentage,
        "difficulty_breakdown": diff_breakdown,
        "adaptive_path": session.get("adaptive_path", []),
        "responses": responses,
        "started_at": session["started_at"],
        "completed_at": completed_at
    }

    # Save to attempts storage
    all_attempts = load_attempts()
    all_attempts.append(attempt_record)
    save_attempts(all_attempts)

    # Performance feedback message
    if percentage >= 85:
        feedback = "Outstanding performance! You demonstrated exceptional mastery across advanced concepts."
    elif percentage >= 70:
        feedback = "Great work! Solid understanding of core topics with strong potential for advanced mastery."
    elif percentage >= 50:
        feedback = "Good effort! You've grasped basic principles, but focused practice on medium and hard questions is recommended."
    else:
        feedback = "Review recommended. We've highlighted foundational topics in your Personalized Learning Path to strengthen key concepts."

    return {
        "attempt_id": attempt_id,
        "subject": session["subject"],
        "total_questions": total_q,
        "correct_answers": correct_count,
        "score": total_score,
        "max_score": max_score,
        "percentage": percentage,
        "difficulty_breakdown": diff_breakdown,
        "adaptive_path": session.get("adaptive_path", []),
        "feedback": feedback,
        "completed_at": completed_at,
        "responses": responses
    }
