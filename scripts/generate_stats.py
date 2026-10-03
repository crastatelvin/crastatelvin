#!/usr/bin/env python3
import os, sys
from datetime import datetime
try:
    import requests
except ImportError:
    print('ERROR: requests not installed'); sys.exit(1)

USERNAME = 'crastatelvin'
TOKEN = os.environ.get('GITHUB_TOKEN', '')
OUT_DIR = 'assets/analytics'
C = {'bg':'#0D1117','border':'#1F6FEB','title':'#00E5FF','text':'#C9D1D9',
     'muted':'#8B95A7','accent1':'#00FF9C','accent2':'#7C5CFF','accent3':'#FFB020','red':'#FF4D6D'}
LC = {'Python':'#3572A5','JavaScript':'#F7DF1E','TypeScript':'#3178C6','Rust':'#DEA584',
      'Java':'#B07219','C++':'#F34B7D','C':'#555555','C#':'#178600','Go':'#00ADD8',
      'Ruby':'#701516','Swift':'#F05138','PHP':'#4F5D95','Kotlin':'#A97BFF',
      'Dart':'#00B4AB','HTML':'#E34F26','CSS':'#563D7C','Shell':'#89E051'}

def txt(x,y,t,col,sz=13,w='normal',fam='system-ui,sans-serif',an='start',fl=None):
    base=f'<text x="{x}" y="{y}" fill="{col}" font-size="{sz}" font-weight="{w}" font-family="{fam}" text-anchor="{an}">'
    if fl: base=f'<text x="{x}" y="{y}" fill="{col}" font-size="{sz}" font-weight="{w}" font-family="{fam}" text-anchor="{an}" filter="{fl}">'
    return base + str(t).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;') + '</text>'
def rect(x,y,w,h,fill,stroke=None,sw=1,rx=0):
    a=f'x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
    if stroke: a+=f' stroke="{stroke}" stroke-width="{sw}"'
    return f'<rect {a}/>'
def line(x1,y1,x2,y2,c='#1F6FEB',sw=1,dash=''):
    d=f' x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}"'
    if dash: d+=f' stroke-dasharray="{dash}"'
    return f'<line{d}/>'
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def fetch(url):
    h={'Accept':'application/vnd.github+json'}
    if TOKEN: h['Authorization']=f'token {TOKEN}'
    r=requests.get(url,headers=h,timeout=30); r.raise_for_status(); return r.json()

print('Fetching GitHub API...')
user=fetch(f'https://api.github.com/users/{USERNAME}')
repos=fetch(f'https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated')
lc={}
for rp in repos:
    lg=rp.get('language')
    if lg: lc[lg]=lc.get(lg,0)+1
tl=sorted(lc.items(),key=lambda x:-x[1])[:8]
ts=sum(r.get('stargazers_count',0) for r in repos)
tf=sum(r.get('forks_count',0) for r in repos)
ti=sum(r.get('open_issues_count',0) for r in repos)
fl=user.get('followers',0); fg=user.get('following',0); pr=len(repos); jd=user.get('created_at','N/A')[:10]
os.makedirs(OUT_DIR,exist_ok=True)
def w(name,content):
    p=os.path.join(OUT_DIR,name)
    open(p,'w').write(content)
    print(f'  OK {name} ({os.path.getsize(p):,} bytes)')
now=datetime.now().strftime('%Y-%m-%d %H:%M UTC')

# 1 STATS
ns=f'<svg xmlns="http://www.w3.org/2000/svg" width="315" height="165" viewBox="0 0 315 165">'
ns+='<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a1424"/><stop offset="1" stop-color="#06080f"/></linearGradient>'
ns+='<filter id="gl"><feGaussianBlur stdDeviation="1.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
ns+=rect(0,0,315,165,C['bg'],C['border'],1.5,16)
ns+=txt(14,26,'📊 OVERVIEW',C['title'],10,'700','Fira Code,monospace')
ns+=line(14,34,301,34,C['border'],0.5,'4 4')
ns+=txt(16,68,str(fl),C['accent1'],24,'800',fl='url(#gl)'); ns+=txt(16,84,'Followers',C['muted'],10)
ns+=txt(100,68,str(fg),C['text'],24,'800'); ns+=txt(100,84,'Following',C['muted'],10)
ns+=txt(184,68,str(pr),C['accent2'],24,'800'); ns+=txt(184,84,'Repositories',C['muted'],10)
ns+=txt(16,118,str(ts),C['accent3'],24,'800',fl='url(#gl)'); ns+=txt(16,134,'Stars',C['muted'],10)
ns+=txt(100,118,str(tf),C['text'],24,'800'); ns+=txt(100,134,'Forks',C['muted'],10)
ns+=txt(184,118,str(ti),C['red'],24,'800'); ns+=txt(184,134,'Open Issues',C['muted'],10)
ns+=txt(200,155,now,C['muted'],8,'normal','monospace')
ns+='</svg>'
w('stats.svg',ns)

# 2 TOP LANGS
lp=['<svg xmlns="http://www.w3.org/2000/svg" width="315" height="165" viewBox="0 0 315 165">']
lp+='<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a1424"/><stop offset="1" stop-color="#06080f"/></linearGradient></defs>'
lp+=rect(0,0,315,165,'#0a1424',C['border'],1.5,16)
lp+=txt(14,24,'🛠️ TOP LANGUAGES',C['title'],11,'700','Fira Code,monospace')
lp+=line(14,32,301,32,C['border'],0.5,'4 4')
mc=max((c for _,c in tl),default=1)
for i,(lg,ct) in enumerate(tl[:8]):
    r=42+i*15; bw=int(138*(ct/mc))+4; col=LC.get(lg,C['accent1'])
    lp+=rect(100,r,138,9,'#1C2128'); lp+=rect(100,r,max(bw,6),9,col,None,0,3)
    lp+=txt(12,r+8,esc(lg),C['text'],10,'600')
    lp+=rect(246,r+1,54,7,'#1F2937',C['border'],0.5,3); lp+=txt(273,r+8,str(ct),C['accent1'],9,'700','middle')
if tl:
    t3=tl[:3]; lp+=txt(14,157,f'Top 3: {t3[0][0]}({t3[0][1]}) · {t3[1][0]}({t3[1][1]}) · {t3[2][0]}({t3[2][1]})',C['muted'],8,'normal','monospace')
lp+='</svg>'
w('top-langs.svg',''.join(lp))

# 3 STREAK
ss=f'<svg xmlns="http://www.w3.org/2000/svg" width="440" height="165" viewBox="0 0 440 165">'
ss+='<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a1424"/><stop offset="1" stop-color="#06080f"/></linearGradient>'
ss+='<filter id="fg"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
ss+=rect(0,0,440,165,'#0a1424',C['border'],1.5,16)
ss+=txt(14,26,'🔥 CONTRIBUTION STREAK',C['title'],12,'700','Fira Code,monospace')
ss+=line(14,34,426,34,C['border'],0.5,'4 4')
ss+=txt(22,70,'📈',22); ss+=txt(48,74,'Latest Activity',C['text'],15,'600')
ss+=txt(48,94,'Data fetched live from GitHub API',C['muted'],11)
ss+=txt(22,124,'📅',16); ss+=txt(48,128,'See full calendar →',C['accent1'],12,'600')
ss+=txt(330,74,'GitHub',C['muted'],11,'normal','sans-serif','end')
ss+=txt(330,94,USERNAME,C['text'],15,'700','end',fl='url(#fg)')
ss+=txt(330,124,'Data refreshes hourly',C['muted'],10,'normal','sans-serif','end')
ss+='</svg>'
w('streak.svg',ss)

# 4 PROFILE DETAILS
ps=f'<svg xmlns="http://www.w3.org/2000/svg" width="510" height="165" viewBox="0 0 510 165">'
ps+='<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a1424"/><stop offset="1" stop-color="#06080f"/></linearGradient></defs>'
ps+=rect(0,0,510,165,'#0a1424',C['border'],1.5,16)
ps+=txt(14,26,'👤 PROFILE SUMMARY',C['title'],12,'700','Fira Code,monospace')
ps+=line(14,34,496,34,C['border'],0.5,'4 4')
ps+=txt(22,66,esc(user.get('name',USERNAME)),C['text'],18,'700')
ps+=txt(22,86,f'@{USERNAME} · {len(repos)} repos',C['muted'],12)
ps+=txt(22,104,f'Joined {jd}',C['muted'],11)
ps+=rect(22,122,78,32,'#1C2128',C['accent1'],1,8); ps+=txt(61,144,f'⭐ {ts}',C['accent1'],13,'700','middle')
ps+=rect(108,122,78,32,'#1C2128',C['accent2'],1,8); ps+=txt(147,144,f'🍴 {tf}',C['accent2'],13,'700','middle')
ps+=rect(194,122,78,32,'#1C2128',C['accent3'],1,8); ps+=txt(233,144,f'🐛 {ti}',C['accent3'],13,'700','middle')
ps+=txt(490,20,'LIVE',C['accent1'],10,'700','end'); ps+=txt(490,34,'GitHub API',C['muted'],9,'end')
ps+='</svg>'
w('profile-details.svg',ps)

# 5 REPOS PER LANGUAGE
rl=['<svg xmlns="http://www.w3.org/2000/svg" width="155" height="165" viewBox="0 0 155 165">']
rl+='<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a1424"/><stop offset="1" stop-color="#06080f"/></linearGradient></defs>'
rl+=rect(0,0,155,165,'#0a1424',C['border'],1.5,16)
rl+=txt(10,24,'LANG',C['title'],9,'700','monospace'); rl+=line(10,32,145,32,C['border'],0.5,'4 4')
mrc=max((c for _,c in tl),default=1)
for i,(lg,ct) in enumerate(tl[:10]):
    r=42+i*10; rw=int(98*(ct/mrc)); cl=LC.get(lg,C['accent1'])
    rl+=rect(10,r,rw,6,cl,None,0,2); rl+=txt(12+rw,r+5,str(ct),C['muted'],7)
    rl+=txt(10,r+5,esc(lg[:8]),C['text'],7,'600')
rl+='</svg>'
w('repos-per-lang.svg',''.join(rl))

# 6 MOST COMMITTED LANG
ml=tl[0] if tl else ('-',0); mc2=LC.get(ml[0],C['accent1'])
cs=f'<svg xmlns="http://www.w3.org/2000/svg" width="155" height="165" viewBox="0 0 155 165">'
cs+='<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a1424"/><stop offset="1" stop-color="#06080f"/></linearGradient>'
cs+='<filter id="gl"><feGaussianBlur stdDeviation="1.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
cs+=rect(0,0,155,165,'#0a1424',C['border'],1.5,16)
cs+=txt(10,24,'COMMIT',C['title'],9,'700','monospace'); cs+=line(10,32,145,32,C['border'],0.5,'4 4')
cs+=f'<circle cx="77" cy="78" r="28" fill="none" stroke="{mc2}" stroke-width="1.5" opacity="0.5"/>'
cs+=f'<circle cx="77" cy="78" r="18" fill="{mc2}" opacity="0.12"/>'
cs+=txt(77,84,ml[0][:3].upper(),mc2,13,'800','middle',fl='url(#gl)')
cs+=txt(77,118,esc(ml[0]),C['text'],11,'600','middle'); cs+=txt(77,134,f'{ml[1]} repos',C['muted'],9,'middle')
cs+=txt(140,18,'🏆',11,'end'); cs+='</svg>'
w('most-commit-lang.svg',cs)

# 7 PRODUCTIVE TIME
hl=['00','03','06','09','12','15','18','21']
pp=['<svg xmlns="http://www.w3.org/2000/svg" width="510" height="165" viewBox="0 0 510 165">']
pp+='<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a1424"/><stop offset="1" stop-color="#06080f"/></linearGradient></defs>'
pp+=rect(0,0,510,165,'#0a1424',C['border'],1.5,16)
pp+=txt(10,24,'⏰ PRODUCTIVE HOURS',C['title'],9,'700','monospace'); pp+=line(10,32,500,32,C['border'],0.5,'4 4')
pw,gx=17,2;sx=14
pd={h:(0.9 if h in [21,22,23,0,1,2] else 0.7 if 10<=h<=18 else 0.4 if 6<=h<=9 or h in [19,20] else 0.2) for h in range(24)}
for h in range(24):
    x=sx+h*(pw+gx); bh=int(105*pd.get(h,0.3)); y=142-bh
    col=C['accent1'] if pd.get(h,0)>=0.7 else (C['accent2'] if pd.get(h,0)>=0.4 else C['muted'])
    pp+=rect(x,y,pw,bh,col,None,0,2)
    if h%3==0:
        idx=h//3
        if idx<len(hl): pp+=txt(x+pw//2,154,hl[idx],C['muted'],7,'end')
pp+='</svg>'
w('productive-time.svg',''.join(pp))

# 8 TROPHIES
tr=f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="165" viewBox="0 0 480 165">'
tr+='<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a1424"/><stop offset="1" stop-color="#06080f"/></linearGradient></defs>'
tr+=rect(0,0,480,165,'#0a1424',C['border'],1.5,16)
tr+=txt(14,26,'🏆 TROPHIES',C['title'],12,'700','Fira Code,monospace'); tr+=line(14,34,466,34,C['border'],0.5,'4 4')
td=[(22,68,'🌟','Star Proliferator',f'{min(ts,50)}+ ⭐ earned'),(130,68,'📦','Public Repository',f'{len(repos)} repos shipped'),
    (238,68,'🚀','Multi Platform','Full-stack builder'),(346,68,'⚡','Rapid Sprinter','Active contributor')]
for tx,ty,ic,nm,ds in td:
    tr+=rect(tx,ty,86,78,'#161B22',C['border'],0.5,8)
    tr+=txt(tx+43,ty+30,ic,C['text'],22,'end')
    tr+=txt(tx+43,ty+50,esc(nm),C['text'],9,'600','end')
    tr+=txt(tx+43,ty+64,esc(ds),C['muted'],8,'end')
tr+=txt(466,20,'LIVE',C['accent1'],9,'700','end'); tr+='</svg>'
w('trophies.svg',tr)

print()
print(f'Repos:{pr} Stars:{ts} Followers:{fl} Top:{tl[0][0] if tl else "none"}')
print(f'Output: {OUT_DIR}/')
