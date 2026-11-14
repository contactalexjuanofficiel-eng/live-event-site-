"""Encrypts / decrypts the pro space (pro/index.html).

The published page only holds the pro tool encrypted with AES-256-GCM; the key is derived
from the access code (PBKDF2-SHA256). Without the code, the page source shows nothing readable.

  python3 _build/pro_crypt.py decrypt CODE out.html     # get the readable page to edit it
  python3 _build/pro_crypt.py encrypt CODE in.html      # publish an edited page (writes pro/index.html)
"""
import base64, json, os, re, sys, hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'pro', 'index.html')
ITER = 400000


def norm(code):
    return re.sub(r'[^A-Z0-9]', '', code.upper())


def key(code, salt):
    return hashlib.pbkdf2_hmac('sha256', ('aj-pro-enc:' + norm(code)).encode(), salt, ITER, 32)


SHELL = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Espace pro · Alex Juan Live Événement</title>
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="../favicon.ico?v=3" sizes="any">
<link rel="apple-touch-icon" sizes="180x180" href="../assets/apple-touch-icon.png?v=3">
<meta name="theme-color" content="#0e1116">
<link rel="stylesheet" href="../assets/fonts.css">
<style>
html,body{margin:0;min-height:100%;background:#0e1116;color:#f6f2ea;font:400 16px/1.5 Jost,system-ui,sans-serif}
.box{min-height:100vh;display:grid;place-items:center;padding:24px;box-sizing:border-box}
form{width:min(360px,100%);text-align:center}
.aj{width:72px;height:72px;margin:0 auto 18px;border:1px solid #cfb489;border-radius:50%;display:grid;place-items:center;font:500 28px "Cormorant Garamond",Georgia,serif;color:#cfb489}
h1{font:500 32px "Cormorant Garamond",Georgia,serif;margin:0 0 6px}
p{margin:0 0 18px;color:#a9a397}
input{width:100%;box-sizing:border-box;padding:14px;border:1px solid rgba(207,180,137,.4);background:#161b24;color:#f6f2ea;font:500 18px/1 Jost,system-ui,sans-serif;letter-spacing:.12em;text-align:center;border-radius:2px}
input:focus{outline:none;border-color:#cfb489}
button{margin-top:14px;width:100%;padding:14px;border:0;background:#b08d57;color:#0e1116;font:500 14px Jost,system-ui,sans-serif;letter-spacing:.2em;text-transform:uppercase;cursor:pointer}
.err{min-height:22px;margin:12px 0 0;color:#e9a08a;font-size:14px}
label{display:flex;gap:8px;justify-content:center;align-items:center;margin-top:14px;color:#a9a397;font-size:14px}
label input{width:auto}
</style>
</head>
<body>
<div class="box"><form id="f" autocomplete="off">
<div class="aj">AJ</div><h1>Espace pro</h1><p>Entrez votre code d'accès</p>
<input id="c" type="password" autocapitalize="characters" spellcheck="false" aria-label="Code d'accès" placeholder="XXXX-XXXX-XXXX-XXXX">
<label><input id="r" type="checkbox" checked> Se souvenir de cet appareil</label>
<button id="b" type="submit">Entrer</button>
<p class="err" id="e" aria-live="polite"></p>
</form></div>
<script>
/* The pro tool below is encrypted (AES-256-GCM). Only the access code can open it. */
var P=__DATA__;
(function(){var $=function(i){return document.getElementById(i)},S=crypto.subtle,te=new TextEncoder();
function b64(s){return Uint8Array.from(atob(s),function(c){return c.charCodeAt(0)})}
function hex(b){return Array.prototype.map.call(new Uint8Array(b),function(x){return x.toString(16).padStart(2,'0')}).join('')}
function norm(v){return String(v||'').toUpperCase().replace(/[^A-Z0-9]/g,'')}
function open(raw,code,remember){return S.importKey('raw',raw,'AES-GCM',false,['decrypt']).then(function(k){return S.decrypt({name:'AES-GCM',iv:b64(P.iv)},k,b64(P.ct))}).then(function(pt){
  var html=new TextDecoder().decode(pt);
  var pre=code?S.digest('SHA-256',te.encode('aj-pro:'+code)).then(function(h){try{localStorage.setItem('aj-pro-ok',hex(h));localStorage.setItem('aj-stats-key',code);localStorage.setItem('aj-me','1');if(remember)localStorage.setItem('aj-pro-k',remember)}catch(e){}}):Promise.resolve();
  return pre.then(function(){document.open();document.write(html);document.close()})})}
function derive(code){return S.importKey('raw',te.encode('aj-pro-enc:'+code),'PBKDF2',false,['deriveBits']).then(function(k){return S.deriveBits({name:'PBKDF2',hash:'SHA-256',salt:b64(P.salt),iterations:P.it},k,256)})}
var saved=null;try{saved=localStorage.getItem('aj-pro-k')}catch(e){}
if(saved){open(b64(saved),null).catch(function(){try{localStorage.removeItem('aj-pro-k')}catch(e){}})}
$('c').focus();
$('f').onsubmit=function(ev){ev.preventDefault();var code=norm($('c').value),keep=$('r').checked;if(!code)return;$('b').disabled=true;$('e').textContent='Ouverture…';
  derive(code).then(function(raw){return open(raw,code,keep?btoa(String.fromCharCode.apply(null,new Uint8Array(raw))):null)})
  .catch(function(){$('b').disabled=false;$('e').textContent='Code incorrect. Réessayez.';$('c').value='';$('c').focus()})};
})();
</script>
</body>
</html>
'''


def encrypt(code, src):
    html = open(src, encoding='utf-8').read()
    salt, iv = os.urandom(16), os.urandom(12)
    try:  # keep the same salt so devices that remember the code stay unlocked after an update
        old = json.loads(re.search(r'var P=(\{.*?\});', open(OUT, encoding='utf-8').read()).group(1))
        salt = base64.b64decode(old['salt'])
    except Exception:
        pass
    ct = AESGCM(key(code, salt)).encrypt(iv, html.encode('utf-8'), None)
    data = {'it': ITER, 'salt': base64.b64encode(salt).decode(), 'iv': base64.b64encode(iv).decode(), 'ct': base64.b64encode(ct).decode()}
    open(OUT, 'w', encoding='utf-8').write(SHELL.replace('__DATA__', json.dumps(data)))


def decrypt(code, dst):
    s = open(OUT, encoding='utf-8').read()
    data = json.loads(re.search(r'var P=(\{.*?\});', s).group(1))
    salt = base64.b64decode(data['salt'])
    k = hashlib.pbkdf2_hmac('sha256', ('aj-pro-enc:' + norm(code)).encode(), salt, data['it'], 32)
    pt = AESGCM(k).decrypt(base64.b64decode(data['iv']), base64.b64decode(data['ct']), None)
    open(dst, 'w', encoding='utf-8').write(pt.decode('utf-8'))


if __name__ == '__main__':
    if len(sys.argv) != 4 or sys.argv[1] not in ('encrypt', 'decrypt'):
        sys.exit(__doc__)
    (encrypt if sys.argv[1] == 'encrypt' else decrypt)(sys.argv[2], sys.argv[3])
