class ThemeToggle {
  constructor() {
    this.toggleBtn = document.getElementById("theme-toggle");
    this.moonIcon = document.querySelector(".moon-icon");
    this.sunIcon = document.querySelector(".sun-icon");

    this.init();
  }

  init() {
    const savedTheme = localStorage.getItem("theme");
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

    if (savedTheme === "dark" || (!savedTheme && prefersDark)) {
      this.enableDarkMode();
    }

    this.bindEvents();
  }

  bindEvents() {
    if (this.toggleBtn) {
      this.toggleBtn.addEventListener("click", () => {
        this.toggleTheme();
      });
    }

    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
      if (!localStorage.getItem("theme")) {
        if (e.matches) {
          this.enableDarkMode();
        } else {
          this.enableLightMode();
        }
      }
    });
  }

  toggleTheme() {
    const isDark = document.body.classList.contains("dark-mode");

    if (isDark) {
      this.enableLightMode();
    } else {
      this.enableDarkMode();
    }

    localStorage.setItem("theme", isDark ? "light" : "dark");
  }

  enableDarkMode() {
    document.body.classList.add("dark-mode");
    document.documentElement.setAttribute("data-theme", "dark");

    if (this.moonIcon) this.moonIcon.classList.add("hidden");
    if (this.sunIcon) this.sunIcon.classList.remove("hidden");
  }

  enableLightMode() {
    document.body.classList.remove("dark-mode");
    document.documentElement.setAttribute("data-theme", "light");

    if (this.moonIcon) this.moonIcon.classList.remove("hidden");
    if (this.sunIcon) this.sunIcon.classList.add("hidden");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  new ThemeToggle();
});