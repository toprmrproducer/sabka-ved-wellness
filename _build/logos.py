"""Generate brand SVGs (wordmarks outlined from the template's own Inter Display font, plus a leaf mark)."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, '..', '_template-mirror', 'assets', 'fonts')
F_MED = os.path.join(FONTS, '6a4d4496920ce6bae1f1d2c9_InterDisplay-Medium.ttf')
F_SEMI = os.path.join(FONTS, '6a4d4496c691221b3c8581a6_InterDisplay-SemiBold.ttf')
F_TIMES = os.path.join(FONTS, '6a4e8a3f43a05021432f0d5a_times.ttf')

_cache = {}


def _font(path):
    if path not in _cache:
        _cache[path] = TTFont(path)
    return _cache[path]


def text_path(text, font_path, size, tracking=0.0):
    """Return (d, width, ascent_box) for text at font size `size`, baseline at y=size*0.8 approx."""
    f = _font(font_path)
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    upm = f['head'].unitsPerEm
    scale = size / upm
    hmtx = f['hmtx']
    x = 0.0
    pen = SVGPathPen(gs)
    bp = BoundsPen(gs)
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            continue
        adv = hmtx[gname][0]
        # flip y: font units y-up -> svg y-down
        t = (scale, 0, 0, -scale, x, 0)
        gs[gname].draw(TransformPen(pen, t))
        gs[gname].draw(TransformPen(bp, t))
        x += adv * scale + tracking * size
    xmin, ymin, xmax, ymax = bp.bounds
    return pen.getCommands(), (xmin, ymin, xmax, ymax), x


def wordmark_svg(text, font_path, height, fill, tracking=0.0, pad=0, opacity=None):
    # render at nominal size then compute bbox and fit to height
    d, (xmin, ymin, xmax, ymax), adv = text_path(text, font_path, 100, tracking)
    h = ymax - ymin
    s = height / h
    w = (xmax - xmin) * s
    op = f' fill-opacity="{opacity}"' if opacity is not None else ''
    W = round(w + 2 * pad, 2)
    H = round(height + 2 * pad, 2)
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{text}">'
            f'<path transform="translate({pad - xmin * s:.3f} {pad - ymin * s:.3f}) scale({s:.5f})" d="{d}" fill="{fill}"{op}/></svg>')


# Leaf mark, drawn on a 36x38 grid (same box as the template's brand mark)
LEAF_CENTER = 'M18 0.8C25.6 8.2 27.4 19.6 18 37.2C8.6 19.6 10.4 8.2 18 0.8Z'
LEAF_LEFT = 'M16.6 37.2C8.2 34.6 2.2 27.4 0.6 14.6C7.6 16.4 13.4 22.4 16.6 37.2Z'
LEAF_RIGHT = 'M19.4 37.2C27.8 34.6 33.8 27.4 35.4 14.6C28.4 16.4 22.6 22.4 19.4 37.2Z'
VEIN = 'M17.35 9.5H18.65V33.5H17.35Z'


def mark_svg(fill, vein_fill=None, w=36, h=38):
    vein = f'<path d="{VEIN}" fill="{vein_fill}"/>' if vein_fill else ''
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 36 38" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Sabka Ved Wellness">'
            f'<path d="{LEAF_LEFT}" fill="{fill}" fill-opacity="0.85"/><path d="{LEAF_RIGHT}" fill="{fill}" fill-opacity="0.85"/>'
            f'<path d="{LEAF_CENTER}" fill="{fill}"/>{vein}</svg>')


def footer_mark_svg():
    # big version: cream leaves with lime centre, like the template's cream/lime starburst
    return (f'<svg width="168" height="177" viewBox="0 0 36 38" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Sabka Ved Wellness">'
            f'<path d="{LEAF_LEFT}" fill="#F3F1EB"/><path d="{LEAF_RIGHT}" fill="#F3F1EB"/>'
            f'<path d="{LEAF_CENTER}" fill="#C1F85F"/><path d="{VEIN}" fill="#F3F1EB"/></svg>')


def write_all(outdir):
    os.makedirs(outdir, exist_ok=True)
    files = {
        'brand-logo.svg': mark_svg('#FFFFFF'),
        'brand-logo-dark.svg': mark_svg('#121212'),
        'brand-logo-text.svg': wordmark_svg('Sabka Ved Wellness', F_MED, 19, '#FFFFFF'),
        'brand-logo-text-dark.svg': wordmark_svg('Sabka Ved Wellness', F_MED, 19, '#121212'),
        'footer-logo.svg': footer_mark_svg(),
        'footer-shape.svg': wordmark_svg('SABKA VED', F_SEMI, 176, '#F3F1EB', tracking=0.02),
        'favicon.svg': mark_svg('#3E5A1E'),
    }
    therapies = ['Vamana', 'Virechana', 'Basti', 'Nasya', 'Raktamokshana', 'Abhyanga', 'Shirodhara']
    for t in therapies:
        files[f'loop-{t.lower()}.svg'] = wordmark_svg(t, F_TIMES, 26, '#000000', opacity=0.45)
    for name, svg in files.items():
        with open(os.path.join(outdir, name), 'w') as fh:
            fh.write(svg)
    return list(files)


if __name__ == '__main__':
    import sys
    print(write_all(sys.argv[1]))
