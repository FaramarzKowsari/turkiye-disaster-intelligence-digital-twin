const buttons = document.querySelectorAll(".lang");
const translatable = document.querySelectorAll("[data-en]");

function applyLanguage(lang) {
  translatable.forEach((node) => {
    const value = node.dataset[lang];
    if (value) node.textContent = value;
  });

  buttons.forEach((button) => {
    button.classList.toggle("active", button.dataset.lang === lang);
  });

  document.documentElement.lang = lang === "es" ? "es-ES" : lang;
  localStorage.setItem("disasterTwinLanguage", lang);
}

buttons.forEach((button) => {
  button.addEventListener("click", () => applyLanguage(button.dataset.lang));
});

const saved = localStorage.getItem("disasterTwinLanguage");
const browser = navigator.language.toLowerCase();
const initial =
  saved ||
  (browser.startsWith("tr") ? "tr" : browser.startsWith("es") ? "es" : "en");

applyLanguage(initial);
