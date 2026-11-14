"""Builds every public page of live.alexjuan.com (French + English) from parts.py and content.py.

    python3 _build/build.py

The private quote tool in pro/ is not generated here.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from parts import INTRO, head, top, foot, ic, url, prefix, business_ld, PATHS, T, TEL, MAIL, CAL, SITE, wa, IG_AJ
import content as C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def write(rel, html):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path) or ROOT, exist_ok=True)
    with open(path, 'w') as f:
        f.write(html)
    print('wrote', rel)


def page(lang, key, title, desc, body, ld=None, extra_js='', path=None, robots=None):
    path = path if path is not None else PATHS[lang][key]
    return head(lang, path, key, title, desc, ld, robots) + (INTRO if key == 'home' else '') + top(lang, path, key) + '<main id="main">\n' + body + '\n</main>\n' + foot(lang, path, extra_js)


def link(href, text):
    return f'<a class="link" href="{href}"><span>{text}</span>{ic("arrow")}</a>'


def page_hero(eyebrow, h1, lead, crumbs=''):
    return f'''<section class="page-hero"><div class="wrap">{crumbs}
<span class="eyebrow">{eyebrow}</span><h1 class="h1">{h1}</h1><p class="lead">{lead}</p></div></section>'''


def cta(lang, p, c=None):
    c = c or C.TXT[lang]['cta']
    return f'''<section class="sec night cta"><div class="wrap fade">
<span class="eyebrow">{c[0]}</span><h2 class="h2">{c[1]}</h2><p class="lead">{c[2]}</p>
<div class="actions"><a class="btn gold" href="{url(lang, "contact", p)}">{C.TXT[lang]["ask_quote"]}</a><a class="tel" href="tel:{TEL}">{ic("phone")}{T[lang]["tel_txt"]}</a></div>
</div></section>'''


def svc_cards(lang, p):
    out = ''
    for k, img, alt, name, text in C.TXT[lang]['svc']:
        out += (f'<a class="fade" href="{url(lang, k, p)}"><figure><img src="{p}assets/{img}" alt="{alt}" loading="lazy" width="900" height="1125"></figure>'
                f'<h3 class="h3">{name}</h3><p>{text}</p><span class="link"><span>{C.TXT[lang]["discover"]}</span>{ic("arrow")}</span></a>')
    return f'<div class="svc">{out}</div>'


def player(p, vid, label, thumb=None):
    img = f'<img src="{p}assets/{thumb}" alt="" loading="lazy" width="720" height="1280">' if thumb else '<img alt="" loading="lazy" width="720" height="1280">'
    return f'<div class="player" data-yt="{vid}"><button type="button" aria-label="{label}">{img}<span class="play">{ic("play")}</span></button></div>'


def facts(items):
    return '<ul class="facts">' + ''.join(f'<li>{ic(i)}<div><b>{b}</b><span>{s}</span></div></li>' for i, b, s in items) + '</ul>'


def steps(items):
    return '<ol class="steps">' + ''.join(f'<li class="fade"><h3>{h}</h3><p>{t}</p></li>' for h, t in items) + '</ol>'


def checks(items, style=''):
    return f'<ul class="checks"{style}>' + ''.join(f'<li>{ic("check")}<span>{x}</span></li>' for x in items) + '</ul>'


def faq(items):
    return '<div class="faq">' + ''.join(f'<details class="fade"><summary>{q}{ic("plus")}</summary><p>{a}</p></details>' for q, a in items) + '</div>'


def faq_ld(items):
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': re.sub('<[^>]+>', '', q), 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', a)}} for q, a in items]}


def crumbs(lang, p, name):
    return f'<p class="crumbs"><a href="{url(lang, "home", p)}">{T[lang]["home"]}</a>{ic("chevron")}<a href="{url(lang, "prestations", p)}">{T[lang]["nav"][0][1]}</a>{ic("chevron")}{name}</p>'


# ---------------------------------------------------------------- pages

def home(lang):
    X, p = C.TXT[lang], prefix(PATHS[lang]['home'])
    team = ''.join(f'<div class="fade"><div class="ph"><img src="{p}assets/{i}" alt="{n}" loading="lazy" width="320" height="320"></div><b>{n}</b><span>{r}</span></div>' for i, n, r in X['team_row'])
    body = f'''<section class="hero">
<video autoplay muted loop playsinline preload="metadata" poster="{p}assets/hero-poster-2.jpg" aria-hidden="true"><source src="{p}assets/hero-720.webm" type="video/webm"><source src="{p}assets/hero-720.mp4" type="video/mp4"></video>
<div class="wrap">
<span class="eyebrow">{X["hero"][0]}</span>
<h1 class="h1">{X["hero"][1]}</h1>
<p class="lead">{X["hero"][2]}</p>
<div class="actions"><a class="btn gold" href="{url(lang, "contact", p)}">{X["ask_quote"]}</a>{link(url(lang, "show", p), X["see_show"])}</div>
</div>
</section>

<section class="sec"><div class="wrap">
<div class="sec-head fade"><span class="eyebrow">{T[lang]["nav"][0][1]}</span><h2 class="h2">{X["svc_title"]}</h2><p class="lead">{X["svc_lead"]}</p></div>
{svc_cards(lang, p)}
</div></section>

<section class="sec dark"><div class="wrap split">
<div class="fade">{player(p, "IAmyNBhYdxw", X["play_label"], "videos/video-2.jpg")}</div>
<div class="fade"><span class="eyebrow">{T[lang]["nav"][1][1]}</span><h2 class="h2" style="margin-top:22px">{X["show_title"]}</h2>
{facts(X["facts"])}
<p style="margin-top:32px">{link(url(lang, "show", p), X["show_link"])}</p></div>
</div></section>

<section class="sec stone"><div class="wrap">
<div class="sec-head center fade"><span class="eyebrow">{T[lang]["nav"][2][1]}</span><h2 class="h2">{X["team_title"]}</h2><p class="lead">{X["team_lead"]}</p></div>
<div class="team">{team}</div>
<p class="fade" style="text-align:center;margin-top:48px">{link(url(lang, "team", p), X["team_link"])}</p>
</div></section>
{cta(lang, p)}'''
    return page(lang, 'home', X['home_title'], X['home_desc'], body, [business_ld(lang)])


def prestations(lang):
    X, p = C.TXT[lang], prefix(PATHS[lang]['prestations'])
    body = page_hero(T[lang]['nav'][0][1], X['svc_title'], X['svc_lead'])
    body += f'<section class="sec"><div class="wrap">{svc_cards(lang, p)}</div></section>'
    if lang == 'en':  # the English site describes each service on this page
        for anchor, s in C.EN_SERVICES:
            body += f'''<section class="sec {s["bg"]}" id="{anchor}"><div class="wrap split{" rev" if s["bg"] == "stone" else ""}">
<div class="fade"><span class="eyebrow">{s["eyebrow"]}</span><h2 class="h2" style="margin:20px 0 22px">{s["title"]}</h2><p class="lead">{s["lead"]}</p>{checks(s["items"], ' style="grid-template-columns:1fr;margin-top:24px"')}</div>
<div class="fade"><img src="{p}assets/{s["img"]}" alt="{s["alt"]}" loading="lazy" width="900" height="1125" style="width:100%;aspect-ratio:4/5;object-fit:cover;object-position:50% 22%"></div>
</div></section>'''
    body += f'''<section class="sec dark"><div class="wrap">
<div class="sec-head fade"><span class="eyebrow">{X["incl_eyebrow"]}</span><h2 class="h2">{X["incl_title"]}</h2></div>
{checks(X["incl"])}
</div></section>''' + cta(lang, p)
    return page(lang, 'prestations', X['svc_page_title'], X['svc_page_desc'], body)


def show(lang):
    X, p = C.TXT[lang], prefix(PATHS[lang]['show'])
    vids = ''.join(f'<div class="fade">{player(p, v, X["play_n"].format(i + 1), th)}</div>' for i, (v, th) in enumerate(C.VIDEOS))
    rep = ''.join(f'<div class="fade"><h3>{h}</h3><ol>' + ''.join(f'<li><b>{s}</b><span>{a}</span></li>' for s, a in songs) + '</ol></div>' for h, songs in X['rep'])
    body = page_hero(T[lang]['nav'][1][1], X['show_h1'], X['show_lead'])
    body += f'''<section class="sec"><div class="wrap">
<div class="sec-head fade"><span class="eyebrow">{X["vid_eyebrow"]}</span><h2 class="h2">{X["vid_title"]}</h2></div>
<div class="vgrid">{vids}</div>
<p class="note fade" style="margin-top:28px">{X["vid_note"].format(p=p)} · <a href="https://www.youtube.com/@alexjuanofficiel" target="_blank" rel="noopener">{X["more_yt"]}</a></p>
</div></section>
<section class="sec dark"><div class="wrap">
<div class="sec-head fade"><span class="eyebrow">{X["flow_eyebrow"]}</span><h2 class="h2">{X["flow_title"]}</h2><p class="lead">{X["flow_lead"]}</p></div>
{steps(X["flow"])}
</div></section>
<section class="sec" id="repertoire"><div class="wrap">
<div class="sec-head fade"><span class="eyebrow">{X["rep_eyebrow"]}</span><h2 class="h2">{X["rep_title"]}</h2><p class="lead">{X["rep_lead"]}</p></div>
<div class="rep">{rep}</div>
</div></section>''' + cta(lang, p, X['rep_cta'])
    return page(lang, 'show', X['show_page_title'], X['show_page_desc'], body)


def team(lang):
    X, p = C.TXT[lang], prefix(PATHS[lang]['team'])
    body = page_hero(T[lang]['nav'][2][1], X['team_h1'], X['team_page_lead'])
    for pr in X['profiles']:
        chips = ''.join(f'<a href="{h}"' + (' target="_blank" rel="noopener"' if h.startswith('http') else '') + f'>{ic(i)}{t}</a>' for i, t, h in pr['links'])
        extra = ''
        if pr.get('card'):
            extra = f'<h3>{X["card_title"]}</h3><div class="bcard"><img src="{p}assets/carte-nbc-recto.jpg" alt="{X["card_alt"]} (recto)" loading="lazy" width="480" height="752"><img src="{p}assets/carte-nbc-verso.jpg?v=2" alt="{X["card_alt"]} (verso)" loading="lazy" width="480" height="760"></div>'
        paras = ''.join(f'<p>{x}</p>' for x in pr['text'])
        body += f'''<section class="sec {pr["bg"]}" id="{pr["id"]}"><div class="wrap profile">
<div class="fade"><div class="ph"><img src="{p}assets/{pr["img"]}" alt="{pr["name"]}" loading="lazy" width="320" height="320"></div></div>
<div class="body fade"><span class="eyebrow">{pr["role"]}</span><h2 class="h2">{pr["name"]}</h2>
{paras}
<h3>{pr["list_title"]}</h3>{checks(pr["list"], ' style="grid-template-columns:1fr"')}
<h3>{pr["links_title"]}</h3><div class="chips">{chips}</div>{extra}</div>
</div></section>'''
    body += cta(lang, p)
    return page(lang, 'team', X['team_page_title'], X['team_page_desc'], body)


def booking(lang):
    X, p = C.TXT[lang], prefix(PATHS[lang]['booking'])
    body = page_hero(T[lang]['nav'][3][1], X['book_h1'], X['book_lead'])
    body += f'''<section class="sec"><div class="wrap">
<div class="sec-head fade"><span class="eyebrow">{X["book_eyebrow"]}</span><h2 class="h2">{X["book_title"]}</h2></div>
{steps(X["book_steps"])}
<div class="fade" style="display:flex;flex-wrap:wrap;gap:16px 24px;align-items:center;margin-top:56px">
<a class="btn" href="{url(lang, "contact", p)}">{X["ask_quote"]}</a>
<a class="btn line" href="{CAL}" target="_blank" rel="noopener">{X["have_quote"]}</a></div>
<p class="note fade" style="margin-top:18px">{X["book_note"].format(p=p)}</p>
</div></section>
<section class="sec stone" id="faq"><div class="wrap">
<div class="sec-head fade"><span class="eyebrow">{X["faq_eyebrow"]}</span><h2 class="h2">{X["faq_title"]}</h2></div>
{faq(X["faq"])}
</div></section>''' + cta(lang, p)
    return page(lang, 'booking', X['book_page_title'], X['book_page_desc'], body, [faq_ld(X['faq'])])


def contact(lang):
    X, p = C.TXT[lang], prefix(PATHS[lang]['contact'])
    F = X['form']
    opts = ''.join(f'<option>{o}</option>' for o in F['types'])
    body = page_hero(X['quote_eyebrow'], X['quote_h1'], X['quote_lead'])
    body += f'''<section class="sec"><div class="wrap form-grid">
<form class="form fade" id="devis-form" novalidate>
<div class="field"><label for="f-nom">{F["name"]}</label><input id="f-nom" autocomplete="name" required></div>
<div class="field"><label for="f-email">{F["email"]}</label><input id="f-email" type="email" autocomplete="email" inputmode="email" required></div>
<div class="field"><label for="f-tel">{F["tel"]} <small>{F["optional"]}</small></label><input id="f-tel" type="tel" autocomplete="tel" inputmode="tel"></div>
<div class="field"><label for="f-type">{F["type"]}</label><select id="f-type">{opts}</select></div>
<div class="field"><label for="f-date">{F["date"]}</label><input id="f-date" type="date"></div>
<div class="field"><label for="f-lieu">{F["place"]}</label><input id="f-lieu" autocomplete="off" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="lieu-list" placeholder="{F["place_ph"]}"><ul class="ac-list" id="lieu-list" role="listbox" hidden></ul></div>
<div class="field full"><label for="f-msg">{F["msg"]} <small>{F["optional"]}</small></label><textarea id="f-msg" rows="6" placeholder="{F["msg_ph"]}"></textarea></div>
<input class="hp" id="f-honey" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="full" style="display:flex;flex-wrap:wrap;align-items:center;gap:16px 24px"><button class="btn" id="send" type="submit">{F["send"]}</button><p class="fstatus" id="f-status" role="status" aria-live="polite"></p></div>
<p class="note full">{F["privacy"].format(p=p)}</p>
</form>
<aside class="aside fade" id="nous-contacter"><span class="eyebrow">{T[lang]["booking"]}</span><h3>{X["aside_title"]}</h3><p>{X["aside_text"]}</p>
<div class="who"><img src="{p}assets/avatar-booking.jpg?v=2" alt="" width="64" height="64" loading="lazy"><div><b>NBC Booking</b><span>{X["aside_role"]}</span></div></div>
<ul><li><a href="tel:{TEL}">{ic("phone")}{T[lang]["tel_txt"]}</a></li><li><a href="{wa(lang)}" target="_blank" rel="noopener">{ic("whatsapp")}WhatsApp</a></li><li><a href="mailto:{MAIL}">{ic("mail")}{MAIL}</a></li><li><a href="{IG_AJ}" target="_blank" rel="noopener">{ic("instagram")}@ajliveevenement</a></li></ul>
<p style="margin-top:24px">{X["aside_note"]}</p></aside>
</div></section>'''
    js = '<script>window.AJ_FORM=' + json.dumps(F['js'], ensure_ascii=False) + ';</script>\n<script src="' + p + 'assets/form.js?v=2" defer></script>\n'
    return page(lang, 'contact', X['quote_page_title'], X['quote_page_desc'], body, extra_js=js)


def reach(lang):
    """Contact page: only the ways to reach the booking team, as large tap targets."""
    X, p = C.TXT[lang], prefix(PATHS[lang]['reach'])
    fr = lang == 'fr'
    cards = [
        ('phone', 'Appeler' if fr else 'Call', T[lang]['tel_txt'], f'tel:{TEL}', ''),
        ('whatsapp', 'WhatsApp', 'Écrire un message' if fr else 'Send a message', wa(lang), ' target="_blank" rel="noopener"'),
        ('mail', 'Email', MAIL, f'mailto:{MAIL}', ''),
        ('instagram', 'Instagram', '@ajliveevenement', IG_AJ, ' target="_blank" rel="noopener"'),
    ]
    grid = ''.join(f'<a class="ct-card fade" href="{h}"{x}>{ic(i)}<span><small>{l}</small><b>{v}</b></span></a>' for i, l, v, h, x in cards)
    body = page_hero('Contact', T[lang]['contact_us'],
                     "Une question, une date à vérifier ? NBC Booking gère l’agenda d’Alex Juan et vous répond rapidement." if fr else
                     "A question or a date to check? NBC Booking manages Alex Juan’s calendar and gets back to you quickly.")
    body += f'''<section class="sec"><div class="wrap">
<div class="ct-who fade"><img src="{p}assets/avatar-booking.jpg?v=2" alt="" width="72" height="72" loading="lazy"><div><b>NBC Booking</b><span>{X["aside_role"]}</span></div></div>
<div class="ct-grid">{grid}</div>
<p class="ct-more fade">{"Vous avez déjà une date et un lieu ?" if fr else "Already have a date and a venue?"} <a href="{url(lang, "contact", p)}">{"Demander un devis gratuit" if fr else "Request a free quote"}</a> · <a href="{url(lang, "booking", p)}">{"Réserver ma date" if fr else "Book my date"}</a></p>
</div></section>'''
    title = ('Nous contacter · Alex Juan Live Événement' if fr else 'Contact us · Alex Juan Live Événement')
    desc = ("Contactez NBC Booking, le booking d’Alex Juan Live Événement : téléphone, WhatsApp, email ou Instagram." if fr else
            "Contact NBC Booking, Alex Juan Live Événement’s booking agency: phone, WhatsApp, email or Instagram.")
    return page(lang, 'reach', title, desc, body)


def service(key):
    S = C.FR_SERVICES[key]
    path = PATHS['fr'][key]
    p = prefix(path)
    moments = ''.join(f'<li>{ic(i)}<div><b>{h}</b><span>{t}</span></div></li>' for i, h, t in S['moments'])
    zones = ''.join(f'<li>{z}</li>' for z in C.ZONES)
    others = ''.join(f'<li>{ic("arrow")}<a href="{url("fr", k, p)}">{n}</a></li>' for k, n in T['fr']['services'] if k != key)
    body = f'''<section class="page-hero"><div class="wrap split">
<div>{crumbs("fr", p, S["crumb"])}<span class="eyebrow">{S["eyebrow"]}</span><h1 class="h1" style="font-size:clamp(40px,5.6vw,76px)">{S["h1"]}</h1><p class="lead">{S["lead"]}</p>
<div style="display:flex;flex-wrap:wrap;gap:16px 32px;align-items:center;margin-top:40px"><a class="btn gold" href="{url("fr", "contact", p)}">Demander un devis</a>{link(url("fr", "booking", p), "Réserver ma date")}</div></div>
<div><img class="hero-img" src="{p}assets/{S["img"]}" alt="{S["alt"]}" width="900" height="1125"></div>
</div></section>
<section class="sec"><div class="wrap split">
<div class="fade"><span class="eyebrow">{S["why_eyebrow"]}</span><h2 class="h2" style="margin:20px 0 22px">{S["why_title"]}</h2><p class="lead">{S["why_lead"]}</p></div>
<div class="ivory fade">{facts([(i, h, t) for i, h, t in S["moments"]])}</div>
</div></section>
<section class="sec dark"><div class="wrap">
<div class="sec-head fade"><span class="eyebrow">Déroulé</span><h2 class="h2">Comment ça se passe</h2></div>
{steps(S["steps"])}
</div></section>
<section class="sec stone"><div class="wrap">
<div class="sec-head fade"><span class="eyebrow">Inclus</span><h2 class="h2">Ce qui est inclus</h2></div>
{checks(S["incl"])}
<p class="fade" style="margin-top:36px">{link(url("fr", "show", p), "Voir les vidéos et le répertoire")}</p>
</div></section>
<section class="sec"><div class="wrap">
<div class="sec-head fade"><span class="eyebrow">Déplacements</span><h2 class="h2">{S["zone_title"]}</h2><p class="lead">{S["zone_lead"]}</p></div>
<ul class="zones fade">{zones}</ul>
</div></section>
<section class="sec stone"><div class="wrap">
<div class="sec-head fade"><span class="eyebrow">Questions</span><h2 class="h2">Questions fréquentes</h2></div>
{faq(S["faq"])}
<p class="eyebrow" style="margin-top:56px">Autres prestations</p><ul class="checks" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr));margin-top:8px">{others}</ul>
</div></section>''' + cta('fr', p, S['cta'])
    ld = [{'@context': 'https://schema.org', '@type': 'Service', 'name': S['stype'], 'serviceType': S['stype'], 'url': SITE + path, 'description': S['desc'],
           'areaServed': {'@type': 'Country', 'name': 'France'}, 'provider': {'@type': ['MusicGroup', 'LocalBusiness'], 'name': 'Alex Juan Live Événement', 'url': SITE, 'telephone': TEL, 'email': MAIL}},
          faq_ld(S['faq']),
          {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
              {'@type': 'ListItem', 'position': 1, 'name': 'Accueil', 'item': SITE},
              {'@type': 'ListItem', 'position': 2, 'name': 'Prestations', 'item': SITE + 'prestations/'},
              {'@type': 'ListItem', 'position': 3, 'name': S['crumb'], 'item': SITE + path}]}]
    return page('fr', key, S['title'], S['desc'], body, ld)


def legal(fname):
    """Re-wraps a legal page's text in the new layout (the text itself is kept as written)."""
    src = open(os.path.join(ROOT, fname)).read()
    main = re.search(r'<main[^>]*>(.*?)</main>', src, re.S).group(1)
    if 'class="legal"' in main:  # already converted once: take the text back out
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', main, re.S).group(1)
        upd = re.search(r'<p class="lead">(.*?)</p>', main, re.S).group(1)
        inner = re.search(r'<div class="legal">(.*)</div></div></section>', main, re.S).group(1)
    else:
        h1 = re.search(r'<h1>(.*?)</h1>', main, re.S).group(1)
        u = re.search(r'<p class="upd">(.*?)</p>', main, re.S)
        upd = u.group(1) if u else ''
        inner = re.sub(r'<p class="upd">.*?</p>', '', re.sub(r'<h1>.*?</h1>', '', main, 1, re.S), 1, re.S)
    title = re.search(r'<title>(.*?)</title>', src).group(1).split(' · ')[0]
    body = page_hero('Informations légales', h1, upd) + f'<section class="sec tight"><div class="wrap"><div class="legal">{inner.strip()}</div></div></section>'
    return page('fr', None, f'{title} · Alex Juan Live Événement', f'{title} du site Alex Juan Live Événement.', body, path=fname, robots='noindex')


def not_found():
    body = page_hero('Erreur 404', "Cette page n'existe pas", "Elle a peut-être changé d'adresse. Retrouvez tout le site depuis l'accueil.")
    body += '<section class="sec tight"><div class="wrap"><a class="btn" href="/">Retour à l\'accueil</a></div></section>'
    html = page('fr', None, 'Page introuvable · Alex Juan Live Événement', 'Page introuvable.', body, path='', robots='noindex')
    # served from any depth: make root-relative links absolute
    return re.sub(r'(href|src)="(?:\./)?(?=assets/|favicon|prestations/|le-show/|equipe/|reserver/|contact/|nous-contacter/|chanteur-|animation-|mentions-|confidentialite|cgu|cgv|en/)', r'\1="/', html).replace('href="./"', 'href="/"')


if __name__ == '__main__':
    for lang in ('fr', 'en'):
        write(PATHS[lang]['home'] + 'index.html', home(lang))
        for k, fn in (('prestations', prestations), ('show', show), ('team', team), ('booking', booking), ('contact', contact), ('reach', reach)):
            write(PATHS[lang][k] + 'index.html', fn(lang))
    for k in ('mariage', 'entreprise', 'prive'):
        write(PATHS['fr'][k] + 'index.html', service(k))
    for f in ('mentions-legales.html', 'confidentialite.html', 'cgu.html', 'cgv.html'):
        write(f, legal(f))
    write('404.html', not_found())
