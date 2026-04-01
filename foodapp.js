// Toggle buttons
const loginBtn = document.getElementById("loginBtn");
const registerBtn = document.getElementById("registerBtn");
const bubble = document.querySelector(".toggle-active");
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

function showRegister() {
  bubble.style.left = "calc(50% + 5px)";
  loginBtn.classList.remove("active");
  registerBtn.classList.add("active");
  loginForm.classList.add("hidden");
  registerForm.classList.remove("hidden");
}

function showLogin() {
  bubble.style.left = "5px";
  registerBtn.classList.remove("active");
  loginBtn.classList.add("active");
  registerForm.classList.add("hidden");
  loginForm.classList.remove("hidden");
}

loginBtn.onclick = showLogin;
registerBtn.onclick = showRegister;

// Register form submission
registerForm.addEventListener("submit", async function(e) {
  e.preventDefault();

  const username = document.getElementById("regName").value;
  const email = document.getElementById("regEmail").value;
  const password = document.getElementById("regPassword").value;

  const response = await fetch("http://localhost:3000/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password })
  });

  const data = await response.json();
  if (response.ok) {
  alert(data.message);
  showLogin(); // switches to login form automatically
} else {
  alert(data.message); // shows "You are already registered! Please log in."
}
});
// Login form submission
loginForm.addEventListener("submit", async function(e) {
  e.preventDefault();

  const email = document.getElementById("loginEmail").value;
  const password = document.getElementById("loginPassword").value;

  const response = await fetch("http://localhost:3000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  const data = await response.json();
  if (response.ok) {
  window.location.href = "home.html"; // redirects to a new page
} else {
  if (response.ok) {
  alert("Registration successful! Please login.");
  showLogin();
} else {
  alert(data.message);
};
}
});