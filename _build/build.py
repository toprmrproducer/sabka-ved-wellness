"""Build the Sabka Ved Wellness static site from the mirrored Medara template.

Keeps every page's DOM, classes, data-wf-* attributes and per-page IX3 chunk intact; swaps only text, images,
alt, href, meta and form options. Run: python3 _build/build.py
"""
import copy
import html
import json
import os
import re
import shutil
import sys
import urllib.parse

from bs4 import BeautifulSoup, NavigableString, Tag

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MIRROR = os.path.join(ROOT, '_template-mirror')
RAW = os.path.join(MIRROR, 'raw')
ASSETS_IN = os.path.join(MIRROR, 'assets')
OUT = ROOT
ASSETS = os.path.join(OUT, 'assets')
sys.path.insert(0, HERE)

import content as C  # noqa: E402
import logos  # noqa: E402
from images import ImageBank  # noqa: E402

MAPPING = json.load(open(os.path.join(MIRROR, 'mapping.json')))
NORM_MAP = {}
for k, v in MAPPING.items():
    NORM_MAP[urllib.parse.unquote(k).split('?')[0]] = v

bank = ImageBank(os.path.join(ASSETS, 'img'))

FOCUS = {
    'doctor-clinic-nehru-jacket': (0.65, 0.33), 'doctor-consult-desk-wide': (0.66, 0.42),
    'doctor-dispensary-herbs': (0.72, 0.35), 'doctor-green-kurta-herbs': (0.34, 0.4),
    'doctor-herb-garden-walk': (0.53, 0.5), 'doctor-manuscript-desk': (0.6, 0.38),
    'doctor-portrait-white-coat': (0.5, 0.36), 'doctor-preparing-herbs': (0.6, 0.4),
    'doctor-real-portrait-round': (0.5, 0.42), 'doctor-with-patient-wide': (0.5, 0.5),
    'stock-golden-milk-spices': (0.5, 0.5), 'stock-herbs-capsules': (0.5, 0.5),
    'stock-shoulder-massage': (0.55, 0.42), 'stock-turmeric': (0.25, 0.42),
}

PAGE_CHUNKS = {}
CSS_NAME = 'sabka-ved.webflow.shared.css'


# ----------------------------------------------------------------------------------------------- helpers
def soup_of(name):
    return BeautifulSoup(open(os.path.join(RAW, name + '.html')).read(), 'html.parser')


class Page:
    def __init__(self, soup, depth):
        self.s = soup
        self.depth = depth

    @property
    def p(self):
        return '../' * self.depth

    def link(self, target):
        """target like '', 'about/', 'services/vamana/', '#faq'."""
        if target.startswith('http') or target.startswith('mailto:') or target.startswith('tel:'):
            return target
        if target.startswith('#'):
            return (self.p or './') + target if self.depth else target
        return (self.p + target) or './'

    def asset(self, path):
        return self.p + 'assets/' + path


def txt(el, text):
    """Replace all text content of el with text (keeps the element)."""
    el.clear()
    el.append(NavigableString(text))


def all_text(el, text):
    for t in el:
        txt(t, text)


def sel(page, css):
    return page.s.select(css)


def one(page, css, root=None):
    r = (root or page.s).select_one(css)
    if r is None:
        raise RuntimeError(f'selector not found: {css}')
    return r


def set_button(a, label, href=None, page=None):
    for t in a.select('.button-text'):
        txt(t, label)
    if href is not None:
        a['href'] = page.link(href)


def set_navlink(a, label, href, page):
    for t in a.select('.nav-text'):
        txt(t, label)
    a['href'] = page.link(href)


def put_img(page, img, key, name, aspect, focus=None, zoom=1.0, alt='', sizes=None, max_w=2000):
    info = bank.make(key, name, aspect, focus or FOCUS.get(name, (0.5, 0.5)), zoom, max_w=max_w)
    img['src'] = page.asset(info['src'])
    if info['single']:
        img.attrs.pop('srcset', None)
        img.attrs.pop('sizes', None)
    else:
        img['srcset'] = ', '.join(page.asset(x) for x in info['srcset'].split(', '))
        if sizes:
            img['sizes'] = sizes
        elif not img.get('sizes'):
            img['sizes'] = '(max-width: 767px) 92vw, 50vw'
    img['alt'] = alt
    img['width'] = str(info['w'])
    img['height'] = str(info['h'])
    return info


def clone_after(el, n=1):
    last = el
    out = []
    for _ in range(n):
        c = copy.copy(el)
        last.insert_after(c)
        last = c
        out.append(c)
    return out


def counter_cols(digit):
    d = int(digit)
    return [str((d + i) % 10) for i in range(11)]


def set_counter(count_num, value, suffix=''):
    """count-num with count-forward/count-reverse columns: keep as many columns as digits in value."""
    cols = [c for c in count_num.find_all(recursive=False) if 'count-forward' in c.get('class', []) or 'count-reverse' in c.get('class', [])]
    tails = [c for c in count_num.find_all(recursive=False) if c not in cols]
    digits = list(value)
    for i, col in enumerate(cols):
        if i >= len(digits):
            col.decompose()
            continue
        kids = col.find_all(recursive=False)
        seq = counter_cols(digits[i])
        for k, d in zip(kids, seq):
            txt(k, d)
    for i, t in enumerate(tails):
        if i == 0 and suffix:
            txt(t, suffix)
        else:
            t.decompose()


# ----------------------------------------------------------------------------------------------- head
def build_head(page, title, desc, path, og_img, extra_ld=None, noindex=False, booking=False):
    s = page.s
    head = s.head
    for t in head.find_all('title'):
        t.decompose()
    for m in head.find_all('meta'):
        if m.get('name') in ('description', 'twitter:title', 'twitter:description', 'twitter:image', 'twitter:card', 'generator') \
                or (m.get('property') or '').startswith('og:'):
            m.decompose()
    for l in head.find_all('link'):
        rel = ' '.join(l.get('rel', []))
        if 'icon' in rel or 'preconnect' in rel or 'apple-touch-icon' in rel:
            l.decompose()
    for sc in head.find_all('script'):
        if sc.get('src') and 'workers.dev' in sc['src']:
            sc.decompose()
        elif sc.string and '__WF_REVIEW_BRIDGE' in sc.string:
            sc.decompose()
    canonical = C.SITE_URL + path
    og = C.SITE_URL + 'assets/' + og_img
    frag = [
        f'<title>{html.escape(title)}</title>',
        f'<meta name="description" content="{html.escape(desc, quote=True)}"/>',
        f'<link rel="canonical" href="{canonical}"/>',
        '<meta name="robots" content="noindex"/>' if noindex else '',
        '<meta property="og:type" content="website"/>',
        f'<meta property="og:site_name" content="{C.BRAND}"/>',
        f'<meta property="og:title" content="{html.escape(title, quote=True)}"/>',
        f'<meta property="og:description" content="{html.escape(desc, quote=True)}"/>',
        f'<meta property="og:url" content="{canonical}"/>',
        f'<meta property="og:image" content="{og}"/>',
        '<meta property="og:image:width" content="1200"/><meta property="og:image:height" content="630"/>',
        '<meta property="og:locale" content="en_IN"/>',
        '<meta name="twitter:card" content="summary_large_image"/>',
        f'<meta name="twitter:title" content="{html.escape(title, quote=True)}"/>',
        f'<meta name="twitter:description" content="{html.escape(desc, quote=True)}"/>',
        f'<meta name="twitter:image" content="{og}"/>',
        '<meta name="theme-color" content="#121212"/>',
        f'<link rel="icon" type="image/svg+xml" href="{page.asset("img/favicon.svg")}"/>',
        f'<link rel="icon" type="image/png" sizes="32x32" href="{page.asset("img/favicon-32.png")}"/>',
        f'<link rel="icon" type="image/png" sizes="192x192" href="{page.asset("img/favicon-192.png")}"/>',
        f'<link rel="apple-touch-icon" sizes="180x180" href="{page.asset("img/apple-touch-icon.png")}"/>',
    ]
    lds = [clinic_ld()] + (extra_ld or [])
    for ld in lds:
        frag.append('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>')
    if booking:
        # must load before webflow.js so its capture-phase submit listener wins
        frag.append(f'<script src="{page.asset("js/booking.js")}"></script>')
    meta_vp = head.find('meta', attrs={'name': 'viewport'})
    anchor = head.find('meta', attrs={'charset': True})
    new = BeautifulSoup(''.join(frag), 'html.parser')
    for node in reversed(list(new.contents)):
        anchor.insert_after(node)
    # html attrs: drop webflow domain/status (badge), keep page/site ids for IX3
    h = s.html
    for a in ('data-wf-domain', 'data-wf-status'):
        h.attrs.pop(a, None)
    h['lang'] = 'en-IN'


def clinic_ld():
    return {
        '@context': 'https://schema.org', '@type': 'MedicalClinic', '@id': C.SITE_URL + '#clinic',
        'name': C.BRAND, 'url': C.SITE_URL,
        'description': 'Panchakarma and Ayurvedic therapy centre near Bajrang Puri, Patna, led by Dr. Aditya Kunal, BAMS.',
        'image': C.SITE_URL + 'assets/img/og-home.jpg',
        'logo': C.SITE_URL + 'assets/img/favicon-512.png',
        'medicalSpecialty': 'Ayurvedic',
        'address': {'@type': 'PostalAddress', 'streetAddress': 'Near Bajrang Puri', 'addressLocality': 'Patna',
                    'addressRegion': 'Bihar', 'addressCountry': 'IN'},
        'areaServed': {'@type': 'City', 'name': 'Patna'},
        'founder': {'@type': 'Person', 'name': C.DOCTOR, 'honorificSuffix': 'BAMS', 'url': C.DOCTOR_SITE},
        'employee': {'@type': 'Physician', 'name': C.DOCTOR, 'medicalSpecialty': 'Ayurvedic', 'url': C.DOCTOR_SITE},
        'availableService': [{'@type': 'MedicalTherapy', 'name': t['name']} for t in C.THERAPIES],
        'sameAs': [C.DOCTOR_SITE],
    }


def faq_ld():
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q,
                            'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in C.FAQ]}


# ----------------------------------------------------------------------------------------------- shared parts
def do_scripts(page):
    s = page.s
    for sc in s.find_all('script'):
        src = sc.get('src')
        if src:
            if 'workers.dev' in src:
                sc.decompose()
                continue
            if 'webflow.' in src and '/js/' in src:
                PAGE_CHUNKS.setdefault(page.name, []).append(src.split('/')[-1])
        elif sc.string and 'new Lenis' in sc.string:
            code = sc.string
            code = re.sub(r"//get scroll value\s*\n", '', code)
            code = re.sub(r"lenis\.on\('scroll'.*?\}\)\s*\n\}\)", '', code, flags=re.S)
            code = re.sub(r"lenis\.on\('scroll',[^\n]*\n\}\)", '', code)
            if 'console.log' in code:
                raise RuntimeError('lenis console.log still present')
            sc.string = code
    for sc in s.find_all('script', src=True):
        sc.attrs.pop('integrity', None)
        sc.attrs.pop('crossorigin', None)
    for l in s.find_all('link', href=True):
        l.attrs.pop('integrity', None)
        l.attrs.pop('crossorigin', None)


NAV_COL1 = [('Home', ''), ('About', 'about/'), ('Our Doctor', 'specialists/'), ('Appointment', 'appointment/'),
            ('Contact', 'contact/')]
NAV_COL2 = [('Therapies', 'services/'), ('Consultation', 'services/panchakarma-consultation/'), ('Journal', 'blog/'),
            ('Panchakarma Explained', 'blog/what-is-panchakarma-explained-simply/')]


def do_nav(page):
    nav = one(page, '.navbar')
    dark = 'v2' in nav.get('class', [])
    brand = one(page, '.brand', nav)
    brand['href'] = page.link('')
    brand['aria-label'] = 'Sabka Ved Wellness home'
    bl = one(page, '.brand-logo', brand)
    bl['src'] = page.asset('img/brand-logo-dark.svg' if dark else 'img/brand-logo.svg')
    bl['alt'] = ''
    bl.attrs.pop('srcset', None); bl.attrs.pop('sizes', None)
    bt = one(page, '.brand-logo-text', brand)
    bt['src'] = page.asset('img/brand-logo-text-dark.svg' if dark else 'img/brand-logo-text.svg')
    bt['alt'] = 'Sabka Ved Wellness'
    bt.attrs.pop('srcset', None); bt.attrs.pop('sizes', None)
    wrapper = one(page, '.nav-menu-wrapper', nav)
    top = [c for c in wrapper.find_all(['a', 'div'], recursive=False)]
    links = [c for c in top if c.name == 'a']
    # About, Services, Blog, Specialists
    for a in links:
        label = a.select_one('.nav-text').get_text(strip=True)
        m = {'About': ('About', 'about/'), 'Services': ('Therapies', 'services/'), 'Blog': ('Journal', 'blog/'),
             'Specialists': ('Our Doctor', 'specialists/')}[label]
        set_navlink(a, m[0], m[1], page)
    for t in nav.select('.dropdown-text'):
        txt(t, 'Explore')
    for box in nav.select('.drop-inner-box'):
        cols = box.select('.menu-colum')
        for col, spec in zip(cols[:2], (NAV_COL1, NAV_COL2)):
            for a, (label, href) in zip(col.select('a.nav-link'), spec):
                set_navlink(a, label, href, page)
        for col in cols[2:]:
            col.decompose()
    for a in nav.select('.nav-menu-button-wrapper a.button'):
        set_button(a, 'Book Appointment', 'appointment/', page)


def do_footer(page):
    f = one(page, 'section.footer')
    txt(one(page, '.footer-title-wrap h2', f), 'Ayurveda that begins with listening.')
    set_button(one(page, '.footer-title-wrap a.button', f), 'Book a Visit', 'appointment/', page)
    menus = f.select('.footer-menu')
    nav1 = [('Home', ''), ('Therapies', 'services/'), ('About', 'about/'), ('Our Doctor', 'specialists/'), ('Contact', 'contact/')]
    nav2 = [('Journal', 'blog/'), (C.DOCTOR, C.DOCTOR_SITE), ('FAQ', '#faq'), ('Appointment', 'appointment/'),
            ('Consultation', 'services/panchakarma-consultation/')]
    txt(one(page, '.stroke', menus[0]), 'Navigation')
    txt(one(page, '.stroke', menus[1]), 'Resources')
    for spec, menu in ((nav1, menus[0]), (nav2, menus[1])):
        for a, (label, href) in zip(menu.select('a.nav-link'), spec):
            set_navlink(a, label, href, page)
            if href.startswith('http'):
                a['target'] = '_blank'
                a['rel'] = 'noopener'
    socials = f.select('.footer-middle a.social-link')
    for a, label in zip(socials, ['Instagram', 'YouTube', 'WhatsApp']):
        txt(one(page, '.social-link-text', a), label)
        a['href'] = '#'
        a['data-todo'] = 'social'
        a['aria-hidden'] = 'true'
        a['tabindex'] = '-1'
    for a in socials[3:]:
        a.decompose()
    blocks = f.select('.copywrite-block > div')
    blocks[0].clear(); blocks[0].append(NavigableString(C.PLACE))
    txt(blocks[1], '© 2026 Sabka Ved Wellness')
    blocks[2].clear()
    blocks[2].append(NavigableString('Run by '))
    a = page.s.new_tag('a', href=C.DOCTOR_SITE, target='_blank', rel='noopener', **{'class': 'company-link v2'})
    a.string = C.DOCTOR_FULL
    blocks[2].append(a)
    imgwrap = page.s.select_one('.footer-img-wrapper')
    for img in imgwrap.select('img.footer-logo'):
        img['src'] = page.asset('img/footer-logo.svg'); img['alt'] = ''
    sh = imgwrap.select_one('img.footer-shape')
    sh['src'] = page.asset('img/footer-shape.svg'); sh['alt'] = ''


def do_cta(page):
    c = page.s.select_one('section.cta')
    if not c:
        return
    txt(one(page, 'h2', c), 'Begin with a conversation, not a commitment.')
    set_button(one(page, 'a.button', c), 'Book a Consultation', 'appointment/', page)


def do_first_visit(page):
    sec = page.s.select_one('section.testimonial')
    if not sec:
        return
    txt(one(page, '.tag-text', sec), 'YOUR FIRST VISIT')
    put_img(page, one(page, 'img.testimonial', sec), 'fv-left', 'doctor-herb-garden-walk', 1.0, (0.53, 0.42),
            alt='Dr. Aditya Kunal walking through a herb garden', sizes='336px')
    txt(one(page, '.testimonial-title-wrap .text-h4', sec), 'A calm, unhurried first visit, led by the doctor.')
    set_button(one(page, '.testimonial-title-wrap a.button', sec), 'Book Appointment', 'appointment/', page)
    for slide, (step, title, msg, img, foc) in zip(sec.select('.w-slide'), C.FIRST_VISIT):
        put_img(page, one(page, 'img.slider-img', slide), 'fv-' + title.lower().replace(' ', '-'), img, 0.9, foc,
                alt=f'{title}: {C.DOCTOR} at Sabka Ved Wellness', sizes='(max-width: 767px) 92vw, 382px')
        ov = one(page, '.slider-overlay', slide)
        txt(one(page, '.body-text-light', ov), title)
        txt(one(page, '.tiny-text', ov), step)
        stars = one(page, '.star-icon-wrap', slide)
        for i in stars.find_all('img'):
            i.decompose()
        stars['aria-hidden'] = 'true'
        txt(one(page, '.testimonial-message .text-h6', slide), msg)
        put_img(page, one(page, 'img.author-img', slide), 'avatar-doctor', 'doctor-real-portrait-round', 1.0,
                (0.5, 0.36), zoom=1.9, alt='Dr. Aditya Kunal', max_w=200)
        info = one(page, '.author-ingo-wrap', slide)
        txt(one(page, '.medium', info), C.DOCTOR)
        txt(one(page, '.tiny-text', info), 'BAMS, Ayurvedic physician')


def blog_card(page, card, item, key_prefix):
    """item: dict(title, href, category, date, img, focus)"""
    card['href'] = page.link(item['href'])
    for i, img in enumerate(card.select('img.blog-card-img')):
        put_img(page, img, 'card-' + item['key'], item['img'], 1.6, item['focus'], alt='' if i else item['title'],
                sizes='(max-width: 767px) 92vw, 33vw')
    cats = card.select('.blog-category-wrap .tiny-text')
    txt(cats[0], item['category'])
    txt(cats[1], item['date'])
    txt(one(page, '.text-h6', card), item['title'])


def post_item(post):
    return dict(key=post['slug'][:24], title=post['title'], href=f"blog/{post['slug']}/", category=post['category'],
                date=post['date'], img=post['img'], focus=post['focus'])


def guide_item(slug):
    t = next(t for t in C.THERAPIES if t['slug'] == slug)
    return dict(key='guide-' + slug, title=f"{t['name']}: what the therapy involves", href=f'services/{slug}/',
                category='Therapy Guide', date=t['category'], img=t['img'], focus=FOCUS.get(t['img'], (0.5, 0.5)))


def do_blog_section(page, items=None):
    sec = page.s.select_one('section.blog')
    if not sec:
        return
    txt(one(page, '.tag-text', sec), 'JOURNAL')
    txt(one(page, 'h2', sec), 'Plain answers about Panchakarma, from the clinic.')
    txt(one(page, '.sub-para-wrap p', sec), 'Short reads for Patna families who want to understand Ayurvedic therapy before they book.')
    items = items or [post_item(p) for p in C.POSTS]
    for card, it in zip(sec.select('a.blog-card'), items):
        blog_card(page, card, it, '')


def do_faq(page):
    sec = page.s.select_one('section.faq')
    if not sec:
        return
    txt(one(page, '.tag-text', sec), 'FAQ')
    txt(one(page, 'h2', sec), 'Questions families ask before they begin.')
    put_img(page, one(page, 'img.faq-img', sec), 'faq', 'stock-turmeric', 1.14, (0.25, 0.42),
            alt='Turmeric powder and fresh turmeric root', sizes='(max-width: 767px) 92vw, 470px')
    items = sec.select('.faq-iteam')
    while len(items) < len(C.FAQ):
        clone_after(items[-1])
        items = sec.select('.faq-iteam')
    for it, (q, a) in zip(items, C.FAQ):
        txt(one(page, '.faq-title', it), q)
        txt(one(page, '.faq-para', it), a)


def do_common_hero(page, tag, h1, para, img, aspect, focus, alt):
    hero = one(page, 'section.common-hero')
    txt(one(page, '.tag-text', hero), tag)
    txt(one(page, 'h1', hero), h1)
    txt(one(page, '.about-para-wrap p', hero), para)
    put_img(page, one(page, 'img.hero-img', hero), 'hero-' + page.name, img, aspect, focus, alt=alt,
            sizes='100vw')


# ----------------------------------------------------------------------------------------------- forms
def opt_list(page, select, placeholder, options):
    select.clear()
    o = page.s.new_tag('option', value='')
    o.string = placeholder
    select.append(o)
    for v in options:
        o = page.s.new_tag('option', value=v)
        o.string = v
        select.append(o)


def field(page, wrap, label, name, ftype=None, placeholder=None, required=True, extra=None):
    lab = one(page, 'label', wrap)
    ctl = wrap.select_one('input, select, textarea')
    ident = 'f-' + name.lower()
    txt(lab, label + (' *' if required else ''))
    lab['for'] = ident
    ctl['id'] = ident
    ctl['name'] = name
    ctl['data-name'] = name
    if ftype:
        ctl['type'] = ftype
    if placeholder is not None:
        ctl['placeholder'] = placeholder
    elif 'placeholder' in ctl.attrs and ftype in ('date',):
        del ctl['placeholder']
    if required:
        ctl['required'] = ''
    else:
        ctl.attrs.pop('required', None)
    for k, v in (extra or {}).items():
        ctl[k] = v
    return ctl


def build_form(page, form, wraps_rows, checkbox_label):
    """wraps_rows: the .field-wrapper rows. We fill name/phone, age/date, therapy/gender, message, consent."""
    form['data-booking'] = ''
    form['novalidate'] = ''
    form['aria-label'] = 'Appointment request'


def fill_booking_form(page, form_block, kind):
    form = one(page, 'form', form_block)
    form['data-booking'] = kind
    form['novalidate'] = ''
    form['aria-label'] = 'Appointment request'
    rows = form.select('.field-wrapper')
    allwraps = form.select('.field-wrap')
    # collect wraps by control type
    inputs = [w for w in allwraps if w.select_one('input')]
    selects = [w for w in allwraps if w.select_one('select')]
    msg = [w for w in allwraps if w.select_one('textarea')][0]
    # Row 1: name + phone, Row 2: age + date, Row 3: therapy + gender
    r1, r2, r3 = rows[0], rows[1], rows[2]
    # ensure each row has the right wraps, moving existing wraps around
    w_name, w_phone, w_age, w_date = inputs[0], inputs[1], inputs[2], inputs[3]
    w_ther, w_gen = selects[0], selects[-1]
    extra_inputs = inputs[4:]
    extra_selects = selects[1:-1]
    for r in rows:
        for w in r.find_all('div', class_='field-wrap', recursive=False):
            w.extract()
    for r, pair in ((r1, (w_name, w_phone)), (r2, (w_age, w_date)), (r3, (w_ther, w_gen))):
        for w in pair:
            r.append(w)
    for w in extra_inputs + extra_selects:
        w.decompose()
    for r in rows[3:]:
        r.decompose()
    field(page, w_name, 'Full Name', 'Name', 'text', 'Your full name', extra={'autocomplete': 'name', 'maxlength': '80'})
    field(page, w_phone, 'Phone Number', 'Phone', 'tel', '10-digit mobile number',
          extra={'autocomplete': 'tel', 'inputmode': 'tel', 'maxlength': '16'})
    field(page, w_age, 'Age', 'Age', 'number', 'Age in years', extra={'min': '1', 'max': '110', 'inputmode': 'numeric'})
    ctl = field(page, w_date, 'Preferred Date', 'Preferred-Date', 'date', None)
    ctl.attrs.pop('placeholder', None)
    ctl.attrs.pop('maxlength', None)
    s1 = field(page, w_ther, 'Therapy', 'Therapy')
    opt_list(page, s1, 'Select a therapy or consultation', C.THERAPY_OPTIONS)
    s2 = field(page, w_gen, 'Gender', 'Gender')
    opt_list(page, s2, 'Select', ['Female', 'Male', 'Other', 'Prefer not to say'])
    field(page, msg, 'Message', 'Message', None,
          'Anything the doctor should know: current medicines, ongoing conditions, questions', required=False,
          extra={'maxlength': '1000'})
    # consent checkbox
    cb = form.select_one('label.w-checkbox')
    if cb is None:
        cb = BeautifulSoup('<label class="w-checkbox checkbox-field"><input type="checkbox" class="w-checkbox-input checkbox"/>'
                           '<span class="body-text-dark w-form-label"></span></label>', 'html.parser').label
        form.select_one('input[type=submit]').insert_before(cb)
    inp = one(page, 'input', cb)
    inp['name'] = 'Consent'
    inp['data-name'] = 'Consent'
    inp['id'] = 'f-consent'
    inp['required'] = ''
    lab = one(page, '.w-form-label', cb)
    lab['for'] = 'f-consent'
    txt(lab, 'I understand this is a request, not a confirmed booking, and that any therapy is planned only after '
             'the doctor\'s assessment.')
    sub = one(page, 'input[type=submit]', form)
    sub['value'] = 'Send Request'
    sub['data-wait'] = 'Please wait...'
    done = form_block.select_one('.w-form-done')
    txt(done.find('div'), 'Thank you. Online booking is opening shortly. Please call or WhatsApp the clinic to confirm your slot.')
    done['role'] = 'status'
    done['aria-live'] = 'polite'
    fail = form_block.select_one('.w-form-fail')
    txt(fail.find('div'), 'Please check the highlighted details and try again.')
    fail['role'] = 'alert'


# ----------------------------------------------------------------------------------------------- pages
def page_home(page):
    s = page.s
    hero = one(page, 'section.hero')
    txt(one(page, '.hero-tag-wrap .tiny-text', hero), 'Ayurveda in Patna')
    h1 = one(page, 'h1.hero-title', hero)
    span = one(page, '.hero-span', h1)
    for n in list(h1.contents):
        if isinstance(n, NavigableString):
            n.extract()
    span.insert_before(NavigableString('Classical Panchakarma, '))
    txt(span, 'Planned Around You')
    txt(one(page, 'p.hero', hero), 'Ayurvedic consultation and Panchakarma near Bajrang Puri, Patna. Every programme '
        'begins with Dr. Aditya Kunal\'s assessment and is shaped to your body, your season and your routine.')
    set_button(one(page, '.button-wrap.hero a.button', hero), 'Explore Therapies', 'services/', page)
    hi = one(page, 'img.hero-img', hero)
    put_img(page, hi, 'hero-home', 'doctor-clinic-nehru-jacket', 1.6, (0.62, 0.4),
            alt='Dr. Aditya Kunal, BAMS, at Sabka Ved Wellness in Patna', sizes='100vw')
    hi['style'] = 'object-position: 68% 30%'
    hi['loading'] = 'eager'
    hi['fetchpriority'] = 'high'
    # therapy name loop instead of partner logos
    names = ['vamana', 'virechana', 'basti', 'nasya', 'raktamokshana', 'abhyanga', 'shirodhara']
    for loop in s.select('.logo-loop'):
        for img, n in zip(loop.select('img.logo'), names):
            img['src'] = page.asset(f'img/loop-{n}.svg')
            img['alt'] = n.capitalize() if loop is s.select('.logo-loop')[0] else ''
    for i, loop in enumerate(s.select('.logo-loop')):
        if i:
            loop['aria-hidden'] = 'true'
    # about
    ab = one(page, 'section.about')
    txt(one(page, '.tag-text', ab), 'WHO WE ARE')
    txt(one(page, 'h2.about-summary', ab), 'Sabka Ved Wellness is a Panchakarma centre in Patna, led by Dr. Aditya '
        'Kunal, BAMS. We practise classical Ayurveda with patience: assess first, treat gently, and explain every step '
        'to you and your family.')
    cards = [('stock-shoulder-massage', (0.55, 0.45), 'Warm oil therapy on the shoulder'),
             ('doctor-preparing-herbs', (0.6, 0.45), 'Dr. Aditya Kunal preparing herbal medicines'),
             ('stock-golden-milk-spices', (0.5, 0.5), 'Golden milk with cinnamon and spices')]
    for img, (n, f, alt) in zip(ab.select('img.about-card-img'), cards):
        put_img(page, img, 'about-card-' + n, n, 0.98, f, alt=alt, sizes='(max-width: 767px) 92vw, 302px')
    loop_imgs = [('doctor-green-kurta-herbs', (0.34, 0.42)), ('stock-herbs-capsules', (0.5, 0.5)),
                 ('doctor-dispensary-herbs', (0.7, 0.4))]
    for wrap in s.select('.about-loop'):
        for img, (n, f) in zip(wrap.select('img.about-loop-img'), loop_imgs):
            put_img(page, img, 'about-loop-' + n, n, 1.42, f, alt='', sizes='(max-width: 767px) 80vw, 593px')
    # services tabs
    sv = one(page, 'section.services')
    txt(one(page, '.tag-text', sv), 'THERAPIES')
    txt(one(page, 'h2', sv), 'Classical therapies, prescribed with care.')
    tabs = [('Consultation and Nadi Pariksha', 'Pulse assessment, prakriti and a full history. The first step for '
             'everyone, and the moment the doctor decides what is right for you.', 'doctor-consult-desk-wide', (0.66, 0.42),
             'Dr. Aditya Kunal at his consultation desk'),
            ('The Classical Five', 'Vamana, Virechana, Basti, Nasya and Raktamokshana. The core Panchakarma procedures, '
             'chosen only when your assessment supports them.', 'doctor-preparing-herbs', (0.6, 0.42),
             'Herbal preparations being measured for a Panchakarma plan'),
            ('Supportive Therapies', 'Abhyanga, Swedana, Shirodhara, Kati, Janu and Greeva Basti, Netra Tarpana, '
             'Pizhichil and Udvartana, used to prepare, support and restore.', 'stock-shoulder-massage', (0.55, 0.4),
             'Hands giving a therapeutic shoulder massage'),
            ('Diet and Ritucharya', 'Food and daily routine for each phase of treatment and each season of the year, '
             'so the work continues once you are home.', 'stock-golden-milk-spices', (0.5, 0.42),
             'Golden milk with whole spices')]
    for a, (t, d, n, f, alt) in zip(sv.select('a.tab-link'), tabs):
        txt(one(page, '.text-h4', a), t)
        txt(one(page, '.body-text-dark', a), d)
    for img, (t, d, n, f, alt) in zip(sv.select('img.tab-img'), tabs):
        put_img(page, img, 'tab-' + n, n, 1.42, f, alt=alt, sizes='(max-width: 767px) 92vw, 593px')
    # difference (video -> still)
    df = one(page, 'section.difference')
    vid = one(page, '.difference-video', df)
    info = bank.make('difference-dark', 'doctor-preparing-herbs', 1.78, (0.6, 0.45), darken=0.55)
    for v in vid.find_all(['video', 'noscript']):
        v.decompose()
    for btn in vid.select('button'):
        btn.parent.decompose()
    vid['style'] = f"background-image:url('{page.asset(info['src'])}');background-size:cover;background-position:60% 40%"
    vid.attrs.pop('data-video-urls', None)
    vid.attrs.pop('data-poster-url', None)
    vid.attrs.pop('data-autoplay', None)
    vid.attrs.pop('data-loop', None)
    vid['role'] = 'img'
    vid['aria-label'] = 'Dr. Aditya Kunal preparing herbal medicines'
    txt(one(page, '.tag-text', df), 'Our difference')
    txt(one(page, 'h2', df), 'Assessment first. Therapy second.')
    txt(one(page, 'p.body-text-light', df), 'Panchakarma is planned only after a doctor\'s assessment, and it is not '
        'suitable for everyone. When it is not right for you, we will say so.')
    set_button(one(page, 'a.button', df), 'Meet the Doctor', 'specialists/', page)
    # choose
    ch = one(page, 'section.choose')
    txt(one(page, '.tag-text', ch), 'WHY CHOOSE US')
    txt(one(page, 'h2', ch), 'Careful Ayurveda for Patna families.')
    txt(one(page, '.sub-para-wrap p', ch), 'A doctor-led centre where every plan is written for one person, explained '
        'in plain words and reviewed as you go.')
    cl = one(page, '.choose-left-content', ch)
    txt(one(page, '.text-h4', cl), C.DOCTOR)
    for i in cl.select('.star-icon-wrap img'):
        i.decompose()
    txt(one(page, '.choose-review-text', cl), 'BAMS, AYURVEDIC PHYSICIAN')
    do_avatars(page, one(page, '.user-wrapper', cl))
    boxes = [('Doctor-led from day one', 'Dr. Aditya Kunal, BAMS, assesses you, writes your plan and reviews your '
              'progress himself.'),
             ('Classical and unhurried', 'Procedures follow the classical order of preparation, main therapy and '
              'recovery, at the pace your body allows.'),
             ('Honest about limits', 'Panchakarma is not for everyone. Pregnancy, acute fever, severe weakness and '
              'some heart conditions call for a different plan.')]
    for b, (t, d) in zip(ch.select('.choose-box'), boxes):
        txt(one(page, 'h3', b), t)
        txt(one(page, '.body-text-dark', b), d)
    # result -> at a glance
    rs = one(page, 'section.result')
    txt(one(page, '.tag-text', rs), 'AT A GLANCE')
    txt(one(page, 'h2', rs), 'What we offer, in plain numbers.')
    txt(one(page, '.sub-para-wrap p', rs), 'No inflated figures. Just the therapies we practise and the way every '
        'programme is structured.')
    txt(one(page, '.result-text', rs), 'At a glance')
    for li, (t, v) in zip(rs.select('.result-list'), [('Classical Panchakarma therapies', '5'),
                                                       ('Supportive therapies', '9'), ('Phases in every programme', '3')]):
        txt(one(page, '.text-h5', li), t)
        txt(one(page, '.counter-wrap div', li), v)
    put_img(page, one(page, 'img.result-img', rs), 'result', 'doctor-manuscript-desk', 0.96, (0.6, 0.4),
            alt='Dr. Aditya Kunal studying a classical Ayurvedic text', sizes='(max-width: 767px) 92vw, 411px')
    rr = one(page, '.result-right', rs)
    txt(one(page, '.text-h6', rr), 'Who plans it')
    txt(one(page, '.text-h3', rr), 'BAMS')
    txt(one(page, '.body-text-dark', rr), 'Every programme is planned and reviewed by Dr. Aditya Kunal, Ayurvedic physician.')
    do_benefit(page, home=True)
    do_first_visit(page)
    do_blog_section(page)
    do_faq(page)
    do_cta(page)


def do_avatars(page, wrap):
    imgs = wrap.find_all('img')
    put_img(page, imgs[0], 'avatar-doctor', 'doctor-real-portrait-round', 1.0, (0.5, 0.36), zoom=1.9,
            alt='Dr. Aditya Kunal', max_w=200)
    for i in imgs[1:]:
        i.decompose()


def do_benefit(page, home=False, therapy=None):
    b = page.s.select_one('section.benefit')
    if not b:
        return
    if home:
        put_img(page, one(page, 'img.benefit-img', b), 'benefit-home', 'doctor-green-kurta-herbs', 1.56, (0.34, 0.42),
                alt='Dr. Aditya Kunal among medicinal plants', sizes='(max-width: 767px) 92vw, 615px')
        txt(one(page, '.tag-text', b), 'WHAT A PROGRAMME INCLUDES')
        txt(one(page, 'h2', b), 'Everything around the therapy, not just the therapy.')
        txt(one(page, '.benefit-para-wrap .body-text-dark', b), 'Panchakarma works as a sequence. Each programme includes '
            'the steps that make the main therapy safe and meaningful.')
        items = ['Consultation and nadi pariksha', 'A clear plan for each phase', 'Diet guidance through recovery',
                 'Follow-up review with the doctor']
    else:
        t = therapy
        put_img(page, one(page, 'img.benefit-img', b), 'benefit-' + t['slug'], t['img3'], 1.56,
                FOCUS.get(t['img3']), alt=f'{C.DOCTOR} at Sabka Ved Wellness', sizes='(max-width: 767px) 92vw, 615px')
        txt(one(page, '.tag-text', b), 'HOW A PROGRAMME RUNS')
        txt(one(page, 'h2', b), 'Preparation, therapy, recovery. In that order.')
        txt(one(page, '.benefit-para-wrap .body-text-dark', b), 'Whatever your plan includes, it follows the classical '
            'sequence, adjusted to your strength and reviewed by the doctor as you go.')
        items = ['Purvakarma: preparation', 'Pradhanakarma: the main therapy', 'Paschatkarma: recovery and diet',
                 'Review with Dr. Aditya Kunal']
    for it, label in zip(b.select('.benefit-iteam'), items):
        txt(one(page, '.text-h6', it), label)
    bottom = b.select_one('.benefit-bottom')
    if bottom:
        do_avatars(page, one(page, '.user-wrapper', bottom))
        ut = one(page, '.benefit-user-text', bottom)
        txt(one(page, '.medium', ut), 'Your physician:')
        txt(one(page, '.tiny-text', ut), C.DOCTOR_FULL)
        mid = one(page, '.benefit-middle-content', bottom)
        txt(one(page, '.text-h4', mid), 'By appointment')
        txt(one(page, '.body-text-dark', mid), C.PLACE)
        set_button(one(page, 'a.button', bottom), 'Explore Therapies', 'services/', page)


def page_about(page):
    do_common_hero(page, 'About Sabka Ved', 'Classical Ayurveda, practised with patience.',
                   'Sabka Ved Wellness is a Panchakarma and Ayurvedic therapy centre near Bajrang Puri, Patna, run by '
                   'Dr. Aditya Kunal, BAMS.', 'doctor-consult-desk-wide', 2.1, (0.66, 0.42),
                   'Dr. Aditya Kunal at his consultation desk in Patna')
    care = one(page, 'section.care')
    txt(one(page, '.care-tag-text', care), 'PATIENT-FIRST CARE')
    txt(one(page, '.care-title-wrap .text-h5', care), 'Sabka Ved means Ayurveda for everyone. The work is simple to '
        'describe and serious to practise: understand the person in front of us, choose only what their body can take, '
        'and explain each step to them and their family.')
    put_img(page, one(page, 'img.care-left-img', care), 'care-left', 'doctor-herb-garden-walk', 0.78, (0.53, 0.5),
            alt='Dr. Aditya Kunal walking through a medicinal herb garden', sizes='(max-width: 767px) 92vw, 525px')
    put_img(page, one(page, 'img.care-right-img', care), 'care-right', 'doctor-manuscript-desk', 1.78, (0.6, 0.4),
            alt='Dr. Aditya Kunal reading a classical Ayurvedic manuscript', sizes='(max-width: 767px) 92vw, 623px')
    ex = one(page, 'section.experience')
    txt(one(page, 'h2', ex), 'How we work with every patient.')
    txt(one(page, '.experience-para-wrap .body-text-dark', ex), 'Four principles shape every consultation and every programme.')
    cards = [('Assess first', 'No therapy begins without a consultation and nadi pariksha.'),
             ('Personal plans', 'Each plan is written for one person, never copied from a package.'),
             ('Family included', 'Family members are welcome to join the consultation and ask questions.'),
             ('Clear limits', 'We say plainly when Panchakarma is not suitable, and why.')]
    for c, (t, d) in zip(ex.select('.experience-card'), cards):
        txt(one(page, '.text-h5', c), t)
        txt(one(page, '.body-text-dark', c), d)
    sp = one(page, 'section.support')
    paras = sp.select('.support-para')
    txt(one(page, '.body-text-light', paras[0]), 'Classical and supportive therapies, practised at one centre in Patna.')
    set_counter(one(page, '.count-num', sp), '14', '')
    txt(one(page, '.text-h5', paras[1]), 'Therapies under one roof')
    txt(one(page, '.body-text-light', paras[1]), 'Five classical Panchakarma procedures and nine supportive therapies, '
        'each used only when your plan calls for it.')
    hs = one(page, 'section.history')
    txt(one(page, 'h2', hs), 'Why Sabka Ved Wellness exists.')
    txt(one(page, '.sub-para-wrap .body-text-dark', hs), 'Patna families deserve Ayurveda that is classical, careful '
        'and honest. That is the whole idea.')
    hc = hs.select('.history-card')
    txt(one(page, '.text-h4', hc[0]), 'Our Mission')
    txt(one(page, 'p', hc[0]), 'To offer classical Panchakarma in Patna with a doctor\'s care at every step, explained '
        'in plain words and planned around each patient\'s health.')
    txt(one(page, '.text-h4', hc[1]), 'Our Vision')
    txt(one(page, 'p', hc[1]), 'A centre families trust for seasonal care and recovery, where the right answer is '
        'sometimes a smaller plan, or none at all.')
    for c, t in zip(hs.select('.history-category .tiny-text'), ['Classical Ayurveda', 'Ritucharya', 'Doctor-led care']):
        txt(c, t)
    hl = one(page, 'section.healthcare')
    txt(one(page, 'h2', hl), 'Rooted in the classics, careful in practice.')
    p = one(page, '.sub-para-wrap p', hl)
    p.clear()
    p.append(NavigableString('Panchakarma follows the order described in the classical texts: preparation, main therapy '
                             'and recovery. We keep that order and adjust the intensity to you. Read more about '))
    a = page.s.new_tag('a', href=C.DOCTOR_SITE, target='_blank', rel='noopener')
    a.string = 'Dr. Aditya Kunal on his personal site'
    a['style'] = 'text-decoration: underline'
    p.append(a)
    p.append(NavigableString('.'))
    infos = [('Preparation and main therapy', 'Oleation and steam prepare the body, then the chosen procedure is done '
              'under supervision.'),
             ('Recovery that is planned', 'A graded diet and routine help the body settle after the main therapy.')]
    for hi, (t, d) in zip(hl.select('.health-info'), infos):
        txt(one(page, '.text-h5', hi), t)
        txt(one(page, '.body-text-dark', hi), d)
    put_img(page, one(page, '.heathcare-wrapper img.img', hl), 'healthcare', 'doctor-green-kurta-herbs', 1.14,
            (0.34, 0.42), alt='Dr. Aditya Kunal with a notebook among medicinal plants',
            sizes='(max-width: 767px) 92vw, 542px')
    counters = [('5', '', 'Classical Panchakarma procedures.'),
                ('9', '', 'Supportive therapies, from Abhyanga to Udvartana.'),
                ('3', '', 'Phases in every programme: preparation, therapy, recovery.')]
    for cc, (v, suf, d) in zip(hl.select('.health-counter-content'), counters):
        set_counter(one(page, '.count-num', cc), v, suf)
        txt(cc.find('div', class_='body-text-dark', recursive=False), d)
    do_first_visit(page)
    do_cta(page)


def page_services(page):
    do_common_hero(page, 'Therapies', 'Panchakarma and Ayurvedic therapies in Patna.',
                   'Every therapy is offered only after a consultation. Your plan may use one of them, several, or none, '
                   'depending on what your assessment shows.', 'doctor-preparing-herbs', 2.1, (0.6, 0.42),
                   'Dr. Aditya Kunal preparing herbal medicines')
    lst = one(page, '.service-list')
    items = lst.select('.w-dyn-item')
    while len(items) < len(C.THERAPIES):
        clone_after(items[-1])
        items = lst.select('.w-dyn-item')
    for i, (it, t) in enumerate(zip(items, C.THERAPIES)):
        a = one(page, 'a.service-card', it)
        a['href'] = page.link(f"services/{t['slug']}/")
        txt(one(page, '.service-number', it), f'{i + 1:03d}/')
        txt(one(page, '.text-h4', it), t['name'])
        txt(one(page, '.service-para .body-text-dark', it), t['summary'])
        put_img(page, one(page, 'img.service-main-img', it), 'svc-' + t['slug'], t['img'], 1.75,
                FOCUS.get(t['img']), alt=f"{t['name']} at Sabka Ved Wellness, Patna",
                sizes='(max-width: 767px) 92vw, 416px')
    do_first_visit(page)
    do_blog_section(page)
    do_faq(page)
    do_cta(page)


def page_service_detail(page, t):
    sec = one(page, 'section.common')
    txt(one(page, '.tag-text', sec), t['category'].upper())
    txt(one(page, 'h1', sec), t['name'])
    txt(one(page, '.service-content-wrapper > .body-text-dark', sec), t['summary'])
    set_button(one(page, '.button-wrap.hero a.button', sec), 'Book Appointment', 'appointment/', page)
    infos = [('Session', t['session']), ('Category', t['category']), ('Planning', 'After assessment')]
    for w, (h, v) in zip(sec.select('.service-info-wrap'), infos):
        txt(one(page, '.text-h6', w), h)
        txt(one(page, '.tiny-text', w), v)
    put_img(page, one(page, 'img.service-card-img', sec), 'detail-' + t['slug'], t['img'], 0.96, FOCUS.get(t['img']),
            alt=f"{t['name']} at Sabka Ved Wellness, Patna", sizes='(max-width: 767px) 92vw, 552px')
    rts = sec.select('.service-details-wrapper > .detail-text')
    r0 = rts[0]
    txt(one(page, 'h2', r0), 'What to expect')
    ps = r0.find_all('p')
    txt(ps[0], t['expect'][0])
    txt(ps[2], t['expect'][1])
    txt(one(page, 'h2', rts[1]), 'Who it is for')
    txt(one(page, 'p', rts[1]), t['whofor'])
    fc = one(page, '.feature-card', sec)
    txt(one(page, 'h3', fc), t['list_title'])
    lis = fc.find_all('li')
    for li, v in zip(lis, t['items']):
        txt(li, v)
    put_img(page, one(page, 'img.feature-img', sec), 'feat-' + t['slug'], t['img2'], 1.29, FOCUS.get(t['img2']),
            alt='', sizes='(max-width: 767px) 92vw, 413px')
    do_benefit(page, therapy=t)
    do_first_visit(page)
    others = [post_item(p) for p in C.POSTS]
    do_blog_section(page, others)
    do_faq(page)
    do_cta(page)


def page_appointment(page):
    do_common_hero(page, 'Book Appointment', 'Request a consultation.',
                   'Tell us a little about yourself and the therapy you are interested in. The clinic confirms every '
                   'slot directly. Hours: by appointment.', 'doctor-with-patient-wide', 2.1, (0.5, 0.5),
                   'Dr. Aditya Kunal in consultation with a patient')
    bk = one(page, 'section.booking')
    txt(one(page, '.tag-text', bk), 'Appointment request')
    txt(one(page, 'h2', bk), 'Your details')
    fill_booking_form(page, one(page, '.w-form', bk), 'appointment')
    do_cta(page)


def page_contact(page):
    do_common_hero(page, 'Contact Us', 'Visit Sabka Ved Wellness.',
                   'Near Bajrang Puri, Patna, Bihar. All visits are by appointment.', 'doctor-manuscript-desk', 2.1,
                   (0.6, 0.4), 'Dr. Aditya Kunal at his study desk')
    ct = one(page, 'section.contact')
    put_img(page, one(page, 'img.contact-img', ct), 'contact', 'doctor-consult-desk-wide', 1.64, (0.66, 0.42),
            alt='Consultation desk at Sabka Ved Wellness', sizes='(max-width: 767px) 92vw, 575px')
    infos = ct.select('.contact-info-wrap')
    for w, (label, value, href) in zip(infos, [('Location:', C.PLACE, C.MAPS), ('Hours:', 'By appointment', None)]):
        t = one(page, '.contact-text', w)
        a = t.find('a')
        for n in list(t.contents):
            if isinstance(n, NavigableString):
                n.extract()
        a.insert_before(NavigableString(label + ' '))
        txt(a, value)
        if href:
            a['href'] = href
            a['target'] = '_blank'
            a['rel'] = 'noopener'
        else:
            a['href'] = page.link('appointment/')
    infos[0].find('img')['alt'] = ''
    infos[1].find('img')['alt'] = ''
    txt(one(page, '.contact-para .body-text-dark', ct), 'Phone and WhatsApp details will be listed here soon. Until '
        'then, send a request through the form and keep your phone handy.')
    ft = one(page, '.contact-form-title', ct)
    txt(one(page, '.text-h4', ft), 'Request a consultation')
    txt(one(page, '.body-text-dark', ft), 'Share your details and preferred date. Any therapy is planned only after '
        'the doctor\'s assessment.')
    fill_booking_form(page, one(page, '.w-form', ct), 'contact')
    do_cta(page)


def page_specialists(page):
    hero = one(page, 'section.common-hero')
    txt(one(page, '.tag-text', hero), 'Our Doctor')
    txt(one(page, 'h1', hero), 'Meet Dr. Aditya Kunal, BAMS.')
    txt(one(page, '.about-para-wrap p', hero), 'Ayurvedic physician and the doctor behind every consultation, plan '
        'and review at Sabka Ved Wellness, Patna.')
    for t, label in zip(hero.select('.treat-wrapper .body-text-light'),
                        ['Nadi Pariksha', 'Panchakarma Planning', 'Ritucharya', 'Herbal Medicine']):
        txt(t, label)
    put_img(page, one(page, 'img.hero-img', hero), 'hero-specialists', 'doctor-dispensary-herbs', 1.84, (0.7, 0.35),
            alt='Dr. Aditya Kunal in the herbal dispensary', sizes='100vw')
    dc = one(page, 'section.doctor')
    txt(one(page, 'h2', dc), 'One physician, from first pulse to final review.')
    p = one(page, '.sub-para-wrap p', dc)
    p.clear()
    p.append(NavigableString('Your plan is made and reviewed by the same doctor from start to finish. '))
    a = page.s.new_tag('a', href=C.DOCTOR_SITE, target='_blank', rel='noopener')
    a.string = 'Visit his personal site'
    a['style'] = 'text-decoration: underline'
    p.append(a)
    p.append(NavigableString('.'))
    cards = [(C.DOCTOR, 'BAMS, Ayurvedic physician', 'doctor-portrait-white-coat', (0.5, 0.36)),
             ('Consultation', 'History, nadi pariksha and prakriti', 'doctor-consult-desk-wide', (0.66, 0.42)),
             ('Panchakarma planning', 'A clear plan for each phase', 'doctor-preparing-herbs', (0.6, 0.42)),
             ('Herbal medicine', 'Formulations prescribed when needed', 'doctor-dispensary-herbs', (0.72, 0.35)),
             ('Classical study', 'Practice rooted in the classical texts', 'doctor-manuscript-desk', (0.6, 0.4)),
             ('Seasonal care', 'Ritucharya through the year', 'doctor-herb-garden-walk', (0.53, 0.45))]
    for card, (t, d, img, f) in zip(dc.select('.doctor-card'), cards):
        txt(one(page, '.text-h5', card), t)
        txt(one(page, '.body-text-dark', card), d)
        put_img(page, one(page, 'img.doctor-img', card), 'doc-' + img, img, 0.96, f,
                alt=f'{C.DOCTOR}: {t.lower() if t != C.DOCTOR else "portrait"}', sizes='(max-width: 767px) 92vw, 413px')
    do_first_visit(page)
    do_faq(page)
    do_cta(page)


def page_blog(page):
    bh = one(page, 'section.blog-hero')
    txt(one(page, 'h1', bh), 'Plain answers about Panchakarma.')
    txt(one(page, '.blog-hero-para p', bh), 'Short reads for Patna families who want to understand Ayurvedic therapy '
        'before they book.')
    txt(one(page, '.explore-wrap .body-text-dark', bh), 'Explore Articles')
    put_img(page, one(page, 'img.blog-hero-img', bh), 'blog-hero', 'doctor-green-kurta-herbs', 1.01, (0.34, 0.42),
            alt='Dr. Aditya Kunal among medicinal plants', sizes='(max-width: 767px) 100vw, 50vw')
    one(page, 'img.explore-icon', bh)['alt'] = 'Scroll to articles'
    lists = page.s.select('section.all-blog .blog-list')
    l1 = lists[0].select('.w-dyn-item')
    l2 = lists[1].select('.w-dyn-item')
    blog_card(page, one(page, 'a.blog-card', l1[0]), post_item(C.POSTS[0]), '')
    blog_card(page, one(page, 'a.blog-card', l1[1]), post_item(C.POSTS[1]), '')
    second = [post_item(C.POSTS[2]), guide_item('panchakarma-consultation'), guide_item('shirodhara')]
    for it, item in zip(l2, second):
        blog_card(page, one(page, 'a.blog-card', it), item, '')
    for it in l2[len(second):]:
        it.decompose()
    sec = page.s.select_one('section.all-blog')
    if not sec.get('id'):
        sec['id'] = 'blogs'
    do_first_visit(page)
    do_faq(page)
    do_cta(page)


def page_post(page, post):
    hero = one(page, 'section.blog-detail-hero')
    txt(one(page, '.blog-category .tiny-text', hero), post['category'])
    txt(one(page, '.blog-info-wrap .body-text-light', hero), post['date'])
    txt(one(page, 'h1', hero), post['title'])
    put_img(page, one(page, 'img.hero-img', hero), 'post-hero-' + post['slug'][:20], post['img'], 2.51, post['focus'],
            alt=post['title'], sizes='100vw')
    bd = one(page, 'section.blog-detail')
    wrap = one(page, '.blog-detail-wrapper', bd)
    rts = wrap.find_all('div', class_='detail-text', recursive=False)
    txt(one(page, 'p', rts[0]), post['intro'])
    txt(one(page, 'h2', rts[1]), post['h2'])
    ps = rts[1].find_all('p')
    txt(ps[0], post['h2p'][0])
    txt(ps[2], post['h2p'][1])
    put_img(page, one(page, 'img.blog-feature', bd), 'post-feat-' + post['slug'][:20], post['feat'], 1.56, post['ffocus'],
            alt='', sizes='(max-width: 767px) 92vw, 840px')
    txt(one(page, '.detail-title-wrap .text-h2', bd), post['mid_title'])
    other = one(page, '.blog-detail-other', bd)
    for blk, (h, ptxt, lst) in zip(other.select('.detail-text'), post['blocks']):
        txt(one(page, 'h3', blk), h)
        if ptxt:
            txt(one(page, 'p', blk), ptxt)
        if lst:
            for li, v in zip(blk.find_all('li'), lst):
                txt(li, v)
    txt(one(page, 'h3', rts[-1]), post['end_h'])
    txt(one(page, 'p', rts[-1]), post['end_p'])
    more = one(page, 'section.more')
    txt(one(page, 'h2', more), 'Related reading')
    rel = [post_item(p) for p in C.POSTS if p is not post] + [guide_item('panchakarma-consultation')]
    for card, it in zip(more.select('a.blog-card'), rel):
        blog_card(page, card, it, '')
    do_cta(page)


def page_404(page):
    w = one(page, '.utility-page-content')
    txt(one(page, 'h1', w), 'We could not find that page.')
    w.find('img')['alt'] = 'Page not found'
    set_button(one(page, 'a.button', w), 'Back to Home', '', page)


# ----------------------------------------------------------------------------------------------- url rewriting
def local_for(url):
    u = html.unescape(url).strip()
    key = urllib.parse.unquote(u).split('?')[0]
    return NORM_MAP.get(key)


def rewrite_urls(page):
    s = page.s
    leftovers = []
    for el in s.find_all(True):
        for attr in ('src', 'href', 'srcset', 'content', 'data-poster-url', 'poster', 'style', 'data-src'):
            v = el.get(attr)
            if not v or not isinstance(v, str):
                continue
            if attr == 'srcset':
                parts = []
                for part in re.split(r',\s+(?=\S)', v):
                    bits = part.strip().rsplit(' ', 1)
                    u = bits[0]
                    if u.startswith('http'):
                        loc = local_for(u)
                        if loc:
                            u = page.asset(loc)
                        else:
                            leftovers.append(u)
                    parts.append(u + (' ' + bits[1] if len(bits) > 1 else ''))
                el[attr] = ', '.join(parts)
            elif attr == 'style':
                def rep(m):
                    u = m.group(2)
                    loc = local_for(u)
                    if loc:
                        return f"url('{page.asset(loc)}')"
                    if u.startswith('http'):
                        leftovers.append(u)
                    return m.group(0)
                el[attr] = re.sub(r'url\((["\']?)([^"\')]+)\1\)', rep, v)
            elif v.startswith('http'):
                host = urllib.parse.urlparse(v).netloc
                if host in ('cdn.prod.website-files.com', 'd3e54v103j8qbb.cloudfront.net', 'cdn.jsdelivr.net'):
                    loc = local_for(v)
                    if loc:
                        el[attr] = page.asset(loc)
                    else:
                        leftovers.append(v)
                elif 'medara-template.webflow.io' in host or host == 'webflow.com':
                    leftovers.append(v)
            elif attr == 'href' and v.startswith('/'):
                # root-relative internal link
                path, _, frag = v.partition('#')
                path = path.strip('/')
                target = (path + '/') if path else ''
                el[attr] = page.link(target) + (('#' + frag) if frag else '')
    return leftovers


def build_css():
    src = open(os.path.join(ASSETS_IN, 'css', 'medara-template.webflow.shared.67a261262.css')).read()
    bgs = {
        '6a525821a95852447e975477_Fram.webp': bank.make('bg-support', 'stock-turmeric', 2.2, (0.25, 0.4), max_w=1600),
        '6a4e9e4f216d469f1d007928_Frame%202147239949.webp': bank.make('bg-choose', 'doctor-portrait-white-coat', 0.85,
                                                                     (0.5, 0.4), max_w=1080),
        '6a511541e3d83c8bdf890563_cta%20img.webp': bank.make('bg-cta', 'doctor-with-patient-wide', 2.3, (0.5, 0.5), max_w=2000),
        '6a52764b3e32430f224b23df_Frame%202147240141.webp': bank.make('bg-history-1', 'doctor-dispensary-herbs', 2.0,
                                                                      (0.7, 0.4), max_w=1080),
        '6a52764bd00e55970e8155fb_Frame%202147240141%20(1).webp': bank.make('bg-history-2', 'doctor-preparing-herbs', 2.0,
                                                                            (0.6, 0.45), max_w=1080),
        '6a50fd144d431bb91be553b8_Frame%202147239688.webp': bank.make('bg-blog-hero', 'doctor-green-kurta-herbs', 1.01,
                                                                      (0.34, 0.42), max_w=1080),
    }

    def rep(m):
        u = m.group(1) or m.group(2) or m.group(3)
        for k, info in bgs.items():
            if u.endswith(k):
                return f'url("../{info["src"]}")'
        loc = local_for(u)
        if loc:
            return f'url("../{loc}")'
        if u.startswith('data:'):
            return m.group(0)
        raise RuntimeError('unmapped css url ' + u)
    out = re.sub(r'url\(\s*(?:"([^"]+)"|\'([^\']+)\'|([^)\s]+))\s*\)', rep, src)
    os.makedirs(os.path.join(ASSETS, 'css'), exist_ok=True)
    open(os.path.join(ASSETS, 'css', CSS_NAME), 'w').write(out)
    for fn in os.listdir(os.path.join(ASSETS, 'css')):
        if fn != CSS_NAME:
            os.remove(os.path.join(ASSETS, 'css', fn))


def copy_assets():
    for d in ('js', 'fonts'):
        shutil.copytree(os.path.join(ASSETS_IN, d), os.path.join(ASSETS, d), dirs_exist_ok=True)
    # only the template images we still reference (icons, arrows, 404 art) get copied; see prune step
    os.makedirs(os.path.join(ASSETS, 'img'), exist_ok=True)
    for fn in os.listdir(os.path.join(ASSETS_IN, 'img')):
        if fn.endswith('.svg') or fn.endswith('.png'):
            shutil.copy2(os.path.join(ASSETS_IN, 'img', fn), os.path.join(ASSETS, 'img', fn))
    shutil.copy2(os.path.join(HERE, 'booking.js'), os.path.join(ASSETS, 'js', 'booking.js'))
    # lenis self-hosted (unchanged library)
    logos.write_all(os.path.join(ASSETS, 'img'))


# ----------------------------------------------------------------------------------------------- driver
def build_page(raw_name, out_rel, depth, fn, seo, *args):
    s = soup_of(raw_name)
    if not s.select_one('section.footer'):
        # the template's CMS service page ships without CTA/footer; borrow them from blog-post, which runs the
        # same IX3 chunk (webflow.2cf540ae), so the footer interactions are already defined for it
        donor = soup_of('blog-post')
        last = s.select('.page-wrapper > section')[-1]
        for part in ('section.cta', 'section.footer'):
            node = copy.copy(donor.select_one(part))
            last.insert_after(node)
            last = node
    page = Page(s, depth)
    page.name = 'index' if raw_name == 'index' else raw_name
    do_scripts(page)
    do_nav(page)
    do_footer(page)
    fn(page, *args)
    build_head(page, **{k: v for k, v in seo.items() if k != 'base'})
    left = rewrite_urls(page)
    out_html = str(s)
    out_html = out_html.replace('<!-- This site was created in Webflow. https://webflow.com -->', '')
    out_html = re.sub(r'<!-- Last Published:.*?-->', '', out_html)
    out_html = out_html.replace('<!-- Smooth Scrolling -->', '')
    out_html = out_html.replace('css/medara-template.webflow.shared.67a261262.css', 'css/' + CSS_NAME)
    if seo.get('base'):
        out_html = out_html.replace('<head>', f'<head><base href="{seo["base"]}"/>', 1)
    path = os.path.join(OUT, out_rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(out_html)
    return out_rel, left


def seo(title, desc, path, og='img/og-home.jpg', **kw):
    d = dict(title=title, desc=desc, path=path, og_img=og)
    d.update(kw)
    return d


def make_favicons():
    from playwright.sync_api import sync_playwright
    svg = open(os.path.join(ASSETS, 'img', 'favicon.svg')).read()
    targets = [('favicon-32.png', 32, False), ('favicon-192.png', 192, False), ('favicon-512.png', 512, False),
               ('apple-touch-icon.png', 180, True)]
    with sync_playwright() as p:
        b = p.chromium.launch(channel='chrome')
        for fn, size, bg in targets:
            pg = b.new_page(viewport={'width': size, 'height': size})
            inner = int(size * (0.72 if bg else 0.92))
            body_bg = '#F3F1EB' if bg else 'transparent'
            s2 = svg.replace('width="36" height="38"', f'width="{inner}" height="{inner}"')
            pg.set_content(f'<html><body style="margin:0;background:{body_bg};width:{size}px;height:{size}px;'
                           f'display:flex;align-items:center;justify-content:center">{s2}</body></html>')
            pg.screenshot(path=os.path.join(ASSETS, 'img', fn), omit_background=not bg)
            pg.close()
        b.close()


def main():
    copy_assets()
    make_favicons()
    build_css()
    og_home = bank.jpg('og-home', 'doctor-clinic-nehru-jacket', (1200, 630), (0.62, 0.4))
    results = []
    B = lambda *a: results.append(build_page(*a))  # noqa: E731
    seo_kw = {}
    B('index', 'index.html', 0, page_home, seo(
        'Panchakarma in Patna | Sabka Ved Wellness | Dr. Aditya Kunal',
        'Doctor-led Panchakarma and Ayurvedic therapies near Bajrang Puri, Patna. Consultation and nadi pariksha '
        'with Dr. Aditya Kunal, BAMS. By appointment.', '', extra_ld=[faq_ld()]))
    B('about', 'about/index.html', 1, page_about, seo(
        'About Sabka Ved Wellness | Ayurveda and Panchakarma in Patna',
        'Sabka Ved Wellness is a Panchakarma and Ayurvedic therapy centre near Bajrang Puri, Patna, run by Dr. Aditya '
        'Kunal, BAMS. Classical, careful and doctor-led.', 'about/'))
    B('services', 'services/index.html', 1, page_services, seo(
        'Panchakarma Therapies in Patna | Vamana, Virechana, Basti | Sabka Ved Wellness',
        'Panchakarma consultation, the classical five (Vamana, Virechana, Basti, Nasya, Raktamokshana) and supportive '
        'therapies like Abhyanga and Shirodhara in Patna, planned after assessment.', 'services/'))
    for t in C.THERAPIES:
        og = bank.jpg('og-' + t['slug'], t['img'], (1200, 630), FOCUS.get(t['img']))
        B('service-detail', f"services/{t['slug']}/index.html", 2, page_service_detail, seo(
            f"{t['name']} in Patna | Panchakarma | Sabka Ved Wellness", t['summary'], f"services/{t['slug']}/",
            og=og), t)
    B('appointment', 'appointment/index.html', 1, page_appointment, seo(
        'Book a Panchakarma Consultation in Patna | Sabka Ved Wellness',
        'Request a Panchakarma or Ayurvedic consultation with Dr. Aditya Kunal, BAMS, near Bajrang Puri, Patna. '
        'Visits by appointment.', 'appointment/', booking=True))
    B('contact', 'contact/index.html', 1, page_contact, seo(
        'Contact Sabka Ved Wellness | Panchakarma Centre near Bajrang Puri, Patna',
        'Visit Sabka Ved Wellness near Bajrang Puri, Patna, Bihar. All consultations and therapies are by '
        'appointment.', 'contact/', booking=True))
    B('specialists', 'specialists/index.html', 1, page_specialists, seo(
        'Dr. Aditya Kunal, BAMS | Ayurvedic Physician in Patna | Sabka Ved Wellness',
        'Meet Dr. Aditya Kunal, BAMS, the Ayurvedic physician behind every consultation and Panchakarma plan at '
        'Sabka Ved Wellness, Patna.', 'specialists/',
        extra_ld=[{'@context': 'https://schema.org', '@type': 'Physician', 'name': C.DOCTOR,
                   'medicalSpecialty': 'Ayurvedic', 'url': C.DOCTOR_SITE,
                   'address': {'@type': 'PostalAddress', 'addressLocality': 'Patna', 'addressRegion': 'Bihar',
                               'addressCountry': 'IN'}, 'worksFor': {'@id': C.SITE_URL + '#clinic'}}]))
    B('blog', 'blog/index.html', 1, page_blog, seo(
        'Panchakarma Journal | Plain Answers | Sabka Ved Wellness, Patna',
        'Plain-language articles on Panchakarma and Ayurvedic therapy from Sabka Ved Wellness, Patna: what it is, '
        'how to prepare and how it differs from a spa massage.', 'blog/'))
    for p in C.POSTS:
        og = bank.jpg('og-' + p['slug'][:24], p['img'], (1200, 630), p['focus'])
        ld = {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': p['title'],
              'datePublished': p['iso'], 'description': p['desc'],
              'image': C.SITE_URL + 'assets/' + og, 'mainEntityOfPage': C.SITE_URL + f"blog/{p['slug']}/",
              'author': {'@type': 'Organization', 'name': C.BRAND},
              'publisher': {'@type': 'Organization', 'name': C.BRAND}}
        B('blog-post', f"blog/{p['slug']}/index.html", 2, page_post, seo(
            f"{p['title']} | Sabka Ved Wellness", p['desc'], f"blog/{p['slug']}/", og=og, extra_ld=[ld]), p)
    B('404', '404.html', 0, page_404, seo('Page Not Found | Sabka Ved Wellness',
                                           'This page does not exist. Return to Sabka Ved Wellness, Panchakarma in Patna.',
                                           '404.html', noindex=True, base='/sabka-ved-wellness/'))
    bad = False
    for rel, left in results:
        if left:
            bad = True
            print('LEFTOVER URLS in', rel, sorted(set(left))[:10])
    # sitemap + robots
    urls = ['', 'about/', 'services/'] + [f"services/{t['slug']}/" for t in C.THERAPIES] + \
           ['appointment/', 'contact/', 'specialists/', 'blog/'] + [f"blog/{p['slug']}/" for p in C.POSTS]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f'  <url><loc>{C.SITE_URL}{u}</loc><lastmod>2026-11-15</lastmod></url>')
    sm.append('</urlset>')
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write('\n'.join(sm) + '\n')
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {C.SITE_URL}sitemap.xml\n')
    open(os.path.join(OUT, '.nojekyll'), 'w').write('')
    # prune images nothing references (template leftovers like the old logos)
    refs = set()
    for dp, dn, fns in os.walk(OUT):
        if '_template-mirror' in dp or '/.git' in dp:
            continue
        for fn in fns:
            if fn.endswith(('.html', '.css', '.xml')):
                refs.update(re.findall(r'img/([A-Za-z0-9._-]+)', open(os.path.join(dp, fn)).read()))
    keep = {'favicon-512.png'}
    removed = 0
    for fn in os.listdir(os.path.join(ASSETS, 'img')):
        if fn not in refs and fn not in keep:
            os.remove(os.path.join(ASSETS, 'img', fn))
            removed += 1
    print('pruned', removed, 'unreferenced images')
    print('built', len(results), 'pages; chunks:', {k: v for k, v in PAGE_CHUNKS.items()})
    if bad:
        sys.exit(1)


if __name__ == '__main__':
    main()
