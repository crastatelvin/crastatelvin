#!/usr/bin/env python3
"""Regenerate assets/identity-core.svg from live GitHub profile data."""
import base64
import json
import os
import urllib.request
from datetime import datetime, timezone

LOGIN = "crastatelvin"
API = "https://api.github.com"


def api(path):
    req = urllib.request.Request(API + path)
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "identity-core-generator")
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def fetch_repos():
    repos = []
    page = 1
    while True:
        data = api(f"/users/{LOGIN}/repos?per_page=100&page={page}&type=owner")
        if not data:
            break
        repos.extend(data)
        if len(data) < 100:
            break
        page += 1
    return [r for r in repos if not r.get("fork")]


def main():
    user = api(f"/users/{LOGIN}")
    repos = fetch_repos()

    repos_count = user.get("public_repos", len(repos))
    stars = sum(r.get("stargazers_count", 0) for r in repos)
    followers = user.get("followers", 0)
    location = user.get("location") or "IND"
    avatar_url = user.get("avatar_url", f"https://github.com/{LOGIN}.png")

    avatar_req = urllib.request.Request(avatar_url + ("&" if "?" in avatar_url else "?") + "s=256")
    avatar_req.add_header("User-Agent", "identity-core-generator")
    with urllib.request.urlopen(avatar_req) as r:
        avatar_bytes = r.read()
    avatar_datauri = "data:image/png;base64," + base64.b64encode(avatar_bytes).decode("ascii")

    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    out_path = os.path.join(os.path.dirname(__file__), "..", "assets", "identity-core.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(TEMPLATE
                .replace("@@AVATAR_DATAURI@@", avatar_datauri)
                .replace("@@REPOS@@", str(repos_count))
                .replace("@@STARS@@", str(stars))
                .replace("@@FOLLOWERS@@", str(followers))
                .replace("@@LOCATION@@", location)
                .replace("@@UPDATED@@", updated))


TEMPLATE = r'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="420" viewBox="0 0 900 420" fill="none" role="img" aria-label="Telvin Crasta — AI Systems Engineer and Full-Stack Developer">
<title>Telvin Crasta — Identity Core</title>
<desc>Auto-generated, animated identity panel. Values and avatar refresh via the generator script.</desc>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#03050C"/><stop offset="0.5" stop-color="#070B16"/><stop offset="1" stop-color="#0A0714"/></linearGradient>
<radialGradient id="neb1" cx="0.78" cy="0.46" r="0.62"><stop offset="0" stop-color="#22E7F5" stop-opacity="0.26"/><stop offset="0.5" stop-color="#7C5CFF" stop-opacity="0.12"/><stop offset="1" stop-color="#7C5CFF" stop-opacity="0"/></radialGradient>
<radialGradient id="neb2" cx="0.14" cy="0.88" r="0.52"><stop offset="0" stop-color="#7C5CFF" stop-opacity="0.20"/><stop offset="1" stop-color="#7C5CFF" stop-opacity="0"/></radialGradient>
<radialGradient id="neb3" cx="0.42" cy="0.12" r="0.42"><stop offset="0" stop-color="#00FF9C" stop-opacity="0.14"/><stop offset="1" stop-color="#00FF9C" stop-opacity="0"/></radialGradient>
<linearGradient id="nameG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.35" stop-color="#8FF0FA"><animate attributeName="stop-color" values="#8FF0FA;#B9A6FF;#8FF0FA" dur="6s" repeatCount="indefinite"/></stop><stop offset="1" stop-color="#B9A6FF"/></linearGradient>
<linearGradient id="ruleG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#22E7F5"/><stop offset="0.5" stop-color="#7C5CFF"/><stop offset="1" stop-color="#00FF9C" stop-opacity="0"/></linearGradient>
<linearGradient id="coreG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22E7F5"/><stop offset="0.5" stop-color="#7C5CFF"/><stop offset="1" stop-color="#00FF9C"/></linearGradient>
<linearGradient id="waveG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#22E7F5" stop-opacity="0"/><stop offset="0.5" stop-color="#22E7F5" stop-opacity="0.55"/><stop offset="1" stop-color="#7C5CFF" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="2.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="bloom" x="-120%" y="-120%" width="340%" height="340%"><feGaussianBlur stdDeviation="14"/></filter>
<clipPath id="frame"><rect width="900" height="420" rx="18"/></clipPath>
<clipPath id="avatarClip"><circle cx="0" cy="0" r="42"/></clipPath>
</defs>
<g clip-path="url(#frame)">
<rect width="900" height="420" fill="url(#bg)"/>
<rect width="900" height="420" fill="url(#neb1)"><animate attributeName="opacity" values="0.75;1;0.75" dur="7s" repeatCount="indefinite"/></rect>
<rect width="900" height="420" fill="url(#neb2)"><animate attributeName="opacity" values="0.6;0.9;0.6" dur="9s" repeatCount="indefinite"/></rect>
<rect width="900" height="420" fill="url(#neb3)"><animate attributeName="opacity" values="0.5;0.85;0.5" dur="6s" repeatCount="indefinite"/></rect>
<g opacity="0.16" stroke="#1F6FEB" stroke-width="0.6">
<line x1="0" y1="60" x2="900" y2="60"/><line x1="0" y1="120" x2="900" y2="120"/><line x1="0" y1="180" x2="900" y2="180"/><line x1="0" y1="240" x2="900" y2="240"/><line x1="0" y1="300" x2="900" y2="300"/><line x1="0" y1="360" x2="900" y2="360"/>
<line x1="90" y1="0" x2="90" y2="420"/><line x1="180" y1="0" x2="180" y2="420"/><line x1="270" y1="0" x2="270" y2="420"/><line x1="360" y1="0" x2="360" y2="420"/><line x1="450" y1="0" x2="450" y2="420"/><line x1="540" y1="0" x2="540" y2="420"/><line x1="630" y1="0" x2="630" y2="420"/><line x1="720" y1="0" x2="720" y2="420"/><line x1="810" y1="0" x2="810" y2="420"/>
</g>
<g opacity="0.9">
<path d="M0,300 C150,260 300,340 450,300 S750,260 900,300" fill="none" stroke="url(#waveG)" stroke-width="2.2">
<animate attributeName="d" dur="8s" repeatCount="indefinite" values="M0,300 C150,260 300,340 450,300 S750,260 900,300;M0,300 C150,340 300,260 450,300 S750,340 900,300;M0,300 C150,260 300,340 450,300 S750,260 900,300"/>
<animate attributeName="stroke-dashoffset" from="0" to="-180" dur="6s" repeatCount="indefinite"/>
</path>
<path d="M0,330 C150,290 300,370 450,330 S750,290 900,330" fill="none" stroke="url(#waveG)" stroke-width="1.4" opacity="0.5">
<animate attributeName="d" dur="10s" repeatCount="indefinite" values="M0,330 C150,290 300,370 450,330 S750,290 900,330;M0,330 C150,370 300,290 450,330 S750,370 900,330;M0,330 C150,290 300,370 450,330 S750,290 900,330"/>
</path>
</g>
<g>
<circle cx="120" cy="90" r="1.3" fill="#BFE9FF" opacity="0.4"><animate attributeName="cy" values="90;84;90" dur="4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.2;0.7;0.2" dur="4s" repeatCount="indefinite"/></circle>
<circle cx="760" cy="70" r="1.0" fill="#BFE9FF" opacity="0.35"><animate attributeName="cy" values="70;76;70" dur="5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.15;0.6;0.15" dur="5s" repeatCount="indefinite"/></circle>
<circle cx="820" cy="330" r="1.2" fill="#BFE9FF" opacity="0.35"><animate attributeName="cy" values="330;324;330" dur="4.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.15;0.65;0.15" dur="4.5s" repeatCount="indefinite"/></circle>
<circle cx="60" cy="360" r="1.1" fill="#BFE9FF" opacity="0.3"><animate attributeName="cy" values="360;354;360" dur="4.8s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.15;0.55;0.15" dur="4.8s" repeatCount="indefinite"/></circle>
<circle cx="430" cy="40" r="0.9" fill="#BFE9FF" opacity="0.3"><animate attributeName="cy" values="40;46;40" dur="6s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.1;0.5;0.1" dur="6s" repeatCount="indefinite"/></circle>
<circle cx="500" cy="390" r="1.0" fill="#BFE9FF" opacity="0.3"><animate attributeName="cy" values="390;384;390" dur="5.2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.1;0.5;0.1" dur="5.2s" repeatCount="indefinite"/></circle>
</g>
<rect x="24" y="24" width="852" height="372" rx="22" fill="#080D18" fill-opacity="0.52" stroke="#22E7F5" stroke-opacity="0.30" stroke-width="1"/>
<rect x="24" y="24" width="852" height="372" rx="22" fill="none" stroke="#7C5CFF" stroke-opacity="0.14" stroke-width="1"/>
<g>
<rect x="44" y="46" width="12" height="12" rx="2" fill="none" stroke="#22E7F5" stroke-opacity="0.75" stroke-width="1.2"><animate attributeName="stroke-opacity" values="0.4;0.9;0.4" dur="2.4s" repeatCount="indefinite"/></rect>
<rect x="844" y="46" width="12" height="12" rx="2" fill="none" stroke="#7C5CFF" stroke-opacity="0.75" stroke-width="1.2"><animate attributeName="stroke-opacity" values="0.4;0.9;0.4" dur="2.8s" repeatCount="indefinite"/></rect>
<rect x="44" y="362" width="12" height="12" rx="2" fill="none" stroke="#7C5CFF" stroke-opacity="0.75" stroke-width="1.2"><animate attributeName="stroke-opacity" values="0.4;0.9;0.4" dur="3.1s" repeatCount="indefinite"/></rect>
<rect x="844" y="362" width="12" height="12" rx="2" fill="none" stroke="#00FF9C" stroke-opacity="0.75" stroke-width="1.2"><animate attributeName="stroke-opacity" values="0.4;0.9;0.4" dur="2.6s" repeatCount="indefinite"/></rect>
</g>
<text x="48" y="62" fill="#22E7F5" font-size="10" font-weight="700" letter-spacing="4" font-family="Fira Code,monospace">// IDENTITY_CORE · LIVE DATA</text>
<text x="760" y="62" fill="#8B95A7" font-size="9" font-family="Fira Code,monospace" text-anchor="end">UPDATED @@UPDATED@@</text>
<circle cx="832" cy="58" r="4" fill="#00FF9C"><animate attributeName="r" values="3;5.5;3" dur="1.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.6;1;0.6" dur="1.6s" repeatCount="indefinite"/></circle>
<text x="48" y="108" fill="url(#nameG)" font-size="46" font-weight="800" font-family="Segoe UI,Helvetica,sans-serif">Telvin Crasta</text>
<text x="48" y="136" fill="#8B95A7" font-size="13" font-family="Fira Code,monospace">AI Systems Engineer · Full-Stack Developer</text>
<text x="48" y="160" fill="#00FF9C" font-size="11.5" font-family="Fira Code,monospace">&gt; Last-mile AI obsessed · Shipping in public</text>
<rect x="48" y="176" width="360" height="1.5" fill="url(#ruleG)"><animate attributeName="width" values="360;390;360" dur="4s" repeatCount="indefinite"/></rect>
<g>
<rect x="48" y="192" width="84" height="24" rx="5" fill="#0d1117" stroke="#FFB020" stroke-opacity="0.65" stroke-width="0.9"><animate attributeName="stroke-opacity" values="0.4;0.9;0.4" dur="2.2s" repeatCount="indefinite"/></rect>
<text x="90" y="208" fill="#FFB020" font-size="10" font-weight="600" text-anchor="middle" font-family="Fira Code,monospace">LegalTech</text>
<rect x="140" y="192" width="86" height="24" rx="5" fill="#0d1117" stroke="#FF4D6D" stroke-opacity="0.65" stroke-width="0.9"><animate attributeName="stroke-opacity" values="0.4;0.9;0.4" dur="2.6s" repeatCount="indefinite"/></rect>
<text x="183" y="208" fill="#FF4D6D" font-size="10" font-weight="600" text-anchor="middle" font-family="Fira Code,monospace">Forensics</text>
<rect x="234" y="192" width="80" height="24" rx="5" fill="#0d1117" stroke="#22E7F5" stroke-opacity="0.65" stroke-width="0.9"><animate attributeName="stroke-opacity" values="0.4;0.9;0.4" dur="3.0s" repeatCount="indefinite"/></rect>
<text x="274" y="208" fill="#22E7F5" font-size="10" font-weight="600" text-anchor="middle" font-family="Fira Code,monospace">CyberSec</text>
<rect x="322" y="192" width="74" height="24" rx="5" fill="#0d1117" stroke="#7C5CFF" stroke-opacity="0.65" stroke-width="0.9"><animate attributeName="stroke-opacity" values="0.4;0.9;0.4" dur="2.4s" repeatCount="indefinite"/></rect>
<text x="359" y="208" fill="#7C5CFF" font-size="10" font-weight="600" text-anchor="middle" font-family="Fira Code,monospace">LLMOps</text>
<rect x="404" y="192" width="68" height="24" rx="5" fill="#0d1117" stroke="#00FF9C" stroke-opacity="0.65" stroke-width="0.9"><animate attributeName="stroke-opacity" values="0.4;0.9;0.4" dur="2.8s" repeatCount="indefinite"/></rect>
<text x="438" y="208" fill="#00FF9C" font-size="10" font-weight="600" text-anchor="middle" font-family="Fira Code,monospace">Agents</text>
<rect x="480" y="192" width="52" height="24" rx="5" fill="#0d1117" stroke="#FFB020" stroke-opacity="0.65" stroke-width="0.9"><animate attributeName="stroke-opacity" values="0.4;0.9;0.4" dur="3.2s" repeatCount="indefinite"/></rect>
<text x="506" y="208" fill="#FFB020" font-size="10" font-weight="600" text-anchor="middle" font-family="Fira Code,monospace">RAG</text>
</g>
<rect x="48" y="232" width="410" height="1" fill="#1F6FEB" fill-opacity="0.35"/>
<g font-family="Fira Code,monospace">
<text x="48" y="258" fill="#22E7F5" font-size="24" font-weight="800">@@REPOS@@</text><animate attributeName="opacity" values="0.85;1;0.85" dur="3s" repeatCount="indefinite"/>
<text x="48" y="274" fill="#8B95A7" font-size="9" letter-spacing="1">REPOS</text>
<text x="118" y="258" fill="#FFB020" font-size="24" font-weight="800">@@STARS@@</text>
<text x="118" y="274" fill="#8B95A7" font-size="9" letter-spacing="1">STARS</text>
<text x="184" y="258" fill="#00FF9C" font-size="24" font-weight="800">@@FOLLOWERS@@</text>
<text x="184" y="274" fill="#8B95A7" font-size="9" letter-spacing="1">FOLLOWERS</text>
<text x="250" y="258" fill="#7C5CFF" font-size="20" font-weight="800">@@LOCATION@@</text>
<text x="250" y="274" fill="#8B95A7" font-size="9" letter-spacing="1">LOCATION</text>
</g>
<g font-family="Fira Code,monospace" font-size="9">
<text x="48" y="300" fill="#8B95A7">Shipping production-grade AI-native products · multi-agent pipelines to live dashboards</text>
<text x="48" y="322" fill="#8B95A7" opacity="0">> booting identity core...<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="0.2s" fill="freeze"/></text>
<text x="48" y="336" fill="#22E7F5" opacity="0">> loading agent graph...<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="0.9s" fill="freeze"/></text>
<text x="48" y="350" fill="#00FF9C" opacity="0">> connecting MCP servers...<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="1.6s" fill="freeze"/></text>
<text x="48" y="364" fill="#FFB020" opacity="0">> all systems nominal ✓<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="2.3s" fill="freeze"/></text>
</g>
<g transform="translate(690,210)">
<circle r="150" fill="none" stroke="#22E7F5" stroke-opacity="0.08" stroke-width="1"><animate attributeName="stroke-opacity" values="0.05;0.12;0.05" dur="4s" repeatCount="indefinite"/></circle>
<circle r="118" fill="none" stroke="#7C5CFF" stroke-opacity="0.12" stroke-width="1"/>
<circle r="86" fill="none" stroke="#22E7F5" stroke-opacity="0.18" stroke-width="1"/>
<g>
<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="20s" repeatCount="indefinite"/>
<circle cx="150" cy="0" r="3.2" fill="#22E7F5" filter="url(#glow)"><animate attributeName="r" values="2.6;4;2.6" dur="2.4s" repeatCount="indefinite"/></circle>
<circle cx="-150" cy="0" r="3.2" fill="#7C5CFF" filter="url(#glow)"><animate attributeName="r" values="2.6;4;2.6" dur="2.8s" repeatCount="indefinite"/></circle>
<circle cx="0" cy="150" r="3.2" fill="#00FF9C" filter="url(#glow)"><animate attributeName="r" values="2.6;4;2.6" dur="2.2s" repeatCount="indefinite"/></circle>
<circle cx="0" cy="-150" r="3.2" fill="#FFB020" filter="url(#glow)"><animate attributeName="r" values="2.6;4;2.6" dur="3s" repeatCount="indefinite"/></circle>
</g>
<g>
<animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="13s" repeatCount="indefinite"/>
<circle cx="118" cy="0" r="2.6" fill="#7C5CFF"/>
<circle cx="-118" cy="0" r="2.6" fill="#22E7F5"/>
<circle cx="0" cy="118" r="2.6" fill="#FF4D6D"/>
<circle cx="0" cy="-118" r="2.6" fill="#00FF9C"/>
</g>
<g>
<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="8s" repeatCount="indefinite"/>
<circle cx="86" cy="0" r="2" fill="#22E7F5"/>
<circle cx="-86" cy="0" r="2" fill="#7C5CFF"/>
<circle cx="0" cy="86" r="2" fill="#FFB020"/>
<circle cx="0" cy="-86" r="2" fill="#00FF9C"/>
</g>
<g>
<line x1="0" y1="0" x2="132" y2="-90" stroke="#22E7F5" stroke-opacity="0.28" stroke-width="0.9" stroke-dasharray="4 6"><animate attributeName="stroke-dashoffset" from="0" to="-50" dur="2.6s" repeatCount="indefinite"/></line>
<line x1="0" y1="0" x2="140" y2="40" stroke="#7C5CFF" stroke-opacity="0.28" stroke-width="0.9" stroke-dasharray="4 6"><animate attributeName="stroke-dashoffset" from="0" to="-50" dur="3s" repeatCount="indefinite"/></line>
<line x1="0" y1="0" x2="-120" y2="95" stroke="#00FF9C" stroke-opacity="0.28" stroke-width="0.9" stroke-dasharray="4 6"><animate attributeName="stroke-dashoffset" from="0" to="-50" dur="3.4s" repeatCount="indefinite"/></line>
<line x1="0" y1="0" x2="-135" y2="-60" stroke="#FFB020" stroke-opacity="0.28" stroke-width="0.9" stroke-dasharray="4 6"><animate attributeName="stroke-dashoffset" from="0" to="-50" dur="2.8s" repeatCount="indefinite"/></line>
</g>
<circle r="46" fill="#080D18" stroke="url(#coreG)" stroke-width="2" filter="url(#glow)"/>
<circle r="42" fill="none" stroke="#22E7F5" stroke-opacity="0.35" stroke-width="1"><animate attributeName="r" values="40;44;40" dur="3s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values="0.2;0.5;0.2" dur="3s" repeatCount="indefinite"/></circle>
<image href="@@AVATAR_DATAURI@@" x="-42" y="-42" width="84" height="84" clip-path="url(#avatarClip)" preserveAspectRatio="xMidYMid slice"/>
<text y="64" fill="#8B95A7" font-size="8" font-family="Fira Code,monospace" text-anchor="middle" letter-spacing="1">PROFILE · LIVE</text>
<g font-family="Fira Code,monospace" font-size="9" font-weight="600">
<text x="150" y="-82" fill="#22E7F5" text-anchor="middle">AI</text>
<text x="175" y="20" fill="#7C5CFF" text-anchor="middle">AGENTS</text>
<text x="150" y="100" fill="#00FF9C" text-anchor="middle">RAG</text>
<text x="40" y="150" fill="#FFB020" text-anchor="middle">LLMOps</text>
<text x="-55" y="145" fill="#FF4D6D" text-anchor="middle">FORENSICS</text>
<text x="-170" y="20" fill="#22E7F5" text-anchor="middle">LEGALTECH</text>
<text x="-150" y="-90" fill="#7C5CFF" text-anchor="middle">MCP</text>
<text x="-40" y="-150" fill="#00FF9C" text-anchor="middle">FULL-STACK</text>
</g>
</g>
<g font-family="Fira Code,monospace" font-size="9">
<rect x="560" y="46" width="118" height="20" rx="4" fill="#0d1117" stroke="#22E7F5" stroke-opacity="0.4" stroke-width="0.8"><animate attributeName="stroke-opacity" values="0.25;0.7;0.25" dur="2.4s" repeatCount="indefinite"/></rect>
<text x="619" y="60" fill="#22E7F5" text-anchor="middle">NEURAL · AGENTIC</text>
<rect x="686" y="46" width="104" height="20" rx="4" fill="#0d1117" stroke="#7C5CFF" stroke-opacity="0.4" stroke-width="0.8"><animate attributeName="stroke-opacity" values="0.25;0.7;0.25" dur="2.8s" repeatCount="indefinite"/></rect>
<text x="738" y="60" fill="#7C5CFF" text-anchor="middle">REALTIME · LIVE</text>
</g>
<circle cx="336" cy="360" r="4" fill="#00FF9C"><animate attributeName="r" values="3;5.5;3" dur="1.8s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.6;1;0.6" dur="1.8s" repeatCount="indefinite"/></circle>
<text x="348" y="364" fill="#00FF9C" font-size="9" font-family="Fira Code,monospace">LIVE · ALL SYSTEMS OPERATIONAL</text>
<rect x="0.5" y="0.5" width="899" height="419" rx="18" fill="none" stroke="#1F6FEB" stroke-opacity="0.3"/>
</g>
</svg>
'''
if __name__ == "__main__":
    main()
