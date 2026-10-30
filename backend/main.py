"""
SkillAdapt - Main Application Entrypoint
FastAPI server unifying authentication, adaptive quiz engine, analytics,
machine learning performance prediction, learning path recommendations,
and CSV reporting.
"""

import os
import sys
import io
import csv
from typing import Dict, Any, Optional

# Ensure backend directory is in Python path regardless of execution working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from fastapi import FastAPI, Depends, HTTPException, status, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

from auth import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    register_user,
    authenticate_user,
    create_session_token,
    invalidate_session,
    get_current_user,
    ACTIVE_SESSIONS
)
from quiz import router as quiz_router
from analytics import get_student_dashboard_metrics, compute_student_topic_analytics, load_attempts
from learning_path import get_personalized_learning_path, toggle_resource_completion
from predictor import predict_future_performance
from scripts.train_model import train_and_evaluate

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Robust multi-location candidate search for frontend directory
candidate_frontend_dirs = [
    os.path.join(os.path.dirname(BASE_DIR), "frontend"), # Sibling of backend
    os.path.join(BASE_DIR, "frontend"),                 # Inside backend (isolated root deployments)
    os.path.join(os.getcwd(), "frontend"),              # Current working directory
    os.path.join(os.getcwd(), "ase project", "frontend"), # Nested inside 'ase project'
    os.path.join(os.path.dirname(BASE_DIR), "ase project", "frontend")
]
FRONTEND_DIR = None
for candidate in candidate_frontend_dirs:
    if os.path.exists(candidate) and os.path.isdir(candidate):
        FRONTEND_DIR = os.path.abspath(candidate)
        break

app = FastAPI(
    title="SkillAdapt API",
    description="Adaptive AI-Based Personalized Learning Assistant REST Backend",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup_check():
    """Ensure data files and models exist upon application launch."""
    questions_file = os.path.join(BASE_DIR, "data", "questions.json")
    if not os.path.exists(questions_file) or os.path.getsize(questions_file) == 0:
        try:
            print("[INFO] Questions file missing or empty. Seeding initial data...")
            from scripts.seed_data import seed_all
            seed_all()
        except Exception as e:
            print(f"[WARN] Startup seed data check: {e}")

    model_file = os.path.join(BASE_DIR, "models", "performance_predictor.joblib")
    if not os.path.exists(model_file) or os.path.getsize(model_file) == 0:
        try:
            print("[INFO] Model weights missing. Training performance predictor...")
            train_and_evaluate()
        except Exception as e:
            print(f"[WARN] Startup model check: {e}")

# Enable CORS for local development origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Quiz Router
app.include_router(quiz_router)

# ----------------- AUTHENTICATION ENDPOINTS -----------------

@app.post("/api/auth/register", response_model=UserResponse)
def register_endpoint(data: RegisterRequest):
    """Register a new student account."""
    user = register_user(data)
    return UserResponse(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        full_name=user["full_name"],
        learning_level=user.get("learning_level", "Beginner"),
        completed_resources=user.get("completed_resources", []),
        created_at=user["created_at"]
    )

@app.post("/api/auth/login")
def login_endpoint(credentials: LoginRequest):
    """Authenticate student credentials and return a session token."""
    user = authenticate_user(credentials)
    token = create_session_token(user)
    return {
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "full_name": user.get("full_name", user["username"]),
            "email": user.get("email", ""),
            "learning_level": user.get("learning_level", "Beginner")
        }
    }

@app.post("/api/auth/logout")
def logout_endpoint(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Terminate the current student session."""
    user_id = current_user["id"]
    # Invalidate all active tokens for this user
    tokens_to_remove = [t for t, s in ACTIVE_SESSIONS.items() if s["user_id"] == user_id]
    for t in tokens_to_remove:
        invalidate_session(t)
    return {"message": "Logged out successfully"}

@app.get("/api/auth/me", response_model=UserResponse)
def get_current_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Retrieve current student profile information."""
    return UserResponse(
        id=current_user["id"],
        username=current_user["username"],
        email=current_user.get("email", ""),
        full_name=current_user.get("full_name", current_user["username"]),
        learning_level=current_user.get("learning_level", "Beginner"),
        completed_resources=current_user.get("completed_resources", []),
        created_at=current_user.get("created_at", "")
    )

# ----------------- DASHBOARD & ANALYTICS ENDPOINTS -----------------

@app.get("/api/dashboard/stats")
def get_dashboard_stats(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Fetch high-level metrics, recent quiz activity, and chart datasets."""
    stats = get_student_dashboard_metrics(current_user)
    # Also fetch AI prediction to display on dashboard
    prediction_info = predict_future_performance(current_user)
    stats["prediction"] = prediction_info
    return stats

@app.get("/api/analytics/topics")
def get_topic_analytics(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Fetch topic-wise accuracy, strength & weakness classifications, and recommendations."""
    return compute_student_topic_analytics(current_user["id"])

# ----------------- LEARNING PATH ENDPOINTS -----------------

class ToggleResourceRequest(BaseModel):
    resource_id: str

@app.get("/api/learning-path")
def get_learning_path(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Retrieve prioritized learning curriculum and completion status for the student."""
    return get_personalized_learning_path(current_user)

@app.post("/api/learning-path/toggle")
def toggle_learning_resource(payload: ToggleResourceRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Toggle completion status of a topic/resource persistently."""
    try:
        result = toggle_resource_completion(current_user["id"], payload.resource_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# ----------------- AI PERFORMANCE PREDICTOR ENDPOINTS -----------------

@app.get("/api/predictor/predict")
def get_performance_prediction(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Generate ML predicted future score and feature impact explanation."""
    return predict_future_performance(current_user)

@app.post("/api/predictor/retrain")
def retrain_model_endpoint(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Retrain the Scikit-learn performance prediction model and return new metrics."""
    try:
        new_metrics = train_and_evaluate()
        return {
            "message": "Model retrained and evaluated successfully",
            "metrics": new_metrics
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Model retraining failed: {str(e)}")

# ----------------- REPORTS & PROGRESS ENDPOINTS -----------------

@app.get("/api/reports/summary")
def get_reports_summary(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Generate comprehensive progress report data suitable for on-screen view and printing."""
    dashboard = get_student_dashboard_metrics(current_user)
    analytics = compute_student_topic_analytics(current_user["id"])
    learning_path = get_personalized_learning_path(current_user)
    prediction = predict_future_performance(current_user)
    attempts = [a for a in load_attempts() if a.get("user_id") == current_user["id"]]

    return {
        "student": {
            "id": current_user["id"],
            "username": current_user["username"],
            "full_name": current_user.get("full_name", current_user["username"]),
            "email": current_user.get("email", ""),
            "learning_level": dashboard["learning_level"]
        },
        "overall_summary": {
            "overall_avg_score": dashboard["overall_avg_score"],
            "total_quizzes": dashboard["total_quizzes"],
            "completed_topics_count": dashboard["completed_topics_count"],
            "strongest_topic": dashboard["strongest_topic"],
            "weakest_topic": dashboard["weakest_topic"]
        },
        "prediction": prediction,
        "topic_breakdown": analytics["topics"],
        "all_attempts": sorted(attempts, key=lambda a: a.get("completed_at", ""), reverse=True)
    }

@app.get("/api/reports/export-csv")
def export_csv_report(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Generate and stream a downloadable CSV progress report."""
    user_id = current_user["id"]
    attempts = [a for a in load_attempts() if a.get("user_id") == user_id]
    sorted_attempts = sorted(attempts, key=lambda a: a.get("completed_at", ""))

    output = io.StringIO()
    writer = csv.writer(output)

    # Header section
    writer.writerow(["SkillAdapt Student Progress Report"])
    writer.writerow(["Student Username", current_user["username"]])
    writer.writerow(["Student Full Name", current_user.get("full_name", "")])
    writer.writerow(["Report Date", os.getenv("REPORT_DATE", "Current Date")])
    writer.writerow([])

    # Table columns
    writer.writerow([
        "Attempt ID",
        "Subject",
        "Topic",
        "Date Completed",
        "Questions Answered",
        "Correct Answers",
        "Score Earned",
        "Max Score",
        "Percentage (%)",
        "Easy Questions",
        "Medium Questions",
        "Hard Questions"
    ])

    for a in sorted_attempts:
        diff_map = a.get("difficulty_breakdown", {})
        writer.writerow([
            a.get("attempt_id", ""),
            a.get("subject", ""),
            a.get("topic", "General"),
            a.get("completed_at", ""),
            a.get("total_questions", 0),
            a.get("correct_answers", 0),
            a.get("score", 0),
            a.get("max_score", 0),
            a.get("percentage", 0.0),
            diff_map.get("Easy", 0),
            diff_map.get("Medium", 0),
            diff_map.get("Hard", 0)
        ])

    output.seek(0)
    filename = f"skilladapt_progress_{current_user['username']}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

# ----------------- STATIC FRONTEND HOSTING -----------------
# Serve frontend assets directly through FastAPI
if FRONTEND_DIR and os.path.exists(FRONTEND_DIR):
    print(f"[INFO] Serving frontend assets from: {FRONTEND_DIR}")
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
else:
    print("[WARN] Frontend directory could not be located; running in API-only mode.")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"Starting SkillAdapt server on http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=False)
