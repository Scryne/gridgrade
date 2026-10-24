// Bill calculator: all in the browser, nothing is sent anywhere.
(function () {
  var root = document.getElementById("calc");
  if (!root) return;
  var states = JSON.parse(root.dataset.states), us = parseFloat(root.dataset.us);
  var sel = document.getElementById("c-state"), kwh = document.getElementById("c-kwh"), rate = document.getElementById("c-rate");
  var total = document.getElementById("c-total"), note = document.getElementById("c-note");
  Object.keys(states).sort(function (a, b) { return states[a].ad.localeCompare(states[b].ad); }).forEach(function (k) {
    var o = document.createElement("option"); o.value = k; o.textContent = states[k].ad + " (" + states[k].fiyat.toFixed(2) + "¢)"; sel.appendChild(o);
  });
  function money(x) { return "$" + x.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
  function update() {
    var st = states[sel.value], r = parseFloat(rate.value), use = parseFloat(kwh.value);
    if (!st && !(r > 0)) { total.textContent = "—"; return; }
    var price = r > 0 ? r : st.fiyat;
    if (!(use >= 0) || kwh.value === "") use = st ? st.tuketim : 0;
    var bill = use * price / 100;
    total.textContent = money(bill) + " / month";
    var parts = [Math.round(use).toLocaleString("en-US") + " kWh × " + price.toFixed(2) + "¢/kWh" + (r > 0 ? " (your rate)" : " (" + st.ad + " average)") + "."];
    if (st) {
      parts.push("At the US average of " + us.toFixed(2) + "¢ the same use costs " + money(use * us / 100) + ".");
      parts.push("Typical " + st.ad + " household: " + st.tuketim.toLocaleString("en-US") + " kWh a month.");
    }
    note.textContent = parts.join(" ");
  }
  [sel, kwh, rate].forEach(function (el) { el.addEventListener("input", update); });
  document.querySelectorAll("button.add").forEach(function (b) {
    b.addEventListener("click", function () {
      var on = b.getAttribute("aria-pressed") === "true", v = parseFloat(b.dataset.kwh), cur = parseFloat(kwh.value) || 0;
      kwh.value = Math.max(0, cur + (on ? -v : v));
      b.setAttribute("aria-pressed", String(!on));
      b.textContent = on ? "+ Add" : "✓ Added";
      update();
    });
  });
})();
