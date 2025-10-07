// Login sahifasi
const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const role = document.getElementById("role").value;
    const username = document.getElementById("username").value;

    localStorage.setItem("role", role);
    localStorage.setItem("username", username);

    window.location.href = "home.html";
  });
}

// Dashboard
const role = localStorage.getItem("role");
const username = localStorage.getItem("username");

// Menyu rollarini boshqarish
document.addEventListener("DOMContentLoaded", () => {
  if (role) {
    // Profil ma'lumotlari
    const profileName = document.getElementById("profileName");
    const profileRole = document.getElementById("profileRole");
    if (profileName) profileName.textContent = username;
    if (profileRole) profileRole.textContent = role;

    // Menyudan role bo‘yicha yashirish
    document.querySelectorAll("#menu li").forEach((li) => {
      if (!li.classList.contains(role) && li.classList.length > 0) {
        li.style.display = "none";
      }
    });
  }

  // Logout
  const logoutBtn = document.getElementById("logout");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      localStorage.clear();
      window.location.href = "index.html";
    });
  }
});
