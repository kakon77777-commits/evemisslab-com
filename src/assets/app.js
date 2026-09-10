/* evemisslab.com — colour scheme, plus the metadata filters on /ai/ index
   pages. Both are enhancements: the index is plain links by design, and every
   /ai/ list is fully visible without this file. */

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

  /* Filters: each card carries data-<facet>="a|b" attributes rendered at
     build time; a select per facet narrows the list. Nothing is fetched. */
  var roots = document.querySelectorAll("[data-filter-root]");
  Array.prototype.forEach.call(roots, function (scope) {
    var selects = scope.querySelectorAll("select[data-facet]");
    var items = scope.querySelectorAll("[data-item]");
    var count = scope.querySelector("[data-count]");
    if (!selects.length) return;

    function apply() {
      var active = [];
      Array.prototype.forEach.call(selects, function (s) {
        if (s.value) active.push([s.getAttribute("data-facet"), s.value]);
      });
      var shown = 0;
      Array.prototype.forEach.call(items, function (it) {
        var ok = active.every(function (pair) {
          var have = (it.getAttribute("data-" + pair[0]) || "").split("|");
          return have.indexOf(pair[1]) !== -1;
        });
        it.hidden = !ok;
        if (ok) shown++;
      });
      if (count) count.textContent = String(shown);
    }

    Array.prototype.forEach.call(selects, function (s) { s.addEventListener("change", apply); });
    scope.addEventListener("reset", function () { setTimeout(apply, 0); });
  });
})();
