"""
SkillAdapt - Automated Test Suite
Covers Authentication, Adaptive Quiz Engine, Analytics/Classification,
and AI Machine Learning Performance Prediction.
"""

import sys
import os
import unittest

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import (
    hash_password,
    verify_password,
    register_user,
    authenticate_user,
    create_session_token,
    invalidate_session,
    RegisterRequest,
    LoginRequest,
    ACTIVE_SESSIONS
)
from adaptive_engine import (
    start_adaptive_session,
    process_answer_submission,
    load_questions,
    load_attempts,
    ACTIVE_QUIZZES
)
from analytics import compute_student_topic_analytics, get_student_dashboard_metrics
from predictor import predict_future_performance, extract_student_features
from learning_path import get_personalized_learning_path, toggle_resource_completion

class TestSkillAdapt(unittest.TestCase):

    def setUp(self):
        self.test_username = "test_student_unit"
        self.test_password = "Password123!"

    def test_01_password_hashing(self):
        """Verify that password hashing uses unique salts and verifies correctly."""
        h1 = hash_password("Secret123")
        h2 = hash_password("Secret123")
        self.assertNotEqual(h1, h2, "Salts must ensure distinct hashes for identical passwords")
        self.assertTrue(verify_password(h1, "Secret123"))
        self.assertFalse(verify_password(h1, "WrongPassword"))

    def test_02_registration_and_authentication(self):
        """Test registration and subsequent login."""
        reg_req = RegisterRequest(
            username=self.test_username,
            password=self.test_password,
            full_name="Unit Test Student",
            email="unittest@skilladapt.edu",
            learning_level="Beginner"
        )
        try:
            user = register_user(reg_req)
            self.assertEqual(user["username"], self.test_username)
        except Exception:
            # User might already exist from previous test run
            pass

        # Valid login
        login_req = LoginRequest(username=self.test_username, password=self.test_password)
        auth_user = authenticate_user(login_req)
        self.assertIsNotNone(auth_user)
        self.assertEqual(auth_user["username"], self.test_username)

        # Invalid login
        with self.assertRaises(Exception):
            authenticate_user(LoginRequest(username=self.test_username, password="WrongPassword!"))

        # Session token generation & invalidation
        token = create_session_token(auth_user)
        self.assertIn(token, ACTIVE_SESSIONS)
        self.assertTrue(invalidate_session(token))
        self.assertNotIn(token, ACTIVE_SESSIONS)

    def test_03_adaptive_quiz_engine(self):
        """Test adaptive quiz question flow and performance-driven difficulty adaptation."""
        # Start a 3-question Python quiz
        session_info = start_adaptive_session(
            user_id="std_demo_01",
            subject="Python",
            total_questions=3
        )
        session_id = session_info["session_id"]
        q1 = session_info["question"]

        self.assertIn(session_id, ACTIVE_QUIZZES)
        self.assertEqual(q1["difficulty"], "Easy", "Adaptive quiz should start beginners with Easy")

        # Get full question to simulate answering
        curr_q = ACTIVE_QUIZZES[session_id]["current_question"]
        correct_ans = curr_q["correct_answer"]

        # 1. Submit correct answer -> Should escalate to Medium
        res1 = process_answer_submission(
            session_id=session_id,
            question_id=curr_q["question_id"],
            selected_option=correct_ans
        )
        self.assertTrue(res1["is_correct"])
        self.assertFalse(res1["is_completed"])
        self.assertEqual(res1["adaptive_level"], "Medium", "Easy + Correct should adaptively escalate to Medium")

        # 2. Submit wrong answer on question 2 -> Should de-escalate back to Easy
        q2 = res1["next_question"]
        wrong_ans = "Deliberately Wrong Answer That Never Matches"
        res2 = process_answer_submission(
            session_id=session_id,
            question_id=q2["question_id"],
            selected_option=wrong_ans
        )
        self.assertFalse(res2["is_correct"])
        self.assertFalse(res2["is_completed"])
        self.assertEqual(res2["adaptive_level"], "Easy", "Medium + Wrong should adaptively de-escalate to Easy")

        # 3. Submit question 3 (final question) -> Quiz should complete
        q3 = res2["next_question"]
        curr_q3 = ACTIVE_QUIZZES[session_id]["current_question"]
        res3 = process_answer_submission(
            session_id=session_id,
            question_id=q3["question_id"],
            selected_option=curr_q3["correct_answer"]
        )
        self.assertTrue(res3["is_completed"])
        self.assertIn("summary", res3)
        self.assertNotIn(session_id, ACTIVE_QUIZZES, "Session should be cleaned up after completion")

    def test_04_analytics_classification(self):
        """Verify strength and weakness classification thresholds."""
        analytics = compute_student_topic_analytics("std_demo_01")
        self.assertIn("topics", analytics)
        
        for topic in analytics["topics"]:
            acc = topic["accuracy"]
            total_q = topic["total_questions"]
            classification = topic["classification"]

            if total_q < 3:
                self.assertEqual(classification, "Not enough data")
            elif acc >= 80.0:
                self.assertEqual(classification, "Strong")
            elif acc >= 50.0:
                self.assertEqual(classification, "Developing")
            else:
                self.assertEqual(classification, "Needs Improvement")

    def test_05_machine_learning_prediction(self):
        """Verify that ML regression model predicts realistic future score and bounds."""
        demo_user = {
            "id": "std_demo_01",
            "username": "demo_student",
            "completed_resources": ["RES_PY_01"]
        }
        pred = predict_future_performance(demo_user)
        self.assertTrue(pred["has_sufficient_data"])
        self.assertIsNotNone(pred["predicted_score"])
        self.assertGreaterEqual(pred["predicted_score"], 0.0)
        self.assertLessEqual(pred["predicted_score"], 100.0)
        self.assertIn("model_metrics", pred)
        self.assertIn("r2_score", pred["model_metrics"])
        self.assertGreater(pred["model_metrics"]["r2_score"], 0.85)

    def test_06_learning_path_prioritization(self):
        """Verify that personalized learning path prioritizes weaker topics."""
        demo_user = {
            "id": "std_demo_01",
            "username": "demo_student",
            "completed_resources": ["RES_PY_01"]
        }
        path = get_personalized_learning_path(demo_user)
        self.assertIn("resources", path)
        resources = path["resources"]
        self.assertGreater(len(resources), 0)

        # Uncompleted high-priority resources should precede mastered resources
        first_res = resources[0]
        self.assertIn(first_res["priority_label"], ["High Priority", "Medium Priority", "Next Up"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
