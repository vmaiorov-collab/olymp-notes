
(function(){
  function h(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e;}
  function mkrow(vals,w){var r=h('div','bsrow');vals.forEach(function(v){var c=h('div','bscell small',v);r.appendChild(c);});return r;}
  var NS='http://www.w3.org/2000/svg';
  function el(n,at){var e=document.createElementNS(NS,n);for(var k in at)e.setAttribute(k,at[k]);return e;}
  function ctl(range,max,lbl){var c=h('div','ctl'),rr=range||h('input');if(!range){rr.type='range';}c.appendChild(rr);c.appendChild(lbl);return {ctl:c,range:rr};}

  function buildCounting(cont,a){
    var k=Math.max.apply(null,a),F=[],cnt=[],out=[],i,v,t;
    for(i=0;i<=k;i++)cnt.push(0);
    for(i=0;i<a.length;i++){cnt[a[i]]++;F.push({i:i,cnt:cnt.slice(),out:out.slice()});}
    for(v=0;v<=k;v++)for(t=0;t<cnt[v];t++){out.push(v);F.push({i:-1,cnt:cnt.slice(),out:out.slice(),ov:v});}
    cont.appendChild(h('div','albl','массив')); var arr=mkrow(a); cont.appendChild(arr);
    cont.appendChild(h('div','albl','cnt  (сколько раз встретилось)')); var cr=mkrow(cnt); cont.appendChild(cr);
    cont.appendChild(h('div','albl','вывод')); var ocont=h('div','bsrow'); cont.appendChild(ocont);
    var r=h('input');r.type='range';r.min=0;r.max=F.length-1;r.value=0;var lbl=h('span','lbl');
    var c=h('div','ctl');var play=h('button',null,'\u25B6');play.type='button';c.appendChild(play);c.appendChild(r);c.appendChild(lbl);cont.appendChild(c);
    function draw(kk){var f=F[kk],ac=arr.children;for(var q=0;q<ac.length;q++)ac[q].className='bscell small'+(q===f.i?' mid':'');
      var cc=cr.children;for(q=0;q<cc.length;q++)cc[q].textContent=f.cnt[q];
      for(q=0;q<cc.length;q++)cc[q].className='bscell small'+(q===(f.i>=0?a[f.i]:f.ov)?' mid':'');
      ocont.innerHTML='';for(q=0;q<f.out.length;q++){var e=h('div','bscell small'+(q===f.out.length-1?' L':''),f.out[q]);ocont.appendChild(e);}
      lbl.textContent=(kk+1)+'/'+F.length;}
    draw(0);
    var tm=null;function stop(){if(tm){clearInterval(tm);tm=null;play.textContent='\u25B6';}}
    r.addEventListener('input',function(){stop();draw(+r.value);});
    play.addEventListener('click',function(){if(tm){stop();return;}if(+r.value>=F.length-1)r.value=0;play.textContent='\u23F8';tm=setInterval(function(){var x=+r.value+1;if(x>F.length-1){stop();return;}r.value=x;draw(x);},600);});
  }

  function buildMerge(cont,a,b){
    var i=0,j=0,out=[],F=[];
    while(i<a.length&&j<b.length){F.push({a:i,b:j,out:out.slice()});if(a[i]<=b[j])out.push(a[i++]);else out.push(b[j++]);F.push({a:i,b:j,out:out.slice()});}
    while(i<a.length){out.push(a[i++]);F.push({a:i,b:j,out:out.slice()});}
    while(j<b.length){out.push(b[j++]);F.push({a:i,b:j,out:out.slice()});}
    cont.appendChild(h('div','albl','a')); var ar=mkrow(a); cont.appendChild(ar);
    cont.appendChild(h('div','albl','b')); var br=mkrow(b); cont.appendChild(br);
    cont.appendChild(h('div','albl','результат')); var oc=h('div','bsrow'); cont.appendChild(oc);
    var r=h('input');r.type='range';r.min=0;r.max=F.length-1;r.value=0;var lbl=h('span','lbl');
    var c=h('div','ctl');var play=h('button',null,'\u25B6');play.type='button';c.appendChild(play);c.appendChild(r);c.appendChild(lbl);cont.appendChild(c);
    function draw(kk){var f=F[kk],q;for(q=0;q<ar.children.length;q++)ar.children[q].className='bscell small'+(q===f.a?' L':(q<f.a?' done':''));for(q=0;q<br.children.length;q++)br.children[q].className='bscell small'+(q===f.b?' R':(q<f.b?' done':''));
      oc.innerHTML='';for(q=0;q<f.out.length;q++)oc.appendChild(h('div','bscell small'+(q===f.out.length-1?' L':''),f.out[q]));
      lbl.textContent=(kk+1)+'/'+F.length;}
    draw(0);
    var tm=null;function stop(){if(tm){clearInterval(tm);tm=null;play.textContent='\u25B6';}}
    r.addEventListener('input',function(){stop();draw(+r.value);});
    play.addEventListener('click',function(){if(tm){stop();return;}if(+r.value>=F.length-1)r.value=0;play.textContent='\u23F8';tm=setInterval(function(){var x=+r.value+1;if(x>F.length-1){stop();return;}r.value=x;draw(x);},600);});
  }

  function buildSlope(cont){
    var brk=[3,5],xmin=0,xmax=8,N=200,fmax=0,t;
    function f(x){var s=0;for(var q=0;q<brk.length;q++)s+=Math.abs(x-brk[q]);return s;}
    for(t=0;t<=N;t++)fmax=Math.max(fmax,f(xmin+(xmax-xmin)*t/N));
    var W=760,Hh=300,x0=64,x1=700,y0=248,y1=54;
    function px(x){return x0+(x-xmin)/(xmax-xmin)*(x1-x0);}
    function py(y){return y0-(y/fmax)*(y0-y1);}
    var svg=el('svg',{viewBox:'0 0 '+W+' '+Hh,role:'img',xmlns:NS});
    svg.style.width='100%';svg.style.height='auto';svg.style.display='block';svg.style.borderRadius='14px';
    svg.appendChild(el('rect',{x:0,y:0,width:W,height:Hh,rx:14,fill:'#141a24'}));
    for(var gy=y1;gy<y0;gy+=32)svg.appendChild(el('line',{x1:x0,y1:gy,x2:x1,y2:gy,stroke:'rgba(255,255,255,.05)'}));
    svg.appendChild(el('line',{x1:x0,y1:y0,x2:x1+6,y2:y0,stroke:'#9aa4b2','stroke-width':1.5}));
    svg.appendChild(el('line',{x1:x0,y1:y0,x2:x0,y2:y1,stroke:'#9aa4b2','stroke-width':1.5}));
    var pts='';for(t=0;t<=N;t++){var xx=xmin+(xmax-xmin)*t/N;pts+=px(xx)+','+py(f(xx))+' ';}
    svg.appendChild(el('polyline',{points:pts,fill:'none',stroke:'#58c4dd','stroke-width':3,'stroke-linejoin':'round'}));
    brk.forEach(function(b){svg.appendChild(el('circle',{cx:px(b),cy:py(f(b)),r:6,fill:'#ffff00',stroke:'#141a24','stroke-width':3}));});
    var vline=el('line',{x1:px(4),y1:y1,x2:px(4),y2:y0,stroke:'#fc6255','stroke-width':1.6,'stroke-dasharray':'5 5'});
    var dot=el('circle',{cx:px(4),cy:py(f(4)),r:7,fill:'#fc6255',stroke:'#141a24','stroke-width':3});
    svg.appendChild(vline);svg.appendChild(dot);
    var t1=el('text',{x:x0+8,y:y1-4,fill:'#dfe7f1','font-size':15,'font-weight':700});t1.textContent='slope trick: выпуклая dp(x)';
    var t2=el('text',{x:x0+8,y:y0+24,fill:'#c2cdde','font-size':13});
    svg.appendChild(t1);svg.appendChild(t2);
    cont.appendChild(svg);
    var r=h('input');r.type='range';r.min=0;r.max=N;r.value=110;var lbl=h('span','lbl');
    var c=h('div','ctl');c.appendChild(r);c.appendChild(lbl);cont.appendChild(c);
    function draw(v){var x=xmin+(xmax-xmin)*v/N,y=f(x);vline.setAttribute('x1',px(x));vline.setAttribute('x2',px(x));dot.setAttribute('cx',px(x));dot.setAttribute('cy',py(y));t2.textContent='x = '+x.toFixed(2)+'    dp(x) = '+y.toFixed(2)+'    (жёлтые точки — изломы)';lbl.textContent='x = '+x.toFixed(1);}
    r.addEventListener('input',function(){draw(+r.value);});draw(+r.value);
  }

  Array.prototype.forEach.call(document.querySelectorAll('.algo'),function(cont){
    var k=cont.getAttribute('data-algo');
    if(k==='counting')buildCounting(cont,(cont.getAttribute('data-arr')||'').split(',').map(Number));
    else if(k==='merge')buildMerge(cont,(cont.getAttribute('data-a')||'').split(',').map(Number),(cont.getAttribute('data-b')||'').split(',').map(Number));
    else if(k==='slope')buildSlope(cont);
  });
})();
