
(function(){
  function h(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e;}
  function bubbleF(a){var n=a.length,ids=[],v=a.slice(),F=[],i;for(i=0;i<n;i++)ids.push(i);function val(p){return v[ids[p]];}
    for(var pass=0;pass<n-1;pass++){var mv=false;for(i=0;i<n-1-pass;i++){F.push({ids:ids.slice(),cmp:[i,i+1],done:pass});if(val(i)>val(i+1)){var t=ids[i];ids[i]=ids[i+1];ids[i+1]=t;mv=true;F.push({ids:ids.slice(),cmp:[i,i+1],done:pass,swap:true});}}if(!mv)break;}
    F.push({ids:ids.slice(),cmp:[],done:n});return F;}
  function selF(a){var n=a.length,ids=[],v=a.slice(),F=[],i,j;for(i=0;i<n;i++)ids.push(i);function val(p){return v[ids[p]];}
    for(i=0;i<n-1;i++){var m=i;for(j=i+1;j<n;j++){F.push({ids:ids.slice(),cmp:[m,j],done:i});if(val(j)<val(m))m=j;}
      if(m!==i){var t=ids[i];ids[i]=ids[m];ids[m]=t;F.push({ids:ids.slice(),cmp:[i,m],done:i,swap:true});}F.push({ids:ids.slice(),cmp:[],done:i+1});}
    F.push({ids:ids.slice(),cmp:[],done:n});return F;}
  function insF(a){var n=a.length,ids=[],v=a.slice(),F=[],i;for(i=0;i<n;i++)ids.push(i);function val(p){return v[ids[p]];}
    for(i=1;i<n;i++){var j=i;while(j>0){F.push({ids:ids.slice(),cmp:[j-1,j],done:0});if(val(j)<val(j-1)){var t=ids[j];ids[j]=ids[j-1];ids[j-1]=t;F.push({ids:ids.slice(),cmp:[j-1,j],done:0,swap:true});j--;}else break;}}
    F.push({ids:ids.slice(),cmp:[],done:n});return F;}
  function buildSort(cont,kind,a){var n=a.length,mx=Math.max.apply(null,a),W=48,G=16,H=170;
    var stage=h('div','stage');stage.style.width=(n*(W+G)-G)+'px';stage.style.height=(H+40)+'px';
    var idEl=[],id;for(id=0;id<n;id++){var b=h('div','bar'),hh=18+(a[id]/mx)*(H-18);b.style.width=W+'px';b.style.height=hh+'px';b.style.left=(id*(W+G))+'px';b.appendChild(h('span','v',a[id]));stage.appendChild(b);idEl.push(b);}
    cont.appendChild(stage);
    var F=kind==='selection'?selF(a):kind==='insertion'?insF(a):bubbleF(a);
    var ctl=h('div','ctl'),play=h('button',null,'\u25B6');play.type='button';
    var range=h('input');range.type='range';range.min=0;range.max=F.length-1;range.value=0;
    var lbl=h('span','lbl');ctl.appendChild(play);ctl.appendChild(range);ctl.appendChild(lbl);cont.appendChild(ctl);
    function draw(k){var f=F[k],pos={};f.ids.forEach(function(x,i){pos[x]=i;});
      for(var id=0;id<n;id++){var b=idEl[id],p=pos[id];b.style.left=(p*(W+G))+'px';b.classList.remove('cmp','swap','done');
        if(f.cmp&&f.cmp.indexOf(p)>=0)b.classList.add(f.swap?'swap':'cmp');else if(p>=n-(f.done||0))b.classList.add('done');}
      lbl.textContent=(k+1)+'/'+F.length;}
    draw(0);
    var tm=null;function stop(){if(tm){clearInterval(tm);tm=null;play.textContent='\u25B6';}}
    range.addEventListener('input',function(){stop();draw(+range.value);});
    play.addEventListener('click',function(){if(tm){stop();return;}if(+range.value>=F.length-1)range.value=0;play.textContent='\u23F8';tm=setInterval(function(){var k=+range.value+1;if(k>F.length-1){stop();return;}range.value=k;draw(k);},550);});
  }
  function buildBS(cont,a,t){var n=a.length,row=h('div','bsrow'),cells=[];
    for(var i=0;i<n;i++){var c=h('div','bscell',a[i]);row.appendChild(c);cells.push(c);}
    cont.appendChild(row);var msg=h('div','bslbl');cont.appendChild(msg);
    var F=[],L=0,R=n;while(R-L>1){var m=(L+R)>>1;F.push({L:L,R:R,m:m,msg:'mid = '+m+', a['+m+'] = '+a[m]+(a[m]<=t?' \u2264 ':' > ')+t});if(a[m]<=t)L=m;else R=m;}
    F.push({L:L,R:R,m:L,found:true,msg:'\u043d\u0430\u0448\u043b\u0438 '+t+' \u0432 \u043f\u043e\u0437\u0438\u0446\u0438\u0438 '+L});
    var ctl=h('div','ctl'),play=h('button',null,'\u25B6');play.type='button';var range=h('input');range.type='range';range.min=0;range.max=F.length-1;range.value=0;var lbl=h('span','lbl');
    ctl.appendChild(play);ctl.appendChild(range);ctl.appendChild(lbl);cont.appendChild(ctl);
    function draw(k){var f=F[k];cells.forEach(function(c,i){c.className='bscell';});
      if(f.R<n)cells[f.R].classList.add('R');cells[f.L].classList.add('L');cells[f.m].classList.add('mid');
      if(f.found)cells[f.L].classList.add('found');msg.textContent=f.msg;lbl.textContent=(k+1)+'/'+F.length;}
    draw(0);
    var tm=null;function stop(){if(tm){clearInterval(tm);tm=null;play.textContent='\u25B6';}}
    range.addEventListener('input',function(){stop();draw(+range.value);});
    play.addEventListener('click',function(){if(tm){stop();return;}if(+range.value>=F.length-1)range.value=0;play.textContent='\u23F8';tm=setInterval(function(){var k=+range.value+1;if(k>F.length-1){stop();return;}range.value=k;draw(k);},700);});
  }
  Array.prototype.forEach.call(document.querySelectorAll('.algo'),function(cont){
    var kind=cont.getAttribute('data-algo'),arr=(cont.getAttribute('data-arr')||'').split(',').map(Number);
    if(kind==='sort')buildSort(cont,cont.getAttribute('data-kind'),arr);
    else if(kind==='binsearch')buildBS(cont,arr,Number(cont.getAttribute('data-target')));
  });
})();
