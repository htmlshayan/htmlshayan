"""
profile_kit.py — builds every SVG on the htmlshayan profile.

  python .github/scripts/profile_kit.py all   -> rebuild all assets
  python .github/scripts/profile_kit.py log   -> rebuild only the live bot log (used by the Action)

Edit the CONFIG block, run `all`, commit. That's it.
"""
import datetime as dt, json, os, sys, urllib.request
from html import escape

# ───────────────────────── CONFIG ─────────────────────────
USER      = "htmlshayan"
NAME      = "SHAYAN"
ROLE      = "automation bots engineer"
TAGLINE   = "i build bots that never sleep"
STATUS    = "online — accepting new automation jobs"

STACK = [
    ("languages",  ["python", "javascript", "bash"]),
    ("automation", ["selenium", "node.js", "github-actions"]),
    ("infra",      ["docker", "linux", "aws"]),
    ("data",       ["redis", "postgresql"]),
]

FLEET = [  # name, image, function
    ("x-bot",       "python:3.12", "full automation of X"),
    ("ig-bot",      "python:3.12", "full automation of Instagram"),
    ("spotify-bot", "python:3.12", "spotify automation"),
]

CONTACTS = [  # file, label, value
    ("linkedin", "linkedin", "/in/htmlshayan"),
    ("telegram", "telegram", "@gotanx"),
    ("email",    "mail",     "shayanmansoor596@gmail.com"),
]

# ───────────────────────── THEME ──────────────────────────
BG, PANEL, BAR, BORDER = "#0A0C0E", "#0F1215", "#14181C", "#1F252B"
LIME, LIME_DIM         = "#B3E625", "#5E7A12"
TEXT, SOFT, MUTED      = "#E6EDF3", "#D9F99D", "#6E7681"
FONT = "'JetBrains Mono','Fira Code','Cascadia Code','SF Mono',Consolas,'Liberation Mono','DejaVu Sans Mono',monospace"
CW = 0.61  # approx monospace char width (em)

ASSETS = os.path.join(os.path.dirname(__file__), "..", "..", "assets")
STATIC = os.environ.get("STATIC") == "1"  # preview mode: no animations

BASE_CSS = f"""
text{{font-family:{FONT};}}
.blink{{animation:blink 1.1s steps(1) infinite}}
.pulse{{animation:pulse 2s ease-in-out infinite}}
.fade{{opacity:0;animation:fade .5s ease forwards}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
@keyframes fade{{to{{opacity:1}}}}
"""
if STATIC:
    BASE_CSS = f"text{{font-family:{FONT};}}"


def svg(w, h, body, css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<style>{BASE_CSS}{css}</style>{body}</svg>')


def window(w, h, title, body):
    """Editor/terminal window chrome."""
    return (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="{PANEL}" stroke="{BORDER}"/>'
            f'<path d="M.5 40V12.5A12 12 0 0 1 12.5 .5h{w-25}A12 12 0 0 1 {w-.5} 12.5V40z" fill="{BAR}"/>'
            f'<line x1="0" y1="40.5" x2="{w}" y2="40.5" stroke="{BORDER}"/>'
            f'<circle cx="24" cy="20.5" r="5.5" fill="#2A3138"/><circle cx="42" cy="20.5" r="5.5" fill="#2A3138"/>'
            f'<circle cx="60" cy="20.5" r="5.5" fill="{LIME}"/>'
            f'<text x="{w/2}" y="25" text-anchor="middle" font-size="13" fill="{MUTED}">{escape(title)}</text>'
            + body)


def delay(sec):
    return "" if STATIC else f' style="animation-delay:{sec:.2f}s"'


def typed(i, x, y, w, begin, dur, content, size=15):
    """Line that 'types' itself via an animated clip rect."""
    cid = f"c{i}"
    width = w if STATIC else 0
    anim = "" if STATIC else (f'<animate attributeName="width" from="0" to="{w}" begin="{begin:.2f}s" '
                              f'dur="{dur:.2f}s" fill="freeze"/>')
    return (f'<clipPath id="{cid}"><rect x="{x-2}" y="{y-size}" width="{width}" height="{size*1.5}">{anim}</rect></clipPath>'
            f'<text x="{x}" y="{y}" font-size="{size}" xml:space="preserve" clip-path="url(#{cid})">{content}</text>')


def tok(text, color, weight=None, italic=False):
    w = f' font-weight="{weight}"' if weight else ""
    it = ' font-style="italic"' if italic else ""
    return f'<tspan fill="{color}"{w}{it}>{escape(text)}</tspan>'


# ───────────────────────── HERO ───────────────────────────
ROBOT = [
    "......A......",
    "......S......",
    "..BBBBBBBBB..",
    ".B.........B.",
    "BB..EE.EE..BB",
    "BB..EE.EE..BB",
    ".B.........B.",
    ".B..MMMMM..B.",
    "..BBBBBBBBB..",
]


def hero():
    w, h = 1000, 300
    px, ox, oy = 13, 770, 62
    robot = ""
    for r, row in enumerate(ROBOT):
        for c, ch in enumerate(row):
            if ch == ".":
                continue
            cls = {"A": "pulse", "E": "eye"}.get(ch, "")
            fill = LIME if ch in "ABE" else (LIME_DIM if ch in "SM" else LIME)
            robot += (f'<rect class="{cls}" x="{ox+c*px}" y="{oy+r*px}" width="{px-2}" height="{px-2}" '
                      f'rx="2" fill="{fill}"/>')
    robot += (f'<text x="{ox+6.5*px}" y="{oy+10.8*px}" text-anchor="middle" font-size="13" fill="{MUTED}">'
              f'&lt;bot status="alive"/&gt;</text>')
    css = "" if STATIC else ".eye{animation:eye 4s infinite;transform-box:fill-box;transform-origin:center}@keyframes eye{0%,92%,100%{transform:scaleY(1)}96%{transform:scaleY(.1)}}"
    body = (
        f'<defs><pattern id="g" width="22" height="22" patternUnits="userSpaceOnUse">'
        f'<circle cx="1" cy="1" r="1" fill="#1A1F24"/></pattern></defs>'
        f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="{BG}" stroke="{BORDER}"/>'
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="url(#g)"/>'
        f'<path d="M24 44V24h20M{w-24} 44V24h-20M24 {h-44}v20h20M{w-24} {h-44}v20h-20" '
        f'stroke="{LIME}" stroke-width="2" fill="none"/>'
        f'<text x="60" y="84" font-size="16">{tok("shayan@bots", LIME)}{tok(":~$ ", MUTED)}{tok("whoami", TEXT)}</text>'
        f'<text x="56" y="168" font-size="86" font-weight="800" fill="{TEXT}" letter-spacing="2">'
        f'{escape(NAME)}<tspan class="blink" fill="{LIME}">_</tspan></text>'
        f'<text x="60" y="210" font-size="18">{tok(ROLE, LIME, 700)}{tok("  // " + TAGLINE, MUTED)}</text>'
        f'<circle class="pulse" cx="66" cy="248" r="5" fill="{LIME}"/>'
        f'<text x="80" y="253" font-size="14" fill="{MUTED}">status: {escape(STATUS)}</text>'
        + robot)
    return svg(w, h, body, css)


# ───────────────────────── ABOUT (editor) ─────────────────
def about():
    K, S, C, W, P, D = LIME, SOFT, MUTED, TEXT, "#8B949E", "#8FB31C"
    lines = [
        [tok("# ~/shayan/profile.py", C, italic=True)],
        [tok("from ", K), tok("bots ", W), tok("import ", K), tok("Bot", W)],
        [],
        [tok("class ", K), tok("Shayan", W, 700), tok("(", P), tok("Engineer", D), tok("):", P)],
        [tok("    role  ", W), tok("= ", P), tok(f'"{ROLE.title()}"', S)],
        [tok("    focus ", W), tok("= ", P), tok("[", P), tok('"scrapers"', S), tok(", ", P),
         tok('"social bots"', S), tok(", ", P), tok('"pipelines"', S), tok("]", P)],
        [tok("    motto ", W), tok("= ", P), tok('"do it twice? a bot does it forever."', S)],
        [],
        [tok("    def ", K), tok("run", D, 700), tok("(", P), tok("self", C), tok("):", P)],
        [tok("        for ", K), tok("task ", W), tok("in ", K), tok("self", C), tok(".", P),
         tok("boring_stuff", D), tok("():", P)],
        [tok("            Bot", W), tok("(", P), tok("task", W), tok(").", P), tok("deploy", D), tok("()", P),
         tok("   # 24/7, no coffee needed", C, italic=True)],
        [],
        [tok("Shayan", W, 700), tok("().", P), tok("run", D), tok("()", P)],
    ]
    import re
    plain = lambda ts: re.sub(r"<[^>]+>", "", "".join(ts)).replace("&quot;", '"').replace("&#x27;", "'")
    w, lh, top = 1000, 26, 78
    h = top + len(lines) * lh + 36
    body, t = "", 0.3
    for i, ts in enumerate(lines):
        y = top + i * lh
        body += f'<text x="44" y="{y}" font-size="14" text-anchor="end" fill="#3A424A">{i+1}</text>'
        n = len(plain(ts))
        if n:
            dur = max(0.12, n * 0.018)
            body += typed(i, 64, y, n * 15 * CW + 20, t, dur, "".join(ts))
            t += dur + 0.05
        else:
            t += 0.1
    last_y = top + (len(lines) - 1) * lh
    cur_x = 64 + len(plain(lines[-1])) * 15 * CW + 4
    body += (f'<rect x="0" y="{last_y-18}" width="{w}" height="{lh}" fill="{LIME}" fill-opacity=".05"/>'
             f'<rect class="blink" x="{cur_x}" y="{last_y-15}" width="9" height="19" fill="{LIME}"/>')
    # status bar
    sb = h - 30
    body += (f'<path d="M.5 {sb}H{w-.5}V{h-12.5}A12 12 0 0 1 {w-12.5} {h-.5}H12.5A12 12 0 0 1 .5 {h-12.5}z" fill="{LIME}"/>'
             f'<text x="18" y="{sb+19}" xml:space="preserve" font-size="12" font-weight="700" fill="{BG}">⎇ main   ● {len(FLEET)} bots online   ✓ 0 errors</text>'
             f'<text x="{w-18}" y="{sb+19}" xml:space="preserve" font-size="12" font-weight="700" fill="{BG}" text-anchor="end">'
             f'Python 3.12   UTF-8   LF   Ln {len(lines)}, Col 15</text>')
    return svg(w, h, window(w, h, "01 — profile.py", body))


# ───────────────────────── STACK ──────────────────────────
def stack():
    w, rh, top = 1000, 50, 104
    h = top + len(STACK) * rh + 40
    body = f'<text x="32" y="74" font-size="15">{tok("$ ", LIME)}{tok("shayan --stack", TEXT)}</text>'
    for i, (cat, items) in enumerate(STACK):
        y = top + i * rh
        g = f'<text x="32" y="{y+5}" font-size="14" fill="{MUTED}">{escape(cat)}</text>'
        x = 200
        for it in items:
            cw = len(it) * 14 * CW + 34
            g += (f'<rect x="{x}" y="{y-17}" width="{cw:.0f}" height="32" rx="6" fill="{BAR}" stroke="{LIME_DIM}"/>'
                  f'<circle cx="{x+14}" cy="{y-1}" r="3" fill="{LIME}"/>'
                  f'<text x="{x+cw/2+6:.0f}" y="{y+4}" font-size="14" text-anchor="middle" fill="{TEXT}">{escape(it)}</text>')
            x += cw + 12
        body += f'<g class="fade"{delay(0.2 + i*0.2)}>{g}</g>'
    body += (f'<text x="32" y="{h-26}" font-size="15">{tok("$ ", LIME)}'
             f'<tspan class="blink" fill="{LIME}">█</tspan></text>')
    return svg(w, h, window(w, h, "02 — zsh: stack", body))


# ───────────────────────── FLEET ──────────────────────────
def fleet():
    w, rh, top = 1000, 42, 132
    h = top + len(FLEET) * rh + 20
    cols = [32, 230, 410, 590]
    body = (f'<text x="32" y="74" font-size="15">{tok("$ ", LIME)}'
            f'{tok("docker ps ", TEXT)}{tok(f"--filter owner={USER}", MUTED)}</text>')
    for x, head in zip(cols, ["CONTAINER", "IMAGE", "STATUS", "FUNCTION"]):
        body += f'<text x="{x}" y="108" font-size="12" font-weight="700" letter-spacing="1.5" fill="{MUTED}">{head}</text>'
    body += f'<line x1="32" y1="118" x2="{w-32}" y2="118" stroke="{BORDER}"/>'
    for i, (name, image, fn) in enumerate(FLEET):
        y = top + i * rh + 10
        g = (f'<text x="{cols[0]}" y="{y}" font-size="15" font-weight="700" fill="{LIME}">{escape(name)}</text>'
             f'<text x="{cols[1]}" y="{y}" font-size="14" fill="{TEXT}">{escape(image)}</text>'
             f'<circle class="pulse" cx="{cols[2]+5}" cy="{y-5}" r="4.5" fill="{LIME}"{delay(i*0.4)}/>'
             f'<text x="{cols[2]+18}" y="{y}" font-size="14" fill="{SOFT}">up 24/7</text>'
             f'<text x="{cols[3]}" y="{y}" font-size="14" fill="{MUTED}">{escape(fn)}</text>')
        if i < len(FLEET) - 1:
            g += f'<line x1="32" y1="{y+17}" x2="{w-32}" y2="{y+17}" stroke="{BORDER}" stroke-dasharray="3 5"/>'
        body += f'<g class="fade"{delay(0.3 + i*0.25)}>{g}</g>'
    return svg(w, h, window(w, h, "03 — fleet", body))


# ───────────────────────── LIVE LOG ───────────────────────
def fetch_repos():
    token = os.environ.get("GH_TOKEN")
    if not token:
        return None
    req = urllib.request.Request(
        f"https://api.github.com/users/{USER}/repos?sort=pushed&per_page=20&type=owner",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
    repos = json.load(urllib.request.urlopen(req))
    return [r for r in repos if not r["fork"] and r["name"].lower() != USER.lower()][:5]


def log():
    now = dt.datetime.now(dt.timezone.utc)
    repos = fetch_repos()

    def ago(ts):
        s = int((now - dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))).total_seconds())
        for unit, n in (("d", 86400), ("h", 3600), ("m", 60)):
            if s >= n:
                return f"{s // n}{unit} ago"
        return "just now"

    stamp = now.strftime("%H:%M:%S")
    rows = [[tok(f"{stamp} ", MUTED), tok("[SYS]  ", LIME, 700), tok("shayan-os booted — scanning deployed units...", TEXT)]]
    if repos is None:
        rows.append([tok(f"{stamp} ", MUTED), tok("[WAIT] ", SOFT, 700), tok("run the bot-log workflow to go live", MUTED)])
    elif not repos:
        rows.append([tok(f"{stamp} ", MUTED), tok("[WARN] ", SOFT, 700), tok("no public units found", MUTED)])
    for r in repos or []:
        rows.append([tok(f"{stamp} ", MUTED), tok("[OK]   ", LIME, 700),
                     tok(f"{r['name'][:24]:<25}", TEXT),
                     tok(f"{(r['language'] or '-')[:12]:<13}", MUTED),
                     tok(f"★{r['stargazers_count']:<5}", SOFT),
                     tok(f"pushed {ago(r['pushed_at'])}", MUTED)])
    rows.append([tok(f"{stamp} ", MUTED), tok("[SYS]  ", LIME, 700), tok("next sync in 6h", MUTED)])

    w, lh, top = 1000, 28, 104
    h = top + len(rows) * lh + 34
    body = (f'<text x="32" y="74" font-size="15">{tok("$ ", LIME)}{tok("tail -f ", TEXT)}'
            f'{tok("/var/log/shayan-os/bots.log", MUTED)}</text>'
            f'<text x="{w-32}" y="74" font-size="12" text-anchor="end" fill="{MUTED}">'
            f'last sync {now:%Y-%m-%d %H:%M} UTC</text>')
    t = 0.3
    for i, ts in enumerate(rows):
        y = top + i * lh
        body += typed(i, 32, y, w - 64, t, 0.45, "".join(ts), size=14)
        t += 0.5
    body += (f'<rect class="blink" x="32" y="{top + len(rows)*lh - 16}" width="9" height="18" fill="{LIME}"/>')
    return svg(w, h, window(w, h, "04 — bot.log (auto-updated by github actions)", body))


# ───────────────────────── CONTACT BUTTONS ────────────────
def button(label, value):
    size = 14
    w = int((len(label) + len(value) + 6) * size * CW + 40)
    h = 46
    body = (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="8" fill="{PANEL}" stroke="{LIME_DIM}"/>'
            f'<rect x="0" y="0" width="5" height="{h}" rx="2" fill="{LIME}"/>'
            f'<text x="22" y="28" font-size="{size}">{tok("> ", LIME, 700)}{tok(label, TEXT, 700)}'
            f'{tok("  " + value, MUTED)}</text>')
    return svg(w, h, body)


# ───────────────────────── FOOTER ─────────────────────────
def footer():
    w, h = 1000, 90
    body = (f'<line x1="0" y1="20" x2="{w}" y2="20" stroke="{BORDER}" stroke-dasharray="4 6"/>'
            f'<text x="{w/2}" y="58" font-size="15" text-anchor="middle" xml:space="preserve">'
            f'{tok("// EOF", MUTED)}{tok("  ·  ", BORDER)}{tok("exit 0", LIME, 700)}{tok("  ·  ", BORDER)}'
            f'{tok("let us automate something", MUTED)}<tspan class="blink" fill="{LIME}"> █</tspan></text>')
    return svg(w, h, body)


def write(name, content):
    os.makedirs(ASSETS, exist_ok=True)
    with open(os.path.join(ASSETS, name), "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("all", "log"):
        write("log.svg", log())
    if mode == "all":
        write("hero.svg", hero())
        write("about.svg", about())
        write("stack.svg", stack())
        write("fleet.svg", fleet())
        write("footer.svg", footer())
        for file, label, value in CONTACTS:
            write(f"btn-{file}.svg", button(label, value))
    print(f"built: {mode}")
