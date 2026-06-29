/* Trustworthy Agentic Systems — client-side browse/filter/search.
   Loads entries.json (built from data/ by scripts/build_site.py) and renders a
   faceted, searchable list. No dependencies, no build step beyond the JSON.

   One script, two views, set by `<body data-view>`:
     - "resources" : canon (papers/classics/courses/oss), faceted sidebar.
     - "incidents" : incident log only, search + list, newest first.
*/

(() => {
  "use strict";

  const VIEW = document.body.dataset.view === "incidents" ? "incidents" : "resources";

  // Facets shown in the sidebar, in order. `field` is the entry key.
  // Incidents view has no sidebar, so it uses no facets.
  const FACET_DEFS = VIEW === "incidents" ? [] : [
    { key: "sprs", field: "sprs", title: "SPRS guarantee" },
    { key: "harness_layer", field: "harness_layer", title: "Harness layer" },
    { key: "type", field: "type", title: "Type" },
    { key: "open_problems", field: "open_problems", title: "Open problem" },
  ];

  const state = {
    q: "",
    sort: VIEW === "incidents" ? "year-desc" : "year-desc",
    selected: {},
  };
  let DATA = null;
  let BASE = [];  // entries scoped to the current view

  const $ = (sel) => document.querySelector(sel);
  const el = (tag, props = {}, kids = []) => {
    const n = Object.assign(document.createElement(tag), props);
    for (const k of [].concat(kids)) n.append(k);
    return n;
  };

  function asList(v) { return Array.isArray(v) ? v : v == null ? [] : [v]; }

  function labelMap(axis) {
    const m = new Map();
    for (const { id, label } of (DATA.taxonomy[axis] || [])) m.set(id, label);
    return m;
  }

  // Entries belonging to this view: incidents-only, or everything-but-incidents.
  function scopeEntries(entries) {
    return VIEW === "incidents"
      ? entries.filter((e) => e.type === "incidents")
      : entries.filter((e) => e.type !== "incidents");
  }

  // The "type" facet should not advertise incidents on the resources view.
  function facetOptions(key) {
    const opts = DATA.taxonomy[key] || [];
    if (key === "type") return opts.filter((o) => o.id !== "incidents");
    return opts;
  }

  // --- Filtering -----------------------------------------------------------

  function entryMatches(e) {
    // Each facet: OR within the facet, AND across facets.
    for (const def of FACET_DEFS) {
      const chosen = state.selected[def.key];
      if (!chosen || chosen.size === 0) continue;
      const vals = asList(e[def.field]);
      if (![...chosen].some((c) => vals.includes(c))) return false;
    }
    if (state.q) {
      const hay = [
        e.title, e.summary, e.org, e.venue,
        ...(e.authors || []), ...(e.tags || []),
      ].join(" ").toLowerCase();
      if (!state.q.split(/\s+/).every((t) => hay.includes(t))) return false;
    }
    return true;
  }

  // Sort key: incidents carry a date string, canon carries a year.
  function timeKey(e) {
    if (e.year) return e.year;
    if (e.date) return Number(String(e.date).slice(0, 4)) || 0;
    return 0;
  }

  function sortEntries(list) {
    const by = {
      "year-desc": (a, b) => timeKey(b) - timeKey(a) || (b.date || "").localeCompare(a.date || "") || a.title.localeCompare(b.title),
      "year-asc": (a, b) => timeKey(a) - timeKey(b) || (a.date || "").localeCompare(b.date || "") || a.title.localeCompare(b.title),
      "title": (a, b) => a.title.localeCompare(b.title),
    }[state.sort];
    return [...list].sort(by);
  }

  // --- Rendering -----------------------------------------------------------

  function highlight(text) {
    const frag = document.createDocumentFragment();
    const terms = state.q.split(/\s+/).filter(Boolean);
    if (!terms.length) { frag.append(text); return frag; }
    const re = new RegExp("(" + terms.map((t) =>
      t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|") + ")", "ig");
    let last = 0, m;
    while ((m = re.exec(text)) !== null) {
      if (m.index > last) frag.append(text.slice(last, m.index));
      frag.append(el("mark", { textContent: m[0] }));
      last = m.index + m[0].length;
      if (m.index === re.lastIndex) re.lastIndex++;
    }
    if (last < text.length) frag.append(text.slice(last));
    return frag;
  }

  function card(e, layerLabels, sprsLabels) {
    const head = el("div", { className: "card-head" }, [
      el("h3", { className: "card-title" },
        el("a", { href: e.url, target: "_blank", rel: "noopener" }, highlight(e.title))),
      el("span", { className: "card-type", textContent: typeLabel(e.type) }),
    ]);

    const metaBits = [];
    if (e.authors && e.authors.length)
      metaBits.push(e.authors.length > 1 ? `${e.authors[0]} et al.` : e.authors[0]);
    else if (e.org) metaBits.push(e.org);
    if (e.venue) metaBits.push(e.venue);
    if (e.year) metaBits.push(String(e.year));
    else if (e.date) metaBits.push(e.date);  // incidents carry a date, not a year
    const meta = el("p", { className: "card-meta", textContent: metaBits.join("  ·  ") });

    const summary = el("p", { className: "card-summary" }, highlight(e.summary || ""));

    const foot = el("div", { className: "card-foot" });
    for (const s of asList(e.sprs))
      foot.append(el("span", { className: `chip sprs ${s}`, textContent: sprsLabels.get(s) || s }));
    for (const l of asList(e.harness_layer))
      foot.append(el("span", { className: "chip layer", textContent: layerLabels.get(l) || l }));

    const links = el("span", { className: "card-links" });
    if (e.code) links.append(el("a", { href: e.code, target: "_blank", rel: "noopener", textContent: "code" }));
    if (links.childNodes.length) foot.append(links);

    return el("li", { className: "card" }, [head, meta, summary, foot]);
  }

  function typeLabel(t) {
    const found = (DATA.taxonomy.type || []).find((x) => x.id === t);
    return found ? found.label : t;
  }

  function renderList() {
    const layerLabels = labelMap("harness_layer");
    const sprsLabels = labelMap("sprs");
    const matched = sortEntries(BASE.filter(entryMatches));

    const list = $("#list");
    list.replaceChildren(...matched.map((e) => card(e, layerLabels, sprsLabels)));

    $("#empty").hidden = matched.length > 0;
    const noun = VIEW === "incidents" ? "incident" : "entry";
    const nounP = VIEW === "incidents" ? "incidents" : "entries";
    if ($("#count"))
      $("#count").replaceChildren(
        el("strong", { textContent: String(matched.length) }),
        ` of ${BASE.length} ${BASE.length === 1 ? noun : nounP}`);

    const anyFilter = state.q || FACET_DEFS.some((d) => state.selected[d.key]?.size);
    if ($("#clear")) $("#clear").hidden = !anyFilter;
  }

  // Live per-option counts reflect the OTHER active facets (classic faceted search).
  function optionCount(def, value) {
    return BASE.filter((e) => {
      for (const other of FACET_DEFS) {
        if (other.key === def.key) continue;
        const chosen = state.selected[other.key];
        if (!chosen || !chosen.size) continue;
        const vals = asList(e[other.field]);
        if (![...chosen].some((c) => vals.includes(c))) return false;
      }
      if (state.q) {
        const hay = [e.title, e.summary, e.org, e.venue,
          ...(e.authors || []), ...(e.tags || [])].join(" ").toLowerCase();
        if (!state.q.split(/\s+/).every((t) => hay.includes(t))) return false;
      }
      return asList(e[def.field]).includes(value);
    }).length;
  }

  function renderFacets() {
    const container = $("#facets");
    if (!container) return;
    container.replaceChildren();
    for (const def of FACET_DEFS) {
      const options = facetOptions(def.key);
      const ul = el("ul");
      for (const opt of options) {
        const n = optionCount(def, opt.id);
        const checked = state.selected[def.key]?.has(opt.id) || false;
        // Zero-count options stay visible but greyed: for a map of the field,
        // the gaps (e.g. a layer with no canon yet) are signal, not noise.
        const dead = n === 0 && !checked;
        const input = el("input", { type: "checkbox", checked, disabled: dead });
        if (!dead) input.addEventListener("change", () => toggle(def.key, opt.id));
        const label = el("label", { className: dead ? "empty-opt" : "" }, [
          input,
          el("span", { className: "fl", textContent: opt.label }),
          el("span", { className: "fc", textContent: String(n) }),
        ]);
        ul.append(label);
      }
      if (ul.childNodes.length)
        container.append(el("div", { className: "facet" },
          [el("h3", { textContent: def.title }), ul]));
    }
  }

  function toggle(key, id) {
    const set = state.selected[key] || (state.selected[key] = new Set());
    set.has(id) ? set.delete(id) : set.add(id);
    if (!set.size) delete state.selected[key];
    render();
  }

  function render() { renderFacets(); renderList(); }

  // Preselect facets from URL query (e.g. resources.html?sprs=security).
  function applyUrlFilters() {
    const params = new URLSearchParams(location.search);
    for (const def of FACET_DEFS) {
      const raw = params.get(def.key);
      if (!raw) continue;
      const valid = new Set(facetOptions(def.key).map((o) => o.id));
      for (const v of raw.split(",")) {
        if (valid.has(v)) (state.selected[def.key] ||= new Set()).add(v);
      }
    }
  }

  // --- Wiring --------------------------------------------------------------

  function attach() {
    const search = $("#search");
    if (search) {
      let t;
      search.addEventListener("input", (ev) => {
        clearTimeout(t);
        t = setTimeout(() => { state.q = ev.target.value.trim().toLowerCase(); render(); }, 120);
      });
    }
    if ($("#sort"))
      $("#sort").addEventListener("change", (ev) => { state.sort = ev.target.value; renderList(); });
    if ($("#clear"))
      $("#clear").addEventListener("click", () => {
        state.q = ""; state.selected = {}; if (search) search.value = ""; render();
      });
  }

  fetch("./entries.json")
    .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then((data) => {
      DATA = data;
      BASE = scopeEntries(data.entries || []);
      applyUrlFilters();
      attach();
      render();
    })
    .catch((err) => {
      $("#list").replaceChildren(el("li", { className: "card" },
        el("p", { textContent:
          "Could not load entries.json. Run `python scripts/build_site.py`, then serve this folder." })));
      console.error(err);
    });
})();
