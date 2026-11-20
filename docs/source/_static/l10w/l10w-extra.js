/*
 * The L10 lecture page's docs-only "Try it" panels (user, 2026-11-20), for sections the class deck cut: the two
 * errors, Stanley, the steering delay, saturation, MPC, the trajectory cost, the two timings, the pedal split and
 * the actuators. Hand-written: the panels are lectures/lecture10/widgets/extra/*.html, and they use the generated
 * panels' helpers (window.L10W, from l10w-core.js) and the MPC data (window.L10W_EXTRA, l10w-extra-data.js).
 * Every number is the lecture's (its section on the page), or says on the panel that it was chosen for the example.
 * Animations run only while their drawing is on screen, and not at all under prefers-reduced-motion.
 */
(function () {
  "use strict";
  var W = window.L10W; if (!W) return;
  var el = W.el, txt = W.txt, tag = W.tag, halo = W.halo, poly = W.poly, f = W.f, nt = W.nt, tex = W.tex, C = W.C;
  var reduce = W.reduce, carIcon = W.carIcon, q = W.q;
  var PURPLE = "#7B5EA7", BRAKE = "#7D3C98", CAP = "#9A6212", CARB = "#9B1B1B", PARKED = "#2D6CA2", GHOST = "#C9D2DC";
  var $ = function (id) { return document.getElementById(id); };
  var val = function (id) { return +$(id).value; };
  var deg = function (r) { return r * 180 / Math.PI; };
  function clear(s) { while (s.firstChild) s.removeChild(s.firstChild); }
  function arrowHead(s, x, y, ang, col, size) { var h = size || 12;
    el(s, "path", { d: "M" + x + "," + y + " L" + (x - h * Math.cos(ang - 0.45)) + "," + (y - h * Math.sin(ang - 0.45)) + " L" + (x - h * Math.cos(ang + 0.45)) + "," + (y - h * Math.sin(ang + 0.45)) + "z", fill: col }); }
  function arrow(s, x1, y1, x2, y2, col, w, both) { el(s, "line", { x1: x1, y1: y1, x2: x2, y2: y2, stroke: col, "stroke-width": w || 3 });
    var a = Math.atan2(y2 - y1, x2 - x1); arrowHead(s, x2, y2, a, col); if (both) arrowHead(s, x1, y1, a + Math.PI, col); }
  /* an arc around (cx, cy) from screen angle a0 to a1 (radians, y down) */
  function arc(s, cx, cy, r, a0, a1, col, w) { var sw = a1 > a0 ? 1 : 0, big = Math.abs(a1 - a0) > Math.PI ? 1 : 0;
    return el(s, "path", { d: "M" + (cx + r * Math.cos(a0)) + "," + (cy + r * Math.sin(a0)) + " A" + r + "," + r + " 0 " + big + " " + sw + " " + (cx + r * Math.cos(a1)) + "," + (cy + r * Math.sin(a1)), fill: "none", stroke: col, "stroke-width": w || 2.5 }); }
  /* buttons in a host span; returns set(v) */
  function choice(host, items, onPick, initial) { var bs = items.map(function (it) { var b = document.createElement("button"); b.textContent = it[0];
      b.addEventListener("click", function (e) { e.stopPropagation(); set(it[1]); onPick(it[1]); }); host.appendChild(b); return [b, it[1]]; });
    function set(v) { bs.forEach(function (p) { p[0].classList.toggle("on", p[1] === v); p[0].setAttribute("aria-pressed", p[1] === v ? "true" : "false"); }); }
    set(initial); return set; }
  /* run fn(dt) every frame while the element is on screen; returns {start, stop} */
  function animator(node, fn) { var seen = !window.IntersectionObserver, raf = null, on = false, last = 0;
    function loop(now) { var dt = Math.min(0.1, (now - last) / 1000); last = now; var go = fn(dt); if (go === false) on = false; raf = (on && seen) ? requestAnimationFrame(loop) : null; }
    function kick() { if (on && seen && !raf) { last = performance.now(); raf = requestAnimationFrame(loop); } }
    if (window.IntersectionObserver) new IntersectionObserver(function (es) { seen = es[0].isIntersecting; kick(); }).observe(node);
    return { start: function () { if (reduce) return false; on = true; kick(); return true; }, stop: function () { on = false; if (raf) cancelAnimationFrame(raf); raf = null; }, running: function () { return on; } }; }
  function ifPanel(id, fn) { if ($(id)) { try { fn(); } catch (e) { if (window.console) console.error("l10w-extra " + id, e); } } }

  /* ---------- 1. The two errors (section "Measure How Far Off the Path: Two Errors"): a straight path (chosen),
     the rear axle d m left of it, the AV turned by h degrees from the path's direction ---------- */
  ifPanel("xe-svg", function () {
    var s = $("xe-svg"), S = 52, Y0 = 236, XA = 330;
    function draw() { var d = val("xe-d"), hd = val("xe-h"), th = hd * Math.PI / 180, ya = Y0 - d * S; clear(s);
      el(s, "line", { x1: 0, y1: Y0, x2: 1100, y2: Y0, stroke: C.muted, "stroke-width": 3, "stroke-dasharray": "14 10" });
      arrow(s, 1000, Y0, 1080, Y0, C.muted, 3);
      txt(s, 1080, Y0 + 32, "path", 20, C.muted, "end");
      carIcon(s, "av", XA + 1.35 * S * Math.cos(th), ya - 1.35 * S * Math.sin(th), 4.5 * S, -hd, GHOST);
      /* 1: the nearest path point, with a square mark */
      el(s, "path", { d: "M" + (XA + 12) + "," + Y0 + " l0," + (d >= 0 ? -12 : 12) + " l-12,0", fill: "none", stroke: C.ink, "stroke-width": 2 });
      el(s, "circle", { cx: XA, cy: Y0, r: 7, fill: C.ink });
      tag(s, XA - 34, Y0 + (d >= 0 ? 30 : -30), 1);
      /* 2: the cross-track error, square to the path */
      if (Math.abs(d) > 0.08) { arrow(s, XA - 70, Y0, XA - 70, ya, C.ink, 3, true);
        el(s, "line", { x1: XA - 80, y1: ya, x2: XA - 6, y2: ya, stroke: C.ink, "stroke-width": 1.2, "stroke-dasharray": "3 4" });
        tag(s, XA - 104, (Y0 + ya) / 2, 2); }
      /* 3: the heading error, between the path's direction (dotted) and the AV's heading */
      var L = 2.9 * S, hx = XA + L * Math.cos(th), hy = ya - L * Math.sin(th);
      el(s, "line", { x1: XA, y1: ya, x2: XA + L, y2: ya, stroke: C.muted, "stroke-width": 2.5, "stroke-dasharray": "3 6" });
      arrow(s, XA, ya, hx, hy, C.ink, 3.5);
      if (Math.abs(hd) >= 1) { var r = 2.2 * S; arc(s, XA, ya, r, 0, -th, C.ink, 2.5);
        var m = -th / 2, rt = r + 30; tag(s, XA + rt * Math.cos(m), ya + rt * Math.sin(m) + (hd > 0 ? -6 : 6), 3); }
      el(s, "circle", { cx: XA, cy: ya, r: 7, fill: C.ink });
      var psi = -th;
      tex("xe-read", "e = " + (d > 0 ? "+" : "") + nt(d, 2) + "\\text{ m}" + (Math.abs(d) < 0.005 ? "\\text{ (on the path)}" : d > 0 ? "\\text{ (left of the path)}" : "\\text{ (right of the path)}") +
        "\\qquad \\psi_e = " + (psi > 0 ? "+" : "") + nt(deg(psi), 0) + "^\\circ = " + nt(psi, 3) + "\\text{ rad}"); }
    ["xe-d", "xe-h"].forEach(function (id) { $(id).addEventListener("input", draw); }); draw();
  });

  /* ---------- 2. Stanley (section "Steer from the Front Axle"): delta = psi_e - arctan(k e / (v + k_s)), k_s = 1 m/s,
     k from the lecture's runs (0.5, 1, 4), cut to the 0.7 rad steering limit ---------- */
  ifPanel("xs-svg", function () {
    var s = $("xs-svg"), S = 80, Y0 = 195, XF = 640, L = 2.875, KS = 1, k = 1;
    function preset(p) { $("xs-psi").value = p[0]; $("xs-e").value = p[1]; $("xs-v").value = p[2]; draw(); }
    choice($("xs-pre"), [["the lecture's moment", "run"], ["drawn larger: 1.0 m, 15°", "big"]], function (v) { preset(v === "run" ? [-0.234, 0.212, 5.22] : [0.262, 1.0, 5.22]);   /* the docs figure: heading 15° below the path's direction */ }, "run");
    var setK = choice($("xs-k"), [["0.5", 0.5], ["1", 1], ["4", 4]], function (v) { k = v; draw(); }, 1);
    function draw() { var psi = val("xs-psi"), e = val("xs-e"), v = val("xs-v"), th = -psi;   /* path direction 0: heading = -psi_e */
      var term = Math.atan(k * e / (v + KS)), d = psi - term, dc = Math.max(-0.7, Math.min(0.7, d)), yf = Y0 - e * S;
      var xr = XF - L * S * Math.cos(th), yr = yf + L * S * Math.sin(th); clear(s);
      el(s, "line", { x1: 0, y1: Y0, x2: 1100, y2: Y0, stroke: C.muted, "stroke-width": 3, "stroke-dasharray": "14 10" });
      arrow(s, 1010, Y0, 1085, Y0, C.muted, 3);
      txt(s, 1085, Y0 + 32, "path", 20, C.muted, "end");
      carIcon(s, "av", xr + 1.35 * S * Math.cos(th), yr - 1.35 * S * Math.sin(th), 4.5 * S, deg(-th), GHOST);
      el(s, "line", { x1: xr, y1: yr, x2: XF, y2: yf, stroke: C.ink, "stroke-width": 2 });
      el(s, "circle", { cx: xr, cy: yr, r: 6, fill: C.ink });
      /* e: front axle to the path, purple */
      if (Math.abs(e) > 0.06) { arrow(s, XF, Y0, XF, yf, PURPLE, 3, true); halo(txt(s, XF - 0.55 * S - 16, (Y0 + yf) / 2 + 8, "e", 24, PURPLE, "end", { "font-style": "italic", "font-weight": 700 }));
        el(s, "line", { x1: XF - 0.55 * S - 12, y1: (Y0 + yf) / 2, x2: XF - 4, y2: (Y0 + yf) / 2, stroke: PURPLE, "stroke-width": 1.2 }); }
      el(s, "circle", { cx: XF, cy: Y0, r: 5, fill: C.muted });
      /* the path's direction at the front axle (dotted), the heading (v), psi_e (red) */
      var R = 2.6 * S; el(s, "line", { x1: XF, y1: yf, x2: XF + R, y2: yf, stroke: C.muted, "stroke-width": 2.5, "stroke-dasharray": "3 6" });
      var hx = XF + R * Math.cos(th), hy = yf - R * Math.sin(th); arrow(s, XF, yf, hx, hy, C.ink, 3.5);
      halo(txt(s, hx + 12 * Math.cos(th), hy - 12 * Math.sin(th) + 8, "v", 24, C.ink, "start", { "font-style": "italic", "font-weight": 700 }));
      if (Math.abs(psi) > 0.01) { var ra = 1.9 * S; arc(s, XF, yf, ra, -th, 0, C.bad, 3);
        var mid = -th / 2, pl = halo(txt(s, XF + (ra + 30) * Math.cos(mid), yf + (ra + 30) * Math.sin(mid) + 8, "ψ", 24, C.bad, "middle", { "font-style": "italic", "font-weight": 700 }));
        var sub = document.createElementNS(W.NS, "tspan"); sub.setAttribute("baseline-shift", "sub"); sub.setAttribute("font-size", "17"); sub.textContent = "e"; pl.appendChild(sub); }
      /* the front wheel at delta from the heading, black */
      var wa = th + dc, wl = 0.55 * S;
      el(s, "line", { x1: XF - wl * Math.cos(wa), y1: yf + wl * Math.sin(wa), x2: XF + wl * Math.cos(wa), y2: yf - wl * Math.sin(wa), stroke: C.ink, "stroke-width": 10, "stroke-linecap": "round" });
      el(s, "line", { x1: XF, y1: yf, x2: XF + 1.3 * S * Math.cos(wa), y2: yf - 1.3 * S * Math.sin(wa), stroke: C.ink, "stroke-width": 1.8, "stroke-dasharray": "6 5" });
      if (Math.abs(dc) > 0.01) { var rd = 1.15 * S; arc(s, XF, yf, rd, -th, -wa, C.ink, 2.5);
        /* the label at the end of the wheel's dashed line, off the dotted path direction */
        halo(txt(s, XF + 1.3 * S * Math.cos(wa) + 14, wa <= 0.05 ? Math.max(yf - 1.3 * S * Math.sin(wa), Y0) + 34 : yf - 1.3 * S * Math.sin(wa) - 12, "δ", 24, C.ink, "start", { "font-style": "italic", "font-weight": 700 })); }
      el(s, "circle", { cx: XF, cy: yf, r: 7, fill: PURPLE });
      var side = d < 0 ? "\\text{ right}" : d > 0 ? "\\text{ left}" : "";
      tex("xs-read", "\\delta = " + nt(psi, 3) + " - \\arctan\\frac{" + nt(k, 1) + " \\times " + nt(e, 3) + "}{" + nt(v, 2) + " + 1} = " + nt(psi, 3) + " - " + (term < 0 ? "(" + nt(term, 3) + ")" : nt(term, 3)) +
        " = " + nt(d, 3) + "\\text{ rad } (" + nt(deg(d), 1) + "^\\circ" + side + ")" + (Math.abs(d) > 0.7 ? "\\text{: cut to the 0.7 rad limit}" : "")); }
    ["xs-psi", "xs-e", "xs-v"].forEach(function (id) { $(id).addEventListener("input", draw); }); draw();
  });

  /* ---------- 3. The steering delay (section "Measure the Steering Delay"): the command jumps at t = 0; the wheel
     waits the delay, then covers 1 - e^(-(t - delay)/tau); models from the section's table ---------- */
  ifPanel("xd-svg", function () {
    var s = $("xd-svg"), M = [0.2, 0.2], GX = 70, GY = 30, GW = 640, GH = 250, T0 = -0.1, T1 = 1.2;
    choice($("xd-model"), [["Lincoln MKZ, measured: 0.2 s, 0.2 s", "mkz"], ["Autoware's MPC: 0.24 s, 0.27 s", "aw"], ["our simulation: 0.1 s, 0.2 s", "sim"]],
      function (v) { M = { mkz: [0.2, 0.2], aw: [0.24, 0.27], sim: [0.1, 0.2] }[v]; draw(); }, "mkz");
    function share(t) { return t < M[0] ? 0 : 1 - Math.exp(-(t - M[0]) / M[1]); }
    function X(t) { return GX + (t - T0) / (T1 - T0) * GW; } function Y(y) { return GY + GH - y * GH; }
    function draw() { var t = val("xd-t"), sh = share(t); clear(s);
      el(s, "line", { x1: GX, y1: Y(0), x2: GX + GW, y2: Y(0), stroke: C.muted, "stroke-width": 1.5 });
      el(s, "line", { x1: X(0), y1: GY, x2: X(0), y2: Y(0), stroke: C.muted, "stroke-width": 1.5 });
      [0.4, 0.8, 1.2].forEach(function (v) { txt(s, X(v), Y(0) + 24, nt(v, 1), 17, C.muted); }); txt(s, X(0), Y(0) + 24, "0", 17, C.muted);
      [0.63, 1].forEach(function (v) { el(s, "line", { x1: X(0) - 5, y1: Y(v), x2: X(0), y2: Y(v), stroke: C.muted, "stroke-width": 1.5 }); txt(s, X(0) - 10, Y(v) + 6, v === 0.63 ? "0.63" : String(v), 17, C.muted, "end"); });
      txt(s, GX + GW + 26, Y(0) + 6, "t (s)", 17, C.muted, "start");
      poly(s, [[X(T0), Y(0)], [X(0), Y(0)], [X(0), Y(1)], [X(T1), Y(1)]], { stroke: C.muted, "stroke-width": 2.5, "stroke-dasharray": "8 6", fill: "none" });
      var full = [], done = []; for (var u = T0; u <= T1 + 1e-9; u += 0.005) { full.push([X(u), Y(share(u))]); if (u <= t) done.push([X(u), Y(share(u))]); }
      poly(s, full, { stroke: C.edge, "stroke-width": 2.5, fill: "none" }); if (done.length > 1) poly(s, done, { stroke: C.ink, "stroke-width": 4, fill: "none" });
      arrow(s, X(0), Y(0) - 26, X(M[0]), Y(0) - 26, C.ink, 2, true); tag(s, (X(0) + X(M[0])) / 2, Y(0) - 52, 1);
      var tc = M[0] + M[1]; el(s, "circle", { cx: X(tc), cy: Y(0.632), r: 6, fill: C.ink }); tag(s, X(tc) + 30, Y(0.632) + 26, 2);
      el(s, "line", { x1: X(t), y1: GY, x2: X(t), y2: Y(0), stroke: C.live, "stroke-width": 2.5 });
      el(s, "circle", { cx: X(t), cy: Y(sh), r: 8, fill: C.live, stroke: "#fff", "stroke-width": 2 });
      /* the front wheel from above: the new commanded angle drawn 30 degrees (chosen, so it shows) */
      var cx = 920, cy = 160, A = 30 * Math.PI / 180, a = (t >= 0 ? sh : 0) * A, R = 120;
      el(s, "line", { x1: cx, y1: cy, x2: cx + R, y2: cy, stroke: C.edge, "stroke-width": 2 });
      el(s, "line", { x1: cx, y1: cy, x2: cx + R * Math.cos(A), y2: cy + R * Math.sin(A), stroke: C.muted, "stroke-width": 2.5, "stroke-dasharray": "8 6" });
      el(s, "line", { x1: cx - 60 * Math.cos(a), y1: cy - 60 * Math.sin(a), x2: cx + 60 * Math.cos(a), y2: cy + 60 * Math.sin(a), stroke: C.ink, "stroke-width": 22, "stroke-linecap": "round" });
      txt(s, cx, cy - 92, t >= 0 ? "the wheel: " + nt(100 * sh, 0) + " % of the way" : "no command yet", 19, C.ink, "middle", { "font-weight": 600 });
      txt(s, cx + 70, cy + 120, "dashed: the command", 17, C.muted, "middle");
      tex("xd-read", "t = " + nt(t, 2) + "\\text{ s}: " + (t < 0 ? "\\text{before the command}" : t < M[0] ? "\\text{the wheel has not moved yet (delay } " + nt(M[0], 2) + "\\text{ s)}" :
        "1 - e^{-(" + nt(t, 2) + " - " + nt(M[0], 2) + ")/" + nt(M[1], 2) + "} = " + nt(sh, 2) + "\\text{ of the way}") +
        (t > 0 ? "\\qquad \\text{at 8 m/s: } 8 \\times " + nt(t, 2) + " = " + nt(8 * t, 2) + "\\text{ m driven}" : "")); }
    var an = animator(s, function (dt) { var t = val("xd-t") + dt / 3; if (t > 1.2) { $("xd-t").value = 1.2; draw(); return false; } $("xd-t").value = t; draw(); });
    $("xd-t").addEventListener("input", function () { an.stop(); draw(); });
    $("xd-play").addEventListener("click", function (e) { e.stopPropagation(); $("xd-t").value = -0.1; draw(); an.start(); });
    draw();
  });

  /* ---------- 4. Saturation (section "Hit the Limit"): throttle = min(u, 0.75); push = 4 x throttle (3 m/s^2 at
     the limit, as the section says) ---------- */
  ifPanel("xt-svg", function () {
    var s = $("xt-svg"), B = 270, H = 220, UMAX = 5;
    function draw() { var u = val("xt-u"), th = Math.min(u, 0.75), push = 4 * th; clear(s);
      var defs = el(s, "defs", {}), pat = el(defs, "pattern", { id: "xt-hatch", width: 10, height: 10, patternUnits: "userSpaceOnUse", patternTransform: "rotate(45)" });
      el(pat, "rect", { width: 10, height: 10, fill: "#fff" }); el(pat, "line", { x1: 0, y1: 0, x2: 0, y2: 10, stroke: C.bad, "stroke-width": 4 });
      function Y(v, max) { return B - v / max * H; }
      el(s, "line", { x1: 40, y1: B, x2: 1060, y2: B, stroke: C.muted, "stroke-width": 2 });
      /* u asked */
      var cap = Y(0.75, UMAX);
      el(s, "rect", { x: 120, y: Y(Math.min(u, 0.75), UMAX), width: 150, height: B - Y(Math.min(u, 0.75), UMAX), fill: C.ok });
      if (u > 0.75) el(s, "rect", { x: 120, y: Y(u, UMAX), width: 150, height: cap - Y(u, UMAX), fill: "url(#xt-hatch)", stroke: C.bad, "stroke-width": 2 });
      txt(s, 195, B + 30, "u asked: " + nt(u, 2), 20, C.ink, "middle", { "font-weight": 600 });
      /* throttle used */
      el(s, "rect", { x: 450, y: Y(th, UMAX), width: 150, height: B - Y(th, UMAX), fill: u > 0.75 ? CAP : C.ok });
      txt(s, 525, B + 30, "throttle: " + nt(th, 2), 20, C.ink, "middle", { "font-weight": 600 });
      el(s, "line", { x1: 90, y1: cap, x2: 640, y2: cap, stroke: C.ink, "stroke-width": 2, "stroke-dasharray": "3 5" });
      halo(txt(s, 640, cap - 10, "limit 0.75", 18, C.ink, "end"));
      if (u > 0.75) halo(txt(s, 290, Math.min(cap - 12, (Y(u, UMAX) + cap) / 2 + 6), "goes nowhere: " + nt(u - 0.75, 2), 18, C.bad, "start", { "font-weight": 600 }));
      /* push, m/s^2, scale to 3 */
      el(s, "rect", { x: 820, y: B - push / 3 * (H * 0.6), width: 150, height: push / 3 * (H * 0.6), fill: u > 0.75 ? CAP : C.ok });
      txt(s, 895, B + 30, "push: " + nt(push, 2) + " m/s²", 20, C.ink, "middle", { "font-weight": 600 });
      txt(s, 895, B - H * 0.6 - 14, "most: 3 m/s²", 17, C.muted, "middle");
      tex("xt-read", "\\text{throttle} = \\min(" + nt(u, 2) + ", 0.75) = " + nt(th, 2) + "\\qquad \\text{push} = 4 \\times " + nt(th, 2) + " = " + nt(push, 2) + "\\text{ m/s}^2" +
        (u > 0.75 ? "\\qquad " + nt(u - 0.75, 2) + "\\text{ of } u \\text{ changes nothing}" : "")); }
    $("xt-u").addEventListener("input", draw); draw();
  });

  /* ---------- 5. MPC (sections "729 Steering Plans" to "Score Each Plan"): the stored 729 plans, stepped through,
     a zoom on the branch angle 1 = 0, and the cheapest kept; three sliders pick any plan ---------- */
  ifPanel("xm-svg", function () {
    var D = window.L10W_EXTRA; if (!D) return;
    var s = $("xm-svg"), SW = 1100, SH = 560, cur = 0, view = null, raf = null;
    var FULL = [68, 100, -14, 6], ZOOM = [75, 99.5, -9, 6];
    var STEPS = [
      ["1. Measured: the AV 2 m before the curve, at " + nt(D.pose.v, 2) + " m/s.", ZOOM],
      ["2. Predict, the first second: 9 branches, one per value of angle 1.", ZOOM],
      ["3. Zoom on angle 1 = 0 rad: at 1 s, 9 branches, one per value of angle 2.", ZOOM],
      ["4. After angle 2 = −0.4 rad: at 2 s, 9 branches again, one per angle 3.", ZOOM],
      ["5. Every plan predicted and scored: 9 × 9 × 9 = 729.", FULL],
      ["6. Keep the lowest score, 0.186: (0, −0.4, 0). Apply its first 0.05 s.", FULL]];
    var G = D.grid, idx = D.step_idx;
    function planOf(a, b, c) { var r = function (v) { return Math.round(v * 10) / 10; }; return D.plans.filter(function (p) { return r(p[0][0]) === r(a) && r(p[0][1]) === r(b) && r(p[0][2]) === r(c); })[0]; }
    function mapper(v) { var sx = SW / (v[1] - v[0]), sy = SH / (v[3] - v[2]), sc = Math.min(sx, sy), ox = (SW - (v[1] - v[0]) * sc) / 2, oy = (SH - (v[3] - v[2]) * sc) / 2;
      return { X: function (x) { return ox + (x - v[0]) * sc; }, Y: function (y) { return SH - oy - (y - v[2]) * sc; }, sc: sc }; }
    function pts(p, upto, m) { var o = []; for (var i = 0; i < idx.length && idx[i] <= upto; i++) o.push([m.X(p[3][i][0] / 100), m.Y(p[3][i][1] / 100)]); return o; }
    function draw() { var m = mapper(view), L = D.lane; clear(s);
      el(s, "rect", { x: 0, y: 0, width: SW, height: SH, fill: "#fff" });
      [-1, 1].forEach(function (side) { var e = []; for (var i = 0; i < L.x.length; i++) e.push([m.X(L.x[i] - side * D.lane_half * Math.sin(L.h[i])), m.Y(L.y[i] + side * D.lane_half * Math.cos(L.h[i]))]); poly(s, e, { stroke: C.ink, "stroke-width": 2, fill: "none" }); });
      poly(s, L.x.map(function (x, i) { return [m.X(x), m.Y(L.y[i])]; }), { stroke: C.muted, "stroke-width": 2, "stroke-dasharray": "10 8", fill: "none" });
      var P = D.pose; carIcon(s, "av", m.X(P.x + 1.35 * Math.cos(P.theta)), m.Y(P.y + 1.35 * Math.sin(P.theta)), 4.5 * m.sc, -deg(P.theta), GHOST);
      var gray = { stroke: C.muted, "stroke-width": 1.6, fill: "none", opacity: 0.55 };
      if (cur === 1) G.forEach(function (a) { poly(s, pts(planOf(a, 0, 0), 20, m), gray); });
      if (cur === 2) { G.forEach(function (a) { if (a !== 0) poly(s, pts(planOf(a, 0, 0), 20, m), { stroke: C.edge, "stroke-width": 1.4, fill: "none" }); });
        G.forEach(function (b) { poly(s, pts(planOf(0, b, 0), 40, m), gray); }); poly(s, pts(planOf(0, 0, 0), 20, m), { stroke: C.ok, "stroke-width": 4, fill: "none" }); }
      if (cur === 3) { G.forEach(function (b) { if (b !== -0.4) poly(s, pts(planOf(0, b, 0), 40, m), { stroke: C.edge, "stroke-width": 1.4, fill: "none" }); });
        G.forEach(function (c) { poly(s, pts(planOf(0, -0.4, c), 60, m), gray); }); poly(s, pts(planOf(0, -0.4, 0), 40, m), { stroke: C.ok, "stroke-width": 4, fill: "none" }); }
      if (cur >= 4) D.plans.forEach(function (p) { poly(s, pts(p, 60, m), { stroke: C.muted, "stroke-width": 0.8, fill: "none", opacity: 0.35 }); });
      if (cur === 5) { var b = D.plans[D.best]; poly(s, pts(b, 60, m), { stroke: C.ok, "stroke-width": 5, fill: "none" });
        [20, 40].forEach(function (k) { var i = idx.indexOf(k); el(s, "circle", { cx: m.X(b[3][i][0] / 100), cy: m.Y(b[3][i][1] / 100), r: 7, fill: C.ok, stroke: "#fff", "stroke-width": 2 }); }); }
      if (cur >= 2 && cur <= 3) [20, 40].forEach(function (k) { if (cur === 2 && k === 40) return; var p = cur === 2 ? planOf(0, 0, 0) : planOf(0, -0.4, 0), i = idx.indexOf(k);
        el(s, "circle", { cx: m.X(p[3][i][0] / 100), cy: m.Y(p[3][i][1] / 100), r: 7, fill: C.ink, stroke: "#fff", "stroke-width": 2 }); });
      var pk = planOf(val("xm-a1"), val("xm-a2"), val("xm-a3")); if (pk && cur >= 4) poly(s, pts(pk, 60, m), { stroke: C.live, "stroke-width": 4, fill: "none", "stroke-dasharray": "10 6" });
      el(s, "circle", { cx: m.X(P.x), cy: m.Y(P.y), r: 7, fill: C.ink });
      txt(s, 14, 30, cur >= 4 ? "gray: the predicted paths; green: the cheapest; teal dashed: the plan you pick" : cur >= 2 ? "green: the branch followed; dark dots: where the held angle changes" : "", 18, C.muted, "start");
      $("xm-step").textContent = STEPS[cur][0]; }
    function goTo(k) { cur = Math.max(0, Math.min(STEPS.length - 1, k)); var from = view ? view.slice() : STEPS[cur][1], to = STEPS[cur][1], t0 = performance.now();
      cancelAnimationFrame(raf); if (reduce || !view) { view = to.slice(); draw(); return; }
      (function run() { var a = Math.min(1, (performance.now() - t0) / 700), e = a < 0.5 ? 2 * a * a : 1 - 2 * (1 - a) * (1 - a);
        view = from.map(function (v, i) { return v + (to[i] - v) * e; }); draw(); if (a < 1) raf = requestAnimationFrame(run); })(); }
    function pick() { var a = [val("xm-a1"), val("xm-a2"), val("xm-a3")], p = planOf(a[0], a[1], a[2]); if (!p) return;
      var rank = 1 + D.plans.filter(function (o) { return o[2] < p[2]; }).length, st = a.reduce(function (x, y) { return x + y * y; }, 0);
      tex("xm-pick", "\\begin{aligned}&(" + a.map(function (v) { return nt(v, 1); }).join(", ") + "):\\ \\text{rank " + rank + " of 729}" + (rank === 1 ? "\\text{, the cheapest}" : "") +
        "\\\\ &\\text{path error } " + nt(p[1], 3) + " + \\text{steering } " + nt(st, 2) + "\\\\ &= " + nt(p[2], 3) + "\\end{aligned}"); if (cur >= 4) draw(); }
    tex("xm-read", "\\text{score} = \\underbrace{\\textstyle\\sum_{60\\text{ steps}} e^2 \\times 0.05}_{\\text{path error}} + \\underbrace{\\delta_1^2 + \\delta_2^2 + \\delta_3^2}_{\\text{steering}}");
    $("xm-back").addEventListener("click", function (e) { e.stopPropagation(); goTo(cur - 1); });
    $("xm-next").addEventListener("click", function (e) { e.stopPropagation(); goTo(cur + 1); });
    ["xm-a1", "xm-a2", "xm-a3"].forEach(function (id) { $(id).addEventListener("input", pick); });
    goTo(0); pick();
  });

  /* ---------- 6. The trajectory cost (section "Tune the Cost"): the first plan's 18 lateral moves from rest at
     d = 0, end offsets and durations from the lecture's samples, scored C_d = k_j J + k_t T + k_d (d1 - 3.5)^2,
     J = 720 d1^2 / T^5 ---------- */
  ifPanel("xc-svg", function () {
    var s = $("xc-svg"), S = W.DATA.traj.SAMPLES, D1 = S.d1, TT = S.T, GX = 80, GY = 44, GW = 820, GH = 270, DMIN = -0.8, DMAX = 4.4;
    function X(t) { return GX + t / 5 * GW; } function Y(d) { return GY + GH - (d - DMIN) / (DMAX - DMIN) * GH; }
    function cands(kj, kt, kd) { var o = []; D1.forEach(function (d1) { TT.forEach(function (T) { var J = 720 * d1 * d1 / Math.pow(T, 5); o.push({ d1: d1, T: T, J: J, c: kj * J + kt * T + kd * (d1 - 3.5) * (d1 - 3.5) }); }); });
      return o.sort(function (a, b) { return a.c - b.c; }); }
    function draw() { var kj = val("xc-kj"), kt = val("xc-kt"), kd = val("xc-kd"), all = cands(kj, kt, kd), b = all[0]; clear(s);
      [0, 3.5].forEach(function (d) { el(s, "line", { x1: GX, y1: Y(d), x2: GX + GW, y2: Y(d), stroke: C.muted, "stroke-width": 1.5, "stroke-dasharray": "8 6" }); });
      el(s, "line", { x1: GX, y1: GY + GH, x2: GX + GW, y2: GY + GH, stroke: C.muted, "stroke-width": 1.5 }); el(s, "line", { x1: GX, y1: GY, x2: GX, y2: GY + GH, stroke: C.muted, "stroke-width": 1.5 });
      [0, 1, 2, 3, 4, 5].forEach(function (t) { txt(s, X(t), GY + GH + 24, String(t), 17, C.muted); });
      [0, 1.75, 3.5].forEach(function (d) { txt(s, GX - 10, Y(d) + 6, nt(d, 2).replace(/\.?0+$/, ""), 17, C.muted, "end"); });
      txt(s, GX + GW + 14, GY + GH + 6, "t (s)", 17, C.muted, "start"); txt(s, GX - 10, GY - 16, "d (m)", 17, C.muted, "end");
      all.slice(1).forEach(function (c) { var p = []; for (var t = 0; t <= 5.0001; t += 0.05) p.push([X(t), Y(c.d1 * q(Math.min(1, t / c.T)))]); poly(s, p, { stroke: C.edge, "stroke-width": 1.6, fill: "none" }); });
      var p = []; for (var t = 0; t <= 5.0001; t += 0.05) p.push([X(t), Y(b.d1 * q(Math.min(1, t / b.T)))]); poly(s, p, { stroke: C.ok, "stroke-width": 5, fill: "none" });
      txt(s, GX + GW, GY - 16, "green: the cheapest, " + nt(b.d1, 1) + " m in " + b.T + " s", 19, C.ok, "end", { "font-weight": 700 });
      txt(s, 1080, Y(3.5) + 6, "left lane", 17, C.muted, "end"); txt(s, 1080, Y(0) + 6, "right lane", 17, C.muted, "end");
      tex("xc-read", "C_d = " + nt(kj, 1) + " \\times " + nt(b.J, 2) + " + " + nt(kt, 1) + " \\times " + b.T + " + " + nt(kd, 1) + " \\times " + nt((b.d1 - 3.5) * (b.d1 - 3.5), 2) + " = " + nt(b.c, 2) +
        "\\qquad \\text{next: } " + nt(all[1].d1, 1) + "\\text{ m in } " + all[1].T + "\\text{ s, } " + nt(all[1].c, 2)); }
    ["xc-kj", "xc-kt", "xc-kd"].forEach(function (id) { $(id).addEventListener("input", draw); }); draw();
  });

  /* ---------- 7. The two timings (sections "Same Path, Two Speeds" and "Check Both Against Car B"): the path
     d = 3.5 q((s - 80)/40); (1) keep 10 m/s; (2) slow to 7 m/s in 2 s, then keep 7; car B at 45 + 15 t in the left lane;
     the gap between the three circles, computed on the lecture's road as the check does ---------- */
  ifPanel("xg-svg", function () {
    var R = W.DATA.traj, ref = R.ref, n = ref.s.length, AV = R.AV, rad = Math.hypot(AV.length / 6, AV.width / 2);
    function interp(a, s) { if (s <= ref.s[0]) return a[0]; if (s >= ref.s[n - 1]) return a[n - 1]; var lo = 0, hi = n - 1; while (hi - lo > 1) { var m = (lo + hi) >> 1; if (ref.s[m] <= s) lo = m; else hi = m; }
      var fr = (s - ref.s[lo]) / (ref.s[hi] - ref.s[lo]); return a[lo] + fr * (a[hi] - a[lo]); }
    function xy(s, d) { var h = interp(ref.heading, s); return [interp(ref.x, s) - d * Math.sin(h), interp(ref.y, s) + d * Math.cos(h), h]; }
    var offs = function (r) { return [0, 1, 2].map(function (i) { return (i + 0.5) * AV.length / 3 - r; }); }, OAV = offs(AV.rear_to_base), OCAR = offs(AV.length / 2);
    function dOf(s) { var u = Math.min(1, Math.max(0, (s - 80) / 40)); return 3.5 * q(u); }
    function dsOf(s) { var u = (s - 80) / 40; return u < 0 || u > 1 ? 0 : 3.5 * (30 * u * u - 60 * u * u * u + 30 * u * u * u * u) / 40; }
    var SP = [function (t) { return 60 + 10 * t; }, function (t) { return t <= 2 ? 60 + 10 * t - 3 * (t * t * t / 4 - t * t * t * t / 16) : 77 + 7 * (t - 2); }];
    function circ(s, d, h, off) { var p = xy(s, d); return off.map(function (o) { return [p[0] + Math.cos(h) * o, p[1] + Math.sin(h) * o]; }); }
    function gap(k, t) { var s = SP[k](t), d = dOf(s), h = interp(ref.heading, s) + Math.atan(dsOf(s)), A = circ(s, d, h, OAV), sb = 45 + 15 * t, B = circ(sb, 3.5, interp(ref.heading, sb), OCAR), g = 1e9;
      A.forEach(function (a) { B.forEach(function (b) { g = Math.min(g, Math.hypot(a[0] - b[0], a[1] - b[1])); }); }); return g - 2 * rad; }
    var MIN = [0, 1].map(function (k) { var best = [1e9, 0]; for (var i = 0; i <= 120; i++) { var g = gap(k, i * 0.05); if (g < best[0]) best = [g, i * 0.05]; } return best; });
    var s = $("xg-svg"), PX = 14, S0 = 55, VH = 180;
    function draw() { var t = val("xg-t"); clear(s);
      [0, 1].forEach(function (k) { var oy = k * VH, Y = function (d) { return oy + 120 - d * PX; }, X = function (sv) { return 40 + (sv - S0) * PX; };
        [-1.75, 5.25].forEach(function (d) { el(s, "line", { x1: 40, y1: Y(d), x2: 1090, y2: Y(d), stroke: C.ink, "stroke-width": 1.5 }); });
        el(s, "line", { x1: 40, y1: Y(1.75), x2: 1090, y2: Y(1.75), stroke: C.muted, "stroke-width": 1.5, "stroke-dasharray": "10 8" });
        var path = []; for (var sv = S0; sv <= 130; sv += 0.5) path.push([X(sv), Y(dOf(sv))]); poly(s, path, { stroke: C.ink, "stroke-width": 2, fill: "none" });
        for (var ts = 0; ts <= 6; ts++) { var sd = SP[k](ts); if (sd >= S0) el(s, "circle", { cx: X(sd), cy: Y(dOf(sd)), r: 4, fill: C.ink }); }
        carIcon(s, "car", X(118), Y(-0.3), AV.length * PX, 0, PARKED);
        var sa = SP[k](t), da = dOf(sa), ha = Math.atan(dsOf(sa)), sb = 45 + 15 * t, g = gap(k, t), hit = g < 0;
        if (sb > S0 - 3) carIcon(s, "car", X(sb), Y(3.5), AV.length * PX, 0, CARB);
        carIcon(s, "av", X(sa + (AV.length / 2 - AV.rear_to_base) * Math.cos(ha)), Y(da + (AV.length / 2 - AV.rear_to_base) * Math.sin(ha)), AV.length * PX, -deg(ha));
        [[sa, da, ha, OAV], [sb, 3.5, 0, OCAR]].forEach(function (c) { c[3].forEach(function (o) { el(s, "circle", { cx: X(c[0] + Math.cos(c[2]) * o), cy: Y(c[1] + Math.sin(c[2]) * o), r: rad * PX, fill: "none", stroke: hit ? C.bad : C.muted, "stroke-width": hit ? 2.5 : 1.2 }); }); });
        tag(s, 22, oy + 70, k + 1);
        halo(txt(s, 1088, oy + 30, (k ? "(2) slow to 7 m/s first" : "(1) keep 10 m/s") + ": gap " + f(g, 2) + " m", 19, hit ? C.bad : C.ink, "end", { "font-weight": 600 })); });
      tex("xg-read", "\\begin{aligned}&t = " + nt(t, 2) + "\\text{ s, car B at } 45 + 15 \\times " + nt(t, 2) + " = " + nt(45 + 15 * t, 2) + "\\text{ m}\\\\ &\\text{closest: (1) } " + f(MIN[0][0], 2) +
        "\\text{ m at } " + nt(MIN[0][1], 2) + "\\text{ s, a crash; (2) } " + nt(MIN[1][0], 2) + "\\text{ m at } " + nt(MIN[1][1], 2) + "\\text{ s, safe}\\end{aligned}"); }
    var an = animator(s, function (dt) { var t = val("xg-t") + dt * 0.6; if (t > 6) { $("xg-t").value = 6; draw(); return false; } $("xg-t").value = t; draw(); });
    $("xg-t").addEventListener("input", function () { an.stop(); draw(); });
    $("xg-play").addEventListener("click", function (e) { e.stopPropagation(); $("xg-t").value = 0; draw(); an.start(); });
    draw();
  });

  /* ---------- 8. The pedal split (section "Drive Two Pedals from One Command"): u > 0 throttle u (at most 0.75),
     u < 0 brake -u; a dead zone (chosen, +-0.05) stops the switching when u wobbles (chosen, +-0.02) ---------- */
  ifPanel("xp-svg", function () {
    var s = $("xp-svg"), DZ = 0.05, dz = false, hist = [], wob = 0, wk = 0;
    choice($("xp-dz"), [["off", false], ["±0.05", true]], function (v) { dz = v; hist = []; draw(); }, false);
    function pedal(u) { if (dz && Math.abs(u) < DZ) return "none"; return u > 0 ? "thr" : u < 0 ? "brk" : "none"; }
    var COL = { thr: C.ok, brk: BRAKE, none: C.muted, cap: CAP };
    function X(u) { return 80 + (u + 1) / 2 * 940; }
    function draw() { var u = val("xp-u"), pd = pedal(u), th = pd === "thr" ? Math.min(u, 0.75) : 0, br = pd === "brk" ? -u : 0; clear(s);
      el(s, "rect", { x: X(-1), y: 40, width: X(0) - X(-1), height: 26, fill: BRAKE, opacity: 0.85 });
      el(s, "rect", { x: X(0), y: 40, width: X(0.75) - X(0), height: 26, fill: C.ok, opacity: 0.85 });
      el(s, "rect", { x: X(0.75), y: 40, width: X(1) - X(0.75), height: 26, fill: CAP, opacity: 0.85 });
      if (dz) el(s, "rect", { x: X(-DZ), y: 34, width: X(DZ) - X(-DZ), height: 38, fill: C.muted });
      [-1, -0.5, 0, 0.5, 0.75, 1].forEach(function (v) { txt(s, X(v), 96, nt(v, 2).replace(/\.?0+$/, "").replace("-", "−"), 17, C.muted); });
      txt(s, X(-0.5), 26, "brake", 18, BRAKE, "middle", { "font-weight": 600 }); txt(s, X(0.37), 26, "throttle", 18, C.ok, "middle", { "font-weight": 600 }); txt(s, X(0.88), 26, "capped", 18, CAP, "middle", { "font-weight": 600 });
      el(s, "path", { d: "M" + X(u) + ",76 l -10,16 l 20,0 z", fill: C.live }); el(s, "line", { x1: X(u), y1: 30, x2: X(u), y2: 76, stroke: C.live, "stroke-width": 4 });
      /* the two pedals */
      [["brake", br, 1, BRAKE, 300], ["throttle", th, 0.75, C.ok, 560]].forEach(function (p) {
        el(s, "rect", { x: p[4], y: 130, width: 90, height: 110, rx: 10, fill: "none", stroke: C.ink, "stroke-width": 2 });
        el(s, "rect", { x: p[4] + 4, y: 236 - 102 * p[1], width: 82, height: 102 * p[1], rx: 6, fill: p[3] });
        txt(s, p[4] + 45, 268, p[0] + " " + nt(p[1], 2), 18, C.ink, "middle", { "font-weight": 600 }); });
      /* the last 20 control steps */
      txt(s, 760, 140, "the last 20 steps:", 17, C.muted, "start");
      hist.forEach(function (h, i) { el(s, "rect", { x: 760 + i * 15, y: 152, width: 12, height: 26, fill: COL[h] }); });
      var sw = 0; for (var i = 1; i < hist.length; i++) if (hist[i] !== hist[i - 1] && hist[i] !== "none" && hist[i - 1] !== "none") sw++;
      if (hist.length) txt(s, 760, 206, sw + " pedal switch" + (sw === 1 ? "" : "es"), 18, sw ? C.bad : C.ok, "start", { "font-weight": 600 });
      tex("xp-read", "u = " + nt(u, 2) + ":\\quad " + (pd === "thr" ? "\\text{throttle} = " + nt(th, 2) + (u > 0.75 ? "\\text{ (capped at 0.75)}" : "") : pd === "brk" ? "\\text{brake} = " + nt(br, 2) : dz && Math.abs(u) < DZ && u !== 0 ? "\\text{in the dead zone: no pedal}" : "\\text{no pedal}")); }
    var an = animator(s, function (dt) { wob += dt; while (wob >= 0.05) { wob -= 0.05; wk++; var u = wk % 2 ? 0.02 : -0.02; $("xp-u").value = u; hist.push(pedal(u)); if (hist.length > 20) hist.shift(); }
      draw(); if (wk >= 40) { return false; } });
    $("xp-u").addEventListener("input", function () { an.stop(); draw(); });
    $("xp-wob").addEventListener("click", function (e) { e.stopPropagation(); hist = []; wk = 0; wob = 0; if (!an.start()) { for (var i = 0; i < 20; i++) hist.push(pedal(i % 2 ? 0.02 : -0.02)); $("xp-u").value = -0.02; draw(); } });
    draw();
  });

  /* ---------- 9. The actuators (sections "Hand Over to the Actuators" and "Let a Computer Drive"): one steering
     command, Pure Pursuit's -0.211 rad (steer = delta / 0.7), over the CAN bus to the steering ECU and back ---------- */
  ifPanel("xn-svg", function () {
    var s = $("xn-svg"), cap = $("xn-cap"), items = document.querySelectorAll("#xn-loop li"), N = items.length, cur = 0, timer = null, raf = null;
    var CAPS = ["The controllers make one command every control step, 0.05 s: Pure Pursuit's −0.211 rad becomes steer = −0.211 / 0.7 = −0.30, with a throttle and a brake.",
      "It goes on the CAN bus as frames: each carries an identifier and up to 8 bytes of data. Every unit on the bus reads every frame.",
      "The steering ECU takes the frame and checks it: range, rate, safety.",
      "It drives its actuator: the power steering motor turns the front wheels.",
      "It reads its own sensor: the steering angle.",
      "It sends feedback back on the bus (dashed); the computer reads it, and the next command comes 0.05 s later."];
    var BX = { pc: [220, 20, 200, 60], st: [20, 200, 180, 56], thr: [230, 200, 180, 56], brk: [440, 200, 180, 56], eps: [20, 310, 180, 56], tb: [230, 310, 180, 56], ba: [440, 310, 180, 56] };
    var NAMES = { pc: "driving computer", st: "steering ECU", thr: "throttle ECU", brk: "brake ECU", eps: "steering motor", tb: "throttle body", ba: "brake actuator" }, BUS = 140;
    function box(k, lit) { var b = BX[k], ecu = ["st", "thr", "brk"].indexOf(k) >= 0;
      el(s, "rect", { x: b[0], y: b[1], width: b[2], height: b[3], rx: 8, fill: k === "pc" ? "#EEF1F4" : ecu ? "#EEF3EE" : "#fff", stroke: lit ? C.live : ecu ? C.ok : C.muted, "stroke-width": lit ? 4 : 2 });
      txt(s, b[0] + b[2] / 2, b[1] + b[3] / 2 + 7, NAMES[k], 18, C.ink, "middle", { "font-weight": lit ? 700 : 400 }); }
    function link(x, y1, y2, fb, lit) { var dx = fb ? 14 : -14;
      el(s, "line", { x1: x + dx, y1: y1, x2: x + dx, y2: y2, stroke: lit ? C.live : C.muted, "stroke-width": lit ? 3.5 : 2, "stroke-dasharray": fb ? "6 5" : "" });
      arrowHead(s, x + dx, y2, y2 > y1 ? Math.PI / 2 : -Math.PI / 2, lit ? C.live : C.muted, 10); }
    function draw(k, p) { clear(s);
      el(s, "line", { x1: 10, y1: BUS, x2: 630, y2: BUS, stroke: k === 1 ? C.live : C.ink, "stroke-width": 8 });
      txt(s, 630, BUS - 12, "CAN bus", 18, C.ink, "end", { "font-weight": 600 });
      link(320, 80, BUS - 4, false, k === 0 || k === 1); link(320, BUS - 4, 80, true, k === 5);
      [["st", "eps"], ["thr", "tb"], ["brk", "ba"]].forEach(function (pr, i) { var x = BX[pr[0]][0] + 90, isSt = i === 0;
        link(x, BUS + 4, 200, false, isSt && (k === 1 || k === 2)); link(x, 200, BUS + 4, true, isSt && k === 5);
        link(x, 256, 310, false, isSt && k === 3); link(x, 310, 256, true, isSt && k === 4); });
      Object.keys(BX).forEach(function (b) { box(b, (k === 0 && b === "pc") || ((k === 2 || k === 5) && b === "st") || ((k === 3 || k === 4) && (b === "st" || b === "eps")) || (k === 5 && b === "pc")); });
      txt(s, 630, 452, "solid: command; dashed: feedback", 16, C.muted, "end");
      /* the message: a dot along the step's path */
      var path = [[[306, 80], [306, BUS]], [[306, BUS], [96, BUS], [96, 200]], [[96, 200], [96, 228]], [[96, 256], [96, 310]], [[124, 310], [124, 256]], [[124, 200], [124, BUS], [334, BUS], [334, 80]]][k];
      var segs = [], tot = 0; for (var i = 1; i < path.length; i++) { var l = Math.hypot(path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1]); segs.push(l); tot += l; }
      var d = p * tot, j = 0; while (j < segs.length - 1 && d > segs[j]) { d -= segs[j]; j++; } var a = Math.min(1, d / segs[j]);
      el(s, "circle", { cx: path[j][0] + (path[j + 1][0] - path[j][0]) * a, cy: path[j][1] + (path[j + 1][1] - path[j][1]) * a, r: 9, fill: C.live, stroke: "#fff", "stroke-width": 2 });
      if (k === 1) { var fx = 20, fy = 392; [["ID: 11 bits", 110], ["data: up to 8 bytes", 250], ["check: 15-bit CRC", 160]].forEach(function (c) {
          el(s, "rect", { x: fx, y: fy, width: c[1], height: 30, fill: "#fff", stroke: C.live, "stroke-width": 2 }); txt(s, fx + c[1] / 2, fy + 21, c[0], 16, C.ink, "middle"); fx += c[1]; }); } }
    function show(k) { cur = Math.max(0, Math.min(N - 1, k)); items.forEach(function (li, j) { li.classList.toggle("lit", j === cur); if (j === cur) li.setAttribute("aria-current", "step"); else li.removeAttribute("aria-current"); });
      cap.textContent = CAPS[cur]; cancelAnimationFrame(raf); var t0 = performance.now();
      if (reduce) { draw(cur, 1); return; }
      (function run() { var p = Math.min(1, (performance.now() - t0) / 1400); draw(cur, p); if (p < 1) raf = requestAnimationFrame(run); })(); }
    function stop() { clearTimeout(timer); timer = null; $("xn-run").textContent = "Follow one command"; }
    $("xn-run").addEventListener("click", function (e) { e.stopPropagation(); if (timer) { stop(); return; } show(0); this.textContent = "Pause";
      (function tick() { timer = setTimeout(function () { if (cur >= N - 1) { stop(); return; } show(cur + 1); if (cur >= N - 1) stop(); else tick(); }, reduce ? 1200 : 2600); })(); });
    $("xn-next").addEventListener("click", function (e) { e.stopPropagation(); stop(); show(cur + 1); });
    $("xn-back").addEventListener("click", function (e) { e.stopPropagation(); stop(); show(cur - 1); });
    items.forEach(function (li, j) { li.style.cursor = "pointer";
      li.addEventListener("click", function (e) { e.stopPropagation(); stop(); show(j); });
      li.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); e.stopPropagation(); stop(); show(j); } }); });
    show(0);
  });
})();
