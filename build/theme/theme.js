
(function(){
  var root = document.documentElement;
  var btn = document.getElementById("theme-toggle");
  if(!btn) return;
  function apply(t){ root.setAttribute("data-theme", t); btn.textContent = t === "dark" ? "светлая тема" : "тёмная тема"; }
  var saved = (function(){ try { return localStorage.getItem("olympTheme"); } catch(e){ return null; } })();
  apply(saved || root.getAttribute("data-theme") || "light");
  btn.addEventListener("click", function(){
    var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    apply(next);
    try { localStorage.setItem("olympTheme", next); } catch(e){}
  });
})();
