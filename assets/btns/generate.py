#!/usr/bin/env python3
"""Generate the contact / demo pill badges used in the profile README.

Run from the repo root:  python3 assets/btns/generate.py

Every pill is measured from its own text content, so labels can be edited
here and re-rendered without hand-tuning widths. Text is real <text>, not
outlined paths, so it stays crisp at any display size.
"""

import pathlib

# monospace advance ratio; exact for the JetBrains Mono / Fira Code / Consolas
# stack the README requests, and a safe approximation for the fallback.
ADVANCE = 0.6

FONT_STACK = "JetBrains Mono, Fira Code, Consolas, monospace"

H = 44
PAD_X = 16
ICON = 20
ICON_GAP = 11
LABEL_SIZE = 13
SUB_SIZE = 11
SEP_GAP = 9
SEP_DOT = 4

BG_TOP = "#1b2434"
BG_BOT = "#0b0f17"
BORDER = "#00E5FF"
LABEL_TEXT = "#e6f7ff"
SUB_TEXT = "#8b95a7"

def text_w(s, size):
    return len(s) * ADVANCE * size

def pill(label, sub, accent, icon):
    lw = text_w(label, LABEL_SIZE)
    sw = text_w(sub, SUB_SIZE)
    width = (PAD_X + ICON + ICON_GAP + lw + SEP_GAP + SEP_DOT
             + SEP_GAP + sw + PAD_X)
    w = round(width, 2)
    cy = H / 2
    lx = PAD_X + ICON + ICON_GAP
    sx = lx + lw + SEP_GAP + SEP_DOT + SEP_GAP
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{H}" viewBox="0 0 {w} {H}" fill="none" role="img" aria-label="{label}: {sub}">
<title>{label} — {sub}</title>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG_TOP}"/><stop offset="1" stop-color="{BG_BOT}"/></linearGradient>
<filter id="glow" x="-40%" y="-60%" width="180%" height="220%"><feGaussianBlur stdDeviation="1.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect x="0.6" y="0.6" width="{round(w - 1.2, 2)}" height="{H - 1.2}" rx="{round(H / 2 - 0.6, 2)}" fill="url(#bg)" stroke="{accent}" stroke-opacity="0.38" stroke-width="1.2"/>
<g transform="translate({PAD_X},{(H - ICON) / 2})" fill="{accent}" color="{accent}" filter="url(#glow)">
{icon}
</g>
<text x="{round(lx, 2)}" y="{round(cy + LABEL_SIZE * 0.36, 2)}" fill="{LABEL_TEXT}" font-family="{FONT_STACK}" font-size="{LABEL_SIZE}" font-weight="700">{label}</text>
<circle cx="{round(sx - SEP_GAP - SEP_DOT / 2, 2)}" cy="{cy}" r="{SEP_DOT / 2}" fill="{accent}" fill-opacity="0.5"/>
<text x="{round(sx, 2)}" y="{round(cy + SUB_SIZE * 0.36, 2)}" fill="{SUB_TEXT}" font-family="{FONT_STACK}" font-size="{SUB_SIZE}">{sub}</text>
</svg>
"""

def icon(body, box=24):
    return f'<g transform="scale({ICON / box:.5f})">{body}</g>'

ICONS = {
    "mail": icon('<path d="M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-2.023 2.309-3.178 3.927-1.964L5.455 4.64 12 9.548l6.545-4.91 1.528-1.145C21.69 2.28 24 3.434 24 5.457z" fill="currentColor"/>'),
    "pin": icon('<path d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z" fill="currentColor"/>'),
    "linkedin": icon('<path d="M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.03-1.85-3.03-1.86 0-2.14 1.45-2.14 2.94v5.66H9.35V9h3.41v1.56h.05a3.74 3.74 0 0 1 3.37-1.85c3.6 0 4.27 2.37 4.27 5.46zM5.34 7.43a2.07 2.07 0 1 1 0-4.14 2.07 2.07 0 0 1 0 4.14zM7.12 20.45H3.55V9h3.57zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z" fill="currentColor"/>'),
    "tool": icon('<path d="M21.7 19.3 13.4 11a5.5 5.5 0 0 0-6.8-6.8l3.3 3.3-2.9 2.9-3.3-3.3a5.5 5.5 0 0 0 6.8 6.8l8.3 8.3a1 1 0 0 0 1.4 0l1.5-1.5a1 1 0 0 0 0-1.4z" fill="currentColor"/>'),
    "doc": icon('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zm0 2.5L17.5 8H14zM8 12h8v1.8H8zm0 3.6h8v1.8H8z" fill="currentColor"/>'),
    "brain": icon('<path d="M12 3a4 4 0 0 0-4 4 3.5 3.5 0 0 0-2 6.2A3.5 3.5 0 0 0 9 19a3 3 0 0 0 3-2 3 3 0 0 0 3 2 3.5 3.5 0 0 0 3-5.8A3.5 3.5 0 0 0 16 7a4 4 0 0 0-4-4zm0 2v14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'),
    "cpu": icon('<path d="M9 2v3H7a2 2 0 0 0-2 2v2H2v2h3v2H2v2h3v2a2 2 0 0 0 2 2h2v3h2v-3h2v3h2v-3h2a2 2 0 0 0 2-2v-2h3v-2h-3v-2h3V9h-3V7a2 2 0 0 0-2-2h-2V2h-2v3h-2V2zm0 5h6a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1zm2 3v4h2v-4z" fill="currentColor"/>'),
}

PILLS = [
    ("mail.svg", "EMAIL", "crastatelvin@gmail.com", BORDER, "mail"),
    ("loc.svg", "LOCATION", "Bengaluru, India", BORDER, "pin"),
    ("linkedin.svg", "LINKEDIN", "Open to work", "#0A66C2", "linkedin"),
    ("forge.svg", "FORGE", "MCP Tool Server", "#7C5CFF", "tool"),
    ("documind.svg", "DOCUMIND", "RAG Document System", "#00FF9C", "doc"),
    ("telvyn.svg", "TELVYN AI", "Hybrid ReAct Agent", "#FF6B6B", "brain"),
    ("onyx.svg", "ONYX", "Edge AI Inference", "#FFB020", "cpu"),
]

out = pathlib.Path(__file__).resolve().parent
for fname, label, sub, accent, ico in PILLS:
    (out / fname).write_text(pill(label, sub, accent, ICONS[ico]), encoding="utf-8")
    print(f"{fname:14} {label} / {sub}")
