// Shared behaviour for every page: mobile menu, one-time fade-in, YouTube on click, discreet WhatsApp button.
(function(){
  var root=document.documentElement;root.classList.remove('no-js');

  // Mobile menu (full-screen drawer)
  var drawer=document.getElementById('drawer'),open=document.querySelector('.burger');
  if(drawer&&open){
    var close=drawer.querySelector('.d-close');
    function set(o){drawer.classList.toggle('open',o);root.classList.toggle('no-scroll',o);open.setAttribute('aria-expanded',o);drawer.setAttribute('aria-hidden',!o);if(o)close.focus();else open.focus()}
    open.addEventListener('click',function(){set(true)});close.addEventListener('click',function(){set(false)});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&drawer.classList.contains('open'))set(false)});
    drawer.addEventListener('click',function(e){if(e.target.closest('nav a'))set(false)});
  }

  // Elements fade in once when they first come into view
  var els=[].slice.call(document.querySelectorAll('.fade'));
  if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion:reduce)').matches){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
    els.forEach(function(e){io.observe(e)});
  }else els.forEach(function(e){e.classList.add('in')});

  // Video players: local thumbnail first, YouTube (no-cookie) only after a tap
  var SIZES=['maxresdefault','sddefault','hqdefault'];
  [].forEach.call(document.querySelectorAll('.player'),function(p){
    var id=p.dataset.yt,b=p.querySelector('button'),img=p.querySelector('img');
    if(img&&!img.getAttribute('src')){var k=0;img.onerror=function(){k<SIZES.length?img.src='https://i.ytimg.com/vi/'+id+'/'+SIZES[k++]+'.jpg':p.classList.add('nothumb')};img.onload=function(){if(img.naturalWidth<=120&&k<SIZES.length)img.onerror()};img.onerror()}
    b.addEventListener('click',function(){
      [].forEach.call(document.querySelectorAll('.player iframe'),function(f){f.parentNode.replaceChild(f._btn,f)});
      var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&playsinline=1&rel=0&modestbranding=1';
      f.title=b.getAttribute('aria-label')||'Vidéo';f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';f.allowFullscreen=true;f._btn=b;p.replaceChild(f,b)});
  });

  // WhatsApp button steps aside over the footer and the quote form
  var wa=document.querySelector('.wa'),hide=[].slice.call(document.querySelectorAll('.foot,#devis-form'));
  if(wa&&hide.length&&'IntersectionObserver' in window){var seen=new Set();
    var o2=new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?seen.add(e.target):seen.delete(e.target)});wa.classList.toggle('away',seen.size>0)});
    hide.forEach(function(h){o2.observe(h)});
  }

  // Hero video: lighter file, never blocks the page
  var v=document.querySelector('.hero video');
  if(v){var p=v.play&&v.play();if(p&&p.catch)p.catch(function(){})}
})();
