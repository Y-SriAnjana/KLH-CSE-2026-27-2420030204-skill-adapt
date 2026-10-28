/**
 * SkillAdapt - Personalized Learning Path Controller
 */

let allResources = [];
let currentFilter = "all";

document.addEventListener("DOMContentLoaded", async () => {
  if (!requireAuth()) return;
  renderSidebar("learning_path");

  setupFilterTabs();
  await loadLearningPath();
});

function setupFilterTabs() {
  const tabs = document.querySelectorAll(".filter-tab");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      currentFilter = tab.dataset.filter;
      renderResources();
    });
  });
}

async function loadLearningPath() {
  const loading = document.getElementById("learning-loading");
  const container = document.getElementById("learning-container");

  try {
    const res = await fetch(`${API_BASE_URL}/api/learning-path`, {
      headers: authHeaders()
    });

    if (!res.ok) throw new Error("Failed to load learning path");

    const data = await res.json();
    allResources = data.resources || [];

    // Update progress header
    document.getElementById("path-progress-text").textContent = 
      `${data.completed_resources} of ${data.total_resources} modules completed (${data.completion_percentage}%)`;
    document.getElementById("path-progress-bar").style.width = `${data.completion_percentage}%`;

    if (loading) loading.style.display = "none";
    if (container) container.style.display = "block";

    renderResources();
  } catch (err) {
    console.error("Error:", err);
    if (loading) {
      loading.innerHTML = `<div class="alert alert-danger">Error loading personalized curriculum.</div>`;
    }
  }
}

function renderResources() {
  const listContainer = document.getElementById("resources-list");
  if (!listContainer) return;

  let filtered = allResources;
  if (currentFilter === "high") {
    filtered = allResources.filter(r => r.priority_label === "High Priority");
  } else if (currentFilter === "medium") {
    filtered = allResources.filter(r => r.priority_label === "Medium Priority");
  } else if (currentFilter === "completed") {
    filtered = allResources.filter(r => r.is_completed);
  }

  if (filtered.length === 0) {
    listContainer.innerHTML = `
      <div class="card" style="text-align: center; padding: 3rem; color: var(--text-muted);">
        No resources match the selected filter.
      </div>
    `;
    return;
  }

  listContainer.innerHTML = filtered.map(res => {
    let priorityBadgeClass = "badge-nodata";
    if (res.priority_label === "High Priority") priorityBadgeClass = "badge-weak";
    else if (res.priority_label === "Medium Priority") priorityBadgeClass = "badge-developing";
    else if (res.priority_label === "Mastered") priorityBadgeClass = "badge-strong";

    const prereqAlert = res.prerequisite_status !== "Satisfied" ? `
      <div style="font-size: 0.8rem; color: var(--warning-text); background: var(--warning-bg); padding: 0.35rem 0.65rem; border-radius: var(--radius-sm); margin-bottom: 0.75rem;">
        &Delta; ${res.prerequisite_status}
      </div>
    ` : '';

    const objectivesHtml = (res.learning_objectives || []).map(obj => `
      <li style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.25rem;">${obj}</li>
    `).join("");

    return `
      <div class="card" style="margin-bottom: 1.5rem; border-left: 4px solid ${res.is_completed ? 'var(--success)' : 'var(--primary)'};">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; flex-wrap: wrap;">
          <div>
            <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.4rem; flex-wrap: wrap;">
              <span class="badge badge-medium">${res.subject}</span>
              <span class="badge ${priorityBadgeClass}">${res.priority_label}</span>
              <span class="badge badge-nodata">&sim;${res.estimated_minutes} mins</span>
              <span class="badge badge-${res.difficulty.toLowerCase()}">${res.difficulty}</span>
            </div>
            <h3 style="font-size: 1.2rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.35rem;">
              ${res.title}
            </h3>
            <p style="color: var(--text-muted); font-size: 0.92rem; margin-bottom: 0.75rem;">
              ${res.description}
            </p>
          </div>
          <div>
            <button 
              class="btn ${res.is_completed ? 'btn-success' : 'btn-outline'}" 
              onclick="toggleCompletion('${res.resource_id}')"
              id="btn-complete-${res.resource_id}"
            >
              ${res.is_completed ? '&check; Completed' : 'Mark as Complete'}
            </button>
          </div>
        </div>

        ${prereqAlert}

        <div style="background-color: var(--bg-subtle); padding: 1rem; border-radius: var(--radius-md); margin-top: 0.75rem;">
          <div style="font-size: 0.85rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.35rem;">
            Core Learning Objectives:
          </div>
          <ul style="padding-left: 1.25rem;">
            ${objectivesHtml}
          </ul>
        </div>

        <div style="margin-top: 1rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
          <span style="font-size: 0.85rem; color: var(--text-muted);">
            Reason: <em>${res.priority_reason}</em>
          </span>
          <a href="${res.reference_url}" target="_blank" rel="noopener noreferrer" style="font-size: 0.85rem; font-weight: 600; display: inline-flex; align-items: center; gap: 0.25rem;">
            Official Documentation Reference &nearr;
          </a>
        </div>
      </div>
    `;
  }).join("");
}

async function toggleCompletion(resourceId) {
  const btn = document.getElementById(`btn-complete-${resourceId}`);
  if (btn) btn.disabled = true;

  try {
    const res = await fetch(`${API_BASE_URL}/api/learning-path/toggle`, {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify({ resource_id: resourceId })
    });

    const data = await res.json();
    if (!res.ok) throw new Error("Toggle failed");

    // Update in-memory resource state
    const target = allResources.find(r => r.resource_id === resourceId);
    if (target) {
      target.is_completed = data.is_completed;
    }

    // Refresh display
    showToast(data.is_completed ? "Module marked as completed!" : "Module marked as pending.", "success");
    await loadLearningPath();
  } catch (err) {
    showToast("Error updating module status.", "danger");
    if (btn) btn.disabled = false;
  }
}
