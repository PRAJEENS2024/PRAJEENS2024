"""Hard-coded terminal-aesthetic SVG generators for GitHub Profile portfolio."""

from __future__ import annotations

from datetime import date
from html import escape
from pathlib import Path
from typing import Any

from scripts.generators.logos import inline_logo_group, write_logo_svgs

FONT_SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif"
FONT_MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"

HEATMAP_COLORS = ["#161B22", "#0E4429", "#006D32", "#26A641", "#39D353"]


def _fmt_int(value: int | float | None, default: str = "—") -> str:
    if value is None:
        return default
    return f"{int(round(value)):,}"


def render_hero_banner_svg(config: dict[str, Any]) -> str:
    """Render a hard-coded Neovim/terminal-style hero SVG with subtle real animations."""
    profile = config.get("profile", {})
    name = escape(profile.get("name", "Prajeen S"))
    username = escape(profile.get("github_username", "PRAJEENS2024"))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 198" width="100%" role="img" aria-label="{name} Terminal Profile Header">
  <defs>
    <clipPath id="waveClip">
      <rect x="618" y="54" width="236" height="96"/>
    </clipPath>
  </defs>

  <!-- Seamless GitHub dark canvas with crisp 1px terminal border -->
  <rect x="0.5" y="0.5" width="879" height="197" rx="6" fill="#0D1117" stroke="#21262D"/>

  <!-- Top window bar -->
  <path d="M1 6.5A5.5 5.5 0 0 1 6.5 1h867A5.5 5.5 0 0 1 879 6.5V30H1V6.5z" fill="#010409"/>
  <line x1="1" y1="30" x2="879" y2="30" stroke="#21262D"/>

  <!-- Muted terminal controls -->
  <circle cx="18" cy="15.5" r="4.5" fill="#30363D"/>
  <circle cx="33" cy="15.5" r="4.5" fill="#30363D"/>
  <circle cx="48" cy="15.5" r="4.5" fill="#30363D"/>
  <text x="68" y="19" fill="#8B949E" font-family="{FONT_MONO}" font-size="11">{username.lower()}@github: ~/profile.ts</text>
  <circle cx="842" cy="15.5" r="3.5" fill="#39D353">
    <animate attributeName="opacity" values="1;0.3;1" dur="2.2s" repeatCount="indefinite"/>
  </circle>
  <text x="852" y="19" fill="#6E7681" font-family="{FONT_MONO}" font-size="10.5">zsh</text>

  <!-- Terminal command prompt -->
  <text x="24" y="58" fill="#39D353" font-family="{FONT_MONO}" font-size="12.5" font-weight="700">$<tspan fill="#8B949E" font-weight="400"> cat ./identity.ts</tspan></text>

  <!-- Primary Name + blinking block cursor -->
  <text x="24" y="94" fill="#F0F6FC" font-family="{FONT_MONO}" font-size="28" font-weight="700" letter-spacing="-0.5">{name}</text>
  <rect x="182" y="71" width="11" height="24" fill="#58A6FF">
    <animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.49;0.5;0.99;1" dur="1.1s" repeatCount="indefinite"/>
  </rect>

  <!-- Hard-coded syntax lines -->
  <text x="24" y="124" font-family="{FONT_MONO}" font-size="12.5">
    <tspan fill="#FF7B72">const</tspan> <tspan fill="#79C0FF">focus</tspan> <tspan fill="#8B949E">=</tspan> <tspan fill="#A5D6FF">"Full-Stack Systems · Competitive Programming · Embedded/IoT"</tspan><tspan fill="#8B949E">;</tspan>
  </text>
  <text x="24" y="146" font-family="{FONT_MONO}" font-size="12.5">
    <tspan fill="#FF7B72">const</tspan> <tspan fill="#79C0FF">edu</tspan>   <tspan fill="#8B949E">=</tspan> <tspan fill="#A5D6FF">"B.E. ECE '28 @ Sri Eshwar College of Engineering (CGPA: 8.12)"</tspan><tspan fill="#8B949E">;</tspan>
  </text>
  <text x="24" y="168" font-family="{FONT_MONO}" font-size="12.5">
    <tspan fill="#FF7B72">const</tspan> <tspan fill="#79C0FF">prev</tspan>  <tspan fill="#8B949E">=</tspan> <tspan fill="#A5D6FF">"MERN Stack Intern @ AlgoTutor · Coimbatore, IN"</tspan><tspan fill="#8B949E">;</tspan>
  </text>

  <!-- Subtle animated ECE oscilloscope trace on right -->
  <line x1="610" y1="48" x2="610" y2="174" stroke="#21262D"/>
  <g clip-path="url(#waveClip)">
    <line x1="618" y1="102" x2="854" y2="102" stroke="#161B22" stroke-dasharray="3 3"/>
    <path d="M618 102 L652 102 L662 84 L672 122 L682 68 L692 134 L702 92 L712 102 L752 102 L762 84 L772 122 L782 68 L792 134 L802 92 L812 102 L854 102"
          fill="none" stroke="#238636" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"
          stroke-dasharray="14 6">
      <animate attributeName="stroke-dashoffset" from="0" to="-40" dur="2.8s" repeatCount="indefinite"/>
    </path>
  </g>
  <text x="622" y="168" fill="#6E7681" font-family="{FONT_MONO}" font-size="10">SIG // ECE + SWE [ONLINE]</text>
</svg>
'''


def render_github_stats_svg(snapshot: dict[str, Any]) -> str:
    """Render flat terminal-grid GitHub Metrics & Language Breakdown SVG."""
    gh = snapshot["derived"]["github"]
    username = escape(str(gh.get("username", "PRAJEENS2024")))
    updated = escape(str(snapshot.get("last_updated", "")))

    total_contrib = _fmt_int(gh.get("total_contributions", 0))
    public_repos = _fmt_int(gh.get("public_repos", 0))
    current_streak = _fmt_int(gh.get("current_streak", 0))
    longest_streak = _fmt_int(gh.get("longest_streak", 0))
    active_days = _fmt_int(gh.get("active_days", 0))
    total_stars = _fmt_int(gh.get("total_stars", 0))
    total_forks = _fmt_int(gh.get("total_forks", 0))

    if gh.get("commits") is not None:
        mix_text = (
            f"commits={_fmt_int(gh['commits'])}  "
            f"prs={_fmt_int(gh.get('pull_requests', 0))}  "
            f"issues={_fmt_int(gh.get('issues', 0))}  "
            f"reviews={_fmt_int(gh.get('reviews', 0))}"
        )
    else:
        mix_text = (
            f"stars={total_stars}  "
            f"forks={total_forks}  "
            f"followers={_fmt_int(gh.get('followers', 0))}"
        )

    langs = gh.get("top_languages") or []
    bar_x = 468.0
    bar_w = 388.0
    bar_segments: list[str] = []
    cursor_x = bar_x
    for idx, lang in enumerate(langs):
        pct = float(lang.get("percent", 0))
        seg_w = (bar_w * pct / 100.0) if idx < len(langs) - 1 else (bar_x + bar_w - cursor_x)
        seg_w = max(seg_w, 2.0) if pct > 0 else 0.0
        if seg_w <= 0:
            continue
        color = escape(str(lang.get("color", "#8B949E")))
        bar_segments.append(
            f'<rect x="{cursor_x:.1f}" y="66" width="{seg_w:.1f}" height="8" fill="{color}"/>'
        )
        cursor_x += seg_w

    legend_items: list[str] = []
    for idx, lang in enumerate(langs[:6]):
        col = idx % 2
        row = idx // 2
        lx = 468 + col * 200
        ly = 104 + row * 28
        color = escape(str(lang.get("color", "#8B949E")))
        lname = escape(str(lang["name"]))
        lpct = f"{lang['percent']}%"
        legend_items.append(
            f'<rect x="{lx}" y="{ly - 9}" width="8" height="8" rx="1.5" fill="{color}"/>'
            f'<text x="{lx + 14}" y="{ly}" fill="#C9D1D9" font-family="{FONT_MONO}" font-size="11.5">{lname}</text>'
            f'<text x="{lx + 186}" y="{ly}" text-anchor="end" fill="#8B949E" font-family="{FONT_MONO}" font-size="11.5">{lpct}</text>'
        )

    gh_icon = inline_logo_group("github", 20, 15, size=16.0, fill="#F0F6FC")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 218" width="100%" role="img" aria-label="GitHub Engineering Stats for {username}">
  <defs>
    <clipPath id="langBarClip">
      <rect x="468" y="66" width="388" height="8" rx="2"/>
    </clipPath>
  </defs>

  <rect x="0.5" y="0.5" width="879" height="217" rx="6" fill="#0D1117" stroke="#21262D"/>

  <!-- Header Strip -->
  <rect x="1" y="1" width="878" height="42" rx="5" fill="#010409"/>
  <line x1="1" y1="43" x2="879" y2="43" stroke="#21262D"/>
  {gh_icon}
  <text x="44" y="27" fill="#F0F6FC" font-family="{FONT_MONO}" font-size="13" font-weight="700">GITHUB // TELEMETRY</text>
  <text x="434" y="27" text-anchor="end" fill="#6E7681" font-family="{FONT_MONO}" font-size="11">@{username}</text>
  <text x="468" y="27" fill="#F0F6FC" font-family="{FONT_MONO}" font-size="13" font-weight="700">LANGUAGES // FOOTPRINT</text>
  <text x="856" y="27" text-anchor="end" fill="#6E7681" font-family="{FONT_MONO}" font-size="11">sync={updated}</text>

  <!-- Vertical column divider -->
  <line x1="450" y1="1" x2="450" y2="217" stroke="#21262D"/>

  <!-- Left 2x2 flat metric grid -->
  <line x1="20" y1="115" x2="434" y2="115" stroke="#21262D"/>
  <line x1="226" y1="54" x2="226" y2="176" stroke="#21262D"/>

  <text x="24" y="72" fill="#8B949E" font-family="{FONT_MONO}" font-size="11">CONTRIBUTIONS (12M)</text>
  <text x="24" y="100" fill="#58A6FF" font-family="{FONT_MONO}" font-size="23" font-weight="700">{total_contrib}</text>

  <text x="244" y="72" fill="#8B949E" font-family="{FONT_MONO}" font-size="11">STREAK (CUR / MAX)</text>
  <text x="244" y="100" fill="#39D353" font-family="{FONT_MONO}" font-size="23" font-weight="700">{current_streak}d <tspan fill="#6E7681" font-size="14">/ {longest_streak}d</tspan></text>

  <text x="24" y="136" fill="#8B949E" font-family="{FONT_MONO}" font-size="11">PUBLIC REPOS</text>
  <text x="24" y="164" fill="#F0F6FC" font-family="{FONT_MONO}" font-size="23" font-weight="700">{public_repos}</text>

  <text x="244" y="136" fill="#8B949E" font-family="{FONT_MONO}" font-size="11">ACTIVE DAYS (12M)</text>
  <text x="244" y="164" fill="#C9D1D9" font-family="{FONT_MONO}" font-size="23" font-weight="700">{active_days}</text>

  <line x1="20" y1="180" x2="434" y2="180" stroke="#21262D"/>
  <text x="24" y="200" fill="#8B949E" font-family="{FONT_MONO}" font-size="11">{escape(mix_text)}</text>

  <!-- Right Language Bar & Legend -->
  <rect x="468" y="66" width="388" height="8" rx="2" fill="#161B22"/>
  <g clip-path="url(#langBarClip)">
    {''.join(bar_segments)}
  </g>
  {''.join(legend_items)}
  <line x1="468" y1="180" x2="856" y2="180" stroke="#21262D"/>
  <text x="468" y="200" fill="#6E7681" font-family="{FONT_MONO}" font-size="10.5">Weighted by repository source bytes (excluding vendored artifacts)</text>
</svg>
'''


def render_contribution_heatmap_svg(snapshot: dict[str, Any]) -> str:
    """Render flat 52-week contribution heatmap + 6-month velocity chart SVG."""
    gh = snapshot["derived"]["github"]
    days = sorted(gh.get("calendar_days") or [], key=lambda d: d["date"])
    monthly = gh.get("monthly_contributions") or []
    total_contrib = _fmt_int(gh.get("total_contributions", 0))

    cells: list[str] = []
    month_labels: list[str] = []
    seen_months: set[tuple[int, str]] = set()
    last_labeled_col = -4

    if days:
        first_dt = date.fromisoformat(days[0]["date"])
        first_sun_offset = (first_dt.weekday() + 1) % 7
        for idx, d in enumerate(days):
            dt = date.fromisoformat(d["date"])
            pos = idx + first_sun_offset
            col = pos // 7
            row = pos % 7
            if col >= 53:
                continue
            x = 56 + col * 14.8
            y = 74 + row * 14.8
            level = max(0, min(4, int(d.get("level", 0))))
            fill = HEATMAP_COLORS[level]
            count = int(d.get("count", 0))
            cells.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="11.2" height="11.2" rx="2" fill="{fill}">'
                f'<title>{escape(d["date"])}: {count} contribution(s)</title></rect>'
            )
            if dt.day <= 7 and row == 0:
                m_lbl = dt.strftime("%b")
                if col - last_labeled_col >= 3 and (col, m_lbl) not in seen_months:
                    seen_months.add((col, m_lbl))
                    last_labeled_col = col
                    month_labels.append(
                        f'<text x="{x:.1f}" y="64" fill="#8B949E" font-family="{FONT_MONO}" font-size="10">{m_lbl}</text>'
                    )

    bars: list[str] = []
    if monthly:
        max_m = max((m["count"] for m in monthly), default=1) or 1
        bar_area_x = 190
        step = 110
        for i, m in enumerate(monthly[-6:]):
            bx = bar_area_x + i * step
            val = int(m["count"])
            bh = max(4, round((val / max_m) * 38)) if val > 0 else 2
            by = 248 - bh
            bars.append(
                f'<rect x="{bx}" y="{by}" width="40" height="{bh}" rx="2" fill="#238636"/>'
                f'<text x="{bx + 20}" y="{by - 5}" text-anchor="middle" fill="#C9D1D9" font-family="{FONT_MONO}" font-size="10.5">{val}</text>'
                f'<text x="{bx + 20}" y="264" text-anchor="middle" fill="#8B949E" font-family="{FONT_MONO}" font-size="10.5">{escape(m["label"])}</text>'
            )

    legend_boxes = "".join(
        f'<rect x="{748 + i * 15}" y="182" width="10.5" height="10.5" rx="2" fill="{c}"/>'
        for i, c in enumerate(HEATMAP_COLORS)
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 280" width="100%" role="img" aria-label="GitHub 52-Week Contribution Heatmap">
  <rect x="0.5" y="0.5" width="879" height="279" rx="6" fill="#0D1117" stroke="#21262D"/>
  <rect x="1" y="1" width="878" height="40" rx="5" fill="#010409"/>
  <line x1="1" y1="41" x2="879" y2="41" stroke="#21262D"/>

  <text x="20" y="26" fill="#F0F6FC" font-family="{FONT_MONO}" font-size="13" font-weight="700">CONTRIBUTION // 52W CALENDAR</text>
  <text x="858" y="26" text-anchor="end" fill="#39D353" font-family="{FONT_MONO}" font-size="11.5">{total_contrib} contributions / year</text>

  <text x="24" y="99" fill="#6E7681" font-family="{FONT_MONO}" font-size="10">Mon</text>
  <text x="24" y="129" fill="#6E7681" font-family="{FONT_MONO}" font-size="10">Wed</text>
  <text x="24" y="159" fill="#6E7681" font-family="{FONT_MONO}" font-size="10">Fri</text>

  {''.join(month_labels)}
  {''.join(cells)}

  <text x="716" y="191" fill="#6E7681" font-family="{FONT_MONO}" font-size="10">Less</text>
  {legend_boxes}
  <text x="828" y="191" fill="#6E7681" font-family="{FONT_MONO}" font-size="10">More</text>

  <line x1="20" y1="202" x2="860" y2="202" stroke="#21262D"/>
  <text x="24" y="232" fill="#C9D1D9" font-family="{FONT_MONO}" font-size="12" font-weight="700">MONTHLY_TOTALS</text>
  <text x="24" y="250" fill="#6E7681" font-family="{FONT_MONO}" font-size="10.5">last 6 months</text>
  {''.join(bars)}
</svg>
'''


def render_coding_profiles_svg(snapshot: dict[str, Any]) -> str:
    """Render hard-coded Competitive Programming Dashboard with embedded platform vector logos."""
    coding = snapshot["derived"]["coding"]
    lc = coding.get("leetcode") or {}
    sr = coding.get("skillrack") or {}
    cc = coding.get("codechef") or {}
    hr = coding.get("hackerrank") or {}
    updated = escape(str(snapshot.get("last_updated", "")))

    lc_total = int(lc.get("total_solved") or 0)
    lc_easy = int(lc.get("easy") or 0)
    lc_med = int(lc.get("medium") or 0)
    lc_hard = int(lc.get("hard") or 0)
    lc_denom = max(lc_total, 1)
    easy_w = max(6, round((lc_easy / lc_denom) * 230)) if lc_easy else 0
    med_w = max(6, round((lc_med / lc_denom) * 230)) if lc_med else 0
    hard_w = max(4, round((lc_hard / lc_denom) * 230)) if lc_hard else 0

    lc_rating = _fmt_int(lc.get("contest_rating"))
    lc_contests = _fmt_int(lc.get("contests_attended"))
    lc_top = f"top {lc['top_percentage']}%" if lc.get("top_percentage") is not None else "—"
    lc_streak = _fmt_int(lc.get("streak"))
    lc_rank = _fmt_int(lc.get("profile_ranking"))

    sr_solved = _fmt_int(sr.get("programs_solved"))
    sr_medals = _fmt_int(sr.get("bronze_medals"))
    sr_certs = _fmt_int(sr.get("certificates"))
    sr_rank = _fmt_int(sr.get("rank"))
    sr_langs = sr.get("languages") or {}
    sr_lang_str = "  ".join(f"{k}:{v}" for k, v in list(sr_langs.items())[:4]) or "C Java C++ Python"

    cc_solved = _fmt_int(cc.get("total_solved"))
    cc_rating = _fmt_int(cc.get("rating"))
    cc_high = _fmt_int(cc.get("highest_rating"))
    cc_contests = _fmt_int(cc.get("contests"))
    cc_stars = f"{cc['stars']}★" if cc.get("stars") else "—"

    hr_badges = hr.get("badges") or []
    hr_summary = " · ".join(f"{b['name']} ({b['solved']})" for b in hr_badges[:3]) or "SQL &amp; Java Certified"

    lc_logo = inline_logo_group("leetcode", 22, 56, size=18.0)
    sr_logo = inline_logo_group("skillrack", 468, 56, size=18.0)
    cc_logo = inline_logo_group("codechef", 468, 174, size=18.0)
    hr_logo = inline_logo_group("hackerrank", 468, 250, size=15.0)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 284" width="100%" role="img" aria-label="Competitive Programming Metrics">
  <rect x="0.5" y="0.5" width="879" height="283" rx="6" fill="#0D1117" stroke="#21262D"/>

  <!-- Top header bar -->
  <rect x="1" y="1" width="878" height="40" rx="5" fill="#010409"/>
  <line x1="1" y1="41" x2="879" y2="41" stroke="#21262D"/>
  <text x="22" y="26" fill="#F0F6FC" font-family="{FONT_MONO}" font-size="13" font-weight="700">PROBLEM_SOLVING // LIVE PLATFORM METRICS</text>
  <text x="858" y="26" text-anchor="end" fill="#6E7681" font-family="{FONT_MONO}" font-size="11">sync={updated}</text>

  <!-- Vertical column split -->
  <line x1="448" y1="41" x2="448" y2="283" stroke="#21262D"/>

  <!-- Left: LeetCode -->
  {lc_logo}
  <text x="48" y="70" fill="#F0F6FC" font-family="{FONT_MONO}" font-size="13.5" font-weight="700">LeetCode</text>
  <text x="426" y="70" text-anchor="end" fill="#FFA116" font-family="{FONT_MONO}" font-size="11.5">@{escape(str(lc.get("username", "PRAJEEN24")))}</text>

  <text x="22" y="114" fill="#F0F6FC" font-family="{FONT_MONO}" font-size="32" font-weight="700">{_fmt_int(lc_total)}</text>
  <text x="22" y="131" fill="#8B949E" font-family="{FONT_MONO}" font-size="11">SOLVED</text>

  <line x1="176" y1="88" x2="176" y2="134" stroke="#21262D"/>
  <text x="194" y="104" fill="#8B949E" font-family="{FONT_MONO}" font-size="11">CONTEST RATING ({lc_contests} contests)</text>
  <text x="194" y="126" fill="#FFA116" font-family="{FONT_MONO}" font-size="18" font-weight="700">{lc_rating} <tspan fill="#39D353" font-size="12">({escape(lc_top)})</tspan></text>

  <!-- E/M/H progress bars -->
  <text x="22" y="164" fill="#39D353" font-family="{FONT_MONO}" font-size="11.5">EASY</text>
  <rect x="94" y="155" width="230" height="8" rx="2" fill="#161B22"/>
  <rect x="94" y="155" width="{easy_w}" height="8" rx="2" fill="#39D353"/>
  <text x="426" y="164" text-anchor="end" fill="#C9D1D9" font-family="{FONT_MONO}" font-size="12">{lc_easy}</text>

  <text x="22" y="190" fill="#FBBF24" font-family="{FONT_MONO}" font-size="11.5">MEDIUM</text>
  <rect x="94" y="181" width="230" height="8" rx="2" fill="#161B22"/>
  <rect x="94" y="181" width="{med_w}" height="8" rx="2" fill="#FBBF24"/>
  <text x="426" y="190" text-anchor="end" fill="#C9D1D9" font-family="{FONT_MONO}" font-size="12">{lc_med}</text>

  <text x="22" y="216" fill="#FB7185" font-family="{FONT_MONO}" font-size="11.5">HARD</text>
  <rect x="94" y="207" width="230" height="8" rx="2" fill="#161B22"/>
  <rect x="94" y="207" width="{hard_w}" height="8" rx="2" fill="#FB7185"/>
  <text x="426" y="216" text-anchor="end" fill="#C9D1D9" font-family="{FONT_MONO}" font-size="12">{lc_hard}</text>

  <line x1="22" y1="238" x2="426" y2="238" stroke="#21262D"/>
  <text x="22" y="262" fill="#8B949E" font-family="{FONT_MONO}" font-size="11.5">streak={lc_streak}d  ·  rank=#{lc_rank}</text>

  <!-- Right Top: SkillRack -->
  {sr_logo}
  <text x="494" y="70" fill="#F0F6FC" font-family="{FONT_MONO}" font-size="13.5" font-weight="700">SkillRack</text>
  <text x="856" y="70" text-anchor="end" fill="#58A6FF" font-family="{FONT_MONO}" font-size="11.5">rank=#{sr_rank}</text>

  <text x="468" y="106" fill="#58A6FF" font-family="{FONT_MONO}" font-size="22" font-weight="700">{sr_solved}</text>
  <text x="468" y="122" fill="#8B949E" font-family="{FONT_MONO}" font-size="10.5">SOLVED</text>

  <text x="614" y="106" fill="#F0F6FC" font-family="{FONT_MONO}" font-size="20" font-weight="700">{sr_medals}</text>
  <text x="614" y="122" fill="#8B949E" font-family="{FONT_MONO}" font-size="10.5">BRONZE MEDALS</text>

  <text x="758" y="106" fill="#39D353" font-family="{FONT_MONO}" font-size="20" font-weight="700">{sr_certs}</text>
  <text x="758" y="122" fill="#8B949E" font-family="{FONT_MONO}" font-size="10.5">CERTS</text>

  <text x="468" y="144" fill="#8B949E" font-family="{FONT_MONO}" font-size="11">{escape(sr_lang_str)}</text>

  <!-- Right Middle: CodeChef -->
  <line x1="448" y1="158" x2="879" y2="158" stroke="#21262D"/>
  {cc_logo}
  <text x="494" y="188" fill="#F0F6FC" font-family="{FONT_MONO}" font-size="13.5" font-weight="700">CodeChef</text>
  <text x="856" y="188" text-anchor="end" fill="#D0C3B7" font-family="{FONT_MONO}" font-size="11.5">{escape(cc_stars)} · {cc_contests} contests</text>

  <text x="468" y="218" fill="#F0F6FC" font-family="{FONT_MONO}" font-size="20" font-weight="700">{cc_solved} <tspan fill="#8B949E" font-size="11" font-weight="400">solved</tspan></text>
  <text x="668" y="218" fill="#79C0FF" font-family="{FONT_MONO}" font-size="20" font-weight="700">{cc_rating} <tspan fill="#8B949E" font-size="11" font-weight="400">rating (peak {cc_high})</tspan></text>

  <!-- Right Bottom: HackerRank -->
  <line x1="448" y1="238" x2="879" y2="238" stroke="#21262D"/>
  {hr_logo}
  <text x="490" y="262" fill="#C9D1D9" font-family="{FONT_MONO}" font-size="11.5">{escape(hr_summary)}</text>
</svg>
'''


def write_all_svgs(svg_dir: Path, config: dict[str, Any], snapshot: dict[str, Any]) -> None:
    """Generate and write all portfolio SVG assets and platform logo icons."""
    svg_dir.mkdir(parents=True, exist_ok=True)
    write_logo_svgs(svg_dir / "logos")
    files = {
        "hero-banner.svg": render_hero_banner_svg(config),
        "github-stats.svg": render_github_stats_svg(snapshot),
        "contribution-heatmap.svg": render_contribution_heatmap_svg(snapshot),
        "coding-profiles.svg": render_coding_profiles_svg(snapshot),
    }
    for filename, content in files.items():
        (svg_dir / filename).write_text(content, encoding="utf-8")
