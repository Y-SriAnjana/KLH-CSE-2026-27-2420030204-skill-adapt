# SkillAdapt: An Adaptive AI-Based Personalized Learning Assistant

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-F7931E.svg)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/Data-Pandas-150458.svg)](https://pandas.pydata.org/)
[![Chart.js](https://img.shields.io/badge/Visualizations-Chart.js-FF6384.svg)](https://www.chartjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**SkillAdapt** is an intelligent, full-stack educational web application designed for college academic project demonstrations. It dynamically personalizes computer science education by adapting quiz difficulty in real time based on student performance, classifying strengths and weaknesses, prescribing individualized learning pathways with prerequisite awareness, and forecasting future academic performance using a trained Scikit-learn regression model.

---

## Key Features

1. **Secure Student Authentication & Data Privacy**
   - Student registration, login, profile management, and logout.
   - Passwords hashed using standard library **PBKDF2-HMAC-SHA256** (100,000 iterations + unique 16-byte random salt).
   - Cryptographically random session tokens with server-side validation.
   - Strict student data isolation preventing unauthorized access to other students' records.

2. **Performance-Driven Adaptive Quiz Engine**
   - Real-time difficulty transitions (**Easy**, **Medium**, **Hard**) across 5 core subjects: **Python**, **Java**, **Data Structures**, **SQL**, and **Machine Learning**.
   - Beginners start with Easy questions.
   - High consecutive accuracy triggers escalation (Easy &rarr; Medium &rarr; Hard).
   - Errors trigger de-escalation (Hard &rarr; Medium &rarr; Easy).
   - Recency avoidance prevents recently answered questions from repeating.
   - Interactive UI displaying progress bar, question counter, marks, difficulty badge, and instant pedagogical explanations.

3. **Strength & Weakness Analysis**
   - Empirical classification of topics into:
     - **Strong**: Accuracy &ge; 80% (with at least 3 questions attempted).
     - **Developing**: Accuracy between 50% and 79%.
     - **Needs Improvement**: Accuracy &lt; 50%.
     - **Not enough data**: Displayed gracefully when fewer than 3 questions have been attempted.
   - Context-aware pedagogical recommendations for every topic.

4. **Personalized Learning Path**
   - Dynamically prioritizes topics marked *Needs Improvement* and *Developing*.
   - Evaluates prerequisite topic mastery before recommending advanced modules.
   - Provides learning objectives, estimated study time, and reference links.
   - Persistent completion toggling synchronized to `users.json`.

5. **AI Performance Predictor (Scikit-learn)**
   - Trained regression pipeline (`StandardScaler` + regularized `Ridge` regression).
   - Predicts student's next score (0&ndash;100) using real extracted features:
     - Previous Score (recent quiz average)
     - Quiz Accuracy (historical percentage)
     - Attempts Count (total quizzes taken)
     - Completion Rate (% of learning resources completed)
     - Estimated Study Hours
   - Statistical confidence interval (MAE &plusmn;2.71 points) and $R^2 = 0.9074$.
   - Transparent disclaimer identifying synthetic training data for formative self-tracking.

6. **Interactive Visualizations & Academic Reports**
   - Dynamic **Chart.js** score progression line chart and topic accuracy bar chart.
   - Downloadable student progress report in **CSV format**.
   - Printable progress transcript with dedicated `@media print` clean styling.

---

## Demo Account Credentials

A pre-seeded demonstration student account is ready for immediate evaluation:

| Field | Value |
| :--- | :--- |
| **Username** | `demo_student` |
| **Password** | `Student@123` |
| **Full Name** | Alex Morgan |
| **Role** | Intermediate Student |
| **Seeded History** | 5 completed quizzes across Python, Java, Data Structures, SQL, ML |

*(A 1-Click "Auto-Fill Demo Credentials" button is also provided on the login page).*

---

## Project Structure

```text
SkillAdapt/
├── backend/
│   ├── main.py                  # FastAPI server, static file hosting, CORS, report export
│   ├── auth.py                  # PBKDF2 hashing, session tokens, login/register logic
│   ├── quiz.py                  # Quiz REST API endpoints and session management
│   ├── adaptive_engine.py       # Adaptive difficulty algorithm, question picker, scoring
│   ├── analytics.py             # Topic classification (Strong/Developing/Weak) & dashboard stats
│   ├── predictor.py             # Scikit-learn model loading, feature extraction, predictions
│   ├── learning_path.py         # Personalized curriculum prioritization & completion toggle
│   ├── requirements.txt         # Python package dependencies
│   ├── data/
│   │   ├── users.json           # User profiles and resource completion state
│   │   ├── questions.json       # 60 questions across 5 subjects & 3 difficulty tiers
│   │   ├── quiz_attempts.json   # Full attempt history and question-by-question responses
│   │   ├── learning_resources.json # Structured curriculum resources and objectives
│   │   └── student_performance.csv # Synthetic dataset for ML regression training
│   ├── models/
│   │   ├── performance_predictor.joblib # Serialized Scikit-learn Pipeline
│   │   └── metrics.json         # Evaluation metrics (MAE, RMSE, R2, feature weights)
│   ├── scripts/
│   │   ├── seed_data.py         # Seeds demo student, questions, resources, and attempts
│   │   └── train_model.py       # Trains, evaluates, and serializes the ML regression model
│   └── tests/
│       ├── test_all.py          # Unit tests for auth, adaptive engine, analytics, ML
│       └── test_api_endpoints.py # End-to-end integration tests using FastAPI TestClient
├── frontend/
│   ├── index.html               # Welcome landing page with feature overview
│   ├── login.html               # Login page with demo credentials button
│   ├── register.html            # Registration form with skill level selection
│   ├── dashboard.html           # Main student dashboard with stats, prediction, and charts
│   ├── quiz.html                # Interactive real-time adaptive quiz interface
│   ├── learning_path.html       # Prioritized curriculum cards and completion toggles
│   ├── progress.html            # 3-column topic mastery classification & history
│   ├── reports.html             # Printable academic transcript and CSV export
│   ├── css/
│   │   └── style.css            # Light theme (soft sky-blue), responsive layouts, print CSS
│   └── js/
│       ├── app.js               # Common API helpers, token management, unified sidebar
│       ├── auth.js              # Login and registration event handlers
│       ├── dashboard.js         # Loads metrics, renders Chart.js charts and predictions
│       ├── quiz.js              # Adaptive quiz state machine and explanation feedback
│       ├── learning_path.js     # Curriculum priority filter tabs and toggle actions
│       ├── progress.js          # Classification grids and score progression chart
│       └── reports.js           # Academic report compiler, CSV download, print handler
├── README.md                    # Beginner-friendly setup, execution, and architectural guide
└── .gitignore                   # Git ignore patterns for venv, cache, and logs
```

---

## Machine Learning Model Evaluation

The model was trained on `student_performance.csv` (500 synthetic student records) using an 80/20 train/test split.

| Metric | Score | Interpretation |
| :--- | :--- | :--- |
| **Model Type** | `Ridge Regression` with `StandardScaler` | Regularized linear model preventing overfitting |
| **Mean Absolute Error (MAE)** | **2.710 points** | Average prediction deviation is under 3 marks on a 0–100 scale |
| **Root Mean Squared Error (RMSE)** | **3.402 points** | Penalizes larger outliers; demonstrates tight residual clustering |
| **Coefficient of Determination ($R^2$)** | **0.9074** | Explains over 90.7% of variance in future student scores |

### Normalized Feature Importance:
- `quiz_accuracy`: **+5.063** (strongest positive driver)
- `previous_score`: **+3.016**
- `study_hours`: **+2.968**
- `completion_rate`: **+1.741**
- `attempts_count`: **+1.046**

> **Note on Training Data**: The training dataset is synthetically generated for academic demonstration. Predictions provide formative self-tracking guidance and are not clinically or academically certified.

---

## Step-by-Step Windows Installation & Execution Guide

### Prerequisites
- **Operating System**: Windows 10 or Windows 11
- **Python**: Python 3.10, 3.11, 3.12, 3.13, or 3.14
- **Terminal**: Windows PowerShell or VS Code Integrated Terminal

---

### Step 1: Open the Project in VS Code
1. Open Visual Studio Code.
2. Select **File &rarr; Open Folder...** and choose `c:\Users\yanam\OneDrive\Desktop\ase project`.
3. Open the integrated terminal (**Ctrl + `** or **Terminal &rarr; New Terminal**).

---

### Step 2: Create and Activate Virtual Environment

In Windows PowerShell, run:

```powershell
# Create the virtual environment named .venv
python -m venv .venv

# If PowerShell blocks script execution, temporarily allow local scripts:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1
```

*(You will see `(.venv)` appear at the start of your terminal prompt).*

---

### Step 3: Install Required Dependencies

```powershell
pip install -r backend\requirements.txt
```

---

### Step 4: Seed Data and Train the ML Model (Optional - Pre-Generated)

Seed data and model weights are already included, but you can regenerate or retrain anytime:

```powershell
# 1. Regenerate realistic question bank and demo records
python backend\scripts\seed_data.py

# 2. Train and evaluate the Scikit-learn Ridge regression model
python backend\scripts\train_model.py
```

---

### Step 5: Start the FastAPI Backend Server

Run Uvicorn from the project root:

```powershell
python -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```

---

### Step 6: Access the Application

Once the server is running, open your web browser:

| Interface | Local URL |
| :--- | :--- |
| **SkillAdapt Web App** | [http://127.0.0.1:8000](http://127.0.0.1:8000) |
| **Interactive API Documentation (Swagger UI)** | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) |
| **Alternative API Documentation (ReDoc)** | [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) |

> **Alternative Frontend Hosting**: You can also open `frontend/index.html` directly in your browser or via the VS Code **Live Server** extension at `http://127.0.0.1:5500`. Full CORS headers are enabled to support local development ports.

---

### Step 7: Running the Automated Test Suite

To run all 13 automated unit and API integration tests:

```powershell
python -m unittest discover -s backend/tests -p "test_*.py" -v
```

All 13 tests will execute and output `OK`.

---

## REST API Reference

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/auth/register` | Register a new student account | No |
| `POST` | `/api/auth/login` | Authenticate student and issue session token | No |
| `POST` | `/api/auth/logout` | Invalidate current session token | Yes |
| `GET` | `/api/auth/me` | Retrieve authenticated student profile | Yes |
| `GET` | `/api/dashboard/stats` | Dashboard indicators, predictions, and Chart.js datasets | Yes |
| `GET` | `/api/analytics/topics` | Granular topic accuracy and Strong/Developing/Weak classification | Yes |
| `GET` | `/api/quiz/subjects` | List available quiz subjects and question counts | No |
| `POST` | `/api/quiz/start` | Initialize an adaptive quiz session | Yes |
| `POST` | `/api/quiz/submit-answer` | Submit answer, evaluate difficulty adjustment, get next question | Yes |
| `GET` | `/api/quiz/history` | Retrieve full history of completed student quiz attempts | Yes |
| `GET` | `/api/learning-path` | Retrieve personalized prioritized learning curriculum | Yes |
| `POST` | `/api/learning-path/toggle` | Toggle persistent completion status of a topic/resource | Yes |
| `GET` | `/api/predictor/predict` | Compute ML performance prediction and confidence intervals | Yes |
| `POST` | `/api/predictor/retrain` | Trigger retraining of Scikit-learn regression model | Yes |
| `GET` | `/api/reports/summary` | Academic summary report dataset | Yes |
| `GET` | `/api/reports/export-csv` | Download student progress report as a CSV file | Yes |

---

## Troubleshooting & FAQs

### 1. `Execution_Policies` error in PowerShell
If activating `.venv\Scripts\Activate.ps1` produces an execution policy error:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 2. Port 8000 Already in Use
If port 8000 is occupied by another process, run Uvicorn on another port (e.g. 8005):
```powershell
python -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8005 --reload
```

### 3. Missing Data Files on Fresh Clone
`backend/main.py` automatically initializes missing directories and files on startup. You can also manually re-run `python backend/scripts/seed_data.py`.

---

## License

This project is developed for college academic coursework and demonstration purposes under the MIT License.
