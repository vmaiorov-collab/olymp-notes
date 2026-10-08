
(function(){
  var heads = [].slice.call(document.querySelectorAll(".wrap h2[id], .wrap h3[id]"));
  if (!heads.length) return;
  var bar = document.createElement("div"); bar.className = "progress"; document.body.appendChild(bar);
  function label(h){ var c = h.cloneNode(true); [].forEach.call(c.querySelectorAll(".ts"), function(x){ x.remove(); });
    return c.textContent.replace(/^\s*(?:\d+\.)+\s*/, "").trim(); }
  function links(box){ return heads.map(function(h){ var a = document.createElement("a"); a.href = "#" + h.id; a.textContent = label(h); if (h.tagName === "H3") a.className = "sub"; box.appendChild(a); return a; }); }
  var side = document.createElement("nav"); side.className = "side-toc"; side.setAttribute("aria-label", "Разделы");
  side.innerHTML = "<p>Разделы</p>"; var sideLinks = links(side); document.body.appendChild(side);
  var btn = document.createElement("button"); btn.className = "secbtn"; btn.type = "button"; btn.textContent = "≡ разделы";
  btn.setAttribute("aria-expanded", "false");
  var panel = document.createElement("nav"); panel.className = "secpanel"; panel.hidden = true; panel.setAttribute("aria-label", "Разделы");
  var panelLinks = links(panel); document.body.appendChild(panel); document.body.appendChild(btn);
  function toggle(open){ panel.hidden = !open; btn.setAttribute("aria-expanded", open); }
  btn.addEventListener("click", function(e){ e.stopPropagation(); toggle(panel.hidden); });
  panel.addEventListener("click", function(e){ if (e.target.closest("a")) toggle(false); });
  document.addEventListener("click", function(e){ if (!panel.hidden && !panel.contains(e.target)) toggle(false); });
  document.addEventListener("keydown", function(e){ if (e.key === "Escape") toggle(false); });
  var toc = document.querySelector(".toc"); var cur = -1; var ticking = false;
  // Позиции заголовков и высота страницы меряются один раз, а не на каждом
  // кадре прокрутки: getBoundingClientRect() по всем заголовкам — это до 44
  // вынужденных пересчётов раскладки в кадр (столько разделов в конспекте по
  // C++), и прокрутка из-за этого подлагивала. Перемер — на resize и load:
  // KaTeX и картинки доезжают после первого кадра и сдвигают разметку.
  var tops = [], tocEnd = 400, maxScroll = 0;
  function measure(){
    tops.length = 0;
    for (var k = 0; k < heads.length; k++) tops.push(heads[k].getBoundingClientRect().top + scrollY);
    tocEnd = toc ? toc.getBoundingClientRect().bottom + scrollY : 400;
    maxScroll = document.documentElement.scrollHeight - innerHeight;
  }
  function update(){
    ticking = false;
    bar.style.transform = "scaleX(" + (maxScroll > 0 ? Math.min(1, scrollY / maxScroll) : 0) + ")";
    var past = scrollY > tocEnd;
    side.classList.toggle("show", past); btn.classList.toggle("show", past);
    var lim = scrollY + innerHeight * 0.3;
    var i = -1; for (var k = 0; k < tops.length; k++) if (tops[k] < lim) i = k;
    if (i !== cur) {
      [sideLinks, panelLinks].forEach(function(l){ if (cur >= 0) l[cur].classList.remove("on"); if (i >= 0) l[i].classList.add("on"); });
      if (i >= 0 && side.classList.contains("show")) { var a = sideLinks[i]; if (a.offsetTop < side.scrollTop || a.offsetTop > side.scrollTop + side.clientHeight - 30) side.scrollTop = a.offsetTop - 60; }
      cur = i;
    }
  }
  addEventListener("scroll", function(){ if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  addEventListener("resize", function(){ measure(); update(); });
  addEventListener("load", function(){ measure(); update(); });
  measure(); update();
})();
