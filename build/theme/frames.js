/* Общий плеер кадров: window.ALGOS[имя]() -> {title, vb, frames:[{svg, msg}]} ; контейнер <div class="algo" data-frames="имя">.
   Кадры рисуются цветами палитры 3B1B — тему подстраивает CSS страницы. */
(function(){
  function h(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
  Array.prototype.forEach.call(document.querySelectorAll('.algo[data-frames]'),function(cont){
    var f=(window.ALGOS||{})[cont.getAttribute('data-frames')]; if(!f) return;
    var a=f(), i=0, tm=null;
    if(a.title) cont.appendChild(h('div','fcap',a.title));
    var NS='http://www.w3.org/2000/svg', svg=document.createElementNS(NS,'svg'); svg.setAttribute('viewBox',a.vb); svg.setAttribute('class','fsvg'); cont.appendChild(svg);
    var ctl=h('div','ctl'), play=h('button',null,'▶'); play.type='button';
    var range=h('input'); range.type='range'; range.min=0; range.max=a.frames.length-1; range.value=0;
    var lbl=h('span','lbl'); ctl.appendChild(play); ctl.appendChild(range); ctl.appendChild(lbl); cont.appendChild(ctl);
    var msg=h('div','fmsg'); cont.appendChild(msg);
    function draw(k){i=k; svg.innerHTML='<rect width="100%" height="100%" fill="#141a24"/>'+a.frames[k].svg; msg.textContent=a.frames[k].msg||''; lbl.textContent=(k+1)+'/'+a.frames.length; range.value=k}
    function stop(){if(tm){clearInterval(tm);tm=null;play.textContent='▶'}}
    range.addEventListener('input',function(){stop();draw(+range.value)});
    play.addEventListener('click',function(){ if(tm){stop();return} if(i>=a.frames.length-1) draw(0);
      play.textContent='⏸'; tm=setInterval(function(){ if(i>=a.frames.length-1){stop();return} draw(i+1)},800)});
    draw(0);
  });
})();
