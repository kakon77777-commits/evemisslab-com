/* evemisslab.com — colour scheme only. The index is plain links by design. */

(function () {
  "use strict";

  var root = document.documentElement;

  function currentTheme() {
    var stored = null;
    try { stored = localStorage.getItem("eml-theme"); } catch (e) { /* private mode */ }
    if (stored === "light" || stored === "dark") return stored;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  var button = document.querySelector("[data-theme-toggle]");
  if (button) {
    button.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("eml-theme", next); } catch (e) { /* private mode */ }
    });
  }
})();
