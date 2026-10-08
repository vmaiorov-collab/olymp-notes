(function(){
  var root=document.documentElement,btn=document.getElementById('theme-toggle');
  function apply(t){root.setAttribute('data-theme',t);if(btn)btn.textContent=t==='dark'?'светлая тема':'тёмная тема'}
  if(btn){
    var saved=null;try{saved=localStorage.getItem('olympTheme')}catch(e){}
    apply(saved||root.getAttribute('data-theme')||'dark');
    btn.addEventListener('click',function(){
      root.classList.add('theme-anim');setTimeout(function(){root.classList.remove('theme-anim')},350);
      var next=root.getAttribute('data-theme')==='dark'?'light':'dark';apply(next);
      try{localStorage.setItem('olympTheme',next)}catch(e){}
    });
  }
  var top=document.getElementById('topBtn');
  if(top){addEventListener('scroll',function(){top.classList.toggle('show',scrollY>600)});top.onclick=function(){scrollTo({top:0,behavior:'smooth'})}}
  var q=document.getElementById('q'),h=document.getElementById('hits');
  if(q&&window.D){q.addEventListener('input',function(){var v=q.value.trim().toLowerCase();
    h.innerHTML=v?D.filter(function(x){return (x.t+' '+x.s).toLowerCase().indexOf(v)>=0}).map(function(x){return '<p><a href="'+x.h+'">'+x.t+'</a></p>'}).join('')||'<p>Ничего не найдено</p>':''})}
  try{if(location.protocol.indexOf('http')===0&&navigator.sendBeacon)navigator.sendBeacon('https://olymp-notes-bots.d6544559.workers.dev/hit?p='+encodeURIComponent(location.pathname))}catch(e){}
})();
