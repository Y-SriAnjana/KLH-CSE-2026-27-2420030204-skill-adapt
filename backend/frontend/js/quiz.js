/**
 * SkillAdapt - Adaptive Quiz Controller
 */

let activeSessionId = null;
let currentQuestionData = null;
let selectedOption = null;
let isAnswerSubmitted = false;

document.addEventListener("DOMContentLoaded", async () => {
  if (!requireAuth()) return;
  renderSidebar("quiz");

  await loadSubjects();
  setupEventListeners();
});

function setupEventListeners() {
  const startBtn = document.getElementById("btn-start-quiz");
  if (startBtn) {
    startBtn.addEventListener("click", startQuiz);
  }

  const submitBtn = document.getElementById("btn-submit-answer");
  if (submitBtn) {
    submitBtn.addEventListener("click", submitAnswer);
  }

  const nextBtn = document.getElementById("btn-next-question");
  if (nextBtn) {
    nextBtn.addEventListener("click", advanceToNextQuestion);
  }
}

async function loadSubjects() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/quiz/subjects`);
    const data = await res.json();
    const select = document.getElementById("quiz-subject-select");
    if (!select) return;

    select.innerHTML = "";
    data.subjects.forEach(s => {
      const opt = document.createElement("option");
      opt.value = s.subject;
      opt.textContent = `${s.subject} (${s.total_questions} questions available)`;
      select.appendChild(opt);
    });
  } catch (err) {
    console.error("Failed to load subjects:", err);
  }
}

async function startQuiz() {
  const subject = document.getElementById("quiz-subject-select").value;
  const numQuestions = parseInt(document.getElementById("quiz-count-select").value, 10) || 5;
  const startBtn = document.getElementById("btn-start-quiz");

  startBtn.disabled = true;
  startBtn.textContent = "Initializing Adaptive Quiz...";

  try {
    const res = await fetch(`${API_BASE_URL}/api/quiz/start`, {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify({
        subject: subject,
        total_questions: numQuestions
      })
    });

    const data = await res.json();
    if (!res.ok) {
      alert(data.detail || "Unable to start quiz.");
      startBtn.disabled = false;
      startBtn.textContent = "Start Adaptive Quiz";
      return;
    }

    activeSessionId = data.session_id;
    currentQuestionData = data.question;

    // Transition view
    document.getElementById("quiz-setup-card").style.display = "none";
    document.getElementById("quiz-active-card").style.display = "block";
    document.getElementById("quiz-results-card").style.display = "none";

    renderQuestion(data.question, data.current_question_index, data.total_questions);
  } catch (err) {
    alert("Error starting quiz. Please check backend connection.");
    startBtn.disabled = false;
    startBtn.textContent = "Start Adaptive Quiz";
  }
}

function renderQuestion(q, currentIdx, totalQ) {
  isAnswerSubmitted = false;
  selectedOption = null;

  // Header info
  document.getElementById("quiz-subject-badge").textContent = q.subject;
  document.getElementById("quiz-topic-badge").textContent = q.topic;
  document.getElementById("quiz-counter").textContent = `Question ${currentIdx} of ${totalQ}`;
  
  // Progress bar
  const progressPct = ((currentIdx - 1) / totalQ) * 100;
  document.getElementById("quiz-progress-fill").style.width = `${progressPct}%`;

  // Difficulty badge
  const diffBadge = document.getElementById("quiz-difficulty-badge");
  diffBadge.textContent = q.difficulty;
  diffBadge.className = `badge badge-${q.difficulty.toLowerCase()}`;

  document.getElementById("quiz-marks-badge").textContent = `${q.marks} Mark${q.marks > 1 ? 's' : ''}`;
  document.getElementById("question-text-content").textContent = q.question_text;

  // Options list
  const optionsContainer = document.getElementById("quiz-options-container");
  optionsContainer.innerHTML = "";

  const prefixes = ["A", "B", "C", "D"];
  q.options.forEach((optText, i) => {
    const card = document.createElement("div");
    card.className = "option-card";
    card.dataset.option = optText;
    card.innerHTML = `
      <div class="option-prefix">${prefixes[i]}</div>
      <div class="option-text">${optText}</div>
    `;

    card.addEventListener("click", () => {
      if (isAnswerSubmitted) return;
      document.querySelectorAll(".option-card").forEach(c => c.classList.remove("selected"));
      card.classList.add("selected");
      selectedOption = optText;
      document.getElementById("btn-submit-answer").disabled = false;
    });

    optionsContainer.appendChild(card);
  });

  // Reset buttons & hide explanation
  document.getElementById("btn-submit-answer").style.display = "inline-flex";
  document.getElementById("btn-submit-answer").disabled = true;
  document.getElementById("btn-next-question").style.display = "none";
  document.getElementById("quiz-explanation-box").style.display = "none";
}

async function submitAnswer() {
  if (!selectedOption || isAnswerSubmitted) return;
  isAnswerSubmitted = true;

  const submitBtn = document.getElementById("btn-submit-answer");
  submitBtn.disabled = true;
  submitBtn.textContent = "Evaluating...";

  try {
    const res = await fetch(`${API_BASE_URL}/api/quiz/submit-answer`, {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify({
        session_id: activeSessionId,
        question_id: currentQuestionData.question_id,
        selected_option: selectedOption
      })
    });

    const data = await res.json();
    if (!res.ok) {
      alert(data.detail || "Error evaluating answer.");
      submitBtn.disabled = false;
      submitBtn.textContent = "Submit Answer";
      isAnswerSubmitted = false;
      return;
    }

    // Highlight options
    const optionCards = document.querySelectorAll(".option-card");
    optionCards.forEach(c => {
      c.classList.add("locked");
      const optVal = c.dataset.option;
      if (optVal === data.correct_answer) {
        c.classList.add("correct");
      }
      if (optVal === selectedOption && !data.is_correct) {
        c.classList.add("incorrect");
      }
    });

    // Show Explanation & Adaptive Adjustment Notice
    const expBox = document.getElementById("quiz-explanation-box");
    const expTitle = document.getElementById("explanation-result-title");
    const expText = document.getElementById("explanation-text");
    const adaptNotice = document.getElementById("adaptive-adjustment-notice");

    if (data.is_correct) {
      expTitle.innerHTML = `<span style="color:var(--success);">&check; Correct! (+${data.marks_earned} Marks)</span>`;
    } else {
      expTitle.innerHTML = `<span style="color:var(--danger);">&#10006; Incorrect (0 Marks)</span>`;
    }

    expText.textContent = data.explanation;

    if (!data.is_completed) {
      adaptNotice.innerHTML = `
        <div style="margin-top: 0.5rem; font-size: 0.85rem; color: var(--primary);">
          <strong>Adaptive Engine:</strong> Next question difficulty adjusted to <strong>${data.adaptive_level}</strong> based on performance.
        </div>
      `;
    } else {
      adaptNotice.innerHTML = `
        <div style="margin-top: 0.5rem; font-size: 0.85rem; color: var(--success-text);">
          <strong>Quiz Completed!</strong> Ready to see your final score.
        </div>
      `;
    }

    expBox.style.display = "block";

    // Switch buttons
    submitBtn.style.display = "none";
    const nextBtn = document.getElementById("btn-next-question");
    nextBtn.style.display = "inline-flex";

    if (data.is_completed) {
      nextBtn.textContent = "View Final Results";
      nextBtn.onclick = () => renderResults(data.summary);
    } else {
      nextBtn.textContent = "Next Question &rarr;";
      nextBtn.onclick = () => {
        currentQuestionData = data.next_question;
        renderQuestion(data.next_question, data.current_question_index, data.total_questions);
      };
    }
  } catch (err) {
    alert("Connection error evaluating answer.");
    submitBtn.disabled = false;
    submitBtn.textContent = "Submit Answer";
    isAnswerSubmitted = false;
  }
}

function advanceToNextQuestion() {
  // Handled dynamically by nextBtn.onclick
}

function renderResults(summary) {
  document.getElementById("quiz-active-card").style.display = "none";
  document.getElementById("quiz-results-card").style.display = "block";

  // Fill summary metrics
  document.getElementById("result-score-number").textContent = `${summary.score} / ${summary.max_score}`;
  document.getElementById("result-percentage").textContent = `${summary.percentage}%`;
  document.getElementById("result-feedback-text").textContent = summary.feedback;

  const diff = summary.difficulty_breakdown || {};
  document.getElementById("result-diff-breakdown").innerHTML = `
    <span class="badge badge-easy">Easy: ${diff.Easy || 0}</span>
    <span class="badge badge-medium">Medium: ${diff.Medium || 0}</span>
    <span class="badge badge-hard">Hard: ${diff.Hard || 0}</span>
  `;

  // Render question review accordion
  const reviewContainer = document.getElementById("result-review-list");
  reviewContainer.innerHTML = "";

  (summary.responses || []).forEach((r, idx) => {
    const item = document.createElement("div");
    item.className = "card";
    item.style.marginBottom = "1rem";
    item.style.padding = "1.25rem";
    item.style.borderLeft = r.is_correct ? "4px solid var(--success)" : "4px solid var(--danger)";

    item.innerHTML = `
      <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
        <span style="font-weight: 700; font-size: 0.95rem;">Q${idx + 1}. ${r.question_text}</span>
        <span class="badge badge-${r.difficulty.toLowerCase()}">${r.difficulty}</span>
      </div>
      <div style="font-size: 0.9rem; margin-bottom: 0.35rem;">
        Your answer: <strong style="color: ${r.is_correct ? 'var(--success-text)' : 'var(--danger-text)'}">${r.selected_option}</strong>
        ${!r.is_correct ? ` | Correct: <strong style="color: var(--success-text)">${r.correct_answer}</strong>` : ''}
      </div>
      <div style="font-size: 0.85rem; color: var(--text-muted); background: var(--bg-subtle); padding: 0.5rem 0.75rem; border-radius: var(--radius-sm);">
        ${r.explanation}
      </div>
    `;
    reviewContainer.appendChild(item);
  });
}
