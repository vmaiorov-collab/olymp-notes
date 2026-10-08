(function(){
  var d=document, root=d.documentElement;
  // тема
  function setTheme(t){root.setAttribute('data-theme',t);try{localStorage.setItem('olympTheme',t)}catch(e){}
    var b=d.getElementById('themeBtn'); if(b) b.textContent=t==='dark'?'☀':'☾';}
  var tbtn=d.getElementById('themeBtn');
  if(tbtn){tbtn.textContent=root.getAttribute('data-theme')==='dark'?'☀':'☾';
    tbtn.addEventListener('click',function(){setTheme(root.getAttribute('data-theme')==='dark'?'light':'dark')});}
  var bg=d.getElementById('burger'); if(bg) bg.addEventListener('click',function(){d.body.classList.toggle('menu')});
  d.querySelectorAll('.side nav a').forEach(function(a){a.addEventListener('click',function(){d.body.classList.remove('menu')})});

  // прогресс и подсветка раздела
  var bar=d.getElementById('progress');
  var heads=[].slice.call(d.querySelectorAll('main h2[id],main h3[id]'));
  var links={};d.querySelectorAll('.side nav a').forEach(function(a){links[a.getAttribute('href').slice(1)]=a});
  function onScroll(){
    var h=d.documentElement; var p=h.scrollTop/(h.scrollHeight-h.clientHeight||1);
    if(bar) bar.style.width=(Math.min(1,Math.max(0,p))*100)+'%';
    var cur=null; for(var i=0;i<heads.length;i++){ if(heads[i].getBoundingClientRect().top<120) cur=heads[i]; else break; }
    for(var k in links) links[k].classList.remove('on');
    if(cur&&links[cur.id]){links[cur.id].classList.add('on');
      var a=links[cur.id], s=d.querySelector('.side'); if(s){var r=a.getBoundingClientRect(); if(r.top<80||r.bottom>innerHeight-40) a.scrollIntoView({block:'center'});}}
  }
  addEventListener('scroll',onScroll,{passive:true}); onScroll();

  // копирование кода
  d.querySelectorAll('.code').forEach(function(c){
    var b=c.querySelector('button'); if(!b) return;
    b.addEventListener('click',function(){
      var t=c.querySelector('pre').innerText;
      (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){b.textContent='скопировано'},function(){b.textContent='ошибка'});
      setTimeout(function(){b.textContent='копировать'},1400);
    });
  });

  // формулы
  if(window.renderMathInElement){
    renderMathInElement(d.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],
      ignoredTags:['script','style','pre','code'],throwOnError:false});
  }

  // интерактивные плееры: window.ALGOS[name] = function(){return {title, frames:[{svg:'<g>..</g>', msg:'..'}], vb:'0 0 760 220'}}
  d.querySelectorAll('.algo[data-algo]').forEach(function(el){
    var f=(window.ALGOS||{})[el.getAttribute('data-algo')]; if(!f) return;
    var a=f(); var i=0, timer=null;
    el.innerHTML='<div class="cap">'+a.title+'</div><svg viewBox="'+a.vb+'" xmlns="http://www.w3.org/2000/svg"></svg>'+
      '<div class="ctl"><button type="button" aria-label="play">▶</button><input type="range" min="0" max="'+(a.frames.length-1)+'" value="0"></div><div class="msg"></div>';
    var svg=el.querySelector('svg'), btn=el.querySelector('button'), rg=el.querySelector('input'), msg=el.querySelector('.msg');
    function show(k){i=k;rg.value=k;svg.innerHTML='<rect width="100%" height="100%" rx="10" fill="#0e1a1f"/>'+a.frames[k].svg;msg.textContent=a.frames[k].msg||'';}
    function stop(){clearInterval(timer);timer=null;btn.textContent='▶'}
    btn.addEventListener('click',function(){
      if(timer){stop();return}
      if(i>=a.frames.length-1) show(0);
      btn.textContent='⏸'; timer=setInterval(function(){ if(i>=a.frames.length-1){stop();return} show(i+1)},900);
    });
    rg.addEventListener('input',function(){stop();show(+rg.value)});
    show(0);
  });
})();
