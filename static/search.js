// Header search: loads search.json on first focus, matches all words, keyboard navigable.
(function () {
  var box = document.querySelector(".search");
  if (!box) return;
  var input = box.querySelector("input"), list = box.querySelector("#q-results"), data = null, active = -1;
  function norm(s) { return s.toLowerCase().normalize("NFKD").replace(/[̀-ͯ]/g, "").replace(/&/g, " and "); }
  function load() {
    if (data) return Promise.resolve(data);
    return fetch(box.dataset.index).then(function (r) { return r.json(); }).then(function (d) {
      data = d.map(function (r) { return { name: r[0], ctx: r[1], url: r[2], key: norm(r[0] + " " + r[1]) }; });
      return data;
    });
  }
  function render(items) {
    list.innerHTML = "";
    active = -1;
    items.forEach(function (it, i) {
      var li = document.createElement("li"), a = document.createElement("a"), span = document.createElement("span");
      a.href = it.url; a.textContent = it.name; a.setAttribute("role", "option"); a.id = "qr" + i;
      span.textContent = it.ctx; a.appendChild(span); li.appendChild(a); list.appendChild(li);
    });
    list.hidden = items.length === 0;
    input.setAttribute("aria-expanded", String(items.length > 0));
  }
  function search() {
    var q = norm(input.value.trim());
    if (q.length < 2) { render([]); return; }
    var words = q.split(/\s+/);
    load().then(function (d) {
      var hits = [];
      for (var i = 0; i < d.length && hits.length < 40; i++) {
        if (words.every(function (w) { return d[i].key.indexOf(w) !== -1; })) hits.push(d[i]);
      }
      hits.sort(function (a, b) { return (norm(a.name).indexOf(words[0]) === 0 ? 0 : 1) - (norm(b.name).indexOf(words[0]) === 0 ? 0 : 1); });
      render(hits.slice(0, 12));
    });
  }
  input.setAttribute("role", "combobox");
  input.setAttribute("aria-controls", "q-results");
  input.setAttribute("aria-expanded", "false");
  input.addEventListener("focus", load, { once: true });
  input.addEventListener("input", search);
  input.addEventListener("keydown", function (e) {
    var links = list.querySelectorAll("a");
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      if (!links.length) return;
      e.preventDefault();
      active = (active + (e.key === "ArrowDown" ? 1 : -1) + links.length) % links.length;
      links.forEach(function (l, i) { l.setAttribute("aria-selected", String(i === active)); });
      input.setAttribute("aria-activedescendant", links[active].id);
    } else if (e.key === "Enter" && links.length) {
      e.preventDefault();
      window.location = links[Math.max(active, 0)].href;
    } else if (e.key === "Escape") { render([]); }
  });
  document.addEventListener("click", function (e) { if (!box.contains(e.target)) render([]); });
})();
