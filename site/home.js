/* Home landing: fill the stat counters from entries.json. Degrades gracefully
   (the markup ships with em-dash placeholders) if the fetch fails. */
(() => {
  "use strict";
  fetch("./entries.json")
    .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then((data) => {
      const entries = data.entries || [];
      const incidents = entries.filter((e) => e.type === "incidents").length;
      const resources = entries.length - incidents;
      const layers = (data.taxonomy?.harness_layer || []).length;

      const nums = document.querySelectorAll("#stats .num");
      // Order matches the markup: Resources, Incidents, SPRS axes, Harness layers.
      if (nums[0]) nums[0].textContent = String(resources);
      if (nums[1]) nums[1].textContent = String(incidents);
      if (nums[3]) nums[3].textContent = String(layers);
    })
    .catch((err) => console.error("home stats:", err));
})();
