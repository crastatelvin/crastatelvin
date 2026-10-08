#!/usr/bin/env python3
"""Generate the identity panel used in the profile README.

Run from the repo root:  python3 assets/generate-identity.py

Everything is SMIL animation so it stays live inside GitHub's README image
proxy, with no external fonts or scripts. Every coordinate is derived, so
labels can be re-worded here without hand-placing anything.
"""

import base64
import math
import pathlib
import random

HERE = pathlib.Path(__file__).resolve().parent
AVATAR = HERE / "avatar.jpg"

W, H = 900, 420

CYAN = "#22E7F5"
VIOLET = "#7C5CFF"
GREEN = "#00FF9C"
AMBER = "#FFB020"
ROSE = "#FF4D6D"
ORANGE = "#FF8A4C"

HI = "#EAF6FF"
MID = "#93A7BC"
LO = "#5A6B80"

FONT = "'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "'Fira Code',Consolas,'Liberation Mono',monospace"

CORE = (700, 206)

# the orbit map needs to clear both the panel edge and its own labels,
# which extend past the node by roughly the label width plus a 13px gap
LABEL_PAD = 13
ORBIT_RX = 116
ORBIT_RY = 84
LABEL_MAX = W - 26

DOMAINS = [
    ("RAG", CYAN),
    ("AGENTS", VIOLET),
    ("LLMOPS", AMBER),
    ("FORENSICS", ROSE),
    ("CYBERSEC", GREEN),
    ("LEGALTECH", ORANGE),
]

CHIPS = [
    ("LegalTech", AMBER),
    ("Forensics", ROSE),
    ("CyberSec", GREEN),
    ("LLMOps", VIOLET),
    ("Agents", CYAN),
    ("RAG", AMBER),
]

STATS = [("38", "REPOS", CYAN), ("9+", "STARS", AMBER),
         ("4", "FOLLOWERS", GREEN), ("IND", "LOCATION", VIOLET)]

BOOT = "▸ initializing 6 agents · 38 repos deployed · 0 blockers"

LX_TY = 44  # left text origin, shared by the boot line and its clip

out = []
add = out.append


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def mono_w(s, size, ratio=0.6):
    return len(s) * size * ratio


# ---------------------------------------------------------------- backdrop
rng = random.Random(20261008)

add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" fill="none" role="img" '
    f'aria-label="Telvin Crasta — AI Systems Engineer and Full-Stack Developer">')
add("<title>Telvin Crasta — Identity Core</title>")
add("<desc>Animated identity panel: name, role, domain chips, live stats "
    "and an orbiting system map of the practice areas.</desc>")

add("<defs>")
add('<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#05070E"/>'
    '<stop offset="0.55" stop-color="#080D18"/>'
    '<stop offset="1" stop-color="#0B0A1A"/></linearGradient>')
add('<radialGradient id="neb" cx="0.79" cy="0.5" r="0.62">'
    '<stop offset="0" stop-color="#22E7F5" stop-opacity="0.16"/>'
    '<stop offset="0.45" stop-color="#7C5CFF" stop-opacity="0.08"/>'
    '<stop offset="1" stop-color="#7C5CFF" stop-opacity="0"/></radialGradient>')
add('<radialGradient id="neb2" cx="0.12" cy="0.88" r="0.5">'
    '<stop offset="0" stop-color="#7C5CFF" stop-opacity="0.14"/>'
    '<stop offset="1" stop-color="#7C5CFF" stop-opacity="0"/></radialGradient>')
add('<linearGradient id="nameG" x1="0" y1="0" x2="1" y2="0">'
    '<stop offset="0" stop-color="#FFFFFF"/>'
    '<stop offset="0.45" stop-color="#8FF0FA"/>'
    '<stop offset="1" stop-color="#B9A6FF"/></linearGradient>')
add('<linearGradient id="ruleG" x1="0" y1="0" x2="1" y2="0">'
    f'<stop offset="0" stop-color="{CYAN}"/>'
    '<stop offset="0.6" stop-color="#7C5CFF" stop-opacity="0.5"/>'
    '<stop offset="1" stop-color="#7C5CFF" stop-opacity="0"/></linearGradient>')
# a light vignette only; the portrait is already dark and a heavy wash
# swallows the face
add('<linearGradient id="shade" x1="0.2" y1="0" x2="0.6" y2="1">'
    '<stop offset="0" stop-color="#05070E" stop-opacity="0"/>'
    '<stop offset="0.62" stop-color="#05070E" stop-opacity="0.10"/>'
    '<stop offset="1" stop-color="#05070E" stop-opacity="0.42"/>'
    "</linearGradient>")
add('<radialGradient id="sweep" cx="0.5" cy="0.5" r="0.5">'
    '<stop offset="0" stop-color="#22E7F5" stop-opacity="0.30"/>'
    '<stop offset="1" stop-color="#22E7F5" stop-opacity="0"/></radialGradient>')
add('<linearGradient id="sweepEdge" x1="0" y1="0" x2="1" y2="0">'
    '<stop offset="0" stop-color="#22E7F5" stop-opacity="0.9"/>'
    '<stop offset="1" stop-color="#22E7F5" stop-opacity="0"/></linearGradient>')
add('<filter id="glow" x="-60%" y="-60%" width="220%" height="220%">'
    '<feGaussianBlur stdDeviation="2.2" result="b"/>'
    '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/>'
    "</feMerge></filter>")
add('<filter id="softGlow" x="-70%" y="-70%" width="240%" height="240%">'
    '<feGaussianBlur stdDeviation="5" result="b"/>'
    '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/>'
    "</feMerge></filter>")
add('<filter id="bloom" x="-80%" y="-80%" width="260%" height="260%">'
    '<feGaussianBlur stdDeviation="9"/></filter>')
add('<clipPath id="frame"><rect width="%d" height="%d" rx="18"/></clipPath>'
    % (W, H))

# typing window for the boot line; must span the text's own baseline band
add(f'<clipPath id="typer"><rect x="{LX_TY}" y="318" width="0" height="18">'
    f'<animate attributeName="width" from="0" to="{mono_w(BOOT, 11):.0f}" '
    f'dur="2.6s" begin="1.1s" fill="freeze"/></rect></clipPath>')
add("</defs>")

add('<g clip-path="url(#frame)">')
add(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
add(f'<rect width="{W}" height="{H}" fill="url(#neb)"/>')
add(f'<rect width="{W}" height="{H}" fill="url(#neb2)"/>')

# ---------------------------------------------------------------- starfield
add("<g>")
for _ in range(120):
    x = round(rng.uniform(6, W - 6), 1)
    y = round(rng.uniform(6, H - 6), 1)
    r = round(rng.uniform(0.35, 1.15), 2)
    dur = round(rng.uniform(2.6, 7.5), 2)
    begin = round(rng.uniform(0, 6), 2)
    op = round(rng.uniform(0.10, 0.30), 2)
    hi_ = round(rng.uniform(0.35, 0.85), 2)
    add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#BFE9FF" opacity="{op}">'
        f'<animate attributeName="opacity" values="{op};{hi_};{op}" '
        f'dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></circle>')
add("</g>")

# a few bright sparkles
for _ in range(9):
    x = round(rng.uniform(40, W - 40), 1)
    y = round(rng.uniform(30, H - 30), 1)
    s = round(rng.uniform(3.0, 5.5), 1)
    d = round(rng.uniform(3.2, 6.0), 2)
    add(f'<g opacity="0.55"><path d="M{x} {y - s:.1f}V{y + s:.1f} '
        f'M{x - s:.1f} {y}H{x + s:.1f}" stroke="#CFF6FF" stroke-width="0.7" '
        f'stroke-linecap="round" opacity="0.5">'
        f'<animate attributeName="opacity" values="0.15;0.5;0.15" dur="{d}s" '
        f'repeatCount="indefinite"/></path>'
        f'<circle cx="{x}" cy="{y}" r="1.1" fill="#EAFBFF" opacity="0.85">'
        f'<animate attributeName="opacity" values="0.4;1;0.4" dur="{d}s" '
        f'begin="0.7s" repeatCount="indefinite"/></circle></g>')

# ---------------------------------------------------------------- flow ribbons
RIBBONS = [
    ("M-20 330C150 250 260 380 470 300S760 190 940 250", CYAN, 0.16, 15),
    ("M-20 90C170 150 300 40 520 110S800 200 940 140", VIOLET, 0.14, 19),
]
for d, col, op, dur in RIBBONS:
    add(f'<path d="{d}" stroke="{col}" stroke-opacity="{op}" '
        f'stroke-width="1.1" fill="none" stroke-linecap="round">'
        f'<animate attributeName="stroke-dashoffset" values="0;-400" '
        f'dur="{dur}s" repeatCount="indefinite"/>'
        f'<animate attributeName="stroke-opacity" values="{op};{op * 2.1};{op}" '
        f'dur="{dur / 2:.1f}s" repeatCount="indefinite"/></path>')
    add(f'<path d="{d}" stroke="{col}" stroke-opacity="0.5" '
        f'stroke-width="0.8" fill="none" stroke-dasharray="26 300" '
        f'stroke-linecap="round">'
        f'<animate attributeName="stroke-dashoffset" values="326;0" '
        f'dur="{dur / 3:.1f}s" repeatCount="indefinite"/></path>')

# ---------------------------------------------------------------- frame
add(f'<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="17.5" '
    f'fill="none" stroke="{CYAN}" stroke-opacity="0.16" stroke-width="1.5"/>')
for cx, cy, dx, dy in ((18, 18, 1, 1), (W - 18, 18, -1, 1),
                       (18, H - 18, 1, -1), (W - 18, H - 18, -1, -1)):
    add(f'<path d="M{cx - dx * 22} {cy}H{cx}V{cy + dy * 22}" stroke="{CYAN}" '
        f'stroke-opacity="0.55" stroke-width="1.6" fill="none" '
        f'stroke-linecap="round"/>')

# ---------------------------------------------------------------- left column
LX = 44

add(f'<g opacity="0.95"><rect x="{LX}" y="46" width="3" height="13" rx="1.5" '
    f'fill="{CYAN}" filter="url(#glow)">'
    f'<animate attributeName="opacity" values="1;0.25;1" dur="2.4s" '
    f'repeatCount="indefinite"/></rect>'
    f'<text x="{LX + 12}" y="57" fill="{CYAN}" font-family="{MONO}" '
    f'font-size="12" font-weight="600" letter-spacing="2.6">IDENTITY_CORE'
    f'</text></g>')

add(f'<text x="{LX}" y="112" fill="url(#nameG)" font-family="{FONT}" '
    f'font-size="46" font-weight="700" letter-spacing="-1">'
    f'Telvin Crasta'
    f'<animate attributeName="fill-opacity" values="0.85;1;0.85" '
    f'dur="6s" repeatCount="indefinite"/></text>')

add(f'<rect x="{LX}" y="128" width="330" height="1.6" fill="url(#ruleG)">'
    f'<animate attributeName="width" values="0;330" dur="1s" begin="0.35s" '
    f'fill="freeze"/></rect>')

def mixed_line(x, y, size, lead, parts, sep_col=LO, extra=""):
    """Lay out one monospace line: `lead` glyph, then coloured word groups.

    Groups are separated by a drawn dot rather than a ' · ' string, because
    renderers strip the spaces around a tspan and the gap silently vanishes.
    Every group gets an absolute x; librsvg ignores relative dx on tspans.
    """
    lead_txt, lead_col = lead
    segs = [f'<tspan x="{x}" fill="{lead_col}">{esc(lead_txt)}</tspan>']
    pen = x + mono_w(lead_txt, size) + size * 0.55
    dots = []
    for i, (txt, col) in enumerate(parts):
        if i:
            r = size * 0.12
            gap = size * 2.1
            dots.append(f'<circle cx="{round(pen + gap / 2, 2)}" '
                        f'cy="{round(y - size * 0.31, 2)}" r="{r:.2f}" '
                        f'fill="{sep_col}" fill-opacity="0.8"/>')
            pen += gap
        segs.append(f'<tspan x="{round(pen, 2)}" fill="{col}">{esc(txt)}</tspan>')
        pen += mono_w(txt, size)
    return (f'<text y="{y}" font-family="{MONO}" font-size="{size}"{extra}>'
            f'{"".join(segs)}</text>' + "".join(dots))


add(mixed_line(LX, 156, 13.5, ("", MID),
               [("AI Systems Engineer", MID), ("Full-Stack Developer", MID)]))

add(mixed_line(LX, 182, 12.5, (">", GREEN),
               [("Last-mile AI obsessed", CYAN), ("Shipping in public", CYAN)],
               extra=' filter="url(#glow)"'))

# chips
cx = LX
for i, (label, col) in enumerate(CHIPS):
    w = mono_w(label, 10.5) + 20
    begin = 0.85 + i * 0.09
    add(f'<g opacity="0"><rect x="{cx:.1f}" y="200" width="{w:.1f}" '
        f'height="25" rx="12.5" fill="{col}" fill-opacity="0.09" '
        f'stroke="{col}" stroke-opacity="0.55" stroke-width="1"/>'
        f'<text x="{cx + w / 2:.1f}" y="217" fill="{col}" '
        f'font-family="{MONO}" font-size="10.5" font-weight="600" '
        f'text-anchor="middle">{esc(label)}</text>'
        f'<animate attributeName="opacity" values="0;1" dur="0.35s" '
        f'begin="{begin}s" fill="freeze"/></g>')
    cx += w + 7

# stats
sx = LX
for i, (num, label, col) in enumerate(STATS):
    add(f'<g opacity="0"><text x="{sx}" y="278" fill="{col}" '
        f'font-family="{FONT}" font-size="27" font-weight="700" '
        f'filter="url(#glow)">{num}</text>'
        f'<text x="{sx + 1}" y="294" fill="{LO}" font-family="{MONO}" '
        f'font-size="9" letter-spacing="1.5">{label}</text>'
        f'<animate attributeName="opacity" values="0;1" dur="0.4s" '
        f'begin="{1.5 + i * 0.08}s" fill="freeze"/></g>')
    if i < len(STATS) - 1:
        add(f'<line x1="{sx + 62}" y1="256" x2="{sx + 62}" y2="294" '
            f'stroke="{CYAN}" stroke-opacity="0.14" stroke-width="1"/>')
    sx += 80

add(f'<text x="{LX}" y="330" fill="{MID}" font-family="{MONO}" '
    f'font-size="11" clip-path="url(#typer)">{esc(BOOT)}</text>')
add(f'<rect x="{LX + mono_w(BOOT, 11) + 6:.0f}" y="320" width="7" height="12" '
    f'fill="{CYAN}" opacity="0.9">'
    f'<animate attributeName="opacity" values="0.9;0;0.9" dur="1.05s" '
    f'repeatCount="indefinite"/></rect>')

add(f'<circle cx="{LX + 5}" cy="{362}" r="4" fill="{GREEN}" '
    f'filter="url(#glow)">'
    f'<animate attributeName="r" values="4;6.4;4" dur="2.2s" '
    f'repeatCount="indefinite"/></circle>')
add(f'<text x="{LX + 18}" y="366" fill="{GREEN}" font-family="{MONO}" '
    f'font-size="10.5" letter-spacing="1.4">LIVE · ALL SYSTEMS OPERATIONAL'
    f'</text>')

# ---------------------------------------------------------------- orbit map
cx0, cy0 = CORE

# radar sweep
SWEEP_R = 150
add(f'<g><path d="M{cx0} {cy0}L{cx0 + SWEEP_R} {cy0}'
    f'A{SWEEP_R} {SWEEP_R} 0 0 1 '
    f'{cx0 + SWEEP_R * 0.707:.0f} {cy0 - SWEEP_R * 0.707:.0f}Z" '
    f'fill="url(#sweep)"/>'
    f'<line x1="{cx0}" y1="{cy0}" x2="{cx0 + SWEEP_R}" y2="{cy0}" '
    f'stroke="url(#sweepEdge)" stroke-width="1.2"/>'
    f'<animateTransform attributeName="transform" type="rotate" '
    f'from="0 {cx0} {cy0}" to="360 {cx0} {cy0}" dur="7.5s" '
    f'repeatCount="indefinite"/></g>')

# outer orbit carries the six labelled domain stations; the two inner
# orbits are decoration. Labels stay pinned to their station, so the
# travellers moving along the ring never collide with the type.
OUT_RX, OUT_RY = ORBIT_RX, ORBIT_RY
OUT_ROT = -20

ORBITS = [(OUT_RX, OUT_RY, OUT_ROT), (112, 76, 18), (86, 56, 46)]
for rx, ry, rot in ORBITS:
    per = 2 * math.pi * math.sqrt((rx * rx + ry * ry) / 2)
    add(f'<g transform="rotate({rot} {cx0} {cy0})">'
        f'<ellipse cx="{cx0}" cy="{cy0}" rx="{rx}" ry="{ry}" '
        f'stroke="{CYAN}" stroke-opacity="0.18" stroke-width="1" '
        f'stroke-dasharray="{per * 0.5:.0f} {per * 0.5:.0f}" fill="none">'
        f'<animateTransform attributeName="transform" type="rotate" '
        f'from="0 {cx0} {cy0}" to="360 {cx0} {cy0}" '
        f'dur="{30 + rx / 3:.0f}s" repeatCount="indefinite"/></ellipse></g>')


def on_ring(rx, ry, rot, ang_deg):
    a = math.radians(ang_deg + rot)
    return (cx0 + math.cos(a) * rx, cy0 + math.sin(a) * ry)


# six evenly spread stations; nudged so no label runs off the panel
node_xy = []
for i, (label, col) in enumerate(DOMAINS):
    deg = -90 + i * 60
    x, y = on_ring(OUT_RX, OUT_RY, OUT_ROT, deg)
    w = mono_w(label, 9, 0.62) + 5
    # prefer the label outboard of the node; flip it inboard only if that
    # side has no room, since pulling it back would sit it on the dot
    if x + LABEL_PAD + w <= LABEL_MAX:
        lx, anchor = x + LABEL_PAD, "start"
    elif x - LABEL_PAD - w >= 26:
        lx, anchor = x - LABEL_PAD, "end"
    else:
        lx, anchor = min(x + LABEL_PAD, LABEL_MAX - w), "start"
    node_xy.append((x, y, col, label, lx, anchor))

# spokes from the core to each station
for x, y, col, _, _, _ in node_xy:
    add(f'<line x1="{cx0}" y1="{cy0}" x2="{x:.1f}" y2="{y:.1f}" '
        f'stroke="{col}" stroke-opacity="0.20" stroke-width="1"/>')
    add(f'<line x1="{cx0}" y1="{cy0}" x2="{x:.1f}" y2="{y:.1f}" '
        f'stroke="{col}" stroke-opacity="0.5" stroke-width="1.4" '
        f'stroke-dasharray="3 120">'
        f'<animate attributeName="stroke-dashoffset" values="123;0" '
        f'dur="{2.4 + (x % 7) * 0.2:.1f}s" repeatCount="indefinite"/></line>')

# packets travelling out along each spoke
for i, (x, y, col, _, _, _) in enumerate(node_xy):
    add(f'<circle r="2.6" fill="{col}" filter="url(#glow)">'
        f'<animateMotion dur="{2.4 + i * 0.4:.1f}s" begin="{i * 0.5}s" '
        f'repeatCount="indefinite" '
        f'path="M{cx0} {cy0}L{x:.1f} {y:.1f}"/></circle>')

# stations: fixed node + label
for i, (x, y, col, label, lx, anchor) in enumerate(node_xy):
    add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="#060A12" '
        f'stroke="{col}" stroke-width="1.6"/>')
    add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.1" fill="{col}" '
        f'filter="url(#glow)">'
        f'<animate attributeName="opacity" values="0.5;1;0.5" dur="2s" '
        f'begin="{i * 0.3}s" repeatCount="indefinite"/></circle>')
    add(f'<text x="{lx:.1f}" y="{y + 3.4:.1f}" fill="{col}" '
        f'font-family="{MONO}" font-size="9" letter-spacing="1" '
        f'text-anchor="{anchor}" opacity="0.92">{label}</text>')

# travellers running the outer ring, inside the station dots
ring_path = (f'M{cx0 - OUT_RX} {cy0}a{OUT_RX} {OUT_RY} 0 1 0 '
             f'{2 * OUT_RX} 0a{OUT_RX} {OUT_RY} 0 1 0 {-2 * OUT_RX} 0')
for i, (_, _, col, _, _, _) in enumerate(node_xy):
    add(f'<circle r="2" fill="{col}" fill-opacity="0.75" '
        f'filter="url(#glow)">'
        f'<animateMotion dur="{30 + OUT_RX / 3:.0f}s" begin="{i * 5}s" '
        f'repeatCount="indefinite" path="{ring_path}"/></circle>')

# core: hexagonal portrait, masked to the same shape as the frame
HEX_R = 52
hexpts = []
for k in range(6):
    a = math.radians(60 * k - 90)
    hexpts.append(f"{cx0 + HEX_R * math.cos(a):.1f} {cy0 + HEX_R * math.sin(a):.1f}")
hexpath = "M" + "L".join(hexpts) + "Z"

add(f'<clipPath id="hexclip"><path d="{hexpath}"/></clipPath>')

add(f'<circle cx="{cx0}" cy="{cy0}" r="62" fill="{CYAN}" fill-opacity="0.10" '
    f'filter="url(#bloom)">'
    f'<animate attributeName="fill-opacity" values="0.07;0.17;0.07" dur="4.5s" '
    f'repeatCount="indefinite"/></circle>')

# the portrait, inlined: an SVG referenced through <img> cannot fetch
# external resources, so the bytes have to travel with the file
if AVATAR.exists():
    b64 = base64.b64encode(AVATAR.read_bytes()).decode()
    add(f'<g clip-path="url(#hexclip)">'
        f'<image href="data:image/jpeg;base64,{b64}" '
        f'x="{cx0 - HEX_R:.1f}" y="{cy0 - HEX_R:.1f}" '
        f'width="{HEX_R * 2}" height="{HEX_R * 2}" '
        f'preserveAspectRatio="xMidYMid slice"/>'
        f'<rect x="{cx0 - HEX_R:.1f}" y="{cy0 - HEX_R:.1f}" '
        f'width="{HEX_R * 2}" height="{HEX_R * 2}" fill="url(#shade)"/>'
        f'</g>')
else:
    add(f'<path d="{hexpath}" fill="#070B14"/>')

add(f'<path d="{hexpath}" fill="none" stroke="{VIOLET}" '
    f'stroke-opacity="0.4" stroke-width="1" '
    f'transform="rotate(30 {cx0} {cy0})">'
    f'<animateTransform attributeName="transform" type="rotate" '
    f'from="30 {cx0} {cy0}" to="390 {cx0} {cy0}" dur="24s" '
    f'repeatCount="indefinite"/></path>')
add(f'<path d="{hexpath}" fill="none" stroke="{CYAN}" '
    f'stroke-opacity="0.9" stroke-width="1.8" filter="url(#glow)"/>')
add(f'<path d="{hexpath}" fill="none" stroke="{CYAN}" stroke-opacity="0.55" '
    f'stroke-width="1.4" stroke-dasharray="7 9">'
    f'<animateTransform attributeName="transform" type="rotate" '
    f'from="360 {cx0} {cy0}" to="-360 {cx0} {cy0}" dur="9s" '
    f'repeatCount="indefinite"/></path>')

add(f'<rect x="{cx0 - HEX_R - 9:.1f}" y="{cy0 + HEX_R - 9:.1f}" '
    f'width="{mono_w("TELVIN CRASTA", 7.5) + 16:.0f}" height="17" rx="8.5" '
    f'fill="#070B14" fill-opacity="0.82" stroke="{CYAN}" '
    f'stroke-opacity="0.3" stroke-width="1"/>')
add(f'<text x="{cx0}" y="{cy0 + HEX_R + 3:.1f}" fill="{MID}" '
    f'font-family="{MONO}" font-size="7.5" letter-spacing="2" '
    f'text-anchor="middle">TELVIN CRASTA</text>')

add("</g>")
add("</svg>")

dest = HERE / "identity-core.svg"
dest.write_text("\n".join(out), encoding="utf-8")
print(f"wrote {dest.name}  ({dest.stat().st_size} bytes)"
      f"{'' if AVATAR.exists() else '  [no avatar.jpg: core left empty]'}")
