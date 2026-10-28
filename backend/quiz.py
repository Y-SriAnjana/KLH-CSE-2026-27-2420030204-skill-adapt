"""
SkillAdapt - Quiz Router Module
Exposes endpoints for starting adaptive quiz sessions, submitting answers,
querying subjects, and retrieving student attempt history.
"""

import os
import sys
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from auth import get_current_user
from adaptive_engine import (
    start_adaptive_session,
    process_answer_submission,
    load_attempts,
    load_questions
)

router = APIRouter(prefix="/api/quiz", tags=["Quiz"])

class StartQuizRequest(BaseModel):
    subject: str = Field(..., description="Subject name e.g. Python, Java, Data Structures, SQL, Machine Learning")
    total_questions: Optional[int] = Field(5, ge=3, le=15)

class SubmitAnswerRequest(BaseModel):
    session_id: str
    question_id: str
    selected_option: str

@router.get("/subjects")
def get_available_subjects():
    """Retrieve available subjects and their respective topics."""
    questions = load_questions()
    subjects_map: Dict[str, set] = {}
    
    for q in questions:
        subj = q.get("subject", "General")
        top = q.get("topic", "General")
        if subj not in subjects_map:
            subjects_map[subj] = set()
        subjects_map[subj].add(top)

    result = []
    for s, topics in subjects_map.items():
        result.append({
            "subject": s,
            "topics": sorted(list(topics)),
            "total_questions": sum(1 for q in questions if q.get("subject") == s)
        })
    
    return {"subjects": sorted(result, key=lambda x: x["subject"])}

@router.post("/start")
def start_quiz(payload: StartQuizRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Initialize an adaptive quiz session for the logged-in student."""
    try:
        session_data = start_adaptive_session(
            user_id=current_user["id"],
            subject=payload.subject,
            total_questions=payload.total_questions or 5
        )
        return session_data
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to start quiz: {str(e)}")

@router.post("/submit-answer")
def submit_answer(payload: SubmitAnswerRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Submit an answer to the current active question and receive adaptive feedback."""
    try:
        result = process_answer_submission(
            session_id=payload.session_id,
            question_id=payload.question_id,
            selected_option=payload.selected_option
        )
        return result
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error evaluating answer: {str(e)}")

@router.get("/history")
def get_quiz_history(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Retrieve all completed quiz attempts for the authenticated student."""
    attempts = [a for a in load_attempts() if a.get("user_id") == current_user["id"]]
    sorted_attempts = sorted(attempts, key=lambda a: a.get("completed_at", ""), reverse=True)
    return {"attempts": sorted_attempts, "total_attempts": len(sorted_attempts)}

@router.get("/attempt/{attempt_id}")
def get_attempt_details(attempt_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Retrieve detailed responses and breakdown for a specific attempt."""
    attempts = [a for a in load_attempts() if a.get("user_id") == current_user["id"]]
    for a in attempts:
        if a["attempt_id"] == attempt_id:
            return a
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt record not found.")
