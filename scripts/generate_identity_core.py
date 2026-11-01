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

    # Download the current avatar so the SVG carries a fresh snapshot each run.
    avatar_req = urllib.request.Request(avatar_url + ("&" if "?" in avatar_url else "?") + "s=200")
    avatar_req.add_header("User-Agent", "identity-core-generator")
    with urllib.request.urlopen(avatar_req) as r:
        avatar_bytes = r.read()
    avatar_datauri = "data:image/png;base64," + base64.b64encode(avatar_bytes).decode("ascii")

    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    with open(os.path.join(os.path.dirname(__file__), "..", "assets", "identity-core.svg"), "w", encoding="utf-8") as f:
        f.write(TEMPLATE
                .replace("@@AVATAR_DATAURI@@", avatar_datauri)
                .replace("@@REPOS@@", str(repos_count))
                .replace("@@STARS@@", str(stars))
                .replace("@@FOLLOWERS@@", str(followers))
                .replace("@@LOCATION@@", location)
                .replace("@@UPDATED@@", updated))


TEMPLATE = r'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="420" viewBox="0 0 900 420" fill="none" role="img" aria-label="Telvin Crasta — AI Systems Engineer and Full-Stack Developer">
<title>Telvin Crasta — Identity Core</title>
<desc>Auto-generated identity panel. Values refresh via GitHub Actions.</desc>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#05070E"/><stop offset="0.5" stop-color="#080D18"/><stop offset="1" stop-color="#0B0A1A"/></linearGradient>
<radialGradient id="mesh1" cx="0.78" cy="0.48" r="0.58"><stop offset="0" stop-color="#22E7F5" stop-opacity="0.22"/><stop offset="0.5" stop-color="#7C5CFF" stop-opacity="0.10"/><stop offset="1" stop-color="#7C5CFF" stop-opacity="0"/></radialGradient>
<radialGradient id="mesh2" cx="0.14" cy="0.86" r="0.52"><stop offset="0" stop-color="#7C5CFF" stop-opacity="0.18"/><stop offset="1" stop-color="#7C5CFF" stop-opacity="0"/></radialGradient>
<linearGradient id="nameG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.45" stop-color="#8FF0FA"/><stop offset="1" stop-color="#B9A6FF"/></linearGradient>
<linearGradient id="ruleG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#22E7F5"/><stop offset="0.6" stop-color="#7C5CFF" stop-opacity="0.55"/><stop offset="1" stop-color="#7C5CFF" stop-opacity="0"/></linearGradient>
<linearGradient id="coreG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22E7F5"/><stop offset="0.5" stop-color="#7C5CFF"/><stop offset="1" stop-color="#00FF9C"/></linearGradient>
<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="frame"><rect width="900" height="420" rx="18"/></clipPath>
<clipPath id="avatarClip"><circle cx="0" cy="0" r="40"/></clipPath>
</defs>
<g clip-path="url(#frame)">
<rect width="900" height="420" fill="url(#bg)"/>
<rect width="900" height="420" fill="url(#mesh1)"/>
<rect width="900" height="420" fill="url(#mesh2)"/>
<rect x="24" y="24" width="852" height="372" rx="22" fill="#080D18" fill-opacity="0.55" stroke="#22E7F5" stroke-opacity="0.28" stroke-width="1"/>
<text x="48" y="62" fill="#22E7F5" font-size="10" font-weight="700" letter-spacing="4" font-family="Fira Code,monospace">// IDENTITY_CORE · LIVE DATA</text>
<text x="760" y="62" fill="#8B95A7" font-size="9" font-family="Fira Code,monospace" text-anchor="end">UPDATED @@UPDATED@@</text>
<circle cx="832" cy="58" r="4" fill="#00FF9C"/>
<text x="48" y="108" fill="url(#nameG)" font-size="46" font-weight="800" font-family="Segoe UI,Helvetica,sans-serif">Telvin Crasta</text>
<text x="48" y="136" fill="#8B95A7" font-size="13" font-family="Fira Code,monospace">AI Systems Engineer · Full-Stack Developer</text>
<text x="48" y="160" fill="#00FF9C" font-size="11.5" font-family="Fira Code,monospace">&gt; Last-mile AI obsessed · Shipping in public</text>
<rect x="48" y="176" width="360" height="1.5" fill="url(#ruleG)"/>
<rect x="48" y="192" width="84" height="24" rx="5" fill="#0d1117" stroke="#FFB020" stroke-opacity="0.65" stroke-width="0.9"/>
<text x="90" y="208" fill="#FFB020" font-size="10" font-weight="600" text-anchor="middle" font-family="Fira Code,monospace">LegalTech</text>
<rect x="140" y="192" width="86" height="24" rx="5" fill="#0d1117" stroke="#FF4D6D" stroke-opacity="0.65" stroke-width="0.9"/>
<text x="183" y="208" fill="#FF4D6D" font-size="10" font-weight="600" text-anchor="middle" font-family="Fira Code,monospace">Forensics</text>
<rect x="234" y="192" width="80" height="24" rx="5" fill="#0d1117" stroke="#22E7F5" stroke-opacity="0.65" stroke-width="0.9"/>
<text x="274" y="208" fill="#22E7F5" font-size="10" font-weight="600" text-anchor="middle" font-family="Fira Code,monospace">CyberSec</text>
<rect x="322" y="192" width="74" height="24" rx="5" fill="#0d1117" stroke="#7C5CFF" stroke-opacity="0.65" stroke-width="0.9"/>
<text x="359" y="208" fill="#7C5CFF" font-size="10" font-weight="600" text-anchor="middle" font-family="Fira Code,monospace">LLMOps</text>
<rect x="404" y="192" width="68" height="24" rx="5" fill="#0d1117" stroke="#00FF9C" stroke-opacity="0.65" stroke-width="0.9"/>
<text x="438" y="208" fill="#00FF9C" font-size="10" font-weight="600" text-anchor="middle" font-family="Fira Code,monospace">Agents</text>
<rect x="480" y="192" width="52" height="24" rx="5" fill="#0d1117" stroke="#FFB020" stroke-opacity="0.65" stroke-width="0.9"/>
<text x="506" y="208" fill="#FFB020" font-size="10" font-weight="600" text-anchor="middle" font-family="Fira Code,monospace">RAG</text>
<rect x="48" y="232" width="410" height="1" fill="#1F6FEB" fill-opacity="0.35"/>
<g font-family="Fira Code,monospace">
<text x="48" y="258" fill="#22E7F5" font-size="24" font-weight="800">@@REPOS@@</text>
<text x="48" y="274" fill="#8B95A7" font-size="9" letter-spacing="1">REPOS</text>
<text x="118" y="258" fill="#FFB020" font-size="24" font-weight="800">@@STARS@@</text>
<text x="118" y="274" fill="#8B95A7" font-size="9" letter-spacing="1">STARS</text>
<text x="184" y="258" fill="#00FF9C" font-size="24" font-weight="800">@@FOLLOWERS@@</text>
<text x="184" y="274" fill="#8B95A7" font-size="9" letter-spacing="1">FOLLOWERS</text>
<text x="250" y="258" fill="#7C5CFF" font-size="20" font-weight="800">@@LOCATION@@</text>
<text x="250" y="274" fill="#8B95A7" font-size="9" letter-spacing="1">LOCATION</text>
</g>
<g transform="translate(690,210)">
<circle r="150" fill="none" stroke="#22E7F5" stroke-opacity="0.08" stroke-width="1"/>
<circle r="118" fill="none" stroke="#7C5CFF" stroke-opacity="0.12" stroke-width="1"/>
<circle r="86" fill="none" stroke="#22E7F5" stroke-opacity="0.18" stroke-width="1"/>
<circle r="46" fill="#080D18" stroke="url(#coreG)" stroke-width="2" filter="url(#glow)"/>
<image href="@@AVATAR_DATAURI@@" x="-40" y="-40" width="80" height="80" clip-path="url(#avatarClip)" preserveAspectRatio="xMidYMid slice"/>
<circle r="40" fill="none" stroke="#22E7F5" stroke-opacity="0.4" stroke-width="1"/>
<text y="62" fill="#8B95A7" font-size="8" font-family="Fira Code,monospace" text-anchor="middle" letter-spacing="1">PROFILE · LIVE</text>
</g>
<rect x="0.5" y="0.5" width="899" height="419" rx="18" fill="none" stroke="#1F6FEB" stroke-opacity="0.3"/>
</g>
</svg>
'''
if __name__ == "__main__":
    main()
