/**
 * SkillAdapt - Progress & Mastery Analytics Controller
 */

let progressChart = null;

document.addEventListener("DOMContentLoaded", async () => {
  if (!requireAuth()) return;
  renderSidebar("progress");

  await loadProgressAnalytics();
});

async function loadProgressAnalytics() {
  const loading = document.getElementById("progress-loading");
  const content = document.getElementById("progress-content");

  try {
    const [topicsRes, historyRes] = await Promise.all([
      fetch(`${API_BASE_URL}/api/analytics/topics`, { headers: authHeaders() }),
      fetch(`${API_BASE_URL}/api/quiz/history`, { headers: authHeaders() })
    ]);

    const topicsData = await topicsRes.json();
    const historyData = await historyRes.json();

    if (loading) loading.style.display = "none";
    if (content) content.style.display = "block";

    renderClassificationGrids(topicsData.topics || []);
    renderHistoryTable(historyData.attempts || []);
    renderProgressChart(historyData.attempts || []);
  } catch (err) {
    console.error("Progress loading error:", err);
    if (loading) {
      loading.innerHTML = `<div class="alert alert-danger">Error loading progress analytics.</div>`;
    }
  }
}

function renderClassificationGrids(topics) {
  const strongContainer = document.getElementById("grid-strong");
  const developingContainer = document.getElementById("grid-developing");
  const weakContainer = document.getElementById("grid-weak");

  const strongList = topics.filter(t => t.classification === "Strong");
  const developingList = topics.filter(t => t.classification === "Developing");
  const weakList = topics.filter(t => t.classification === "Needs Improvement" || t.classification === "Not enough data");

  function renderCards(list, colorClass) {
    if (list.length === 0) {
      return `<p style="color: var(--text-muted); font-size: 0.9rem; padding: 0.5rem 0;">No topics in this category.</p>`;
    }
    return list.map(t => {
      const isNoData = t.classification === "Not enough data";
      return `
        <div class="card" style="margin-bottom: 0.85rem; padding: 1rem; border-left: 3px solid ${isNoData ? '#94a3b8' : `var(--${colorClass})`};">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
            <strong style="font-size: 0.95rem;">${t.topic}</strong>
            <span class="badge ${isNoData ? 'badge-nodata' : (colorClass === 'success' ? 'badge-strong' : (colorClass === 'warning' ? 'badge-developing' : 'badge-weak'))}">
              ${isNoData ? 'Not enough data' : `${t.accuracy}%`}
            </span>
          </div>
          <div style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.35rem;">
            Subject: ${t.subject} &bull; ${t.correct_answers} of ${t.total_questions} questions correct
          </div>
          <div style="font-size: 0.82rem; color: var(--text-main);">
            ${t.recommendation}
          </div>
        </div>
      `;
    }).join("");
  }

  if (strongContainer) strongContainer.innerHTML = renderCards(strongList, "success");
  if (developingContainer) developingContainer.innerHTML = renderCards(developingList, "warning");
  if (weakContainer) weakContainer.innerHTML = renderCards(weakList, "danger");
}

function renderHistoryTable(attempts) {
  const tbody = document.getElementById("history-table-body");
  if (!tbody) return;

  if (attempts.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6" style="text-align: center; padding: 2rem; color: var(--text-muted);">
          No quiz history found.
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = attempts.map((a, idx) => {
    const dateFormatted = a.completed_at ? new Date(a.completed_at).toLocaleDateString(undefined, {
      year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit"
    }) : "Recent";

    const diff = a.difficulty_breakdown || {};
    const diffBadge = `
      <span class="badge badge-easy">E: ${diff.Easy || 0}</span>
      <span class="badge badge-medium">M: ${diff.Medium || 0}</span>
      <span class="badge badge-hard">H: ${diff.Hard || 0}</span>
    `;

    let badgeClass = "badge-developing";
    if (a.percentage >= 80) badgeClass = "badge-strong";
    else if (a.percentage < 50) badgeClass = "badge-weak";

    return `
      <tr>
        <td><strong>#${attempts.length - idx}</strong></td>
        <td><strong>${a.subject}</strong></td>
        <td>${dateFormatted}</td>
        <td>${diffBadge}</td>
        <td><strong>${a.score}</strong> / ${a.max_score} (${a.total_questions} Qs)</td>
        <td><span class="badge ${badgeClass}">${a.percentage}%</span></td>
      </tr>
    `;
  }).join("");
}

function renderProgressChart(attempts) {
  const ctx = document.getElementById("progressChartCanvas");
  if (!ctx || attempts.length === 0) return;

  // Chronological order
  const chronological = [...attempts].reverse();
  const labels = chronological.map((a, i) => `Quiz #${i+1} (${a.subject})`);
  const scores = chronological.map(a => a.percentage);

  if (progressChart) progressChart.destroy();

  progressChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [{
        label: "Score Percentage (%)",
        data: scores,
        borderColor: "#0284c7",
        backgroundColor: "rgba(2, 132, 199, 0.1)",
        fill: true,
        tension: 0.3,
        pointRadius: 5,
        pointBackgroundColor: "#0284c7"
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
      }
    }
  });
}
