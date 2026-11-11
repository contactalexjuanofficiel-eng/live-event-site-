"""Builds the French pages of live.alexjuan.com from parts.py.  Run:  python3 _build/build.py [--preview]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from parts import head, top, foot, ic, TEL, TEL_TXT, SERVICES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def write(rel, html):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(html)
    print('wrote', rel)


def home(p=''):
    svc_img = {'chanteur-mariage-bordeaux/': ('portrait.jpg?v=2', 'Alex Juan, chanteur pour mariages', "Cérémonie, vin d'honneur, dîner, ouverture de bal : la musique suit chaque moment de votre journée."),
               'animation-musicale-entreprise-bordeaux/': ('scene.jpg', 'Alex Juan sur scène sous les projecteurs', 'Soirées de gala, séminaires, lancements : un show soigné, avec sa propre sonorisation.'),
               'chanteur-anniversaire-soiree-privee-bordeaux/': ('contact.jpg', 'Alex Juan, micro en main', 'Anniversaires, cocktails, réceptions : du set intimiste au grand show.')}
    cards = ''.join(f'''<a class="fade" href="{p}{h}"><figure><img src="{p}assets/{svc_img[h][0]}" alt="{svc_img[h][1]}" loading="lazy" width="900" height="1125"></figure>
<h3 class="h3">{t}</h3><p>{svc_img[h][2]}</p><span class="link"><span>Découvrir</span>{ic("arrow")}</span></a>''' for h, t in SERVICES)
    team = [('avatar-alex.jpg?v=2', 'Alex Juan', 'Chanteur'), ('avatar-antonin.jpg?v=2', 'Antonin', 'Son et lumière'), ('avatar-booking.jpg?v=2', 'NBC Booking', 'Booking et réservations')]
    team_html = ''.join(f'<div class="fade"><div class="ph"><img src="{p}assets/{i}" alt="{n}" loading="lazy" width="320" height="320"></div><b>{n}</b><span>{r}</span></div>' for i, n, r in team)
    body = f'''<main id="main">
<section class="hero">
<video autoplay muted loop playsinline preload="metadata" poster="{p}assets/hero-poster-2.jpg" aria-hidden="true"><source src="{p}assets/hero-720.webm" type="video/webm"><source src="{p}assets/hero-720.mp4" type="video/mp4"></video>
<div class="wrap">
<span class="eyebrow">Alex Juan · Chanteur live</span>
<h1 class="h1">Un show live d'exception pour vos plus beaux moments</h1>
<p class="lead">Chanson française et pop, son et lumière inclus. Mariages, événements d'entreprise et soirées privées, partout en France.</p>
<div class="actions"><a class="btn gold" href="{p}contact/">Demander un devis</a><a class="link" href="{p}le-show/"><span>Voir le show</span>{ic("arrow")}</a></div>
</div>
</section>

<section class="sec"><div class="wrap">
<div class="sec-head fade"><span class="eyebrow">Prestations</span><h2 class="h2">Un show pour chaque événement</h2><p class="lead">Le format se compose avec vous, de l'accueil de vos invités au dernier titre de la soirée.</p></div>
<div class="svc">{cards}</div>
</div></section>

<section class="sec dark"><div class="wrap split">
<div class="fade"><div class="player" data-yt="IAmyNBhYdxw"><button type="button" aria-label="Lire la vidéo d'Alex Juan en live"><img src="{p}assets/videos/video-2.jpg" alt="" loading="lazy" width="720" height="1280"><span class="play">{ic("play")}</span></button></div></div>
<div class="fade"><span class="eyebrow">Le show</span><h2 class="h2" style="margin-top:22px">Une voix, une équipe, une soirée qui vous ressemble</h2>
<ul class="facts">
<li>{ic("sound")}<div><b>Son et lumière inclus</b><span>Antonin, notre ingénieur, est présent à chaque prestation.</span></div></li>
<li>{ic("note")}<div><b>Répertoire sur mesure</b><span>Les grands classiques et la chanson d'aujourd'hui, choisis avec vous.</span></div></li>
<li>{ic("pin")}<div><b>Partout en France</b><span>Nous venons là où se tient votre événement.</span></div></li>
</ul>
<a class="link" href="{p}le-show/" style="margin-top:32px"><span>Vidéos et répertoire</span>{ic("arrow")}</a></div>
</div></section>

<section class="sec stone"><div class="wrap">
<div class="sec-head center fade"><span class="eyebrow">L'équipe</span><h2 class="h2">Une équipe à vos côtés</h2><p class="lead">De la première prise de contact au dernier rappel, les mêmes personnes s'occupent de votre soirée.</p></div>
<div class="team">{team_html}</div>
<p style="text-align:center;margin-top:48px" class="fade"><a class="link" href="{p}equipe/"><span>Rencontrer l'équipe</span>{ic("arrow")}</a></p>
</div></section>

<section class="sec night cta"><div class="wrap fade">
<span class="eyebrow">Réservation</span>
<h2 class="h2">Votre date est&#8209;elle encore libre&nbsp;?</h2>
<p class="lead">Devis gratuit et personnalisé, réponse sous 24 h.</p>
<div class="actions"><a class="btn gold" href="{p}contact/">Demander un devis</a><a class="tel" href="tel:{TEL}">{ic("phone")}{TEL_TXT}</a></div>
</div></section>
</main>
'''
    return (head(p, 'Alex Juan · Chanteur live pour mariages et événements, partout en France',
                 "Chant live, son et lumière inclus, pour mariages, événements d'entreprise et soirées privées. Alex Juan et son équipe se déplacent partout en France. Devis gratuit sous 24 h.", '')
            + top(p, '') + body + foot(p))


if __name__ == '__main__':
    if '--preview' in sys.argv:
        write('preview.html', home(''))
    else:
        write('index.html', home(''))
