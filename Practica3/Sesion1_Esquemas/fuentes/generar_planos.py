# -*- coding: utf-8 -*-
"""
Proyecto ICT - Universidad de Huelva - Sesión 1
Generador de la base arquitectónica del conjunto residencial:
  ICT_01  Esquema 3D (axonometría) + modelo OBJ/MTL + DXF 3D
  ICT_02  Plano general 2D del complejo
  ICT_03  Vivienda tipo - Planta baja
  ICT_04  Vivienda tipo - Planta primera
  ICT_05  Local comercial LC1 y zonas comunes ZC1 / ZC2

Todas las medidas están en metros y son HIPÓTESIS DE DISEÑO (no existen datos
oficiales). Una sola fuente de geometría alimenta todos los planos, de modo que
el 3D y los 2D representan exactamente el mismo proyecto.

No se dibuja ningún elemento de telecomunicaciones: las capas ICT-* se crean
vacías (o desactivadas) para la siguiente sesión.

Uso:  python generar_planos.py <carpeta_salida>
"""
import math
import os
import sys
from collections import OrderedDict
from xml.sax.saxutils import escape

import ezdxf
from ezdxf.enums import TextEntityAlignment
from shapely import affinity
from shapely.geometry import LineString, Point, box
from shapely.ops import unary_union

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
FECHA = "13/11/2026"
FONT = "Arial, Helvetica, sans-serif"

# ---------------------------------------------------------------- colores
C_WALL, C_WALL_LN = "#b0b0b0", "#3c3c3c"
C_BASE = "#f3f7ef"      # terreno ajardinado del complejo
C_ROAD = "#c9c9c9"      # vial rodado
C_SIDE = "#ececec"      # aceras y caminos peatonales
C_PAVED = "#e6e2da"     # explanadas pavimentadas
C_GREEN = "#d3e7c5"     # zona verde común
C_HOUSE = "#d9d9d9"     # vivienda (planta general)
C_LC = "#f6e0c2"        # local comercial
C_ZC = "#d9e5f3"        # edificio de zona común
C_FENCE = "#5f6b55"     # límite de parcela
C_LIMIT = "#a01818"     # límite del complejo

# ============================================================ GEOMETRÍA BASE
# Conjunto: 138 x 50 m. Origen en la esquina suroeste. Eje Y = norte.
SITE_W, SITE_H = 138.0, 50.0
ROAD = (0.0, 21.5, 136.0, 28.5)          # vial interior (7,00 m)
SIDE_S = (0.0, 20.0, 136.0, 21.5)        # acera sur (1,50 m)
SIDE_N = (0.0, 28.5, 136.0, 30.0)        # acera norte (1,50 m)
PUB_ROAD = (-12.0, -3.0, -2.0, 53.0)     # vial público (fuera del conjunto)
PUB_SIDE = (-2.0, -3.0, 0.0, 53.0)       # acera pública

PARCEL_W, PARCEL_D = 14.0, 18.0
HOUSE_W, HOUSE_D = 11.0, 8.0             # vivienda tipo 11,00 x 8,00 m
H_FLOOR = 3.0                            # altura entre plantas
H_EAVE, H_RIDGE = 6.0, 7.6               # alero y cumbrera

PAIR_X = [26.0, 58.0, 90.0]              # inicio de cada pareja (2 parcelas)
HOUSES = OrderedDict()
for _i, _px in enumerate([26.0, 40.0, 58.0, 72.0, 90.0, 104.0]):
    HOUSES["V%02d" % (_i + 1)] = ("N", _px)
for _i, _px in enumerate([26.0, 40.0, 58.0, 72.0, 90.0, 104.0]):
    HOUSES["V%02d" % (_i + 7)] = ("S", _px)
HOUSES["V13"] = ("S", 122.0)

GROUPS = [("Pareja 1", "V01", "V02"), ("Pareja 2", "V03", "V04"),
          ("Pareja 3", "V05", "V06"), ("Pareja 4", "V07", "V08"),
          ("Pareja 5", "V09", "V10"), ("Pareja 6", "V11", "V12"),
          ("Grupo 7", "V13", None)]

# Local comercial y zonas comunes
LC1 = (3.0, 5.0, 19.0, 15.0)             # 16,00 x 10,00 m, una planta
LC1_COURT = (0.0, 15.0, 22.0, 20.0)      # explanada de acceso
ZC1_BLOCK = (2.0, 30.0, 22.0, 48.0)
ZC1 = (4.0, 35.0, 16.0, 43.0)            # 12,00 x 8,00 m, una planta
ZC2 = (122.0, 30.0, 136.0, 48.0)         # 14,00 x 18,00 m, espacio libre
H_LC1, H_ZC1 = 4.5, 3.8


def parcel(row, px):
    return (px, 30.0, px + PARCEL_W, 48.0) if row == "N" else (px, 2.0, px + PARCEL_W, 20.0)


def to_world(row, px, lx, ly, lz=0.0):
    """Coordenadas locales de la vivienda tipo (fachada principal en y=0) a
    coordenadas del conjunto. Fila norte: fachada al sur. Fila sur: girada 180°."""
    if row == "N":
        return (px + 1.5 + lx, 34.0 + ly, lz)
    return (px + 1.5 + HOUSE_W - lx, 16.0 - ly, lz)


def footprint(row, px):
    a = to_world(row, px, 0, 0)
    b = to_world(row, px, HOUSE_W, HOUSE_D)
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1]))


# ---------------------------------------------------- vivienda tipo (local)
E, I = 0.25, 0.10   # espesor muro exterior / tabique interior

# puerta: (orientación muro, cara1, cara2, desde, hasta, sentido de giro, bisagra)
#   'v' muro vertical (x cte), 'h' muro horizontal (y cte); sentido +1/-1 hacia +x/+y
# ventana: (orientación, cara1, cara2, desde, hasta)
FLOORS = {
    "PB": {
        "doors": [("h", 0.0, E, 5.4, 6.4, +1, "lo"),          # acceso principal
                  ("v", 5.0, 5.1, 1.6, 2.4, -1, "lo"),        # dormitorio 4
                  ("v", 5.0, 5.1, 4.0, 4.8, -1, "lo"),        # salón-comedor
                  ("v", 7.2, 7.3, 1.0, 1.75, +1, "lo"),       # baño 2
                  ("v", 7.2, 7.3, 6.8, 7.6, +1, "hi")],       # cocina
        "windows": [("h", 0.0, E, 1.4, 3.6), ("v", 0.0, E, 1.0, 2.2),
                    ("h", 0.0, E, 8.6, 9.6),
                    ("h", 8 - E, 8.0, 1.0, 4.0), ("v", 0.0, E, 4.6, 6.4),
                    ("h", 8 - E, 8.0, 8.2, 10.0), ("v", 11 - E, 11.0, 5.6, 6.8)],
        "rooms": [("Dormitorio 4 / despacho", (0.25, 0.25, 5.0, 3.0), (2.6, 1.55)),
                  ("Salón-comedor", (0.25, 3.1, 5.0, 7.75), (2.6, 5.45)),
                  ("Vestíbulo-distribuidor", None, (6.15, 2.05)),
                  ("Baño 2", (7.3, 0.25, 10.75, 2.4), (8.95, 0.85)),
                  ("Cocina", (7.3, 2.5, 10.75, 7.75), (8.7, 4.9))],
    },
    "P1": {
        "doors": [("v", 5.0, 5.1, 1.6, 2.4, -1, "lo"),        # dormitorio 2
                  ("v", 5.0, 5.1, 4.0, 4.8, -1, "lo"),        # dormitorio 1
                  ("v", 7.2, 7.3, 1.0, 1.75, +1, "lo"),       # baño 1
                  ("v", 7.2, 7.3, 6.8, 7.6, +1, "hi")],       # dormitorio 3
        "windows": [("h", 0.0, E, 1.4, 3.6), ("v", 0.0, E, 1.0, 2.2),
                    ("h", 0.0, E, 5.6, 6.8), ("h", 0.0, E, 8.6, 9.6),
                    ("h", 8 - E, 8.0, 1.0, 4.0), ("v", 0.0, E, 4.6, 6.4),
                    ("h", 8 - E, 8.0, 8.2, 10.0), ("v", 11 - E, 11.0, 4.4, 6.0)],
        "rooms": [("Dormitorio 2", (0.25, 0.25, 5.0, 3.0), (2.6, 1.55)),
                  ("Dormitorio 1 (principal)", (0.25, 3.1, 5.0, 7.75), (2.6, 5.45)),
                  ("Distribuidor", None, (6.15, 1.75)),
                  ("Baño 1", (7.3, 0.25, 10.75, 2.4), (8.95, 0.85)),
                  ("Dormitorio 3", (7.3, 2.5, 10.75, 7.75), (9.0, 4.9))],
    },
}
STAIR = (6.2, 3.0, 7.2, 6.64, 14)        # x0, y0, x1, y1, nº de huellas (sube hacia -y)
CENTRAL_AREA = (7.2 - 5.1) * (7.75 - 0.25) - (STAIR[2] - STAIR[0]) * (STAIR[3] - STAIR[1])

# Local comercial / zona común 1 (coordenadas del conjunto, muros de 0,30 m)
LC1_DOORS = [("h", 14.7, 15.0, 10.1, 11.0, +1, "lo"), ("h", 14.7, 15.0, 11.0, 11.9, +1, "hi")]
LC1_WINDOWS = [("h", 14.7, 15.0, 4.0, 9.4), ("h", 14.7, 15.0, 12.6, 18.0),
               ("v", 3.0, 3.3, 7.0, 13.0)]
ZC1_DOORS = [("h", 35.0, 35.3, 9.1, 10.0, -1, "lo"), ("h", 35.0, 35.3, 10.0, 10.9, -1, "hi")]
ZC1_WINDOWS = [("h", 35.0, 35.3, 5.0, 8.0), ("h", 35.0, 35.3, 12.0, 15.0),
               ("h", 42.7, 43.0, 6.0, 14.0), ("v", 4.0, 4.3, 37.0, 41.0),
               ("v", 15.7, 16.0, 37.0, 41.0)]


def opening_box(o):
    kind, w0, w1, a, b = o[:5]
    return box(w0, a, w1, b) if kind == "v" else box(a, w0, b, w1)


def house_walls(floor):
    walls = [box(0, 0, 11, E), box(0, 8 - E, 11, 8), box(0, 0, E, 8), box(11 - E, 0, 11, 8),
             box(5.0, E, 5.1, 8 - E), box(7.2, E, 7.3, 8 - E),
             box(E, 3.0, 5.0, 3.1), box(7.3, 2.4, 11 - E, 2.5)]
    f = FLOORS[floor]
    cuts = unary_union([opening_box(o) for o in f["doors"] + f["windows"]])
    return unary_union(walls).difference(cuts)


def shell_walls(rect, t, doors, windows):
    x0, y0, x1, y1 = rect
    ring = box(x0, y0, x1, y1).difference(box(x0 + t, y0 + t, x1 - t, y1 - t))
    return ring.difference(unary_union([opening_box(o) for o in doors + windows]))


def fmt(v, d=2):
    return ("%.*f" % (d, v)).replace(".", ",")


# ============================================================ SALIDA SVG/DXF
def style(fill="none", stroke="#000", sw=0.25, dash=None):
    s = ' fill="%s"' % fill
    if stroke:
        s += ' stroke="%s" stroke-width="%.3f" stroke-linejoin="miter" stroke-miterlimit="4"' % (stroke, sw)
        if dash:
            s += ' stroke-dasharray="%s"' % dash
    else:
        s += ' stroke="none"'
    return s


class Sheet:
    """Lámina A3 apaisada (420 x 297 mm). Capas en orden de dibujo."""

    def __init__(self, code, title, layers):
        self.code, self.title = code, title
        self.layers = OrderedDict((n, [lab, vis]) for n, lab, vis in layers)
        self.svg = {n: [] for n in self.layers}
        self.dxf = []

    # primitivas en milímetros de papel (no se exportan a DXF)
    def prect(self, layer, x, y, w, h, fill="none", stroke="#000", sw=0.25, dash=None):
        self.svg[layer].append('<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f"%s/>'
                               % (x, y, w, h, style(fill, stroke, sw, dash)))

    def ppath(self, layer, pts, close=False, fill="none", stroke="#000", sw=0.25, dash=None):
        d = "M " + " L ".join("%.3f,%.3f" % p for p in pts) + (" Z" if close else "")
        self.svg[layer].append('<path d="%s"%s/>' % (d, style(fill, stroke, sw, dash)))

    def ptext(self, layer, x, y, txt, size=3.0, anchor="middle", weight="normal",
              fill="#000", rot=0.0, halo=False, italic=False):
        tr = ' transform="rotate(%.2f %.3f %.3f)"' % (-rot, x, y) if rot else ""
        h = (' stroke="#ffffff" stroke-width="%.2f" stroke-linejoin="round" paint-order="stroke"'
             % (size * 0.35)) if halo else ""
        it = ' font-style="italic"' if italic else ""
        self.svg[layer].append(
            '<text x="%.3f" y="%.3f" font-family="%s" font-size="%.2f" font-weight="%s" '
            'text-anchor="%s" dominant-baseline="central" fill="%s"%s%s%s>%s</text>'
            % (x, y, FONT, size, weight, anchor, fill, it, h, tr, escape(txt)))

    def ptexts(self, layer, x, y, lines, size=2.5, lead=1.45, **kw):
        for i, ln in enumerate(lines):
            if isinstance(ln, tuple):
                self.ptext(layer, x, y + i * size * lead, ln[0], size=size, weight=ln[1], **kw)
            else:
                dx = size * 1.3 if ln.startswith("  ") else 0.0
                self.ptext(layer, x + dx, y + i * size * lead, ln.strip(), size=size, **kw)

    def write_svg(self, path):
        out = ['<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
               '<svg xmlns="http://www.w3.org/2000/svg" '
               'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
               'width="420mm" height="297mm" viewBox="0 0 420 297" version="1.1">',
               '<title>%s</title>' % escape(self.code + " - " + self.title),
               '<rect id="fondo" x="0" y="0" width="420" height="297" fill="#ffffff"/>']
        for n, (lab, vis) in self.layers.items():
            out.append('<g id="%s" inkscape:groupmode="layer" inkscape:label="%s" style="display:%s">'
                       % (n, escape(n + " | " + lab), "inline" if vis else "none"))
            out.extend(self.svg[n])
            out.append("</g>")
        out.append("</svg>")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(out))

    def write_dxf(self, path):
        doc = ezdxf.new("R2010", setup=True)
        doc.units = ezdxf.units.M
        doc.header["$LTSCALE"] = 1.0
        doc.styles.add("ARIAL", font="arial.ttf")
        msp = doc.modelspace()
        for n, (lab, vis) in self.layers.items():
            if n.startswith("P-"):
                continue  # marco, cajetín y leyenda solo existen en papel
            lay = doc.layers.add(n, color=7)
            lay.description = lab
            if not vis:
                lay.off()
        for e in self.dxf:
            kind, layer = e[0], e[1]
            at = {"layer": layer}
            if kind == "poly":
                rings, fill, stroke, sw, dash = e[2:]
                if fill not in (None, "none", "#fff", "#ffffff"):
                    h = msp.add_hatch(dxfattribs=at)
                    h.rgb = hex_rgb(fill)
                    for j, r in enumerate(rings):
                        h.paths.add_polyline_path([p[:2] for p in r[:-1]], is_closed=True,
                                                  flags=1 if j == 0 else 0)
                if stroke:
                    for r in rings:
                        pl = msp.add_lwpolyline([p[:2] for p in r[:-1]], close=True,
                                                dxfattribs=line_attrs(at, stroke, sw, dash))
            elif kind == "line":
                pts, stroke, sw, dash = e[2:]
                msp.add_lwpolyline([p[:2] for p in pts], dxfattribs=line_attrs(at, stroke, sw, dash))
            elif kind == "arc":
                c, r, a0, a1, stroke, sw = e[2:]
                msp.add_arc(c, r, a0, a1, dxfattribs=line_attrs(at, stroke, sw, None))
            elif kind == "text":
                p, txt, hgt, anchor, rot, fill = e[2:]
                al = {"middle": TextEntityAlignment.MIDDLE_CENTER,
                      "start": TextEntityAlignment.MIDDLE_LEFT,
                      "end": TextEntityAlignment.MIDDLE_RIGHT}[anchor]
                t = msp.add_text(txt, height=hgt, rotation=rot,
                                 dxfattribs=dict(at, style="ARIAL"))
                t.rgb = hex_rgb(fill)
                t.set_placement(p[:2], align=al)
            elif kind == "face3d":
                pts, color = e[2:]
                tris = [pts] if len(pts) <= 4 else [[pts[0], pts[i], pts[i + 1]] for i in range(1, len(pts) - 1)]
                for q in tris:
                    f = msp.add_3dface(list(q) + [q[-1]] * (4 - len(q)), dxfattribs=at)
                    f.rgb = hex_rgb(color)
        doc.saveas(path)


LWS = [0, 5, 9, 13, 15, 18, 20, 25, 30, 35, 40, 50, 53, 60, 70, 80, 90, 100]


def line_attrs(at, stroke, sw, dash):
    d = dict(at)
    d["lineweight"] = min(LWS, key=lambda v: abs(v - sw * 100))
    d["true_color"] = ezdxf.colors.rgb2int(hex_rgb(stroke))
    if dash:
        d["linetype"] = "DASHED"
        d["ltscale"] = 0.05
    return d


def hex_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


class View:
    """Ventana de dibujo a escala: coordenadas del mundo (m) -> papel (mm)."""

    def __init__(self, sheet, scale, wx0, wy1, px0, py0, clip=None):
        self.sh, self.k = sheet, 1000.0 / scale
        self.wx0, self.wy1, self.px0, self.py0 = wx0, wy1, px0, py0
        self.clip = box(*clip) if clip else None

    def P(self, x, y):
        return (self.px0 + (x - self.wx0) * self.k, self.py0 + (self.wy1 - y) * self.k)

    def geom(self, layer, g, fill="none", stroke="#000", sw=0.25, dash=None):
        if self.clip is not None:
            g = g.intersection(self.clip)
        if g.is_empty:
            return
        for p in (g.geoms if hasattr(g, "geoms") else [g]):
            if p.geom_type != "Polygon" or p.area < 1e-9:
                continue
            rings = [list(p.exterior.coords)] + [list(r.coords) for r in p.interiors]
            d = " ".join("M " + " L ".join("%.3f,%.3f" % self.P(*q[:2]) for q in r[:-1]) + " Z"
                         for r in rings)
            self.sh.svg[layer].append('<path d="%s" fill-rule="evenodd"%s/>'
                                      % (d, style(fill, stroke, sw, dash)))
            self.sh.dxf.append(("poly", layer, rings, fill, stroke, sw, dash))

    def rect(self, layer, r, **kw):
        self.geom(layer, box(*r), **kw)

    def line(self, layer, pts, stroke="#000", sw=0.25, dash=None):
        g = LineString(pts)
        if self.clip is not None:
            g = g.intersection(self.clip)
        for s in (g.geoms if hasattr(g, "geoms") else [g]):
            if s.is_empty or s.geom_type != "LineString":
                continue
            c = list(s.coords)
            self.sh.svg[layer].append('<path d="M %s"%s/>' % (
                " L ".join("%.3f,%.3f" % self.P(*q[:2]) for q in c), style("none", stroke, sw, dash)))
            self.sh.dxf.append(("line", layer, c, stroke, sw, dash))

    def arc(self, layer, c, r, a0, a1, stroke="#000", sw=0.18):
        """Arco antihorario de a0 a a1 (grados)."""
        if self.clip is not None and not self.clip.contains(Point(c)):
            return
        p0 = self.P(c[0] + r * math.cos(math.radians(a0)), c[1] + r * math.sin(math.radians(a0)))
        p1 = self.P(c[0] + r * math.cos(math.radians(a1)), c[1] + r * math.sin(math.radians(a1)))
        rk = r * self.k
        large = 1 if (a1 - a0) % 360 > 180 else 0
        self.sh.svg[layer].append('<path d="M %.3f,%.3f A %.3f %.3f 0 %d 1 %.3f,%.3f"%s/>'
                                  % (p0 + (rk, rk, large) + p1 + (style("none", stroke, sw),)))
        self.sh.dxf.append(("arc", layer, c, r, a0, a1, stroke, sw))

    def text(self, layer, x, y, txt, size=2.5, anchor="middle", weight="normal", rot=0.0,
             fill="#000", halo=False, italic=False):
        if self.clip is not None and not self.clip.contains(Point(x, y)):
            return
        px, py = self.P(x, y)
        self.sh.ptext(layer, px, py, txt, size, anchor, weight, fill, rot, halo, italic)
        self.sh.dxf.append(("text", layer, (x, y), txt, size / self.k, anchor, rot, fill))

    def texts(self, layer, x, y, lines, size=2.5, lead=1.4, **kw):
        """Bloque de líneas centrado verticalmente en (x, y)."""
        sizes = [ln[2] if isinstance(ln, tuple) and len(ln) > 2 else size for ln in lines]
        offs = [0.0]
        for a, b in zip(sizes, sizes[1:]):
            offs.append(offs[-1] + (a + b) / 2 * lead / self.k)
        for i, ln in enumerate(lines):
            yy = y + offs[-1] / 2 - offs[i]
            if isinstance(ln, tuple):
                self.text(layer, x, yy, ln[0], size=ln[2] if len(ln) > 2 else size, weight=ln[1], **kw)
            else:
                self.text(layer, x, yy, ln, size=size, **kw)

    # ---------------- cotas (trazos oblicuos de arquitectura)
    def hdim(self, layer, x1, x2, y, yref=None, size=2.2, txt=None):
        t, g = 1.1 / self.k, 1.0 / self.k
        if yref is not None:
            sg = 1 if y > yref else -1
            for x in (x1, x2):
                self.line(layer, [(x, yref + sg * g), (x, y + sg * 1.5 / self.k)], sw=0.13)
        self.line(layer, [(x1 - 1.5 / self.k, y), (x2 + 1.5 / self.k, y)], sw=0.15)
        for x in (x1, x2):
            self.line(layer, [(x - t, y - t), (x + t, y + t)], sw=0.35)
        self.text(layer, (x1 + x2) / 2, y + 1.7 / self.k, txt or fmt(abs(x2 - x1)), size=size)

    def vdim(self, layer, y1, y2, x, xref=None, size=2.2, txt=None):
        t, g = 1.1 / self.k, 1.0 / self.k
        if xref is not None:
            sg = 1 if x > xref else -1
            for y in (y1, y2):
                self.line(layer, [(xref + sg * g, y), (x + sg * 1.5 / self.k, y)], sw=0.13)
        self.line(layer, [(x, y1 - 1.5 / self.k), (x, y2 + 1.5 / self.k)], sw=0.15)
        for y in (y1, y2):
            self.line(layer, [(x - t, y - t), (x + t, y + t)], sw=0.35)
        self.text(layer, x - 1.7 / self.k, (y1 + y2) / 2, txt or fmt(abs(y2 - y1)), size=size, rot=90)


# ---------------------------------------------------------- carpintería
def draw_door(v, d, layer="A-PUERTAS", sw=0.2):
    kind, w0, w1, a, b, s, hinge = d
    w = b - a
    th = 0.045 * (1 if hinge == "lo" else -1)
    if kind == "v":
        f = w1 if s > 0 else w0
        hy = a if hinge == "lo" else b
        c = (f, hy)
        leaf = box(min(f, f + s * w), min(hy, hy + th), max(f, f + s * w), max(hy, hy + th))
        a_leaf = 0 if s > 0 else 180
        a_closed = 90 if hinge == "lo" else 270
        for x in (w0, w1):
            v.line(layer, [(x, a), (x, b)], stroke="#808080", sw=0.1)
    else:
        f = w1 if s > 0 else w0
        hx = a if hinge == "lo" else b
        c = (hx, f)
        leaf = box(min(hx, hx + th), min(f, f + s * w), max(hx, hx + th), max(f, f + s * w))
        a_leaf = 90 if s > 0 else 270
        a_closed = 0 if hinge == "lo" else 180
        for y in (w0, w1):
            v.line(layer, [(a, y), (b, y)], stroke="#808080", sw=0.1)
    v.geom(layer, leaf, fill="#ffffff", stroke="#000", sw=sw)
    if (a_closed - a_leaf) % 360 == 90:
        v.arc(layer, c, w, a_leaf, a_closed, sw=0.15)
    else:
        v.arc(layer, c, w, a_closed, a_leaf, sw=0.15)


def draw_window(v, o, layer="A-VENTANAS"):
    kind, w0, w1, a, b = o
    v.geom(layer, opening_box(o), fill="#ffffff", stroke="#000", sw=0.18)
    for f in (0.42, 0.58):
        c = w0 + (w1 - w0) * f
        v.line(layer, [(c, a), (c, b)] if kind == "v" else [(a, c), (b, c)], sw=0.13)


def arrow(v, layer, p0, p1, size=0.18, sw=0.2):
    v.line(layer, [p0, p1], sw=sw)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    l, r = ang + math.radians(155), ang - math.radians(155)
    tri = [p1, (p1[0] + size * math.cos(l), p1[1] + size * math.sin(l)),
           (p1[0] + size * math.cos(r), p1[1] + size * math.sin(r))]
    v.geom(layer, LineString(tri + [p1]).convex_hull, fill="#000", stroke="#000", sw=0.1)


def ellipse(c, rx, ry):
    return affinity.scale(Point(c).buffer(1.0, 24), rx, ry)


# ============================================================ LÁMINAS: COMUNES
def frame(sh, code, plano, escala, hoja):
    L = "P-MARCO"
    sh.prect(L, 10, 10, 400, 277, stroke="#000", sw=0.7)
    x0, y0, w = 285.0, 235.0, 125.0
    rows = [9, 7, 8, 11, 8.5, 8.5]
    sh.prect(L, x0, y0, w, sum(rows), fill="#ffffff", stroke="#000", sw=0.5)
    y = y0
    for h in rows[:-1]:
        y += h
        sh.ppath(L, [(x0, y), (x0 + w, y)], sw=0.25)
    sh.ptext(L, x0 + w / 2, y0 + 4.5, "UNIVERSIDAD DE HUELVA · E.T.S. de Ingeniería", 3.0, weight="bold")
    sh.ptext(L, x0 + w / 2, y0 + 12.5, "Diseño de Infraestructura Común de Telecomunicaciones", 2.4)
    sh.ptext(L, x0 + w / 2, y0 + 20, "Proyecto ICT · Conjunto residencial de 13 viviendas unifamiliares",
             2.3, weight="bold")
    sh.ptext(L, x0 + w / 2, y0 + 29.5, plano, 3.6, weight="bold")
    yr = y0 + 35 + 4.25
    for xs, txt in ((x0 + 3, "Plano: " + code), (x0 + 50, "Escala: " + escala), (x0 + 95, "Hoja: " + hoja)):
        sh.ptext(L, xs, yr, txt, 2.6, anchor="start")
    for xs in (x0 + 47, x0 + 92):
        sh.ppath(L, [(xs, y0 + 35), (xs, y0 + 43.5)], sw=0.25)
    sh.ptext(L, x0 + 3, y0 + 47.75, "Sesión 1 · Base arquitectónica (sin instalaciones ICT)", 2.3, anchor="start")
    sh.ptext(L, x0 + w - 3, y0 + 47.75, FECHA, 2.3, anchor="end")


def legend_item(sh, x, y, kind, label, **kw):
    L = "P-LEYENDA"
    if kind == "fill":
        sh.prect(L, x, y - 2, 9, 4, fill=kw["fill"], stroke=kw.get("stroke", "#000"), sw=kw.get("sw", 0.25))
    elif kind == "line":
        sh.ppath(L, [(x, y), (x + 9, y)], stroke=kw["stroke"], sw=kw.get("sw", 0.3), dash=kw.get("dash"))
    sh.ptext(L, x + 12, y, label, 2.4, anchor="start")


def north_arrow(sh, x, y, r=7.0, dx=0.0, dy=-1.0, label="N"):
    L = "P-LEYENDA"
    n = math.hypot(dx, dy)
    dx, dy = dx / n, dy / n
    px, py = -dy, dx
    tip = (x + dx * r, y + dy * r)
    tail = (x - dx * r * 0.6, y - dy * r * 0.6)
    sh.ppath(L, [tip, (tail[0] + px * r * 0.45, tail[1] + py * r * 0.45), (x, y)], close=True,
             fill="#000", stroke="#000", sw=0.2)
    sh.ppath(L, [tip, (tail[0] - px * r * 0.45, tail[1] - py * r * 0.45), (x, y)], close=True,
             fill="#fff", stroke="#000", sw=0.2)
    sh.ptext(L, x + dx * (r + 3.2), y + dy * (r + 3.2), label, 3.5, weight="bold")


def scale_bar(sh, x, y, k, meters, step):
    L = "P-LEYENDA"
    n = int(meters / step)
    for i in range(n):
        sh.prect(L, x + i * step * k, y, step * k, 1.6, fill="#000" if i % 2 == 0 else "#fff", sw=0.2)
    for i in range(n + 1):
        sh.ptext(L, x + i * step * k, y + 4.2, "%d" % (i * step), 2.0)
    sh.ptext(L, x + n * step * k + 3, y + 0.8, "m", 2.2, anchor="start")


# ============================================================ PLANO GENERAL / DETALLE
def draw_house_footprint(v, name, row, px):
    fp = footprint(row, px)
    v.rect("A-EDIF-VIVIENDAS", fp, fill=C_HOUSE, stroke="#222", sw=0.5)
    # línea de cumbrera (cubierta a dos aguas, eje este-oeste)
    ym = (fp[1] + fp[3]) / 2
    v.line("A-EDIF-VIVIENDAS", [(fp[0], ym), (fp[2], ym)], stroke="#777", sw=0.15, dash="1.2,0.8")
    cx = (fp[0] + fp[2]) / 2
    off = 1.6 if row == "N" else -1.6
    v.text("A-TEXTOS", cx, ym + off, name, size=4.2, weight="bold")
    v.text("A-TEXTOS", cx, ym - off, "PB+1 · 11,00×8,00", size=1.8, fill="#333")
    # acceso: camino desde la acera hasta la puerta principal
    dx, dy, _ = to_world(row, px, 5.9, 0.0)
    if row == "N":
        v.rect("A-ACERAS-CAMINOS", (dx - 0.6, 30.0, dx + 0.6, fp[1]), fill=C_SIDE, stroke="#8a8a8a", sw=0.12)
        tri = [(dx - 0.55, fp[1] - 1.1), (dx + 0.55, fp[1] - 1.1), (dx, fp[1] - 0.1)]
    else:
        v.rect("A-ACERAS-CAMINOS", (dx - 0.6, fp[3], dx + 0.6, 20.0), fill=C_SIDE, stroke="#8a8a8a", sw=0.12)
        tri = [(dx - 0.55, fp[3] + 1.1), (dx + 0.55, fp[3] + 1.1), (dx, fp[3] + 0.1)]
    v.geom("A-EDIF-VIVIENDAS", LineString(tri + [tri[0]]).convex_hull, fill="#000", stroke=None)


def draw_site(v, detail=False):
    v.rect("A-TERRENO", (0, 0, SITE_W, SITE_H), fill=C_BASE, stroke=None)
    v.rect("A-VIALES", PUB_ROAD, fill=C_ROAD, stroke="#777", sw=0.2)
    v.rect("A-ACERAS-CAMINOS", PUB_SIDE, fill=C_SIDE, stroke="#888", sw=0.15)
    v.rect("A-VIALES", ROAD, fill=C_ROAD, stroke="#777", sw=0.2)
    v.line("A-VIALES", [(0.5, 25.0), (135.0, 25.0)], stroke="#ffffff", sw=0.35, dash="3,2")
    v.line("A-VIALES", [(-7.0, -2.5), (-7.0, 52.5)], stroke="#ffffff", sw=0.35, dash="3,2")
    v.rect("A-ACERAS-CAMINOS", SIDE_S, fill=C_SIDE, stroke="#888", sw=0.15)
    v.rect("A-ACERAS-CAMINOS", SIDE_N, fill=C_SIDE, stroke="#888", sw=0.15)
    v.rect("A-ACERAS-CAMINOS", LC1_COURT, fill=C_PAVED, stroke="#888", sw=0.15)
    v.rect("A-ACERAS-CAMINOS", (9.3, 30.0, 10.7, 35.0), fill=C_SIDE, stroke="#8a8a8a", sw=0.12)
    # ZC2: zona verde con caminos
    v.rect("A-ZONAS-VERDES", ZC2, fill=C_GREEN, stroke="#4f7a3a", sw=0.35)
    v.rect("A-ZONAS-VERDES", (128.25, 30.0, 129.75, 46.0), fill=C_SIDE, stroke="#8a8a8a", sw=0.12)
    v.rect("A-ZONAS-VERDES", (123.0, 38.25, 135.0, 39.75), fill=C_SIDE, stroke="#8a8a8a", sw=0.12)
    # parcelas
    for name, (row, px) in HOUSES.items():
        v.rect("A-PARCELAS", parcel(row, px), stroke=C_FENCE, sw=0.2, dash="1.5,0.8")
    v.rect("A-PARCELAS", ZC1_BLOCK, stroke=C_FENCE, sw=0.2, dash="1.5,0.8")
    v.rect("A-PARCELAS", (2.0, 2.0, 22.0, 15.0), stroke=C_FENCE, sw=0.2, dash="1.5,0.8")
    # edificaciones
    for name, (row, px) in HOUSES.items():
        draw_house_footprint(v, name, row, px)
    if detail:
        v.rect("A-EDIF-LOCAL", LC1, fill="#ffffff", stroke=None)
        v.geom("A-MUROS", shell_walls(LC1, 0.30, LC1_DOORS, LC1_WINDOWS), fill=C_WALL, stroke=C_WALL_LN, sw=0.25)
        v.rect("A-EDIF-ZONAS-COMUNES", ZC1, fill="#ffffff", stroke=None)
        v.geom("A-MUROS", shell_walls(ZC1, 0.30, ZC1_DOORS, ZC1_WINDOWS), fill=C_WALL, stroke=C_WALL_LN, sw=0.25)
        for d in LC1_DOORS + ZC1_DOORS:
            draw_door(v, d)
        for w in LC1_WINDOWS + ZC1_WINDOWS:
            draw_window(v, w)
    else:
        v.rect("A-EDIF-LOCAL", LC1, fill=C_LC, stroke="#222", sw=0.5)
        v.rect("A-EDIF-ZONAS-COMUNES", ZC1, fill=C_ZC, stroke="#222", sw=0.5)
        for (x0, x1, y) in ((10.1, 11.9, 15.0), (9.1, 10.9, 35.0)):
            v.line("A-EDIF-LOCAL" if y < 30 else "A-EDIF-ZONAS-COMUNES", [(x0, y), (x1, y)],
                   stroke="#ffffff", sw=0.9)
        tri_lc = [(10.45, 16.1), (11.55, 16.1), (11.0, 15.1)]
        tri_zc = [(9.45, 33.9), (10.55, 33.9), (10.0, 34.9)]
        for t, lay in ((tri_lc, "A-EDIF-LOCAL"), (tri_zc, "A-EDIF-ZONAS-COMUNES")):
            v.geom(lay, LineString(t + [t[0]]).convex_hull, fill="#000", stroke=None)
    # límite del complejo (abierto en el acceso desde el vial público)
    v.line("A-LIMITE", [(0, 15.0), (0, 0), (SITE_W, 0), (SITE_W, SITE_H), (0, SITE_H), (0, 30.0)],
           stroke=C_LIMIT, sw=0.5, dash="4,1,0.8,1")


def site_texts_general(v):
    T = "A-TEXTOS"
    v.text(T, 60.0, 23.3, "VIAL INTERIOR (7,00 m) · acceso rodado y peatonal a todas las parcelas",
           size=2.4, fill="#333")
    v.text(T, -7.0, 40.0, "VIAL PÚBLICO (propuesto)", size=2.4, rot=90, fill="#333")
    v.text(T, -7.0, 10.0, "Calle de acceso", size=2.0, rot=90, fill="#333", italic=True)
    v.texts(T, 3.8, 25.0, [("ACCESO", "bold"), "PRINCIPAL"], size=2.0, anchor="start", halo=True)
    arrow(v, T, (-1.0, 25.0), (2.6, 25.0), size=0.9, sw=0.35)
    v.texts(T, 11.0, 10.0, [("LC1", "bold", 4.2), "Local comercial", "160,00 m² · 1 planta"], size=2.0)
    v.texts(T, 10.0, 39.0, [("ZC1", "bold", 4.2), "Zona común 1", "edificio de uso común", "96,00 m² (propuesta)"],
            size=1.9)
    v.texts(T, 125.6, 43.7, [("ZC2", "bold", 4.2), "Zona común 2"], size=1.9, halo=True)
    v.texts(T, 125.6, 34.3, ["zona verde", "252,00 m²", "(propuesta)"], size=1.7, halo=True)
    v.text(T, 11.0, 17.5, "Explanada de acceso LC1", size=1.8, fill="#444")
    for gx in (22.0, 54.0, 86.0, 118.0):
        v.text(T, gx + 2.0, 11.0, "franja verde 4,00 m", size=1.6, rot=90, fill="#4f6b3f")
    v.text(T, 134.6, 25.0, "fondo de saco", size=1.6, rot=90, fill="#444")


def site_groups(v):
    """Agrupación por parejas (capa propia, solo rotulación arquitectónica)."""
    L = "A-AGRUPACION"
    for gname, a, b in GROUPS:
        row, px = HOUSES[a]
        if b:
            x0, x1 = px, px + 2 * PARCEL_W
            txt = "%s · %s–%s" % (gname, a, b)
        else:
            x0, x1 = px, px + PARCEL_W
            txt = "%s · %s (pendiente)" % (gname, a)
        y = 46.4 if row == "N" else 3.6
        yb = 47.5 if row == "N" else 2.5
        v.line(L, [(x0 + 0.6, yb), (x1 - 0.6, yb)], stroke="#2c5d8a", sw=0.35)
        for xx in (x0 + 0.6, x1 - 0.6):
            v.line(L, [(xx, yb), (xx, yb + (-0.7 if row == "N" else 0.7))], stroke="#2c5d8a", sw=0.35)
        v.text(L, (x0 + x1) / 2, y, txt, size=2.2, weight="bold", fill="#2c5d8a", halo=True)


def site_reserve(v):
    """Ubicaciones reservadas (capa DESACTIVADA). Sin equipos ni función asignada."""
    L = "ICT-RESERVA"
    spots = [(40.0, 30.9), (72.0, 30.9), (104.0, 30.9), (40.0, 19.1), (72.0, 19.1), (104.0, 19.1),
             (123.0, 19.1)]
    for i, (x, y) in enumerate(spots):
        v.rect(L, (x - 0.5, y - 0.5, x + 0.5, y + 0.5), stroke="#7a3fa0", sw=0.3, dash="0.8,0.5")
        lab = "R%d" % (i + 1) + (" (pend.)" if i == 6 else "")
        v.text(L, x, y + (1.3 if y > 25 else -1.3), lab, size=1.8, fill="#7a3fa0", halo=True)


# ============================================================ VIVIENDA TIPO
def draw_stair(v, floor):
    L = "A-ESCALERA"
    x0, y0, x1, y1, n = STAIR
    t = (y1 - y0) / n
    v.rect(L, (x0, y0, x1, y1), fill="#ffffff", stroke="#000", sw=0.25)
    for i in range(1, n):
        v.line(L, [(x0, y0 + i * t), (x1, y0 + i * t)], sw=0.15)
    xm = (x0 + x1) / 2
    v.rect(L, (x0 - 0.05, y0, x0, y1), fill="#ffffff", stroke="#000", sw=0.15)   # barandilla
    if floor == "PB":
        v.geom(L, Point(xm, y1 - 0.18).buffer(0.06, 12), fill="#000", stroke=None)
        arrow(v, L, (xm, y1 - 0.18), (xm, y0 + 0.15), size=0.22)
        v.text(L, xm, y1 + 0.32, "SUBE", size=2.2, weight="bold")
    else:
        v.rect(L, (x0 - 0.05, y1, x1, y1 + 0.05), fill="#ffffff", stroke="#000", sw=0.15)
        v.geom(L, Point(xm, y0 + 0.15).buffer(0.06, 12), fill="#000", stroke=None)
        arrow(v, L, (xm, y0 + 0.15), (xm, y1 - 0.18), size=0.22)
        v.text(L, xm, y0 - 0.32, "BAJA", size=2.2, weight="bold")


def draw_fixtures(v, floor):
    L = "A-SANITARIOS"
    k = dict(fill="#ffffff", stroke="#000", sw=0.18)
    v.rect(L, (9.85, 0.25, 10.75, 1.45), **k)                      # plato de ducha
    v.line(L, [(9.85, 0.25), (10.75, 1.45)], sw=0.1)
    v.line(L, [(9.85, 1.45), (10.75, 0.25)], sw=0.1)
    v.rect(L, (8.6, 2.18, 9.1, 2.4), **k)                          # inodoro
    v.geom(L, ellipse((8.85, 1.93), 0.19, 0.26), **k)
    v.rect(L, (9.45, 1.98, 10.15, 2.4), **k)                       # lavabo
    v.geom(L, ellipse((9.8, 2.17), 0.25, 0.14), **k)
    if floor == "PB":                                             # cocina
        v.rect(L, (10.05, 2.5, 10.75, 3.15), **k)                  # frigorífico
        v.line(L, [(10.05, 2.5), (10.75, 3.15)], sw=0.1)
        v.rect(L, (10.15, 3.15, 10.75, 5.0), **k)                  # encimera lateral
        for cx in (10.32, 10.58):
            for cy in (3.7, 4.05):
                v.geom(L, Point(cx, cy).buffer(0.1, 16), **k)      # placa de cocción
        v.rect(L, (8.6, 7.15, 10.75, 7.75), **k)                   # encimera posterior
        v.rect(L, (9.0, 7.25, 9.8, 7.65), **k)                     # fregadero


def house_sheet(floor, code, hoja):
    titulo = "Planta baja" if floor == "PB" else "Planta primera"
    layers = [("A-SUELO", "Fondo de estancias", True),
              ("A-MUROS", "Muros exteriores (0,25) y tabiques (0,10)", True),
              ("A-VENTANAS", "Ventanas", True),
              ("A-PUERTAS", "Puertas y sentido de giro", True),
              ("A-ESCALERA", "Escalera y barandilla", True),
              ("A-SANITARIOS", "Aparatos sanitarios y cocina (referencia)", True),
              ("A-ESTANCIAS", "Rótulos de dependencias y superficies", True),
              ("A-COTAS", "Cotas generales", True),
              ("A-TEXTOS", "Textos de fachada", True),
              ("ICT-RIU-REGISTROS", "VACÍA - registros red interior (sesión siguiente)", True),
              ("ICT-RIU-CANALIZACION", "VACÍA - canalización red interior (sesión siguiente)", True),
              ("ICT-RIU-TOMAS", "VACÍA - tomas de usuario (sesión siguiente)", True),
              ("P-MARCO", "Marco y cajetín", True), ("P-LEYENDA", "Leyenda, cuadro y notas", True)]
    sh = Sheet(code, "Vivienda tipo - " + titulo, layers)
    v = View(sh, 50, -1.5, 9.0, 17.0, 34.0)
    f = FLOORS[floor]
    v.rect("A-SUELO", (0, 0, 11, 8), fill="#ffffff", stroke=None)
    v.geom("A-MUROS", house_walls(floor), fill=C_WALL, stroke=C_WALL_LN, sw=0.3)
    for w in f["windows"]:
        draw_window(v, w)
    for d in f["doors"]:
        draw_door(v, d)
    draw_stair(v, floor)
    draw_fixtures(v, floor)
    total = 0.0
    for name, r, (lx, ly) in f["rooms"]:
        area = CENTRAL_AREA if r is None else (r[2] - r[0]) * (r[3] - r[1])
        total += area
        words = name.split(" ")
        if name.startswith("Vestíbulo"):
            lines = [("Vestíbulo-", "bold"), ("distribuidor", "bold"), fmt(area) + " m²"]
        elif name.startswith("Dormitorio 4"):
            lines = [("Dormitorio 4", "bold"), "(o despacho)", fmt(area) + " m²"]
        elif name.startswith("Dormitorio 1"):
            lines = [("Dormitorio 1", "bold"), "(principal)", fmt(area) + " m²"]
        else:
            lines = [(name, "bold"), fmt(area) + " m²"]
        v.texts("A-ESTANCIAS", lx, ly, lines, size=2.6 if r else 2.2, lead=1.35)
    stair_area = (STAIR[2] - STAIR[0]) * (STAIR[3] - STAIR[1])
    total += stair_area
    # cotas
    C = "A-COTAS"
    v.hdim(C, 0, 11, -1.35, 0)
    v.hdim(C, 0, 5.05, -0.7, 0)
    v.hdim(C, 5.05, 7.25, -0.7, 0)
    v.hdim(C, 7.25, 11, -0.7, 0)
    v.vdim(C, 0, 8, 12.35, 11)
    v.vdim(C, 0, 2.45, 11.7, 11)
    v.vdim(C, 2.45, 8, 11.7, 11)
    v.vdim(C, 0, 3.05, -0.7, 0)
    v.vdim(C, 3.05, 8, -0.7, 0)
    v.text("A-TEXTOS", 5.5, -2.15, "FACHADA PRINCIPAL · acceso desde el vial interior", size=2.6, weight="bold")
    v.text("A-TEXTOS", 5.5, 9.05 - 0.05, "Fachada posterior · jardín privado", size=2.4, italic=True)
    # título y panel derecho
    sh.ptext("P-LEYENDA", 20, 19, "VIVIENDA UNIFAMILIAR TIPO · %s" % titulo.upper(), 5.0,
             anchor="start", weight="bold")
    sh.ptext("P-LEYENDA", 20, 26, "Planta común a las 13 viviendas (V01–V13) · dos plantas (PB + P1) · "
             "huella 11,00 × 8,00 m · altura libre propuesta 2,70 m", 2.6, anchor="start")
    X = 300.0
    sh.ptext("P-LEYENDA", X, 40, "CUADRO DE SUPERFICIES ÚTILES · " + titulo.upper(), 2.8, anchor="start",
             weight="bold")
    y = 47.0
    sh.prect("P-LEYENDA", X, y - 3.5, 103, 7.0, fill="#eeeeee", sw=0.25)
    sh.ptext("P-LEYENDA", X + 2, y, "Dependencia", 2.4, anchor="start", weight="bold")
    sh.ptext("P-LEYENDA", X + 101, y, "Sup. (m²)", 2.4, anchor="end", weight="bold")
    for name, r, _ in f["rooms"] + [("Escalera (proyección)", (STAIR[0], STAIR[1], STAIR[2], STAIR[3]), None)]:
        y += 7.0
        area = CENTRAL_AREA if r is None else (r[2] - r[0]) * (r[3] - r[1])
        sh.prect("P-LEYENDA", X, y - 3.5, 103, 7.0, sw=0.2)
        sh.ptext("P-LEYENDA", X + 2, y, name, 2.4, anchor="start")
        sh.ptext("P-LEYENDA", X + 101, y, fmt(area), 2.4, anchor="end")
    y += 7.0
    sh.prect("P-LEYENDA", X, y - 3.5, 103, 7.0, fill="#eeeeee", sw=0.25)
    sh.ptext("P-LEYENDA", X + 2, y, "Total útil de la planta", 2.4, anchor="start", weight="bold")
    sh.ptext("P-LEYENDA", X + 101, y, fmt(total), 2.4, anchor="end", weight="bold")
    y += 7.0
    sh.ptext("P-LEYENDA", X, y, "Superficie construida por planta: 88,00 m² · total vivienda: 176,00 m²",
             2.2, anchor="start")
    # leyenda gráfica
    y += 11
    sh.ptext("P-LEYENDA", X, y, "SIMBOLOGÍA", 2.8, anchor="start", weight="bold")
    y += 7
    legend_item(sh, X, y, "fill", "Muro exterior 0,25 m / tabique 0,10 m", fill=C_WALL, stroke=C_WALL_LN)
    y += 7
    sh.ppath("P-LEYENDA", [(X, y + 2), (X, y - 2), (X + 1.0, y - 2), (X + 1.0, y + 2)], sw=0.2)
    sh.ppath("P-LEYENDA", [(X + 1.0, y + 2), (X + 6, y + 2)], sw=0.2)
    sh.ppath("P-LEYENDA", [(X + 1.0, y - 2.8), (X + 1.0, y + 2)], sw=0.4)
    sh.svg["P-LEYENDA"].append('<path d="M %.2f,%.2f A 4.8 4.8 0 0 1 %.2f,%.2f"%s/>'
                               % (X + 1.0, y - 2.8, X + 5.8, y + 2, style("none", "#000", 0.15)))
    sh.ptext("P-LEYENDA", X + 12, y, "Puerta abatible (hoja y sentido de giro)", 2.4, anchor="start")
    y += 7
    sh.prect("P-LEYENDA", X, y - 1.2, 9, 2.4, fill="#fff", sw=0.2)
    sh.ppath("P-LEYENDA", [(X, y - 0.3), (X + 9, y - 0.3)], sw=0.13)
    sh.ppath("P-LEYENDA", [(X, y + 0.3), (X + 9, y + 0.3)], sw=0.13)
    sh.ptext("P-LEYENDA", X + 12, y, "Ventana", 2.4, anchor="start")
    y += 7
    sh.prect("P-LEYENDA", X, y - 2, 9, 4, fill="#fff", sw=0.2)
    for i in range(1, 6):
        sh.ppath("P-LEYENDA", [(X + i * 1.5, y - 2), (X + i * 1.5, y + 2)], sw=0.13)
    sh.ptext("P-LEYENDA", X + 12, y, "Escalera recta, 14 huellas de 0,26 m", 2.4, anchor="start")
    # notas
    y += 11
    sh.ptext("P-LEYENDA", X, y, "NOTAS", 2.8, anchor="start", weight="bold")
    notas = ["1. Cotas en metros. Dimensiones de diseño",
             "    propuestas (hipótesis), comunes a todos los planos.",
             "2. Superficies útiles medidas a cara interior.",
             "3. V01–V06: fachada principal al sur.",
             "    V07–V13: misma planta girada 180°.",
             "4. Capas ICT-RIU-* vacías: reservadas para",
             "    registros, canalización y tomas (sesión 2).",
             "5. Mobiliario no representado salvo sanitarios",
             "    y cocina, como referencia de uso."]
    sh.ptexts("P-LEYENDA", X, y + 6, notas, size=2.2, lead=1.55, anchor="start")
    frame(sh, code, "Vivienda tipo · " + titulo, "1:50", hoja)
    return sh


# ============================================================ LÁMINA PLANO GENERAL
def general_sheet():
    layers = [("A-TERRENO", "Terreno del conjunto (ajardinado)", True),
              ("A-VIALES", "Viales rodados", True),
              ("A-ACERAS-CAMINOS", "Aceras, caminos y explanadas", True),
              ("A-ZONAS-VERDES", "Zona verde común", True),
              ("A-PARCELAS", "Límites de parcela", True),
              ("A-EDIF-VIVIENDAS", "Viviendas V01-V13", True),
              ("A-EDIF-LOCAL", "Local comercial LC1", True),
              ("A-EDIF-ZONAS-COMUNES", "Zona común edificada ZC1", True),
              ("A-LIMITE", "Límite del complejo", True),
              ("A-AGRUPACION", "Agrupación propuesta por parejas", True),
              ("A-COTAS", "Cotas", True), ("A-TEXTOS", "Rótulos", True),
              ("ICT-RESERVA", "DESACTIVADA - ubicaciones técnicas reservadas (sin denominación)", False),
              ("ICT-ELEMENTOS", "VACÍA - elementos ICT (sesión siguiente)", True),
              ("ICT-CANALIZACIONES", "VACÍA - canalizaciones (sesión siguiente)", True),
              ("ICT-CABLEADO", "VACÍA - cableado (sesión siguiente)", True),
              ("P-MARCO", "Marco y cajetín", True), ("P-LEYENDA", "Leyenda, cuadros y notas", True)]
    sh = Sheet("ICT-02", "Plano general del complejo", layers)
    v = View(sh, 400, -13.0, 54.0, 17.0, 20.0)
    draw_site(v)
    site_texts_general(v)
    site_groups(v)
    site_reserve(v)
    C = "A-COTAS"
    v.hdim(C, 0, SITE_W, -2.6, 0, size=2.2, txt="138,00")
    v.vdim(C, 0, SITE_H, 141.6, SITE_W, size=2.2, txt="50,00")
    v.hdim(C, 27.5, 38.5, 51.6, 48.0, size=1.9)
    v.hdim(C, 38.5, 41.5, 51.6, 48.0, size=1.9)
    v.hdim(C, 41.5, 52.5, 51.6, 48.0, size=1.9)
    v.hdim(C, 54.0, 58.0, 51.6, 48.0, size=1.9)
    v.hdim(C, 58.0, 72.0, 51.6, 48.0, size=1.9)
    v.vdim(C, 2.0, 20.0, 140.1, 136.0, size=1.9)
    v.vdim(C, 21.5, 28.5, 140.1, 136.0, size=1.9)
    v.vdim(C, 30.0, 48.0, 140.1, 136.0, size=1.9)
    # ---- panel inferior
    L = "P-LEYENDA"
    sh.ptext(L, 17, 180, "PLANO GENERAL DEL COMPLEJO RESIDENCIAL · PLANTA", 4.4, anchor="start", weight="bold")
    sh.ptext(L, 17, 186.5, "13 viviendas unifamiliares independientes (V01–V13) · 2 zonas comunes (ZC1, ZC2) · "
             "1 local comercial (LC1)", 2.6, anchor="start")
    x, y = 17, 196
    sh.ptext(L, x, y, "LEYENDA", 2.8, anchor="start", weight="bold")
    items = [("fill", "Vivienda unifamiliar PB+1 (11,00 × 8,00 m)", dict(fill=C_HOUSE, stroke="#222", sw=0.4)),
             ("fill", "Local comercial LC1", dict(fill=C_LC, stroke="#222", sw=0.4)),
             ("fill", "Zona común edificada ZC1", dict(fill=C_ZC, stroke="#222", sw=0.4)),
             ("fill", "Zona común libre ZC2 (zona verde)", dict(fill=C_GREEN, stroke="#4f7a3a", sw=0.4)),
             ("fill", "Vial rodado", dict(fill=C_ROAD, stroke="#777", sw=0.2)),
             ("fill", "Acera / camino peatonal", dict(fill=C_SIDE, stroke="#888", sw=0.2)),
             ("fill", "Explanada pavimentada", dict(fill=C_PAVED, stroke="#888", sw=0.2)),
             ("fill", "Jardín privado / zona ajardinada", dict(fill=C_BASE, stroke="#888", sw=0.2)),
             ("line", "Límite del complejo", dict(stroke=C_LIMIT, sw=0.5, dash="4,1,0.8,1")),
             ("line", "Límite de parcela (14,00 × 18,00 m)", dict(stroke=C_FENCE, sw=0.25, dash="1.5,0.8")),
             ("line", "Agrupación por parejas", dict(stroke="#2c5d8a", sw=0.4))]
    for i, (kind, lab, kw) in enumerate(items):
        col, rowi = divmod(i, 6)
        legend_item(sh, x + col * 72, y + 7 + rowi * 6.5, kind, lab, **kw)
    yy = y + 7 + 5 * 6.5
    sh.ppath(L, [(x + 72 + 3.2, yy - 1.6), (x + 72 + 5.8, yy - 1.6), (x + 72 + 4.5, yy + 1.4)],
             close=True, fill="#000", stroke=None)
    sh.ptext(L, x + 72 + 12, yy, "Acceso principal a cada edificación", 2.4, anchor="start")
    north_arrow(sh, x + 162, y + 22, r=8)
    scale_bar(sh, x + 140, y + 43, 2.5, 20, 5)
    sh.ptext(L, x + 162, y + 53, "Escala 1:400 (A3)", 2.2)
    # cuadro de agrupación
    X, Y = 17, 262
    sh.ptext(L, X, Y - 6.5, "AGRUPACIÓN PROPUESTA (preparación de la ICT, sin asignación técnica)", 2.6,
             anchor="start", weight="bold")
    cols = [g[0] for g in GROUPS]
    w = 37.0
    for i, (gname, a, b) in enumerate(GROUPS):
        cx = X + i * w
        sh.prect(L, cx, Y - 3, w, 6, fill="#eeeeee", sw=0.2)
        sh.prect(L, cx, Y + 3, w, 6, sw=0.2)
        sh.ptext(L, cx + w / 2, Y, gname, 2.3, weight="bold")
        sh.ptext(L, cx + w / 2, Y + 6, "%s – %s" % (a, b) if b else "V13 · pendiente*", 2.3)
    sh.ptext(L, X, Y + 13, "* 13 viviendas = 6 parejas + 1 vivienda restante. La asignación técnica del grupo 7 "
             "(V13) se resolverá en sesiones siguientes considerando el local LC1.", 2.1, anchor="start")
    # notas
    X = 287
    sh.ptext(L, X, 180, "NOTAS", 2.8, anchor="start", weight="bold")
    notas = ["1. Cotas en metros. Dimensiones de diseño propuestas",
             "    (hipótesis), mantenidas en todos los planos y en el 3D.",
             "2. Cada vivienda es una edificación aislada en su parcela;",
             "    separación mínima entre viviendas: 3,00 m.",
             "3. Usos de ZC1 y ZC2 propuestos (no definidos en la consigna).",
             "4. Capa ICT-RESERVA desactivada: ubicaciones reservadas",
             "    sin equipos ni función asignada. Denominación del",
             "    elemento (RTS / RS / RTR) pendiente de confirmar.",
             "5. Sin canalizaciones, cableado ni elementos ICT."]
    sh.ptexts(L, X, 186.5, notas, size=2.15, lead=1.6, anchor="start")
    frame(sh, "ICT-02", "Plano general del complejo · Planta", "1:400", "2/5")
    return sh


# ============================================================ LÁMINA LOCAL + ZONAS COMUNES
def lc_zc_sheet():
    layers = [("A-TERRENO", "Terreno del conjunto", True), ("A-VIALES", "Viales", True),
              ("A-ACERAS-CAMINOS", "Aceras, caminos y explanadas", True),
              ("A-ZONAS-VERDES", "Zona verde común", True), ("A-PARCELAS", "Límites de parcela", True),
              ("A-EDIF-VIVIENDAS", "Viviendas (contexto)", True),
              ("A-EDIF-LOCAL", "Local comercial LC1 (interior vacío)", True),
              ("A-EDIF-ZONAS-COMUNES", "Edificio ZC1", True),
              ("A-MUROS", "Muros exteriores 0,30 m", True), ("A-VENTANAS", "Ventanas / escaparates", True),
              ("A-PUERTAS", "Puertas de acceso", True), ("A-LIMITE", "Límite del complejo", True),
              ("A-COTAS", "Cotas", True), ("A-TEXTOS", "Rótulos", True),
              ("ICT-ELEMENTOS", "VACÍA - elementos ICT (sesión siguiente)", True),
              ("ICT-CANALIZACIONES", "VACÍA - canalizaciones (sesión siguiente)", True),
              ("P-MARCO", "Marco y cajetín", True), ("P-LEYENDA", "Títulos y notas", True)]
    sh = Sheet("ICT-05", "Local comercial y zonas comunes", layers)
    T, C = "A-TEXTOS", "A-COTAS"
    views = [(-3.0, 23.0, -1.0, 22.0, 20.0, "A · LOCAL COMERCIAL LC1"),
             (-1.0, 23.0, 28.0, 51.5, 162.0, "B · ZONA COMÚN 1 · ZC1"),
             (121.0, 139.5, 28.0, 51.5, 294.0, "C · ZONA COMÚN 2 · ZC2")]
    py0 = 42.0
    for x0, x1, y0, y1, px0, title in views:
        v = View(sh, 200, x0, y1, px0, py0, clip=(x0, y0, x1, y1))
        draw_site(v, detail=True)
        pw, ph = (x1 - x0) * v.k, (y1 - y0) * v.k
        sh.prect("P-LEYENDA", px0, py0, pw, ph, stroke="#555", sw=0.3)
        sh.ptext("P-LEYENDA", px0, py0 - 5, title, 3.4, anchor="start", weight="bold")
        sh.ptext("P-LEYENDA", px0 + pw, py0 - 5, "E 1:200", 2.6, anchor="end")
        if x0 < 0 and y0 < 0:      # LC1
            v.hdim(C, 3, 19, 4.2, 5.0)
            v.vdim(C, 5, 15, 20.6, 19.0)
            v.texts(T, 11.0, 3.05, [("Local comercial LC1", "bold", 3.0), "interior en blanco (sin distribuir)"],
                    size=2.0)
            v.text(T, 11.0, 18.9, "Explanada de acceso (pavimentada)", size=2.0, fill="#444")
            v.texts(T, 11.0, 16.75, ["Acceso principal"], size=2.0, weight="bold", halo=True)
            v.text(T, 6.7, 16.0, "escaparate", size=1.8, fill="#444")
            v.text(T, 15.3, 16.0, "escaparate", size=1.8, fill="#444")
            v.texts(T, -1.0, 9.0, ["Acera pública"], size=1.9, rot=90, fill="#444")
            arrow(v, T, (-1.0, 17.5), (1.6, 17.5), size=0.6, sw=0.3)
            v.text(T, 10.0, 21.0, "Acera del vial interior", size=1.9, fill="#444")
            v.text(T, 21.3, 12.0, "S. const. 160,00 m²", size=1.8, rot=90, fill="#333")
        elif x0 < 0:               # ZC1
            v.hdim(C, 4, 16, 44.3, 43.0)
            v.vdim(C, 35, 43, 17.3, 16.0)
            v.texts(T, 10.0, 39.0, [("ZC1 · Zona común 1", "bold", 3.0), "Edificio de uso común",
                                    "(uso propuesto)", "S. const. 96,00 m²"], size=2.2)
            v.text(T, 10.0, 32.5, "Acceso", size=2.0, weight="bold", halo=True)
            v.text(T, 10.0, 29.25, "Acera del vial interior", size=1.9, fill="#444")
            v.text(T, 19.5, 46.0, "Parcela ZC1 · 20,00 × 18,00 m", size=1.8, rot=90, fill="#444")
        else:                      # ZC2
            v.hdim(C, 122, 136, 49.0, 48.0)
            v.vdim(C, 30, 48, 137.1, 136.0)
            v.texts(T, 125.3, 43.6, [("ZC2", "bold", 3.4), "Zona común 2"], size=2.0, halo=True)
            v.texts(T, 125.3, 34.2, ["Zona verde /", "esparcimiento", "(uso propuesto)"], size=1.8, halo=True)
            v.texts(T, 132.6, 34.2, ["S ≈ 252,00 m²"], size=1.8, halo=True)
            v.text(T, 129.0, 29.25, "Acera del vial interior", size=1.9, fill="#444")
            v.texts(T, 132.6, 43.6, ["Camino", "peatonal"], size=1.8, halo=True)
    L = "P-LEYENDA"
    sh.ptext(L, 20, 19, "LOCAL COMERCIAL Y ZONAS COMUNES · PLANTA", 5.0, anchor="start", weight="bold")
    sh.ptext(L, 20, 26, "Detalle de LC1, ZC1 y ZC2 extraído del plano general ICT-02 (misma geometría)",
             2.6, anchor="start")
    X, Y = 20, 172
    sh.ptext(L, X, Y, "CRITERIOS DE REPRESENTACIÓN", 2.8, anchor="start", weight="bold")
    notas = ["• LC1: se dibuja solo el perímetro (muro 0,30 m), el acceso exterior y los escaparates. El interior se deja",
             "   en blanco por indicación del profesor: sin distribución, sin aseos, sin equipamiento y sin instalaciones.",
             "• Las puertas de LC1 y ZC1 abren hacia el exterior para no ocupar el interior y facilitar la evacuación.",
             "• ZC1 y ZC2: forma y uso propuestos (no definidos en la consigna). ZC1 sin compartimentar interiormente.",
             "• Cotas en metros; dimensiones de diseño (hipótesis) idénticas a las del plano general y del esquema 3D.",
             "• No se representa ningún elemento, canalización ni cableado de telecomunicaciones (capas ICT-* vacías)."]
    sh.ptexts(L, X, Y + 7, notas, size=2.4, lead=1.65, anchor="start")
    X2, Y2 = 20, 222
    sh.ptext(L, X2, Y2, "LEYENDA", 2.8, anchor="start", weight="bold")
    legend_item(sh, X2, Y2 + 7, "fill", "Muro exterior 0,30 m", fill=C_WALL, stroke=C_WALL_LN)
    legend_item(sh, X2 + 70, Y2 + 7, "fill", "Zona verde común", fill=C_GREEN, stroke="#4f7a3a")
    legend_item(sh, X2 + 140, Y2 + 7, "fill", "Vial rodado", fill=C_ROAD, stroke="#777")
    legend_item(sh, X2, Y2 + 14, "fill", "Acera / camino peatonal", fill=C_SIDE, stroke="#888")
    legend_item(sh, X2 + 70, Y2 + 14, "fill", "Explanada pavimentada", fill=C_PAVED, stroke="#888")
    legend_item(sh, X2 + 140, Y2 + 14, "line", "Límite del complejo", stroke=C_LIMIT, sw=0.5, dash="4,1,0.8,1")
    legend_item(sh, X2, Y2 + 21, "line", "Límite de parcela", stroke=C_FENCE, sw=0.25, dash="1.5,0.8")
    legend_item(sh, X2 + 70, Y2 + 21, "fill", "Vivienda (contexto)", fill=C_HOUSE, stroke="#222")
    north_arrow(sh, 250, 255, r=8)
    sh.ptext(L, 250, 276, "Orientación común a A, B y C", 2.0)
    frame(sh, "ICT-05", "Local comercial LC1 y zonas comunes", "1:200", "5/5")
    return sh


# ============================================================ 3D
TH, PH = math.radians(20.0), math.radians(35.0)
VIEWV = (-math.sin(TH) * math.cos(PH), -math.cos(TH) * math.cos(PH), math.sin(PH))
LIGHT = (-0.45, -0.65, 0.62)


def proj(p):
    x, y, z = p
    d = x * math.sin(TH) + y * math.cos(TH)
    return (x * math.cos(TH) - y * math.sin(TH), d * math.sin(PH) + z * math.cos(PH))


def depth(p):
    x, y, z = p
    return (x * math.sin(TH) + y * math.cos(TH)) * math.cos(PH) - z * math.sin(PH)


def newell(pts):
    nx = ny = nz = 0.0
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        nx += (a[1] - b[1]) * (a[2] + b[2])
        ny += (a[2] - b[2]) * (a[0] + b[0])
        nz += (a[0] - b[0]) * (a[1] + b[1])
    n = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
    return (nx / n, ny / n, nz / n)


def shade(hexc, n):
    ln = math.sqrt(sum(c * c for c in LIGHT))
    f = 0.62 + 0.38 * max(0.0, sum(a * b / ln for a, b in zip(n, LIGHT)))
    r, g, b = hex_rgb(hexc)
    return "#%02x%02x%02x" % (int(r * f), int(g * f), int(b * f))


class Obj3D:
    def __init__(self, name, layer, center):
        self.name, self.layer, self.center = name, layer, center
        self.faces = []    # (pts, color, normal)
        self.decals = []   # (pts, color, normal)  ventanas/puertas sobre una cara
        self.lines = []    # (pts, normal)

    def face(self, pts, color):
        n = newell(pts)
        c = [sum(p[i] for p in pts) / len(pts) for i in range(3)]
        if sum((c[i] - self.center[i]) * n[i] for i in range(3)) < 0:
            pts, n = list(reversed(pts)), tuple(-a for a in n)
        self.faces.append((pts, color, n))
        return n


def wall_decals(obj, opening, kind_face, tf, zr, color):
    """Hueco (puerta/ventana) proyectado sobre la fachada correspondiente."""
    kind, w0, w1, a, b = opening[:5]
    out = 0.03
    if kind == "h":
        y = w0 - out if w0 < 0.5 or (w0 < w1 and kind_face == "lo") else w1 + out
        pts = [(a, y, zr[0]), (b, y, zr[0]), (b, y, zr[1]), (a, y, zr[1])]
    else:
        x = w0 - out if kind_face == "lo" else w1 + out
        pts = [(x, a, zr[0]), (x, b, zr[0]), (x, b, zr[1]), (x, a, zr[1])]
    pw = [tf(*p) for p in pts]
    obj.decals.append((pw, color, newell(pw)))


def house_obj(name, row, px):
    tf = lambda x, y, z=0.0: to_world(row, px, x, y, z)
    fp = footprint(row, px)
    o = Obj3D(name, "3D-VIVIENDAS", ((fp[0] + fp[2]) / 2, (fp[1] + fp[3]) / 2, 3.5))
    W, D = HOUSE_W, HOUSE_D
    wall, roof = "#ece6da", "#b0573d"
    o.face([tf(0, 0, 0), tf(W, 0, 0), tf(W, 0, H_EAVE), tf(0, 0, H_EAVE)], wall)
    o.face([tf(0, D, 0), tf(W, D, 0), tf(W, D, H_EAVE), tf(0, D, H_EAVE)], wall)
    o.face([tf(0, 0, 0), tf(0, D, 0), tf(0, D, H_EAVE), tf(0, D / 2, H_RIDGE), tf(0, 0, H_EAVE)], wall)
    o.face([tf(W, 0, 0), tf(W, D, 0), tf(W, D, H_EAVE), tf(W, D / 2, H_RIDGE), tf(W, 0, H_EAVE)], wall)
    o.face([tf(0, 0, H_EAVE), tf(W, 0, H_EAVE), tf(W, D / 2, H_RIDGE), tf(0, D / 2, H_RIDGE)], roof)
    o.face([tf(0, D, H_EAVE), tf(W, D, H_EAVE), tf(W, D / 2, H_RIDGE), tf(0, D / 2, H_RIDGE)], roof)
    glass = "#5d7590"
    for floor, zr in (("PB", (0.9, 2.1)), ("P1", (3.9, 5.1))):
        for w in FLOORS[floor]["windows"]:
            side = "lo" if w[1] < 0.5 else "hi"
            wall_decals(o, w, side, tf, zr, glass)
    wall_decals(o, FLOORS["PB"]["doors"][0], "lo", tf, (0.0, 2.2), "#6b4a2f")
    o.floor_line = True   # se dibuja la línea de forjado entre plantas en las fachadas visibles
    return o


def block_obj(name, layer, rect, h, color, doors, windows, roofc):
    x0, y0, x1, y1 = rect
    o = Obj3D(name, layer, ((x0 + x1) / 2, (y0 + y1) / 2, h / 2))
    o.face([(x0, y0, 0), (x1, y0, 0), (x1, y0, h), (x0, y0, h)], color)
    o.face([(x0, y1, 0), (x1, y1, 0), (x1, y1, h), (x0, y1, h)], color)
    o.face([(x0, y0, 0), (x0, y1, 0), (x0, y1, h), (x0, y0, h)], color)
    o.face([(x1, y0, 0), (x1, y1, 0), (x1, y1, h), (x1, y0, h)], color)
    o.face([(x0, y0, h), (x1, y0, h), (x1, y1, h), (x0, y1, h)], roofc)
    ident = lambda x, y, z=0.0: (x, y, z)
    for w in windows:
        side = "lo" if (w[0] == "h" and abs(w[1] - y0) < 0.5) or (w[0] == "v" and abs(w[1] - x0) < 0.5) else "hi"
        wall_decals(o, w, side, ident, (0.9, 2.6) if name == "LC1" else (1.0, 2.2), "#5d7590")
    for d in doors:
        side = "lo" if (d[0] == "h" and abs(d[1] - y0) < 0.5) or (d[0] == "v" and abs(d[1] - x0) < 0.5) else "hi"
        wall_decals(o, d, side, ident, (0.0, 2.4), "#6b4a2f")
    return o


def ground_items():
    """Polígonos del suelo (orden de dibujo) y líneas sobre el terreno."""
    polys = [("Terreno", (0, 0, SITE_W, SITE_H), "#e3edd8"),
             ("Vial_publico", PUB_ROAD, "#9d9d9d"), ("Acera_publica", PUB_SIDE, "#dcdcdc"),
             ("Vial_interior", ROAD, "#9d9d9d"), ("Acera_sur", SIDE_S, "#dcdcdc"),
             ("Acera_norte", SIDE_N, "#dcdcdc"), ("Explanada_LC1", LC1_COURT, "#d8d2c6"),
             ("ZC2_zona_verde", ZC2, "#a9cf92"),
             ("ZC2_camino_NS", (128.25, 30.0, 129.75, 46.0), "#dcdcdc"),
             ("ZC2_camino_EO", (123.0, 38.25, 135.0, 39.75), "#dcdcdc"),
             ("ZC1_camino", (9.3, 30.0, 10.7, 35.0), "#dcdcdc")]
    for name, (row, px) in HOUSES.items():
        polys.append(("Jardin_" + name, parcel(row, px), "#d6e6c6"))
        fp = footprint(row, px)
        dx = to_world(row, px, 5.9, 0)[0]
        polys.append(("Camino_" + name, (dx - 0.6, 30.0, dx + 0.6, fp[1]) if row == "N"
                      else (dx - 0.6, fp[3], dx + 0.6, 20.0), "#dcdcdc"))
    lines = []
    for name, (row, px) in HOUSES.items():
        x0, y0, x1, y1 = parcel(row, px)
        lines.append(([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], "#6d7f5f", 0.15, None))
    lines.append(([(0, 15.0), (0, 0), (SITE_W, 0), (SITE_W, SITE_H), (0, SITE_H), (0, 30.0)],
                  C_LIMIT, 0.45, "3,1,0.7,1"))
    lines.append(([(0.5, 25.0), (135.0, 25.0)], "#ffffff", 0.3, "2.5,2"))
    lines.append(([(-7.0, -2.5), (-7.0, 52.5)], "#ffffff", 0.3, "2.5,2"))
    return polys, lines


def build_3d():
    objs = [house_obj(n, r, px) for n, (r, px) in HOUSES.items()]
    objs.append(block_obj("LC1", "3D-LOCAL", LC1, H_LC1, "#f2d2a6", LC1_DOORS, LC1_WINDOWS, "#cfc6b8"))
    objs.append(block_obj("ZC1", "3D-ZONAS-COMUNES", ZC1, H_ZC1, "#c6d8ee", ZC1_DOORS, ZC1_WINDOWS, "#cfc6b8"))
    return objs


def sheet_3d(objs):
    layers = [("3D-SUELO", "Terreno, viales, parcelas y zona verde", True),
              ("3D-EDIFICACIONES", "Viviendas, local y zona común (ordenadas por profundidad)", True),
              ("3D-ROTULOS", "Identificación", True),
              ("P-MARCO", "Marco y cajetín", True), ("P-LEYENDA", "Leyenda y notas", True)]
    sh = Sheet("ICT-01", "Esquema 3D del conjunto", layers)
    polys, lines = ground_items()
    corners = [(-12, -3, 0), (SITE_W, -3, 0), (SITE_W, 53, 0), (-12, 53, 0), (SITE_W, 50, H_RIDGE)]
    us = [proj(p)[0] for p in corners]
    vs = [proj(p)[1] for p in corners]
    k = min(386.0 / (max(us) - min(us)), 178.0 / (max(vs) - min(vs) + 4))
    ox = 17.0 - min(us) * k + (386.0 - (max(us) - min(us)) * k) / 2
    oy = 30.0 + max(vs) * k + 4

    def S(p):
        u, vv = proj(p)
        return (ox + u * k, oy - vv * k)

    def poly_svg(layer, pts, fill, stroke="#333", sw=0.15, dash=None):
        sh.svg[layer].append('<path d="M %s Z"%s/>' % (" L ".join("%.3f,%.3f" % S(p) for p in pts),
                                                       style(fill, stroke, sw, dash)))

    for name, (x0, y0, x1, y1), col in polys:
        pts = [(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)]
        poly_svg("3D-SUELO", pts, col, "#7d7d7d", 0.1)
        sh.dxf.append(("face3d", "3D-SUELO", pts, col))
    for pts, col, sw, dash in lines:
        sh.svg["3D-SUELO"].append('<path d="M %s"%s/>' % (" L ".join("%.3f,%.3f" % S((x, y, 0)) for x, y in pts),
                                                          style("none", col, sw, dash)))
    for o in sorted(objs, key=lambda o: -depth(o.center)):
        g = ['<g id="%s">' % o.name]
        for pts, col, n in o.faces:
            if sum(a * b for a, b in zip(n, VIEWV)) <= 1e-6:
                continue
            g.append('<path d="M %s Z"%s/>' % (" L ".join("%.3f,%.3f" % S(p) for p in pts),
                                                style(shade(col, n), "#2b2b2b", 0.2)))
            for dp, dc, dn in o.decals:
                if sum(a * b for a, b in zip(dn, n)) > 0.99 and abs(
                        sum((dp[0][i] - pts[0][i]) * n[i] for i in range(3))) < 0.1:
                    g.append('<path d="M %s Z"%s/>' % (" L ".join("%.3f,%.3f" % S(p) for p in dp),
                                                        style(shade(dc, dn), "#2b2b2b", 0.08)))
            if getattr(o, "floor_line", False) and abs(n[2]) < 0.1:
                zs = [p[2] for p in pts]
                if max(zs) >= H_EAVE - 1e-6:
                    base = [p for p in pts if p[2] == 0]
                    if len(base) == 2:
                        a, b = base
                        g.append('<path d="M %.3f,%.3f L %.3f,%.3f"%s/>'
                                 % (S((a[0], a[1], H_FLOOR)) + S((b[0], b[1], H_FLOOR))
                                    + (style("none", "#6f6a60", 0.15),)))
        g.append("</g>")
        sh.svg["3D-EDIFICACIONES"].extend(g)
        for pts, col, n in o.faces + o.decals:
            sh.dxf.append(("face3d", o.layer, pts, col))
    # rótulos
    R = "3D-ROTULOS"
    for n, (row, px) in HOUSES.items():
        fp = footprint(row, px)
        x, y = S(((fp[0] + fp[2]) / 2, (fp[1] + fp[3]) / 2, H_RIDGE + 2.6))
        sh.ptext(R, x, y, n, 3.4, weight="bold", halo=True)
        sh.dxf.append(("text", R, ((fp[0] + fp[2]) / 2, (fp[1] + fp[3]) / 2, H_RIDGE + 1.5), n, 1.2,
                       "middle", 0, "#000000"))
    for txt, p, size in (("LC1 · Local comercial", (11.0, 10.0, H_LC1 + 2.2), 3.0),
                         ("ZC1 · Zona común 1", (10.0, 39.0, H_ZC1 + 2.2), 3.0),
                         ("ZC2 · Zona común 2 (zona verde)", (129.0, 35.0, 0.5), 2.6),
                         ("Vial interior", (16.0, 25.0, 0.2), 2.4),
                         ("Vial público", (-7.0, 6.0, 0.2), 2.2),
                         ("Acceso principal", (-1.0, 25.0, 3.0), 2.4)):
        x, y = S(p)
        sh.ptext(R, x, y, txt, size, weight="bold", halo=True)
        sh.dxf.append(("text", R, p, txt, 1.0, "middle", 0, "#000000"))
    # panel
    L = "P-LEYENDA"
    sh.ptext(L, 20, 19, "ESQUEMA 3D DEL CONJUNTO RESIDENCIAL · AXONOMETRÍA", 5.0, anchor="start", weight="bold")
    sh.ptext(L, 20, 26, "Vista desde el suroeste (giro 20°, elevación 35°) · 13 viviendas unifamiliares "
             "aisladas · ZC1 · ZC2 · LC1 · sin escala", 2.6, anchor="start")
    X, Y = 20, 232
    sh.ptext(L, X, Y, "HIPÓTESIS DE DISEÑO (comunes a todos los planos)", 2.8, anchor="start", weight="bold")
    notas = ["• Conjunto 138,00 × 50,00 m · vial interior de 7,00 m con aceras de 1,50 m · acceso desde vial público al oeste.",
             "• Vivienda: 11,00 × 8,00 m, PB + P1 (3,00 m por planta), alero 6,00 m y cumbrera 7,60 m · parcela 14,00 × 18,00 m.",
             "• Separación mínima entre viviendas 3,00 m (cada vivienda es una edificación independiente).",
             "• LC1: 16,00 × 10,00 m, una planta (4,50 m) · ZC1: 12,00 × 8,00 m, una planta (3,80 m) · ZC2: zona verde 14,00 × 18,00 m.",
             "• Modelo editable: ICT_01_Conjunto_3D.obj/.mtl (Blender: Archivo › Importar › Wavefront) y ICT_01_Conjunto_3D.dxf."]
    sh.ptexts(L, X, Y + 7, notas, size=2.35, lead=1.65, anchor="start")
    # flecha de norte proyectada
    a, b = S((0, 0, 0)), S((0, 1, 0))
    north_arrow(sh, 262, 255, r=8, dx=b[0] - a[0], dy=b[1] - a[1])
    sh.ptext(L, 262, 276, "Norte (proyectado)", 2.0)
    frame(sh, "ICT-01", "Esquema 3D del conjunto", "Sin escala", "1/5")
    return sh


def write_obj(objs, path):
    """OBJ en convención Y-arriba (Blender lo convierte a Z-arriba al importar)."""
    polys, _ = ground_items()
    mats = OrderedDict()
    lines, vi = ["# Proyecto ICT UHU - Sesión 1 - Conjunto de 13 viviendas (unidades: metros)",
                 "mtllib " + os.path.basename(path).replace(".obj", ".mtl")], 1

    def emit(name, faces):
        nonlocal vi
        lines.append("o " + name)
        for pts, col in faces:
            m = "mat_" + col.lstrip("#")
            mats[m] = col
            lines.append("usemtl " + m)
            for x, y, z in pts:
                lines.append("v %.4f %.4f %.4f" % (x, z, -y))
            lines.append("f " + " ".join(str(vi + i) for i in range(len(pts))))
            vi += len(pts)

    for i, (name, (x0, y0, x1, y1), col) in enumerate(polys):
        z = 0.005 * min(i, 12)
        emit(name, [([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], col)])
    for o in objs:
        emit(o.name, [(p, c) for p, c, n in o.faces] + [(p, c) for p, c, n in o.decals])
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(path.replace(".obj", ".mtl"), "w", encoding="utf-8") as fh:
        for m, col in mats.items():
            r, g, b = (c / 255.0 for c in hex_rgb(col))
            fh.write("newmtl %s\nKd %.4f %.4f %.4f\nKa 0 0 0\nKs 0 0 0\nd 1\nillum 1\n\n" % (m, r, g, b))


# ============================================================ MAIN
def main():
    os.makedirs(OUT, exist_ok=True)
    dxf_dir = os.path.join(OUT, "DXF")
    m3d = os.path.join(OUT, "3D")
    os.makedirs(dxf_dir, exist_ok=True)
    os.makedirs(m3d, exist_ok=True)
    objs = build_3d()
    sheets = [("ICT_01_Conjunto_3D", sheet_3d(objs)),
              ("ICT_02_Plano_General_2D", general_sheet()),
              ("ICT_03_Vivienda_Planta_Baja", house_sheet("PB", "ICT-03", "3/5")),
              ("ICT_04_Vivienda_Planta_Primera", house_sheet("P1", "ICT-04", "4/5")),
              ("ICT_05_Local_y_Zonas_Comunes", lc_zc_sheet())]
    for fname, sh in sheets:
        sh.write_svg(os.path.join(OUT, fname + ".svg"))
        sh.write_dxf(os.path.join(dxf_dir, fname + ".dxf"))
    write_obj(objs, os.path.join(m3d, "ICT_01_Conjunto_3D.obj"))
    print("OK:", ", ".join(f for f, _ in sheets))


if __name__ == "__main__":
    main()
