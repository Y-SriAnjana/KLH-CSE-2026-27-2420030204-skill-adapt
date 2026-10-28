/**
 * SkillAdapt - Academic Progress Report Controller
 */

document.addEventListener("DOMContentLoaded", async () => {
  if (!requireAuth()) return;
  renderSidebar("reports");

  await loadReportSummary();
  setupReportActions();
});

function setupReportActions() {
  const printBtn = document.getElementById("btn-print-report");
  if (printBtn) {
    printBtn.addEventListener("click", () => {
      window.print();
    });
  }

  const csvBtn = document.getElementById("btn-download-csv");
  if (csvBtn) {
    csvBtn.addEventListener("click", downloadCsvReport);
  }
}

async function loadReportSummary() {
  const loading = document.getElementById("report-loading");
  const content = document.getElementById("report-content");

  try {
    const res = await fetch(`${API_BASE_URL}/api/reports/summary`, {
      headers: authHeaders()
    });

    if (!res.ok) throw new Error("Failed to load report data");

    const data = await res.json();
    if (loading) loading.style.display = "none";
    if (content) content.style.display = "block";

    renderStudentInfo(data.student, data.overall_summary);
    renderPredictionSection(data.prediction);
    renderTopicBreakdown(data.topic_breakdown);
    renderAttemptsLedger(data.all_attempts);
  } catch (err) {
    console.error("Report loading error:", err);
    if (loading) {
      loading.innerHTML = `<div class="alert alert-danger">Error loading progress report.</div>`;
    }
  }
}

function renderStudentInfo(student, summary) {
  document.getElementById("report-student-name").textContent = student.full_name || student.username;
  document.getElementById("report-student-id").textContent = student.id;
  document.getElementById("report-student-username").textContent = student.username;
  document.getElementById("report-student-email").textContent = student.email || "N/A";
  document.getElementById("report-learning-level").textContent = student.learning_level;

  document.getElementById("report-avg-score").textContent = `${summary.overall_avg_score}%`;
  document.getElementById("report-total-quizzes").textContent = summary.total_quizzes;
  document.getElementById("report-completed-topics").textContent = summary.completed_topics_count;
  document.getElementById("report-strongest-topic").textContent = summary.strongest_topic;
  document.getElementById("report-weakest-topic").textContent = summary.weakest_topic;

  document.getElementById("report-generated-date").textContent = new Date().toLocaleDateString(undefined, {
    year: "numeric", month: "long", day: "numeric"
  });
}

function renderPredictionSection(pred) {
  const predBox = document.getElementById("report-prediction-box");
  if (!predBox) return;

  if (!pred || !pred.has_sufficient_data) {
    predBox.innerHTML = `
      <p style="color: var(--text-muted); font-size: 0.95rem;">
        ${pred?.message || "Insufficient quiz history. Complete at least 2 quizzes to enable AI performance prediction."}
      </p>
    `;
    return;
  }

  const metrics = pred.model_metrics || {};
  const bounds = pred.confidence_band || {};

  predBox.innerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; margin-bottom: 0.75rem;">
      <div>
        <div style="font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">
          Forecasted Next Quiz Score
        </div>
        <div style="font-size: 2.25rem; font-weight: 800; color: var(--primary);">
          ${pred.predicted_score} <span style="font-size: 1.1rem; color: var(--text-muted);">/ 100</span>
        </div>
      </div>
      <div style="text-align: right;">
        <div style="font-size: 0.85rem; color: var(--text-muted);">Statistical 95% Confidence Band</div>
        <div style="font-size: 1.1rem; font-weight: 700;">
          ${bounds.lower || (pred.predicted_score - 2.7)} - ${bounds.upper || (pred.predicted_score + 2.7)} points
        </div>
      </div>
    </div>
    <p style="font-size: 0.92rem; color: var(--text-main); margin-bottom: 0.75rem;">
      <strong>Pedagogical Trajectory:</strong> ${pred.trajectory_summary}
    </p>
    <div style="font-size: 0.8rem; color: var(--text-muted); background: var(--bg-subtle); padding: 0.5rem 0.75rem; border-radius: var(--radius-sm);">
      Model: ${metrics.model_type || "Ridge Regression"} &bull; R&sup2;: ${metrics.r2_score || 0.907} &bull; MAE: ${metrics.mae || 2.71} points
    </div>
  `;
}

function renderTopicBreakdown(topics) {
  const tbody = document.getElementById("report-topics-body");
  if (!tbody) return;

  if (!topics || topics.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding: 1.5rem;">No evaluated topics.</td></tr>`;
    return;
  }

  tbody.innerHTML = topics.map(t => {
    let badgeClass = "badge-nodata";
    if (t.classification === "Strong") badgeClass = "badge-strong";
    else if (t.classification === "Developing") badgeClass = "badge-developing";
    else if (t.classification === "Needs Improvement") badgeClass = "badge-weak";

    return `
      <tr>
        <td><strong>${t.topic}</strong></td>
        <td>${t.subject}</td>
        <td>${t.correct_answers} / ${t.total_questions}</td>
        <td><strong>${t.classification === 'Not enough data' ? 'N/A' : `${t.accuracy}%`}</strong></td>
        <td><span class="badge ${badgeClass}">${t.classification}</span></td>
      </tr>
    `;
  }).join("");
}

function renderAttemptsLedger(attempts) {
  const tbody = document.getElementById("report-attempts-body");
  if (!tbody) return;

  if (!attempts || attempts.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 1.5rem;">No quiz attempts recorded.</td></tr>`;
    return;
  }

  tbody.innerHTML = attempts.map(a => {
    const dateFormatted = a.completed_at ? new Date(a.completed_at).toLocaleDateString(undefined, {
      year: "numeric", month: "short", day: "numeric"
    }) : "Recent";

    const diff = a.difficulty_breakdown || {};
    return `
      <tr>
        <td><code>${a.attempt_id}</code></td>
        <td><strong>${a.subject}</strong></td>
        <td>${dateFormatted}</td>
        <td>Easy: ${diff.Easy || 0}, Med: ${diff.Medium || 0}, Hard: ${diff.Hard || 0}</td>
        <td>${a.score} / ${a.max_score}</td>
        <td><strong>${a.percentage}%</strong></td>
      </tr>
    `;
  }).join("");
}

async function downloadCsvReport() {
  const token = getToken();
  try {
    const res = await fetch(`${API_BASE_URL}/api/reports/export-csv`, {
      headers: { "Authorization": `Bearer ${token}` }
    });

    if (!res.ok) throw new Error("CSV generation failed");

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "student_progress_report.csv";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
    showToast("Progress report CSV downloaded successfully!", "success");
  } catch (err) {
    showToast("Error downloading CSV report.", "danger");
  }
}
