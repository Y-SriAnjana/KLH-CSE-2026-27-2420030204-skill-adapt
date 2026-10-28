/**
 * SkillAdapt - Core Application Utilities & Navigation
 */

// Determine API base URL dynamically
const API_BASE_URL = window.location.origin.includes("http") ? window.location.origin : "http://127.0.0.1:8000";

// Token and User Management
function getToken() {
  return localStorage.getItem("skilladapt_token");
}

function setToken(token) {
  localStorage.setItem("skilladapt_token", token);
}

function getUser() {
  const u = localStorage.getItem("skilladapt_user");
  try {
    return u ? JSON.parse(u) : null;
  } catch (e) {
    return null;
  }
}

function setUser(user) {
  localStorage.setItem("skilladapt_user", JSON.stringify(user));
}

function removeAuth() {
  localStorage.removeItem("skilladapt_token");
  localStorage.removeItem("skilladapt_user");
}

function authHeaders() {
  const token = getToken();
  return {
    "Content-Type": "application/json",
    "Authorization": token ? `Bearer ${token}` : ""
  };
}

function requireAuth() {
  const token = getToken();
  if (!token) {
    window.location.href = "login.html";
    return false;
  }
  return true;
}

async function logout() {
  try {
    await fetch(`${API_BASE_URL}/api/auth/logout`, {
      method: "POST",
      headers: authHeaders()
    });
  } catch (e) {
    console.error("Logout error:", e);
  } finally {
    removeAuth();
    window.location.href = "login.html";
  }
}

// Unified Sidebar Navigation Renderer
function renderSidebar(activePage) {
  const user = getUser() || { username: "Student", full_name: "Student", learning_level: "Beginner" };
  const initials = (user.full_name || user.username || "ST")
    .split(" ")
    .map(n => n[0])
    .join("")
    .substring(0, 2)
    .toUpperCase();

  const navItems = [
    {
      id: "dashboard",
      label: "Dashboard",
      href: "dashboard.html",
      icon: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>`
    },
    {
      id: "quiz",
      label: "Take Quiz",
      href: "quiz.html",
      icon: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>`
    },
    {
      id: "learning_path",
      label: "Learning Path",
      href: "learning_path.html",
      icon: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>`
    },
    {
      id: "progress",
      label: "My Progress",
      href: "progress.html",
      icon: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>`
    },
    {
      id: "reports",
      label: "Reports",
      href: "reports.html",
      icon: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>`
    }
  ];

  const navHtml = navItems.map(item => `
    <a href="${item.href}" class="nav-link ${activePage === item.id ? 'active' : ''}">
      ${item.icon}
      <span>${item.label}</span>
    </a>
  `).join("");

  const sidebarEl = document.getElementById("sidebar-container");
  if (sidebarEl) {
    sidebarEl.innerHTML = `
      <aside class="sidebar">
        <div class="sidebar-header">
          <div class="brand-icon">S</div>
          <div class="brand-name">Skill<span>Adapt</span></div>
        </div>
        <nav class="sidebar-nav">
          ${navHtml}
        </nav>
        <div class="sidebar-footer">
          <div class="user-badge">
            <div class="user-avatar">${initials}</div>
            <div class="user-info">
              <div class="user-name">${user.full_name || user.username}</div>
              <div class="user-level">${user.learning_level || "Beginner"} Student</div>
            </div>
          </div>
          <button class="btn-logout" onclick="logout()">
            <svg style="width:16px;height:16px;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
            Logout
          </button>
        </div>
      </aside>
    `;
  }
}

// Toast Notification
function showToast(message, type = "info") {
  let toastContainer = document.getElementById("toast-container");
  if (!toastContainer) {
    toastContainer = document.createElement("div");
    toastContainer.id = "toast-container";
    toastContainer.style.cssText = "position: fixed; top: 20px; right: 20px; z-index: 9999; display: flex; flex-direction: column; gap: 10px;";
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement("div");
  toast.className = `alert alert-${type}`;
  toast.style.cssText = "min-width: 280px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); animation: fadeIn 0.3s ease;";
  toast.textContent = message;

  toastContainer.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transition = "opacity 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}
