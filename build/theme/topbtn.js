
  const btn=document.getElementById('topBtn');
  addEventListener('scroll',()=>btn.classList.toggle('show',scrollY>600));
  btn.onclick=()=>scrollTo({top:0,behavior:'smooth'});
