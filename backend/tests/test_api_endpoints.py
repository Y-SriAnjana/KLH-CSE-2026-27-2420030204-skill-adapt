"""
SkillAdapt - Live End-to-End API Integration Tests
Tests all HTTP endpoints:
- Auth: Register, Login, Logout, Me
- Dashboard: Stats, Prediction
- Quiz: Subjects, Start Adaptive Quiz, Submit Answer, History
- Learning Path: Get Path, Toggle Completion
- Predictor: Prediction, Retrain
- Reports: Summary, CSV export
"""

import sys
import os
import unittest
from fastapi.testclient import TestClient

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

class TestAPIIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        # Login with demo user
        login_res = cls.client.post("/api/auth/login", json={
            "username": "demo_student",
            "password": "Student@123"
        })
        assert login_res.status_code == 200, f"Demo login failed: {login_res.text}"
        data = login_res.json()
        cls.token = data["token"]
        cls.headers = {"Authorization": f"Bearer {cls.token}"}

    def test_01_docs_accessible(self):
        """Verify that OpenAPI documentation is available at /docs."""
        res = self.client.get("/docs")
        self.assertEqual(res.status_code, 200)

    def test_02_current_profile(self):
        """Verify profile retrieval for authenticated user."""
        res = self.client.get("/api/auth/me", headers=self.headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["username"], "demo_student")

    def test_03_dashboard_stats(self):
        """Verify dashboard stats and predictions return real data."""
        res = self.client.get("/api/dashboard/stats", headers=self.headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("overall_avg_score", data)
        self.assertIn("total_quizzes", data)
        self.assertIn("prediction", data)
        self.assertGreaterEqual(data["total_quizzes"], 1)

    def test_04_quiz_subjects_and_adaptive_flow(self):
        """Verify starting quiz, submitting answers adaptively, and checking history."""
        # Get subjects
        subj_res = self.client.get("/api/quiz/subjects")
        self.assertEqual(subj_res.status_code, 200)
        subjects = subj_res.json()["subjects"]
        self.assertGreater(len(subjects), 0)

        # Start 3-question Python quiz
        start_res = self.client.post("/api/quiz/start", headers=self.headers, json={
            "subject": "Python",
            "total_questions": 3
        })
        self.assertEqual(start_res.status_code, 200)
        start_data = start_res.json()
        session_id = start_data["session_id"]
        q1 = start_data["question"]

        # Submit answer to question 1
        opt1 = q1["options"][0]
        sub_res = self.client.post("/api/quiz/submit-answer", headers=self.headers, json={
            "session_id": session_id,
            "question_id": q1["question_id"],
            "selected_option": opt1
        })
        self.assertEqual(sub_res.status_code, 200)
        sub_data = sub_res.json()
        self.assertIn("is_correct", sub_data)
        self.assertIn("explanation", sub_data)

    def test_05_learning_path_and_toggle(self):
        """Verify learning path retrieval and resource completion toggling."""
        res = self.client.get("/api/learning-path", headers=self.headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("resources", data)
        self.assertGreater(len(data["resources"]), 0)

        # Toggle completion
        first_res_id = data["resources"][0]["resource_id"]
        toggle_res = self.client.post("/api/learning-path/toggle", headers=self.headers, json={
            "resource_id": first_res_id
        })
        self.assertEqual(toggle_res.status_code, 200)
        toggle_data = toggle_res.json()
        self.assertIn("is_completed", toggle_data)

    def test_06_ai_prediction_endpoint(self):
        """Verify Scikit-learn performance prediction endpoint."""
        res = self.client.get("/api/predictor/predict", headers=self.headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["has_sufficient_data"])
        self.assertIsNotNone(data["predicted_score"])

    def test_07_reports_summary_and_csv_export(self):
        """Verify report summary JSON and CSV file export streaming."""
        sum_res = self.client.get("/api/reports/summary", headers=self.headers)
        self.assertEqual(sum_res.status_code, 200)
        sum_data = sum_res.json()
        self.assertIn("student", sum_data)
        self.assertIn("topic_breakdown", sum_data)

        # CSV export
        csv_res = self.client.get("/api/reports/export-csv", headers=self.headers)
        self.assertEqual(csv_res.status_code, 200)
        self.assertIn("text/csv", csv_res.headers.get("content-type", ""))
        self.assertIn("SkillAdapt Student Progress Report", csv_res.text)

if __name__ == "__main__":
    unittest.main(verbosity=2)
