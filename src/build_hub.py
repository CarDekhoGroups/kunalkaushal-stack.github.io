"""Build the BikeDekho Analytics Hub page (index.html) from one list of dashboards.

    python src/build_hub.py          -> writes ../index.html

To add or change a dashboard, edit DASHBOARDS below and rebuild; the sidebar counts, KPI tiles, filters, grid and
list view all follow from it. Deploy: `vercel deploy --prod` from the repo root (src/ is not published).
"""
import html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECTIONS = [
    ("ops", "Operations", "fa-gauge-high", "Lead delivery, triggers and business planning across the bikes business."),
    ("oem", "OEM Performance", "fa-motorcycle", "Lead-to-retail performance for each OEM partner."),
    ("bd", "BD Contribution", "fa-chart-pie", "BikeDekho's share of OEM retails, measured against Vahan registrations."),
]

TEXT_LOGO = lambda word, color, w=150: (
    f'<svg viewBox="0 0 {w} 44" xmlns="http://www.w3.org/2000/svg" height="34" role="img" aria-label="{word}">'
    f'<text x="{w // 2}" y="32" text-anchor="middle" font-family="Arial Black,Inter,sans-serif" font-size="27" '
    f'font-weight="900" fill="{color}" letter-spacing="1">{word}</text></svg>')

# section, name, url, tracks, source, refresh, live?, search words, + logo (OEM) or icon/description (others), glow rgb
DASHBOARDS = [
    dict(sec="ops", name="Bike AOP Tracker", url="https://adityakumar-bikes.github.io/leadbu-manager/", icon="fa-briefcase",
         cat="Business Manager", desc="Annual operating plan tracking and lead operations management.",
         tracks="Plan vs actual", source="Firebase app", refresh="Live", live=True, words="aop leadbu manager plan"),
    dict(sec="ops", name="Daily Trigger Dashboard", url="https://daily-trigger-dashboard.vercel.app", icon="fa-bolt",
         cat="Delivery Tracker", desc="Daily triggers, run-rate against target, spends and margin across OEMs.",
         tracks="Leads · Spends · Margin", source="Google Sheets", refresh="Live", live=True, words="trigger run rate spends margin targets"),
    dict(sec="ops", name="CPS Lead Delivery Tracker", url="https://adityakumar-bikes.github.io/cps-leads/", icon="fa-truck-fast",
         cat="Delivery Tracker", desc="CPS leads delivered by brand, model, state, dealer and day.",
         tracks="Leads delivered", source="LMS export", refresh="Daily", live=False, words="cps lead delivery lms"),
    dict(sec="oem", name="Royal Enfield", url="https://royal-enfield-performance-analytics.vercel.app",
         logo='<img src="https://upload.wikimedia.org/wikipedia/commons/8/8f/Royal_Enfield_logo.svg" alt="Royal Enfield">',
         tracks="Leads → Bookings", source="RE LDR sheet", refresh="Daily sync", live=False, glow="200,30,40", words="royal enfield re ldr"),
    dict(sec="oem", name="Hero MotoCorp", url="https://hero-ldr-dashboard.vercel.app/",
         logo='<img src="https://upload.wikimedia.org/wikipedia/commons/e/e2/Hero_MotoCorp_Logo.svg" alt="Hero MotoCorp">',
         tracks="Leads → Retail", source="Google Sheets", refresh="Live", live=True, glow="225,35,40", words="hero ldr motocorp"),
    dict(sec="oem", name="TVS Motor", url="https://tvscpsdashboard.vercel.app/",
         logo='<img src="https://upload.wikimedia.org/wikipedia/en/e/e9/TVS_Motor_logo.svg" alt="TVS Motor">',
         tracks="Leads → Retail", source="LDR pipeline", refresh="Scheduled", live=False, glow="30,60,170", words="tvs ldr apache jupiter"),
    dict(sec="oem", name="Honda (HMSI)", url="https://honda-motorcycles-and-scooters-anal.vercel.app",
         logo='<img src="https://upload.wikimedia.org/wikipedia/commons/0/09/Honda-logo.svg" alt="Honda">',
         tracks="Leads → Retail", source="Google Sheets", refresh="Live", live=True, glow="204,0,0", words="honda hmsi redwing bigwing rw bw scooters"),
    dict(sec="oem", name="Harley-Davidson X440", url="https://h-d-x-440-lead-performance-analytic.vercel.app",
         logo='<img src="https://upload.wikimedia.org/wikipedia/commons/d/de/Harley-Davidson_logo.svg" alt="Harley-Davidson">',
         tracks="Leads → Interest", source="Google Sheets", refresh="Live", live=True, glow="245,120,20", words="harley davidson hd x440 x440t"),
    dict(sec="oem", name="Ather Energy", url="https://ather-ldr-dashboard.vercel.app/", logo=TEXT_LOGO("ather", "#1B2A47", 130),
         tracks="Leads → Retail", source="Google Sheets", refresh="Live", live=True, glow="40,60,100", words="ather ev ldr rizta"),
    dict(sec="oem", name="Ampere", url="https://ampere-ldr-dashboard.vercel.app/", dark=True,
         logo='<img src="ampere-logo.png" alt="Ampere">',
         tracks="Leads → Retail", source="Google Sheets", refresh="Live", live=True, glow="20,160,140", words="ampere greaves ev magnus nexus"),
    dict(sec="oem", name="BGauss", url="https://bgauss-ldr-dashboard.vercel.app/", logo=TEXT_LOGO("BGAUSS", "#0B6E4F", 160),
         tracks="Leads → Retail", source="Google Sheets", refresh="Live", live=True, glow="11,110,79", words="bgauss ev scooter max c12 ruv"),
    dict(sec="oem", name="Bajaj Auto", url="https://bajaj-ldr-dashboard.web.app/",
         logo='<img src="https://upload.wikimedia.org/wikipedia/commons/2/2b/Bajaj_Auto_Ltd_logo.svg" alt="Bajaj Auto">',
         tracks="Leads → Retail", source="Google Sheets", refresh="Live", live=True, glow="0,85,170", words="bajaj ktm triumph chetak pulsar"),
    dict(sec="oem", name="Jawa · Yezdi · BSA", url="https://jawa-dashboard.vercel.app/",
         logo='<img src="https://upload.wikimedia.org/wikipedia/en/7/70/Jawa-logo.gif" alt="Jawa Motorcycles">',
         tracks="Leads → Retail", source="LDR pipeline", refresh="2× daily", live=False, glow="170,30,40", words="jawa yezdi bsa clpl classic legends"),
    dict(sec="bd", name="BD Contribution", url="https://bd-contribution-site.vercel.app", icon="fa-chart-pie", cat="Market share",
         desc="BikeDekho retails against Vahan registrations by state, city and month — TVS, Hero, Honda, Royal Enfield, Ather, CLPL, Ampere and Bajaj.",
         tracks="BD retails ÷ Vahan", source="LDR + Vahan", refresh="Periodic", live=False, words="bd contribution vahan market share rto"),
]

esc = html.escape
counts = {k: sum(d["sec"] == k for d in DASHBOARDS) for k, *_ in SECTIONS}
n_live = sum(d["live"] for d in DASHBOARDS)
sec_name = {k: n for k, n, *_ in SECTIONS}


def search_text(d):
    return esc(" ".join([d["name"], d.get("cat", ""), d.get("desc", ""), d["tracks"], d["source"], sec_name[d["sec"]], d["words"]]).lower())


def status(d):
    cls = "live" if d["live"] else "sched"
    return f'<span class="status {cls}"><span class="dot"></span>{esc(d["refresh"])}</span>'


def card(d):
    attrs = (f'class="card {"card-oem" if d["sec"] == "oem" else "card-tool"}" href="{esc(d["url"])}" target="_blank" '
             f'rel="noopener noreferrer" data-sec="{d["sec"]}" data-search="{search_text(d)}" '
             f'aria-label="{esc(d["name"])} — opens in a new tab"' + (f' style="--glow:{d["glow"]}"' if d.get("glow") else ""))
    meta = (f'<div class="card-meta"><span class="meta-item"><i class="fas fa-database"></i>{esc(d["source"])}</span>'
            f'{status(d)}</div>')
    if d["sec"] == "oem":
        return (f'<a {attrs}><div class="logo-panel{" dark" if d.get("dark") else ""}">{d["logo"]}</div>'
                f'<div class="card-main"><div class="card-title-row"><h3>{esc(d["name"])}</h3>'
                f'<i class="fas fa-arrow-up-right-from-square open-ico" aria-hidden="true"></i></div>'
                f'<div class="tracks">{esc(d["tracks"])}</div>{meta}</div></a>')
    return (f'<a {attrs}><div class="card-main"><div class="card-head"><span class="tool-icon"><i class="fas {d["icon"]}"></i></span>'
            f'<span class="chip">{esc(d["cat"])}</span></div><h3>{esc(d["name"])}</h3><p class="desc">{esc(d["desc"])}</p>'
            f'<div class="tracks">{esc(d["tracks"])}</div>{meta}</div>'
            f'<div class="card-foot"><span>Open dashboard</span><i class="fas fa-arrow-right"></i></div></a>')


def row(d):
    lead = (f'<span class="row-logo{" dark" if d.get("dark") else ""}">{d["logo"]}</span>' if d["sec"] == "oem"
            else f'<span class="row-icon"><i class="fas {d["icon"]}"></i></span>')
    return (f'<a class="lrow" href="{esc(d["url"])}" target="_blank" rel="noopener noreferrer" data-sec="{d["sec"]}" '
            f'data-search="{search_text(d)}"' + (f' style="--glow:{d["glow"]}"' if d.get("glow") else "") + '>'
            f'<span class="c-name">{lead}<span><b>{esc(d["name"])}</b><small>{esc(d.get("cat") or sec_name[d["sec"]])}</small></span></span>'
            f'<span class="c-sec">{esc(sec_name[d["sec"]])}</span><span class="c-tracks">{esc(d["tracks"])}</span>'
            f'<span class="c-src">{esc(d["source"])}</span><span class="c-ref">{status(d)}</span>'
            f'<span class="c-go"><i class="fas fa-arrow-up-right-from-square"></i></span></a>')


nav = "".join(f'<button class="nav-item" data-filter="{k}"><i class="fas {ic}"></i><span>{esc(n)}</span>'
              f'<em data-count="{k}">{counts[k]}</em></button>' for k, n, ic, _ in SECTIONS)
chips = '<button class="fchip on" data-filter="all">All</button>' + "".join(
    f'<button class="fchip" data-filter="{k}">{esc(n)}</button>' for k, n, *_ in SECTIONS)
sections = "".join(
    f'<section class="sec" id="sec-{k}" data-sec="{k}"><div class="sec-head"><div><h2><i class="fas {ic}"></i>{esc(n)}</h2>'
    f'<p>{esc(blurb)}</p></div><span class="sec-count" data-count="{k}">{counts[k]}</span></div>'
    f'<div class="grid grid-{k}">' + "".join(card(d) for d in DASHBOARDS if d["sec"] == k) + "</div></section>"
    for k, n, ic, blurb in SECTIONS)
rows = "".join(row(d) for d in DASHBOARDS)

PAGE = open(os.path.join(ROOT, "src", "template.html"), encoding="utf-8").read()
out = (PAGE.replace("{{NAV}}", nav).replace("{{CHIPS}}", chips).replace("{{SECTIONS}}", sections).replace("{{ROWS}}", rows)
       .replace("{{N_TOTAL}}", str(len(DASHBOARDS))).replace("{{N_OEM}}", str(counts["oem"])).replace("{{N_LIVE}}", str(n_live)))
assert "{{" not in out
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8", newline="\n").write(out)
print(f"index.html: {len(DASHBOARDS)} dashboards ({counts}), {n_live} live")
