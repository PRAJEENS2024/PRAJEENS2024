"""Dark-themed SVG generators for GitHub Profile portfolio visualizations."""

from __future__ import annotations

from datetime import date
from html import escape
from pathlib import Path
from typing import Any

FONT_SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif"
FONT_MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"

HEATMAP_COLORS = ["#161B22", "#0E4429", "#006D32", "#26A641", "#39D353"]


def _fmt_int(value: int | float | None, default: str = "—") -> str:
    if value is None:
        return default
    return f"{int(round(value)):,}"


def render_hero_banner_svg(config: dict[str, Any]) -> str:
    """Render the custom dark-mode developer portfolio hero banner SVG."""
    profile = config.get("profile", {})
    name = escape(profile.get("name", "Prajeen S"))
    headline = escape(
        profile.get(
            "headline",
            "Full Stack Developer · Multi-Agent AI Builder · Competitive Programmer",
        )
    )
    tagline = escape(
        profile.get(
            "tagline",
            "B.E. Electronics & Communication Engineering '28 · Sri Eshwar College of Engineering",
        )
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 216" width="100%" role="img" aria-label="{name} Developer Portfolio Banner">
  <defs>
    <linearGradient id="heroBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090D16"/>
      <stop offset="55%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#0D1117"/>
    </linearGradient>
    <linearGradient id="accentBar" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="50%" stop-color="#818CF8"/>
      <stop offset="100%" stop-color="#34D399"/>
    </linearGradient>
    <radialGradient id="glowCyan" cx="85%" cy="22%" r="45%">
      <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#38BDF8" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowIndigo" cx="15%" cy="85%" r="45%">
      <stop offset="0%" stop-color="#818CF8" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#818CF8" stop-opacity="0"/>
    </radialGradient>
    <pattern id="dotGrid" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#30363D" fill-opacity="0.45"/>
    </pattern>
  </defs>

  <rect x="0.5" y="0.5" width="879" height="215" rx="14" fill="url(#heroBg)" stroke="#30363D"/>
  <rect x="1" y="1" width="878" height="214" rx="14" fill="url(#dotGrid)"/>
  <rect x="1" y="1" width="878" height="214" rx="14" fill="url(#glowCyan)"/>
  <rect x="1" y="1" width="878" height="214" rx="14" fill="url(#glowIndigo)"/>
  <rect x="24" y="0" width="832" height="3" rx="1.5" fill="url(#accentBar)"/>

  <!-- Top status pill -->
  <rect x="34" y="26" width="248" height="26" rx="13" fill="#161B22" stroke="#30363D"/>
  <circle cx="50" cy="39" r="4.5" fill="#34D399">
    <animate attributeName="opacity" values="1;0.35;1" dur="2.4s" repeatCount="indefinite"/>
  </circle>
  <text x="63" y="43" fill="#CBD5E1" font-family="{FONT_MONO}" font-size="11.5" font-weight="600">OPEN TO SWE &amp; FULL-STACK ROLES</text>

  <!-- Right subtle circuit motif -->
  <g stroke="#38BDF8" stroke-opacity="0.28" stroke-width="1.3" fill="none">
    <path d="M720 44 H786 L802 60 H842"/>
    <path d="M746 72 H812 L826 86 H842"/>
    <path d="M700 100 H766 L782 84 H810"/>
    <circle cx="720" cy="44" r="3" fill="#38BDF8" fill-opacity="0.45"/>
    <circle cx="746" cy="72" r="3" fill="#818CF8" fill-opacity="0.45"/>
    <circle cx="700" cy="100" r="3" fill="#34D399" fill-opacity="0.45"/>
    <circle cx="842" cy="60" r="3" fill="#38BDF8" fill-opacity="0.45"/>
  </g>

  <!-- Primary Display Name -->
  <text x="34" y="96" fill="#F8FAFC" font-family="{FONT_SANS}" font-size="40" font-weight="800" letter-spacing="-0.8">{name}</text>

  <!-- Headline -->
  <text x="34" y="128" fill="#38BDF8" font-family="{FONT_SANS}" font-size="16" font-weight="600">{headline}</text>

  <!-- Tagline -->
  <text x="34" y="152" fill="#94A3B8" font-family="{FONT_SANS}" font-size="13">{tagline}</text>

  <!-- Bottom credential chips -->
  <g font-family="{FONT_MONO}" font-size="11">
    <rect x="34" y="170" width="212" height="26" rx="6" fill="#161B22" stroke="#30363D"/>
    <text x="46" y="187" fill="#E2E8F0">Former MERN Intern @ AlgoTutor</text>

    <rect x="256" y="170" width="206" height="26" rx="6" fill="#161B22" stroke="#30363D"/>
    <text x="268" y="187" fill="#E2E8F0">MERN · Django · TypeScript · AI</text>

    <rect x="472" y="170" width="164" height="26" rx="6" fill="#161B22" stroke="#30363D"/>
    <text x="484" y="187" fill="#E2E8F0">Coimbatore, India</text>
  </g>
</svg>
'''


def render_github_stats_svg(snapshot: dict[str, Any]) -> str:
    """Render custom dark-themed GitHub Engineering Stats & Top Languages SVG."""
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
            f"Commits: {_fmt_int(gh['commits'])}  ·  "
            f"PRs: {_fmt_int(gh.get('pull_requests', 0))}  ·  "
            f"Issues: {_fmt_int(gh.get('issues', 0))}  ·  "
            f"Reviews: {_fmt_int(gh.get('reviews', 0))}"
        )
    else:
        mix_text = (
            f"Stars: {total_stars}  ·  "
            f"Forks: {total_forks}  ·  "
            f"Followers: {_fmt_int(gh.get('followers', 0))}  ·  "
            f"Source: Public GitHub API"
        )

    # Top Languages stacked progress bar (width = 368px)
    langs = gh.get("top_languages") or []
    bar_x = 478.0
    bar_w = 368.0
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
            f'<rect x="{cursor_x:.1f}" y="86" width="{seg_w:.1f}" height="12" fill="{color}"/>'
        )
        cursor_x += seg_w

    legend_items: list[str] = []
    for idx, lang in enumerate(langs[:6]):
        col = idx % 2
        row = idx // 2
        lx = 478 + col * 190
        ly = 126 + row * 34
        color = escape(str(lang.get("color", "#8B949E")))
        lname = escape(str(lang["name"]))
        lpct = f"{lang['percent']}%"
        legend_items.append(
            f'<circle cx="{lx + 6}" cy="{ly - 4}" r="5" fill="{color}"/>'
            f'<text x="{lx + 18}" y="{ly}" fill="#E6EDF3" font-family="{FONT_SANS}" font-size="12.5" font-weight="600">{lname}</text>'
            f'<text x="{lx + 174}" y="{ly}" text-anchor="end" fill="#8B949E" font-family="{FONT_MONO}" font-size="12">{lpct}</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 264" width="100%" role="img" aria-label="GitHub Engineering Stats for {username}">
  <defs>
    <clipPath id="langBarClip">
      <rect x="478" y="86" width="368" height="12" rx="6"/>
    </clipPath>
  </defs>

  <rect x="0.5" y="0.5" width="879" height="263" rx="14" fill="#0D1117" stroke="#30363D"/>

  <!-- Left Card: GitHub Overview -->
  <rect x="18" y="18" width="424" height="228" rx="10" fill="#161B22" stroke="#262C36"/>
  <text x="36" y="46" fill="#F0F6FC" font-family="{FONT_SANS}" font-size="15" font-weight="700">GitHub Engineering Metrics</text>
  <text x="424" y="46" text-anchor="end" fill="#38BDF8" font-family="{FONT_MONO}" font-size="11.5">@{username}</text>
  <line x1="36" y1="58" x2="424" y2="58" stroke="#262C36"/>

  <!-- 2x2 Metric Tiles -->
  <rect x="36" y="72" width="186" height="58" rx="8" fill="#0D1117" stroke="#262C36"/>
  <text x="50" y="94" fill="#8B949E" font-family="{FONT_SANS}" font-size="11.5">Contributions (12M)</text>
  <text x="50" y="118" fill="#38BDF8" font-family="{FONT_MONO}" font-size="22" font-weight="700">{total_contrib}</text>

  <rect x="238" y="72" width="186" height="58" rx="8" fill="#0D1117" stroke="#262C36"/>
  <text x="252" y="94" fill="#8B949E" font-family="{FONT_SANS}" font-size="11.5">Current / Best Streak</text>
  <text x="252" y="118" fill="#34D399" font-family="{FONT_MONO}" font-size="22" font-weight="700">{current_streak}d <tspan fill="#64748B" font-size="14">/ {longest_streak}d</tspan></text>

  <rect x="36" y="142" width="186" height="58" rx="8" fill="#0D1117" stroke="#262C36"/>
  <text x="50" y="164" fill="#8B949E" font-family="{FONT_SANS}" font-size="11.5">Public Repositories</text>
  <text x="50" y="188" fill="#F0F6FC" font-family="{FONT_MONO}" font-size="22" font-weight="700">{public_repos}</text>

  <rect x="238" y="142" width="186" height="58" rx="8" fill="#0D1117" stroke="#262C36"/>
  <text x="252" y="164" fill="#8B949E" font-family="{FONT_SANS}" font-size="11.5">Active Days (12M)</text>
  <text x="252" y="188" fill="#818CF8" font-family="{FONT_MONO}" font-size="22" font-weight="700">{active_days}</text>

  <text x="36" y="226" fill="#8B949E" font-family="{FONT_MONO}" font-size="11">{escape(mix_text)}</text>

  <!-- Right Card: Language Footprint -->
  <rect x="458" y="18" width="404" height="228" rx="10" fill="#161B22" stroke="#262C36"/>
  <text x="478" y="46" fill="#F0F6FC" font-family="{FONT_SANS}" font-size="15" font-weight="700">Language Footprint</text>
  <text x="844" y="46" text-anchor="end" fill="#8B949E" font-family="{FONT_MONO}" font-size="11">By Repo Codebase</text>
  <line x1="478" y1="58" x2="844" y2="58" stroke="#262C36"/>

  <rect x="478" y="86" width="368" height="12" rx="6" fill="#0D1117"/>
  <g clip-path="url(#langBarClip)">
    {''.join(bar_segments)}
  </g>

  {''.join(legend_items)}

  <text x="478" y="226" fill="#64748B" font-family="{FONT_MONO}" font-size="10.5">Synced: {updated} · Auto-updated daily via GitHub Actions</text>
</svg>
'''


def render_contribution_heatmap_svg(snapshot: dict[str, Any]) -> str:
    """Render 52-week contribution heatmap + 6-month velocity bar chart SVG."""
    gh = snapshot["derived"]["github"]
    days = sorted(gh.get("calendar_days") or [], key=lambda d: d["date"])
    monthly = gh.get("monthly_contributions") or []
    total_contrib = _fmt_int(gh.get("total_contributions", 0))

    # Build grid aligned by Sunday..Saturday rows (0..6)
    cells: list[str] = []
    month_labels: list[str] = []
    seen_months: set[tuple[int, str]] = set()
    last_labeled_col = -4

    if days:
        first_dt = date.fromisoformat(days[0]["date"])
        # Python weekday(): Mon=0..Sun=6 -> Sun=0..Sat=6
        first_sun_offset = (first_dt.weekday() + 1) % 7
        # Keep up to last 53 weeks
        for idx, d in enumerate(days):
            dt = date.fromisoformat(d["date"])
            pos = idx + first_sun_offset
            col = pos // 7
            row = pos % 7
            if col >= 53:
                continue
            x = 56 + col * 14.8
            y = 66 + row * 14.8
            level = max(0, min(4, int(d.get("level", 0))))
            fill = HEATMAP_COLORS[level]
            count = int(d.get("count", 0))
            cells.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="11.5" height="11.5" rx="2.5" fill="{fill}">'
                f'<title>{escape(d["date"])}: {count} contribution(s)</title></rect>'
            )
            if dt.day <= 7 and row == 0:
                m_lbl = dt.strftime("%b")
                if col - last_labeled_col >= 3 and (col, m_lbl) not in seen_months:
                    seen_months.add((col, m_lbl))
                    last_labeled_col = col
                    month_labels.append(
                        f'<text x="{x:.1f}" y="56" fill="#8B949E" font-family="{FONT_MONO}" font-size="10.5">{m_lbl}</text>'
                    )

    # 6-Month Bar Chart at bottom (y=194..264)
    bars: list[str] = []
    if monthly:
        max_m = max((m["count"] for m in monthly), default=1) or 1
        bar_area_x = 190
        step = 110
        for i, m in enumerate(monthly[-6:]):
            bx = bar_area_x + i * step
            val = int(m["count"])
            bh = max(4, round((val / max_m) * 44)) if val > 0 else 2
            by = 246 - bh
            bars.append(
                f'<rect x="{bx}" y="{by}" width="44" height="{bh}" rx="4" fill="#38BDF8" fill-opacity="0.85"/>'
                f'<text x="{bx + 22}" y="{by - 5}" text-anchor="middle" fill="#E2E8F0" font-family="{FONT_MONO}" font-size="10.5">{val}</text>'
                f'<text x="{bx + 22}" y="263" text-anchor="middle" fill="#8B949E" font-family="{FONT_MONO}" font-size="11">{escape(m["label"])}</text>'
            )

    legend_boxes = "".join(
        f'<rect x="{748 + i * 16}" y="176" width="11" height="11" rx="2.5" fill="{c}"/>'
        for i, c in enumerate(HEATMAP_COLORS)
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 284" width="100%" role="img" aria-label="GitHub Contribution Heatmap and Monthly Velocity">
  <rect x="0.5" y="0.5" width="879" height="283" rx="14" fill="#0D1117" stroke="#30363D"/>
  <rect x="18" y="16" width="844" height="252" rx="10" fill="#161B22" stroke="#262C36"/>

  <text x="34" y="39" fill="#F0F6FC" font-family="{FONT_SANS}" font-size="14.5" font-weight="700">Contribution Consistency &amp; Activity Calendar</text>
  <text x="844" y="39" text-anchor="end" fill="#34D399" font-family="{FONT_MONO}" font-size="11.5">{total_contrib} contributions in the last year</text>

  <!-- Day labels -->
  <text x="32" y="91" fill="#64748B" font-family="{FONT_MONO}" font-size="10">Mon</text>
  <text x="32" y="121" fill="#64748B" font-family="{FONT_MONO}" font-size="10">Wed</text>
  <text x="32" y="151" fill="#64748B" font-family="{FONT_MONO}" font-size="10">Fri</text>

  {''.join(month_labels)}
  {''.join(cells)}

  <text x="716" y="185" fill="#64748B" font-family="{FONT_MONO}" font-size="10">Less</text>
  {legend_boxes}
  <text x="832" y="185" fill="#64748B" font-family="{FONT_MONO}" font-size="10">More</text>

  <line x1="34" y1="196" x2="844" y2="196" stroke="#262C36"/>
  <text x="34" y="224" fill="#E6EDF3" font-family="{FONT_SANS}" font-size="13" font-weight="600">Monthly Velocity</text>
  <text x="34" y="242" fill="#8B949E" font-family="{FONT_SANS}" font-size="11">Last 6 months</text>
  {''.join(bars)}
</svg>
'''


def render_coding_profiles_svg(snapshot: dict[str, Any]) -> str:
    """Render Competitive Programming Dashboard SVG (LeetCode, SkillRack, CodeChef, HackerRank)."""
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
    easy_w = max(8, round((lc_easy / lc_denom) * 230)) if lc_easy else 0
    med_w = max(8, round((lc_med / lc_denom) * 230)) if lc_med else 0
    hard_w = max(6, round((lc_hard / lc_denom) * 230)) if lc_hard else 0

    lc_rating = _fmt_int(lc.get("contest_rating"))
    lc_contests = _fmt_int(lc.get("contests_attended"))
    lc_top = f"Top {lc['top_percentage']}%" if lc.get("top_percentage") is not None else "—"
    lc_streak = _fmt_int(lc.get("streak"))
    lc_rank = _fmt_int(lc.get("profile_ranking"))

    sr_solved = _fmt_int(sr.get("programs_solved"))
    sr_medals = _fmt_int(sr.get("bronze_medals"))
    sr_certs = _fmt_int(sr.get("certificates"))
    sr_rank = _fmt_int(sr.get("rank"))
    sr_langs = sr.get("languages") or {}
    sr_lang_str = " · ".join(f"{k}: {v}" for k, v in list(sr_langs.items())[:4]) or "C · Java · C++ · Python"

    cc_solved = _fmt_int(cc.get("total_solved"))
    cc_rating = _fmt_int(cc.get("rating"))
    cc_high = _fmt_int(cc.get("highest_rating"))
    cc_contests = _fmt_int(cc.get("contests"))
    cc_stars = f"{cc['stars']}★" if cc.get("stars") else "—"

    hr_badges = hr.get("badges") or []
    hr_summary = " · ".join(f"{b['name']} ({b['solved']} solved)" for b in hr_badges[:3]) or "SQL &amp; Java Certified"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 302" width="100%" role="img" aria-label="Competitive Programming Dashboard">
  <rect x="0.5" y="0.5" width="879" height="301" rx="14" fill="#0D1117" stroke="#30363D"/>

  <!-- Left Hero Panel: LeetCode -->
  <rect x="18" y="18" width="414" height="266" rx="10" fill="#161B22" stroke="#262C36"/>
  <circle cx="38" cy="40" r="6" fill="#FFA116"/>
  <text x="52" y="45" fill="#F0F6FC" font-family="{FONT_SANS}" font-size="15.5" font-weight="700">LeetCode</text>
  <text x="414" y="45" text-anchor="end" fill="#FFA116" font-family="{FONT_MONO}" font-size="11.5">@{escape(str(lc.get("username", "PRAJEEN24")))}</text>
  <line x1="36" y1="58" x2="414" y2="58" stroke="#262C36"/>

  <!-- Total Solved & Contest Rating -->
  <text x="36" y="96" fill="#F8FAFC" font-family="{FONT_MONO}" font-size="34" font-weight="800">{_fmt_int(lc_total)}</text>
  <text x="36" y="114" fill="#8B949E" font-family="{FONT_SANS}" font-size="12">Problems Solved</text>

  <rect x="216" y="72" width="198" height="46" rx="8" fill="#0D1117" stroke="#262C36"/>
  <text x="230" y="91" fill="#8B949E" font-family="{FONT_SANS}" font-size="11">Contest Rating ({lc_contests} contests)</text>
  <text x="230" y="110" fill="#FFA116" font-family="{FONT_MONO}" font-size="16" font-weight="700">{lc_rating} <tspan fill="#34D399" font-size="12">({escape(lc_top)})</tspan></text>

  <!-- Easy / Medium / Hard Bars -->
  <text x="36" y="148" fill="#34D399" font-family="{FONT_SANS}" font-size="12" font-weight="600">Easy</text>
  <rect x="108" y="138" width="230" height="10" rx="5" fill="#0D1117"/>
  <rect x="108" y="138" width="{easy_w}" height="10" rx="5" fill="#34D399"/>
  <text x="414" y="148" text-anchor="end" fill="#E2E8F0" font-family="{FONT_MONO}" font-size="12">{lc_easy}</text>

  <text x="36" y="176" fill="#FBBF24" font-family="{FONT_SANS}" font-size="12" font-weight="600">Medium</text>
  <rect x="108" y="166" width="230" height="10" rx="5" fill="#0D1117"/>
  <rect x="108" y="166" width="{med_w}" height="10" rx="5" fill="#FBBF24"/>
  <text x="414" y="176" text-anchor="end" fill="#E2E8F0" font-family="{FONT_MONO}" font-size="12">{lc_med}</text>

  <text x="36" y="204" fill="#FB7185" font-family="{FONT_SANS}" font-size="12" font-weight="600">Hard</text>
  <rect x="108" y="194" width="230" height="10" rx="5" fill="#0D1117"/>
  <rect x="108" y="194" width="{hard_w}" height="10" rx="5" fill="#FB7185"/>
  <text x="414" y="204" text-anchor="end" fill="#E2E8F0" font-family="{FONT_MONO}" font-size="12">{lc_hard}</text>

  <line x1="36" y1="226" x2="414" y2="226" stroke="#262C36"/>
  <text x="36" y="248" fill="#8B949E" font-family="{FONT_MONO}" font-size="11.5">Streak: <tspan fill="#F0F6FC" font-weight="700">{lc_streak}d</tspan>  ·  Global Rank: <tspan fill="#F0F6FC" font-weight="700">#{lc_rank}</tspan></text>
  <text x="36" y="268" fill="#64748B" font-family="{FONT_MONO}" font-size="10.5">Live via LeetCode GraphQL · Synced {updated}</text>

  <!-- Right Top Panel: SkillRack -->
  <rect x="448" y="18" width="414" height="126" rx="10" fill="#161B22" stroke="#262C36"/>
  <circle cx="468" cy="40" r="6" fill="#38BDF8"/>
  <text x="482" y="45" fill="#F0F6FC" font-family="{FONT_SANS}" font-size="15" font-weight="700">SkillRack</text>
  <text x="844" y="45" text-anchor="end" fill="#38BDF8" font-family="{FONT_MONO}" font-size="11.5">Rank #{sr_rank}</text>
  <line x1="466" y1="56" x2="844" y2="56" stroke="#262C36"/>

  <text x="466" y="88" fill="#38BDF8" font-family="{FONT_MONO}" font-size="24" font-weight="800">{sr_solved}</text>
  <text x="466" y="104" fill="#8B949E" font-family="{FONT_SANS}" font-size="11">Programs Solved</text>

  <text x="612" y="88" fill="#F0F6FC" font-family="{FONT_MONO}" font-size="20" font-weight="700">{sr_medals}</text>
  <text x="612" y="104" fill="#8B949E" font-family="{FONT_SANS}" font-size="11">Bronze Medals</text>

  <text x="748" y="88" fill="#34D399" font-family="{FONT_MONO}" font-size="20" font-weight="700">{sr_certs}</text>
  <text x="748" y="104" fill="#8B949E" font-family="{FONT_SANS}" font-size="11">Certificates</text>

  <text x="466" y="128" fill="#94A3B8" font-family="{FONT_MONO}" font-size="11">{escape(sr_lang_str)}</text>

  <!-- Right Bottom Panel: CodeChef & HackerRank -->
  <rect x="448" y="158" width="414" height="126" rx="10" fill="#161B22" stroke="#262C36"/>
  <circle cx="468" cy="180" r="6" fill="#818CF8"/>
  <text x="482" y="185" fill="#F0F6FC" font-family="{FONT_SANS}" font-size="15" font-weight="700">CodeChef &amp; HackerRank</text>
  <text x="844" y="185" text-anchor="end" fill="#818CF8" font-family="{FONT_MONO}" font-size="11.5">{escape(cc_stars)} · {cc_contests} Contests</text>
  <line x1="466" y1="196" x2="844" y2="196" stroke="#262C36"/>

  <text x="466" y="226" fill="#F0F6FC" font-family="{FONT_MONO}" font-size="22" font-weight="800">{cc_solved}</text>
  <text x="466" y="242" fill="#8B949E" font-family="{FONT_SANS}" font-size="11">CodeChef Solved</text>

  <text x="612" y="226" fill="#818CF8" font-family="{FONT_MONO}" font-size="22" font-weight="800">{cc_rating}</text>
  <text x="612" y="242" fill="#8B949E" font-family="{FONT_SANS}" font-size="11">Rating (Peak {cc_high})</text>

  <text x="466" y="268" fill="#34D399" font-family="{FONT_MONO}" font-size="11">HackerRank: <tspan fill="#CBD5E1">{escape(hr_summary)}</tspan></text>
</svg>
'''


def write_all_svgs(svg_dir: Path, config: dict[str, Any], snapshot: dict[str, Any]) -> None:
    """Generate and write all portfolio SVG assets."""
    svg_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "hero-banner.svg": render_hero_banner_svg(config),
        "github-stats.svg": render_github_stats_svg(snapshot),
        "contribution-heatmap.svg": render_contribution_heatmap_svg(snapshot),
        "coding-profiles.svg": render_coding_profiles_svg(snapshot),
    }
    for filename, content in files.items():
        (svg_dir / filename).write_text(content, encoding="utf-8")
