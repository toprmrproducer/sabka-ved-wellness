"""Crop the Sabka Ved photo set into template image slots and emit responsive webp sizes."""
import os
from PIL import Image

SRC = '/Users/shreyasraj/Downloads/Sabka-Ved-Assets'
# AI-generated doctor stills carry a small sparkle mark in the bottom-right corner; keep crops clear of it.
SAFE_TRIM = {'doctor-clinic-nehru-jacket', 'doctor-consult-desk-wide', 'doctor-dispensary-herbs',
             'doctor-green-kurta-herbs', 'doctor-herb-garden-walk', 'doctor-manuscript-desk',
             'doctor-portrait-white-coat', 'doctor-preparing-herbs', 'doctor-with-patient-wide'}
# Hand-picked safe boxes (x0, y0, x1, y1) as fractions, for images that contain things we must not show.
FORCE_BOX = {
    # keep the third-party branded oil bottle out of frame
    'stock-turmeric': (0.0, 0.0, 0.53, 1.0),
}
WIDTHS = [480, 800, 1080, 1600, 2000]


class ImageBank:
    def __init__(self, outdir):
        self.outdir = outdir
        os.makedirs(outdir, exist_ok=True)
        self.made = {}

    def _open(self, name):
        im = Image.open(os.path.join(SRC, name + '.jpg')).convert('RGB')
        W, H = im.size
        x0, y0, x1, y1 = 0, 0, W, H
        if name in SAFE_TRIM:
            x1, y1 = int(W * 0.94), int(H * 0.92)
        if name in FORCE_BOX:
            fx0, fy0, fx1, fy1 = FORCE_BOX[name]
            x0, y0, x1, y1 = int(W * fx0), int(H * fy0), int(W * fx1), int(H * fy1)
        return im, (x0, y0, x1, y1)

    def crop(self, name, aspect, focus=(0.5, 0.5), zoom=1.0, box=None):
        """Largest crop of `aspect` (w/h) inside the safe box, centred on focus (fractions of full image)."""
        im, (bx0, by0, bx1, by1) = self._open(name)
        W, H = im.size
        if box:
            bx0, by0, bx1, by1 = int(W * box[0]), int(H * box[1]), int(W * box[2]), int(H * box[3])
        bw, bh = bx1 - bx0, by1 - by0
        if bw / bh > aspect:
            ch = bh / zoom
            cw = ch * aspect
        else:
            cw = bw / zoom
            ch = cw / aspect
        cx, cy = focus[0] * W, focus[1] * H
        x0 = min(max(cx - cw / 2, bx0), bx1 - cw)
        y0 = min(max(cy - ch / 2, by0), by1 - ch)
        return im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))

    def make(self, key, name, aspect, focus=(0.5, 0.5), zoom=1.0, box=None, max_w=2000, quality=80, darken=0.0):
        """Returns dict(src=relative-to-assets path, srcset=..., w=, h=)."""
        if key in self.made:
            return self.made[key]
        c = self.crop(name, aspect, focus, zoom, box)
        if darken:
            c = Image.blend(c, Image.new('RGB', c.size, (8, 10, 6)), darken)
        cw = c.width
        widths = [w for w in WIDTHS if w < cw and w <= max_w]
        top = min(cw, max_w)
        if top not in widths:
            widths.append(top)
        entries = []
        for w in widths:
            h = round(w / aspect)
            fn = f'{key}-{w}.webp'
            path = os.path.join(self.outdir, fn)
            if not os.path.exists(path):
                c.resize((w, h), Image.LANCZOS).save(path, 'WEBP', quality=quality, method=6)
            entries.append((w, fn, h))
        default = next((e for e in entries if e[0] >= 1080), entries[-1])
        info = {
            'src': 'img/' + default[1],
            'srcset': ', '.join(f'img/{fn} {w}w' for w, fn, h in entries),
            'w': default[0], 'h': default[2],
            'single': len(entries) == 1,
        }
        self.made[key] = info
        return info

    def jpg(self, key, name, size, focus=(0.5, 0.5), box=None):
        """Fixed-size JPG (for OG images)."""
        w, h = size
        c = self.crop(name, w / h, focus, 1.0, box).resize((w, h), Image.LANCZOS)
        fn = f'{key}.jpg'
        c.save(os.path.join(self.outdir, fn), 'JPEG', quality=84, optimize=True, progressive=True)
        return 'img/' + fn
