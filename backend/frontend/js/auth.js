/**
 * SkillAdapt - Authentication Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");
  const demoBtn = document.getElementById("btn-fill-demo");
  const alertBox = document.getElementById("auth-alert");

  function showAlert(msg, isError = true) {
    if (!alertBox) return;
    alertBox.textContent = msg;
    alertBox.className = `alert ${isError ? 'alert-danger' : 'alert-success'}`;
    alertBox.style.display = "block";
  }

  // Auto-fill demo student credentials
  if (demoBtn) {
    demoBtn.addEventListener("click", () => {
      const uField = document.getElementById("username");
      const pField = document.getElementById("password");
      if (uField) uField.value = "demo_student";
      if (pField) pField.value = "Student@123";
      if (alertBox) alertBox.style.display = "none";
    });
  }

  // Handle Login
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const username = document.getElementById("username").value.trim();
      const password = document.getElementById("password").value;

      if (!username || !password) {
        showAlert("Please enter both username and password.");
        return;
      }

      try {
        const res = await fetch(`${API_BASE_URL}/api/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password })
        });

        const data = await res.json();
        if (!res.ok) {
          showAlert(data.detail || "Authentication failed. Please verify credentials.");
          return;
        }

        setToken(data.token);
        setUser(data.user);
        window.location.href = "dashboard.html";
      } catch (err) {
        showAlert("Cannot connect to backend server. Ensure Uvicorn is running on port 8000.");
      }
    });
  }

  // Handle Register
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const fullName = document.getElementById("full_name").value.trim();
      const username = document.getElementById("username").value.trim();
      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value;
      const confirmPassword = document.getElementById("confirm_password").value;
      const level = document.getElementById("learning_level").value;

      if (!fullName || !username || !email || !password) {
        showAlert("Please fill in all required fields.");
        return;
      }

      if (password !== confirmPassword) {
        showAlert("Passwords do not match.");
        return;
      }

      if (password.length < 6) {
        showAlert("Password must be at least 6 characters long.");
        return;
      }

      try {
        const res = await fetch(`${API_BASE_URL}/api/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            full_name: fullName,
            username,
            email,
            password,
            learning_level: level
          })
        });

        const data = await res.json();
        if (!res.ok) {
          showAlert(data.detail || "Registration failed.");
          return;
        }

        showAlert("Account created successfully! Redirecting to login...", false);
        setTimeout(() => {
          window.location.href = "login.html";
        }, 1200);
      } catch (err) {
        showAlert("Network error connecting to backend service.");
      }
    });
  }
});
