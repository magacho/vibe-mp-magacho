#!/usr/bin/env python3
"""
render-deck.py — turn a codebase-360 findings JSON into a single Bemobi-branded
HTML presentation that spans multiple analysis sections (AI/token, maintenance,
code reuse, visual-component reuse, ...).

Follows the `html-presentation` + `bemobi-brand` skill conventions (Poppins,
brand palette, inline horizontal logo, keyboard navigation).

Usage:
    python3 render-deck.py findings.json [output.html]

Schema (all optional except sections[].findings[]):
{
  "project": "Bemobi Teams", "scope": "Repo (src/)", "date": "YYYY-MM-DD",
  "stats": {"documents": 0, "symbols": 0, "tokens": 0},
  "scorecard": [{"dimension": "AI / Token", "grade": "C", "headline": "…"}],
  "sections": [
    {"key": "ai", "title": "AI / Eficiência de Token", "color": "#062EED",
     "icon": "🤖", "summary": "…",
     "findings": [
       {"id": "AI1", "title": "…", "priority": "HIGH|MEDIUM|LOW",
        "problem": "…", "evidence_cmd": "scip-query …",
        "context_cost": "…", "suggestion": "…",
        "options": [{"kind": "Conservadora", "desc": "…", "saves": "…", "risk": "baixo"}],
        "risk_impact": "…", "gain": "…"}]}
  ],
  "not_recommended": ["…"]
}
"""
import sys, os, json, glob, html


def load_logo():
    cache = os.path.expanduser(
        '~/.claude/plugins/cache/bemobi-marketplace/bemobi-skills')
    hits = sorted(glob.glob(
        f'{cache}/*/skills/bemobi-brand/assets/logos/logo-horizontal-black.svg'))
    for h in reversed(hits):
        try:
            return open(h, encoding='utf-8').read()
        except OSError:
            continue
    return '<span style="font-weight:800;color:#0B1B73;font-size:1.1rem">bemobi</span>'


LOGO_SVG = load_logo()
PRIORITY_COLOR = {'HIGH': '#062EED', 'MEDIUM': '#027BFF', 'MED': '#027BFF', 'LOW': '#5561A6'}
GRADE_COLOR = {'A': '#16A34A', 'B': '#16A34A', 'C': '#027BFF', 'D': '#E8852B', 'F': '#DC2626'}


def esc(x):
    return html.escape(str(x if x is not None else ''))


def brand_bar(tag):
    return (f'<div class="brand-bar"><span class="logo">{LOGO_SVG}</span>'
            f'<div class="brand-sep"></div><span class="brand-tag">{esc(tag)}</span></div>')


# ------------------------------------------------------------------- slides
def slide_title(d):
    stats = d.get('stats', {})
    nfind = sum(len(s.get('findings', [])) for s in d.get('sections', []))
    kpis = [('Documentos', stats.get('documents', '—')),
            ('Símbolos', stats.get('symbols', '—')),
            ('Dimensões', len(d.get('sections', []))),
            ('Achados', nfind)]
    cards = ''.join(f'<div class="kpi"><div class="kpi-v">{esc(v)}</div>'
                    f'<div class="kpi-l">{esc(l)}</div></div>' for l, v in kpis)
    return ('<div class="slide" style="background:#fff;position:relative;overflow:hidden">'
            '<div class="title-accent"></div><div class="title-body">'
            f'<span class="logo title-logo">{LOGO_SVG}</span>'
            f'<div class="eyebrow">{esc(d.get("project","Projeto"))} · {esc(d.get("scope",""))}</div>'
            '<h1>Codebase 360<br><em>raio-x para desenvolvimento com IA</em></h1>'
            f'<div class="subtitle">{esc(d.get("date",""))}</div>'
            f'<div class="kpi-row">{cards}</div></div></div>')


def slide_scorecard(d):
    cards = d.get('scorecard', [])
    if not cards:
        return ''
    cells = ''
    for c in cards:
        g = str(c.get('grade', '—')).upper()[:1]
        col = GRADE_COLOR.get(g, '#5561A6')
        cells += ('<div class="score-card">'
                  f'<div class="score-grade" style="color:{col};border-color:{col}">{esc(c.get("grade","—"))}</div>'
                  f'<div class="score-dim">{esc(c.get("dimension",""))}</div>'
                  f'<div class="score-head">{esc(c.get("headline",""))}</div></div>')
    return ('<div class="slide">' + brand_bar(f'{d.get("project","")} · Codebase 360')
            + '<div class="slide-hdr"><div class="slide-hdr-accent" style="background:#6924E1"></div>'
            '<div class="slide-hdr-text"><div class="slide-eyebrow" style="color:#6924E1">PANORAMA GERAL</div>'
            '<h2 class="slide-title">Scorecard por dimensão</h2></div></div>'
            f'<div class="slide-body"><div class="score-grid">{cells}</div></div></div>')


def slide_section_divider(s):
    color = s.get('color', '#062EED')
    return ('<div class="slide section-divider" '
            f'style="background:linear-gradient(135deg,{color},#6924E1)">'
            f'<div class="logo div-logo">{LOGO_SVG}</div>'
            f'<div class="div-icon">{esc(s.get("icon",""))}</div>'
            f'<h2 class="div-title">{esc(s.get("title",""))}</h2>'
            f'<p class="div-summary">{esc(s.get("summary",""))}</p>'
            f'<div class="div-count">{(lambda k: f"{k} achado" if k == 1 else f"{k} achados")(len(s.get("findings", [])))}</div></div>')


def slide_finding(d, s, f):
    color = PRIORITY_COLOR.get(str(f.get('priority', '')).upper(), '#5561A6')
    def render_opt(o):
        pr = ('<div class="opt-prompt"><span class="opt-prompt-lbl">Prompt p/ implementar</span>'
              f'<code>{esc(o.get("prompt",""))}</code></div>') if o.get('prompt') else ''
        return ('<div class="opt"><div class="opt-head">'
                f'<span class="opt-kind">{esc(o.get("kind",""))}</span>'
                f'<span class="opt-meta">poupa {esc(o.get("saves","—"))} · risco {esc(o.get("risk","—"))}</span></div>'
                f'<div class="opt-desc">{esc(o.get("desc",""))}</div>{pr}</div>')
    opts = ''.join(render_opt(o) for o in f.get('options', []))
    ev = f'<code class="cmd">{esc(f.get("evidence_cmd",""))}</code>' if f.get('evidence_cmd') else ''
    cost = (f'<div class="block cost"><span class="lbl">Custo de contexto / token</span>'
            f'<p>{esc(f.get("context_cost",""))}</p></div>') if f.get('context_cost') else ''
    est = ''
    e = f.get('estimate')
    if e and e.get('rows'):
        erows = ''.join('<tr>'
                        f'<td class="act">{esc(r.get("change",""))}</td>'
                        f'<td>{esc(r.get("before",""))}</td>'
                        f'<td>{esc(r.get("after",""))}</td>'
                        f'<td class="saved">{esc(r.get("saved",""))}</td>'
                        f'<td>{esc(r.get("pct",""))}</td></tr>'
                        for r in e.get('rows', []))
        cap = (f'<p class="est-cap">{esc(e.get("caption",""))}</p>') if e.get('caption') else ''
        est = ('<div class="block est"><span class="lbl">Economia estimada de tokens por change</span>'
               '<table class="exec-tbl est-tbl"><thead><tr>'
               '<th>Change</th><th>Antes</th><th>Depois (est.)</th><th>Economia</th><th>%</th>'
               f'</tr></thead><tbody>{erows}</tbody></table>{cap}</div>')
    optblock = (f'<div class="block"><span class="lbl">Avaliação de soluções</span>'
                f'<div class="opts">{opts}</div></div>') if opts else ''
    return ('<div class="slide">' + brand_bar(f'{d.get("project","")} · {esc(s.get("title",""))}')
            + '<div class="slide-hdr">'
            f'<div class="slide-hdr-accent" style="background:{color}"></div>'
            '<div class="slide-hdr-text">'
            f'<div class="slide-eyebrow" style="color:{color}">{esc(s.get("icon",""))} {esc(f.get("id",""))} · PRIORIDADE {esc(f.get("priority",""))}</div>'
            f'<h2 class="slide-title">{esc(f.get("title",""))}</h2></div>'
            f'<div class="slide-meta"><span class="pill" style="background:{color}">{esc(f.get("priority",""))}</span></div></div>'
            '<div class="slide-body">'
            f'<div class="block"><span class="lbl">Problema</span><p>{esc(f.get("problem",""))} {ev}</p></div>'
            f'{cost}'
            f'{est}'
            f'<div class="block"><span class="lbl">Sugestão</span><p>{esc(f.get("suggestion",""))}</p></div>'
            f'{optblock}'
            f'<div class="block risk"><span class="lbl">Risco &amp; impacto</span><p>{esc(f.get("risk_impact",""))}</p></div>'
            f'<div class="block gain"><span class="lbl">Ganho estimado</span><p>{esc(f.get("gain",""))}</p></div>'
            '</div></div>')


SEV = {
    'nenhum': ('rgba(22,163,74,.12)', '#16A34A'), 'baixo': ('rgba(22,163,74,.12)', '#16A34A'),
    'baixa': ('rgba(22,163,74,.12)', '#16A34A'),
    'médio': ('rgba(232,133,43,.16)', '#B45309'), 'medio': ('rgba(232,133,43,.16)', '#B45309'),
    'média': ('rgba(232,133,43,.16)', '#B45309'),
    'alto': ('rgba(220,38,38,.12)', '#DC2626'), 'alta': ('rgba(220,38,38,.12)', '#DC2626'),
}


def sev_pill(v):
    key = str(v or '').strip().lower().split()[0] if v else ''
    bg, fg = SEV.get(key, ('var(--pale)', 'var(--muted)'))
    return f'<span class="sev" style="background:{bg};color:{fg}">{esc(v)}</span>'


def slide_exec_summary(d):
    ex = d.get('exec_summary')
    if not ex:
        return ''
    rows = ex.get('rows', [])
    if not rows:
        return ''
    intro = (f'<div class="exec-intro">{esc(ex.get("intro",""))}</div>') if ex.get('intro') else ''
    # group rows by dimension, preserving first-seen order
    order, groups = [], {}
    for r in rows:
        dim = r.get('dim', '—')
        if dim not in groups:
            groups[dim] = []
            order.append(dim)
        groups[dim].append(r)
    has_rule = any(r.get('rule') for r in rows)
    ncol = 6 if has_rule else 5
    body = ''
    for dim in order:
        body += f'<tr class="grp"><td colspan="{ncol}">{esc(dim)}</td></tr>'
        for r in groups[dim]:
            col = PRIORITY_COLOR.get(str(r.get('priority', '')).upper(), '#5561A6')
            done = '<span class="exec-done">FEITO</span>' if r.get('status') else ''
            aid = (f'<span class="aid" style="background:{col}">{esc(r.get("id",""))}</span>'
                   if r.get('id') else '')
            rulecell = f'<td class="rule">{esc(r.get("rule",""))}</td>' if has_rule else ''
            body += ('<tr>'
                     f'<td class="act">{aid}{esc(r.get("action",""))}{done}</td>'
                     f'<td>{sev_pill(r.get("effort"))}</td>'
                     f'<td>{sev_pill(r.get("ops"))}</td>'
                     f'<td>{sev_pill(r.get("change"))}</td>'
                     f'<td class="gaincell">{esc(r.get("gain",""))}</td>'
                     f'{rulecell}'
                     '</tr>')
    rule_th = '<th>Regra de ouro (CLAUDE.md)</th>' if has_rule else ''
    return ('<div class="slide">' + brand_bar(f'{d.get("project","")} · Codebase 360')
            + '<div class="slide-hdr"><div class="slide-hdr-accent" style="background:#16A34A"></div>'
            '<div class="slide-hdr-text"><div class="slide-eyebrow" style="color:#16A34A">RESUMO EXECUTIVO</div>'
            f'<h2 class="slide-title">{esc(ex.get("title","O que ganhamos com cada ação"))}</h2></div></div>'
            f'<div class="slide-body">{intro}'
            '<table class="exec-tbl"><thead><tr>'
            '<th>Ação</th><th>Esforço</th><th>Impacto na operação</th>'
            f'<th>Impacto na change</th><th>Ganho</th>{rule_th}</tr></thead>'
            f'<tbody>{body}</tbody></table></div></div>')


def slide_not_recommended(d):
    items = d.get('not_recommended', [])
    if not items:
        return ''
    lis = ''.join(f'<li>{esc(x)}</li>' for x in items)
    return ('<div class="slide">' + brand_bar(f'{d.get("project","")} · Codebase 360')
            + '<div class="slide-hdr"><div class="slide-hdr-accent" style="background:#5561A6"></div>'
            '<div class="slide-hdr-text"><div class="slide-eyebrow" style="color:#5561A6">CAUTELA</div>'
            '<h2 class="slide-title">Não recomendado (e por quê)</h2></div></div>'
            f'<div class="slide-body"><ul class="exec-list muted">{lis}</ul></div></div>')


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
:root{--bg:#F0F1FA;--white:#fff;--navy:#0B1B73;--blue:#062EED;--purple:#6924E1;--midblue:#027BFF;--muted:#5561A6;--border:#B8C6E6;--pale:#E8EAF6;}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100%;overflow:hidden;font-family:'Poppins',Arial,sans-serif;background:var(--bg);color:var(--navy)}
.logo svg{height:26px;width:auto;display:block}.title-logo svg{height:46px}.div-logo svg{height:30px}
.div-logo svg path,.div-logo svg rect,.div-logo svg polygon{fill:#fff!important}
.slide-wrapper{width:100vw;height:100vh;display:none;flex-direction:column;overflow:hidden}
.slide-wrapper.active{display:flex}
.slide{flex:1;min-height:0;display:flex;flex-direction:column;background:var(--bg)}
.brand-bar{flex-shrink:0;display:flex;align-items:center;gap:14px;padding:10px 36px;background:#fff;border-bottom:1px solid var(--border)}
.brand-sep{width:1px;height:20px;background:var(--border)}.brand-tag{font-size:.68rem;font-weight:500;color:var(--muted)}
.title-accent{position:absolute;top:0;left:0;right:0;height:6px;background:linear-gradient(to right,#6924E1,#027BFF)}
.title-body{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:20px;padding:24px 40px 80px}
.eyebrow{font-size:.8rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
h1{font-size:clamp(2rem,4.6vw,3.6rem);font-weight:800;color:var(--navy);line-height:1.08}
h1 em{background:linear-gradient(135deg,#6924E1,#027BFF);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-style:normal}
.subtitle{font-size:.9rem;color:var(--muted);font-weight:500}
.kpi-row{display:flex;gap:18px;flex-wrap:wrap;justify-content:center;margin-top:8px}
.kpi{background:#fff;border:1px solid var(--border);border-radius:14px;padding:16px 22px;min-width:140px}
.kpi-v{font-size:1.7rem;font-weight:800;color:var(--blue)}.kpi-l{font-size:.72rem;color:var(--muted);font-weight:500;margin-top:2px}
.section-divider{align-items:center;justify-content:center;text-align:center;gap:14px;color:#fff;position:relative;padding:40px}
.div-logo{position:absolute;top:24px;left:36px}
.div-icon{font-size:3.4rem;line-height:1}
.div-title{font-size:clamp(1.8rem,4vw,3rem);font-weight:800;color:#fff}
.div-summary{font-size:1rem;max-width:760px;color:rgba(255,255,255,.92);line-height:1.55}
.div-count{margin-top:8px;background:rgba(255,255,255,.18);padding:6px 16px;border-radius:20px;font-size:.8rem;font-weight:600}
.slide-hdr{flex-shrink:0;display:flex;align-items:center;gap:16px;padding:16px 36px;background:#fff;border-bottom:2px solid var(--border)}
.slide-hdr-accent{width:5px;min-width:5px;height:52px;border-radius:3px}
.slide-eyebrow{font-size:.78rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase}
.slide-title{font-size:clamp(1.2rem,2.2vw,1.7rem);font-weight:700;color:var(--navy)}
.slide-meta{margin-left:auto}
.pill{display:inline-block;padding:5px 14px;border-radius:20px;font-size:.7rem;font-weight:700;color:#fff;letter-spacing:.04em}
.slide-body{flex:1;min-height:0;overflow-y:auto;padding:26px 40px 80px;display:flex;flex-direction:column;gap:16px}
.block{background:#fff;border:1px solid var(--border);border-radius:12px;padding:14px 18px}
.block .lbl{display:block;font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:6px}
.block p{font-size:.95rem;line-height:1.5;color:var(--navy)}
.block.cost{border-left:4px solid var(--blue)}.block.risk{border-left:4px solid var(--purple)}.block.gain{border-left:4px solid #16A34A}
.cmd{display:inline-block;margin-top:6px;font-family:ui-monospace,Menlo,monospace;font-size:.78rem;background:var(--pale);color:var(--purple);padding:2px 8px;border-radius:6px}
.opts{display:flex;gap:14px;flex-wrap:wrap}
.opt{flex:1;min-width:240px;background:var(--bg);border:1px solid var(--border);border-radius:10px;padding:12px 14px}
.opt-head{display:flex;justify-content:space-between;align-items:baseline;gap:8px;margin-bottom:5px}
.opt-kind{font-weight:700;color:var(--navy);font-size:.86rem}.opt-meta{font-size:.7rem;color:var(--muted);font-weight:600}
.opt-desc{font-size:.86rem;line-height:1.45;color:var(--navy)}
.opt-prompt{margin-top:9px}
.opt-prompt-lbl{display:block;font-size:.6rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--purple);margin-bottom:4px}
.opt-prompt code{display:block;white-space:pre-wrap;font-family:ui-monospace,Menlo,monospace;font-size:.72rem;line-height:1.45;background:var(--navy);color:#E8EAF6;border-radius:8px;padding:9px 11px}
.exec-list{list-style:none;display:flex;flex-direction:column;gap:10px}
.exec-list li{background:#fff;border:1px solid var(--border);border-left:4px solid var(--blue);border-radius:10px;padding:12px 16px;font-size:.95rem;line-height:1.5}
.exec-list.muted li{border-left-color:var(--muted);color:var(--muted)}
.score-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}
.score-card{background:#fff;border:1px solid var(--border);border-radius:14px;padding:18px;display:flex;flex-direction:column;gap:8px}
.score-grade{font-size:2.4rem;font-weight:900;border:3px solid;border-radius:12px;width:62px;height:62px;display:flex;align-items:center;justify-content:center}
.score-dim{font-weight:700;color:var(--navy);font-size:1rem}
.score-head{font-size:.82rem;color:var(--muted);line-height:1.4}
.exec-intro{font-size:.92rem;line-height:1.5;color:var(--navy);background:#fff;border:1px solid var(--border);border-left:4px solid #16A34A;border-radius:10px;padding:12px 16px;margin-bottom:6px}
.exec-tbl{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--border);border-radius:12px;overflow:hidden;font-size:.8rem}
.exec-tbl th{text-align:left;background:var(--pale);color:var(--muted);font-size:.64rem;text-transform:uppercase;letter-spacing:.06em;padding:9px 12px;font-weight:700}
.exec-tbl td{padding:8px 12px;border-top:1px solid var(--border);color:var(--navy);line-height:1.35;vertical-align:top}
.exec-tbl tr.grp td{background:var(--bg);font-weight:700;color:var(--navy);font-size:.76rem;letter-spacing:.02em}
.exec-tbl .act{font-weight:600;max-width:280px}
.exec-tbl .aid{display:inline-block;font-size:.6rem;font-weight:800;color:#fff;border-radius:5px;padding:1px 6px;margin-right:6px;vertical-align:middle}
.exec-tbl .gaincell{color:var(--muted);font-size:.78rem}
.exec-tbl .rule{color:var(--purple);font-weight:600;font-size:.78rem;border-left:2px solid var(--pale);max-width:300px}
.exec-done{display:inline-block;font-size:.58rem;font-weight:800;color:#fff;background:#16A34A;border-radius:5px;padding:1px 6px;margin-left:6px;vertical-align:middle}
.sev{display:inline-block;padding:2px 10px;border-radius:20px;font-size:.7rem;font-weight:700;white-space:nowrap}
.block.est{border-left:4px solid #16A34A}
.est-tbl{margin-top:4px}.est-tbl .saved{color:#16A34A;font-weight:800}
.est-cap{font-size:.72rem;color:var(--muted);margin-top:8px;line-height:1.4}
#counter{position:fixed;top:14px;right:24px;z-index:500;font-size:.72rem;font-weight:600;color:var(--muted);background:rgba(255,255,255,.92);padding:4px 12px;border-radius:20px;border:1px solid var(--border)}
#nav{position:fixed;bottom:0;left:0;right:0;z-index:500;display:flex;justify-content:center;align-items:center;gap:10px;padding:10px 0 12px;background:rgba(255,255,255,.95);backdrop-filter:blur(12px);border-top:1px solid var(--border)}
.nav-btn{width:38px;height:38px;border-radius:50%;border:none;cursor:pointer;background:linear-gradient(135deg,#6924E1,#027BFF);color:#fff;font-size:1rem;display:flex;align-items:center;justify-content:center}
.nav-btn:disabled{opacity:.25;cursor:default}
.nav-dot{width:8px;height:8px;border-radius:50%;background:var(--border);cursor:pointer}
.nav-dot.active{background:var(--blue);width:22px;border-radius:4px}
"""

JS = """
const N={SLIDE_COUNT};let cur=0;
function goTo(i){if(i<0||i>=N)return;
document.querySelector('.slide-wrapper.active')?.classList.remove('active');
document.querySelector('.nav-dot.active')?.classList.remove('active');
document.querySelectorAll('.slide-wrapper')[i].classList.add('active');
document.querySelectorAll('.nav-dot')[i].classList.add('active');
document.getElementById('counter').textContent=(i+1)+' / '+N;
document.getElementById('btn-prev').disabled=i===0;
document.getElementById('btn-next').disabled=i===N-1;cur=i;}
document.getElementById('btn-prev').addEventListener('click',()=>goTo(cur-1));
document.getElementById('btn-next').addEventListener('click',()=>goTo(cur+1));
document.querySelectorAll('.nav-dot').forEach((d,i)=>d.addEventListener('click',()=>goTo(i)));
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowDown')goTo(cur+1);
if(e.key==='ArrowLeft'||e.key==='ArrowUp')goTo(cur-1);});
goTo(0);
"""


def build(d):
    slides = [slide_title(d)]
    sc = slide_scorecard(d)
    if sc:
        slides.append(sc)
    ex = slide_exec_summary(d)
    if ex:
        slides.append(ex)
    for s in d.get('sections', []):
        if not s.get('findings'):
            continue
        slides.append(slide_section_divider(s))
        slides += [slide_finding(d, s, f) for f in s.get('findings', [])]
    nr = slide_not_recommended(d)
    if nr:
        slides.append(nr)
    n = len(slides)

    def wrap(i, s):
        return f'<div class="slide-wrapper{" active" if i == 0 else ""}">{s}</div>'

    body = '\n'.join(wrap(i, s) for i, s in enumerate(slides))
    dots = ''.join(f'<div class="nav-dot" title="Slide {i+1}"></div>' for i in range(n))
    title = esc(d.get('project', 'Bemobi')) + ' — Codebase 360'
    js = JS.replace('{SLIDE_COUNT}', str(n))
    return ('<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title><style>{CSS}</style></head><body>'
            f'<div id="counter">1 / {n}</div>{body}'
            '<div id="nav"><button class="nav-btn" id="btn-prev">&#8592;</button>'
            f'<div class="nav-dots">{dots}</div>'
            '<button class="nav-btn" id="btn-next">&#8594;</button></div>'
            f'<script>{js}</script></body></html>')


def main():
    if len(sys.argv) < 2:
        print('usage: render-deck.py findings.json [output.html]', file=sys.stderr)
        sys.exit(2)
    with open(sys.argv[1], encoding='utf-8') as fh:
        data = json.load(fh)
    out = sys.argv[2] if len(sys.argv) > 2 else 'codebase-360.html'
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write(build(data))
    nf = sum(len(s.get('findings', [])) for s in data.get('sections', []))
    print(f'Wrote {out} ({len(data.get("sections", []))} sections, {nf} findings)')


if __name__ == '__main__':
    main()
