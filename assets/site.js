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

  // Anonymous visit statistics for the pro space: no cookie, no storage, no IP kept.
  // One row per page view and per key action (call, WhatsApp, quote, form sent...).
  var host=location.hostname;
  if(/(^|\.)alexjuan\.com$/.test(host)&&!navigator.webdriver){
    var API='https://hsdjmyngjqpszfvxxova.supabase.co/rest/v1/rpc/track',KEY='sb_publishable_krUr-a-gDTCVow3-hMD1kQ_0eUyWUTH';
    var dev=matchMedia('(max-width:760px)').matches?'Téléphone':matchMedia('(max-width:1100px)').matches?'Tablette':'Ordinateur';
    var lang=root.lang&&root.lang.slice(0,2)||'fr',path=location.pathname.replace(/index\.html$/,'')||'/';
    var send=function(k,l,extra){var b={k:k,p:path,l:l||'',d:dev,g:lang};for(var x in extra)b[x]=extra[x];
      try{fetch(API,{method:'POST',keepalive:true,headers:{'apikey':KEY,'Content-Type':'application/json'},body:JSON.stringify(b)}).catch(function(){})}catch(e){}};
    window.ajTrack=function(l){send(l==='form'?'form':'click',l==='form'?'':l)};
    // Where the visitor comes from (a visit starts when the previous page is not on this site)
    var ref='',entry=true;try{var r=document.referrer&&new URL(document.referrer);if(r){if(r.hostname===host)entry=false;else ref=r.hostname.replace(/^www\.|^l\.|^lm\.|^m\./,'')}}catch(e){}
    var utm=new URLSearchParams(location.search).get('utm_source'),src='Direct';
    var NAMES=[[/google\./,'Google'],[/bing\./,'Bing'],[/instagram/,'Instagram'],[/facebook|fb\.com/,'Facebook'],[/tiktok/,'TikTok'],[/youtube/,'YouTube'],[/linkedin|lnkd/,'LinkedIn'],[/whatsapp/,'WhatsApp'],[/mariages\.net/,'Mariages.net'],[/yahoo|qwant|duckduckgo|ecosia/,'Autre moteur']];
    if(utm)src=utm.slice(0,40);else if(ref){src=ref;NAMES.some(function(n){if(n[0].test(ref)){src=n[1];return true}})}
    send('view','',{s:entry?src:'',e:entry});
    // Key clicks
    document.addEventListener('click',function(ev){var a=ev.target.closest&&ev.target.closest('a,.player button');if(!a)return;
      var h=a.getAttribute('href')||'',l='';
      if(a.tagName==='BUTTON')l='Vidéo regardée';
      else if(/^tel:/.test(h))l='Appel téléphone';
      else if(/wa\.me|whatsapp/.test(h))l='WhatsApp';
      else if(/^mailto:/.test(h))l='Email';
      else if(/cal\.com/.test(h))l='Rendez-vous Cal.com';
      else if(/instagram|facebook|tiktok|youtube\.com\/@|linkedin/.test(h))l='Réseaux sociaux';
      else if(/(reserver|booking)\/?(#.*)?$/.test(h))l='Bouton Devis';
      if(l)send('click',l)},true);
  }
})();
