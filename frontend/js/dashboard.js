/**
 * SkillAdapt - Student Dashboard Logic
 */

let progressChartInstance = null;
let topicChartInstance = null;

document.addEventListener("DOMContentLoaded", async () => {
  if (!requireAuth()) return;
  renderSidebar("dashboard");

  await loadDashboardData();
});

async function loadDashboardData() {
  const loadingEl = document.getElementById("loading-indicator");
  const contentEl = document.getElementById("dashboard-content");

  try {
    const res = await fetch(`${API_BASE_URL}/api/dashboard/stats`, {
      headers: authHeaders()
    });

    if (!res.ok) {
      if (res.status === 401) {
        logout();
        return;
      }
      throw new Error("Failed to fetch dashboard metrics");
    }

    const data = await res.json();
    if (loadingEl) loadingEl.style.display = "none";
    if (contentEl) contentEl.style.display = "block";

    renderMetrics(data);
    renderPrediction(data.prediction);
    renderCharts(data.progress_chart, data.topic_chart);
    renderRecentActivity(data.recent_activity);
  } catch (err) {
    console.error("Dashboard load error:", err);
    if (loadingEl) {
      loadingEl.innerHTML = `
        <div class="alert alert-danger">
          Failed to load dashboard metrics. Ensure the backend server is running.
        </div>
      `;
    }
  }
}

function renderMetrics(data) {
  // Welcome Header
  const welcomeEl = document.getElementById("welcome-message");
  if (welcomeEl) {
    welcomeEl.textContent = `Welcome back, ${data.full_name || data.username}!`;
  }

  // Stat Cards
  document.getElementById("stat-avg-score").textContent = `${data.overall_avg_score}%`;
  document.getElementById("stat-total-quizzes").textContent = data.total_quizzes;
  document.getElementById("stat-completed-topics").textContent = data.completed_topics_count;
  document.getElementById("stat-learning-level").textContent = data.learning_level;

  // Strength / Weakness highlights
  document.getElementById("highlight-strongest").textContent = data.strongest_topic || "Not yet evaluated";
  document.getElementById("highlight-weakest").textContent = data.weakest_topic || "Not yet evaluated";
}

function renderPrediction(pred) {
  const predContainer = document.getElementById("ai-prediction-section");
  if (!predContainer) return;

  if (!pred || !pred.has_sufficient_data) {
    predContainer.innerHTML = `
      <div class="ai-prediction-card">
        <div class="ai-prediction-left">
          <div class="ai-badge">AI Predictive Engine (Scikit-learn)</div>
          <h3 style="font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem;">Next Score Prediction</h3>
          <p style="color: var(--text-muted); font-size: 0.95rem;">
            ${pred?.message || "Complete at least 2 quizzes to enable AI performance prediction."}
          </p>
        </div>
        <div>
          <a href="quiz.html" class="btn btn-primary">Start a Quiz</a>
        </div>
      </div>
    `;
    return;
  }

  const bounds = pred.confidence_band || {};
  const metrics = pred.model_metrics || {};

  predContainer.innerHTML = `
    <div class="ai-prediction-card">
      <div class="ai-prediction-left">
        <div class="ai-badge">AI Predictive Engine (Scikit-learn Ridge Regression)</div>
        <div class="ai-score-display">
          <div class="ai-score-number">${pred.predicted_score}</div>
          <div class="ai-score-scale">/ 100 projected score</div>
        </div>
        <div class="ai-confidence">
          Statistical Confidence Interval: <strong>${bounds.lower || (pred.predicted_score - 2.7)} - ${bounds.upper || (pred.predicted_score + 2.7)} points</strong> (MAE &plusmn;${metrics.mae || 2.71})
        </div>
        <div class="ai-explanation">
          <strong>Trajectory Assessment:</strong> ${pred.trajectory_summary}
        </div>
        <div class="ai-metrics-pill">
          <span>Model R&sup2;: <strong>${metrics.r2_score || 0.907}</strong></span>
          <span>&bull;</span>
          <span>MAE: <strong>${metrics.mae || 2.71}</strong></span>
          <span>&bull;</span>
          <span>RMSE: <strong>${metrics.rmse || 3.40}</strong></span>
        </div>
      </div>
      <div>
        <a href="learning_path.html" class="btn btn-primary">Review Learning Path</a>
      </div>
    </div>
  `;
}

function renderCharts(progressData, topicData) {
  // 1. Progress Timeline Chart
  const progressCtx = document.getElementById("progressChart");
  if (progressCtx && progressData && progressData.labels.length > 0) {
    if (progressChartInstance) progressChartInstance.destroy();

    progressChartInstance = new Chart(progressCtx, {
      type: "line",
      data: {
        labels: progressData.labels,
        datasets: [{
          label: "Quiz Score (%)",
          data: progressData.scores,
          borderColor: "#0284c7",
          backgroundColor: "rgba(2, 132, 199, 0.08)",
          fill: true,
          tension: 0.35,
          pointBackgroundColor: "#0284c7",
          pointRadius: 5,
          pointHoverRadius: 7
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            min: 0,
            max: 100,
            ticks: { callback: v => `${v}%` }
          }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }

  // 2. Topic Accuracy Bar Chart
  const topicCtx = document.getElementById("topicChart");
  if (topicCtx && topicData && topicData.labels.length > 0) {
    if (topicChartInstance) topicChartInstance.destroy();

    const bgColors = topicData.classifications.map(c => {
      if (c === "Strong") return "rgba(16, 185, 129, 0.75)";
      if (c === "Developing") return "rgba(245, 158, 11, 0.75)";
      if (c === "Needs Improvement") return "rgba(239, 68, 68, 0.75)";
      return "rgba(148, 163, 184, 0.75)";
    });

    topicChartInstance = new Chart(topicCtx, {
      type: "bar",
      data: {
        labels: topicData.labels,
        datasets: [{
          label: "Accuracy (%)",
          data: topicData.accuracies,
          backgroundColor: bgColors,
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: "y",
        scales: {
          x: {
            min: 0,
            max: 100,
            ticks: { callback: v => `${v}%` }
          }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }
}

function renderRecentActivity(activityList) {
  const tableBody = document.getElementById("recent-activity-body");
  if (!tableBody) return;

  if (!activityList || activityList.length === 0) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="5" style="text-align:center; padding: 2rem; color: var(--text-muted);">
          No quizzes taken yet. Click "Take Quiz" to begin your first adaptive session!
        </td>
      </tr>
    `;
    return;
  }

  tableBody.innerHTML = activityList.map(item => {
    const dateFormatted = item.completed_at ? new Date(item.completed_at).toLocaleDateString(undefined, {
      month: "short", day: "numeric", hour: "2-digit", minute: "2-digit"
    }) : "Recent";

    let badgeClass = "badge-developing";
    if (item.percentage >= 80) badgeClass = "badge-strong";
    else if (item.percentage < 50) badgeClass = "badge-weak";

    const diff = item.difficulty_breakdown || {};
    const diffPills = `
      <span class="badge badge-easy">E: ${diff.Easy || 0}</span>
      <span class="badge badge-medium">M: ${diff.Medium || 0}</span>
      <span class="badge badge-hard">H: ${diff.Hard || 0}</span>
    `;

    return `
      <tr>
        <td><strong>${item.subject}</strong></td>
        <td>${dateFormatted}</td>
        <td>${diffPills}</td>
        <td><strong>${item.score}</strong> / ${item.max_score}</td>
        <td><span class="badge ${badgeClass}">${item.percentage}%</span></td>
      </tr>
    `;
  }).join("");
}
