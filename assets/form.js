// Quote request form: sends to the inbox through FormSubmit (NBC Booking in copy), with place suggestions
// and a mail-app fallback. Texts come from window.AJ_FORM (French or English page).
(function(){
  var L=window.AJ_FORM||{},form=document.getElementById('devis-form');if(!form)return;
  var $=function(i){return document.getElementById(i)},v=function(i){return $(i).value.trim()};
  var FORM_ID='7e1adee14a65debe62f66d12ed0c07de',MAIL='nbc.booking.co@gmail.com',st=$('f-status'),btn=$('send');
  var PRO_TYPES=['Mariage','Séminaire / entreprise','Événement privé'];// labels used by the pro quote tool
  function say(t,c){st.textContent=t;st.className='fstatus'+(c?' '+c:'')}

  // No date in the past
  var fd=$('f-date'),now=new Date();fd.min=new Date(now.getTime()-now.getTimezoneOffset()*6e4).toISOString().slice(0,10);

  // Place suggestions from the French address service (IGN Géoplateforme), former BAN address as fallback.
  (function(){var inp=$('f-lieu'),ul=$('lieu-list'),timer,ctrl,items=[],cur=-1;
    var URLS=['https://data.geopf.fr/geocodage/search','https://api-adresse.data.gouv.fr/search/'];
    function close(){ul.hidden=true;inp.setAttribute('aria-expanded','false');cur=-1}
    function pick(i){if(!items[i])return;inp.value=items[i].label;close()}
    function render(){ul.innerHTML='';items.forEach(function(it,i){var li=document.createElement('li');li.id='lieu-'+i;li.setAttribute('role','option');li.textContent=it.label;
      if(it.sub){var sm=document.createElement('small');sm.textContent=it.sub;li.appendChild(sm)}
      li.addEventListener('mousedown',function(e){e.preventDefault();pick(i)});ul.appendChild(li)});
      ul.hidden=!items.length;inp.setAttribute('aria-expanded',items.length?'true':'false')}
    function query(q,k){if(k>=URLS.length)return;if(ctrl)ctrl.abort();ctrl=window.AbortController?new AbortController():null;
      fetch(URLS[k]+'?autocomplete=1&limit=6&q='+encodeURIComponent(q),ctrl?{signal:ctrl.signal}:{}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(d){
        if(inp.value.trim()!==q)return;var seen={};items=(d.features||[]).map(function(f){var p=f.properties||{};
          return{label:p.label||'',sub:p.type==='municipality'?(p.postcode?p.postcode+' · ':'')+(p.context||''):(p.context||'')}}).filter(function(it){if(!it.label||seen[it.label])return false;return seen[it.label]=true});
        cur=-1;render()}).catch(function(e){if(e&&e.name==='AbortError')return;query(q,k+1)})}
    inp.addEventListener('input',function(){clearTimeout(timer);var q=inp.value.trim();if(q.length<3){items=[];close();return}timer=setTimeout(function(){query(q,0)},250)});
    inp.addEventListener('keydown',function(e){if(ul.hidden)return;if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();cur=(cur+(e.key==='ArrowDown'?1:-1)+items.length)%items.length;
      [].forEach.call(ul.children,function(li,i){li.setAttribute('aria-selected',i===cur?'true':'false')});inp.setAttribute('aria-activedescendant','lieu-'+cur)}
      else if(e.key==='Enter'&&cur>=0){e.preventDefault();pick(cur)}else if(e.key==='Escape')close()});
    inp.addEventListener('blur',function(){setTimeout(close,150)})})();

  form.addEventListener('submit',function(e){e.preventDefault();
    if(v('f-honey'))return;
    var miss=[];[['f-nom',L.miss_name],['f-email',L.miss_email]].forEach(function(f){var el=$(f[0]),bad=!v(f[0])||(f[0]==='f-email'&&!el.checkValidity());el.classList.toggle('bad',bad);if(bad)miss.push(f[1])});
    if(miss.length){say(L.missing.replace('{}',miss.join(L.and_)),'err');$(miss[0]===L.miss_name?'f-nom':'f-email').focus();return}
    var d=v('f-date'),dd=d?new Date(d+'T12:00').toLocaleDateString(L.locale,{weekday:'long',day:'numeric',month:'long',year:'numeric'}):'';
    var type=v('f-type'),proType=PRO_TYPES[$('f-type').selectedIndex]||type;
    var data={_subject:L.subject+' – '+type+(dd?' – '+dd:''),_replyto:v('f-email'),_cc:MAIL,_template:'table',
      'Nom':v('f-nom'),'Email':v('f-email'),'Téléphone':v('f-tel'),'Date':dd,'Lieu':v('f-lieu'),'Type':type,'Artiste':'Alex Juan','Message':v('f-msg')};
    // One-click link in the email that opens the pro quote page already filled in
    data['Devis']='live.alexjuan.com/pro/?'+new URLSearchParams({nom:v('f-nom'),email:v('f-email'),tel:v('f-tel'),date:d,lieu:v('f-lieu'),type:proType,artiste:'Alex Juan'}).toString();
    btn.disabled=true;say(L.sending);
    fetch('https://formsubmit.co/ajax/'+FORM_ID,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(data)})
      .then(function(r){return r.json().then(function(j){if(!r.ok||String(j.success)!=='true')throw 0})})
      .then(function(){say(L.ok,'ok');form.reset()})
      .catch(function(){say(L.fail,'err');
        var body='Nom : '+data['Nom']+'\nEmail : '+data['Email']+'\nTéléphone : '+data['Téléphone']+'\nDate : '+dd+'\nLieu : '+data['Lieu']+'\nType : '+type+'\n\n'+data['Message'];
        location.href='mailto:'+MAIL+'?subject='+encodeURIComponent(data._subject)+'&body='+encodeURIComponent(body)})
      .then(function(){btn.disabled=false})});
})();
