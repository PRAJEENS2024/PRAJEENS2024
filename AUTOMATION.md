# Profile README Automation Architecture

This repository powers an automatically updated GitHub Profile portfolio for **Prajeen S** (`PRAJEENS2024`). Every day at **06:00 PM IST (`12:30 UTC`)**, a GitHub Actions workflow collects verified statistics across GitHub and competitive programming platforms, renders self-hosted dark-terminal SVG dashboards, and updates only the designated marker sections in `README.md`.

## Directory Structure

```text
.
├── .github/workflows/update-readme.yml   # Daily cron + manual workflow_dispatch pipeline
├── assets/svg/                           # Self-hosted, zero-third-party-outage SVG dashboards
│   ├── hero-banner.svg
│   ├── github-stats.svg
│   ├── contribution-heatmap.svg
│   └── coding-profiles.svg
├── config/profile.yml                    # Usernames, theme tokens, and automation settings
├── data/stats_snapshot.json              # Last-known-good metrics cache & SHA-256 content hash
├── scripts/
│   ├── config_loader.py                  # Loads YAML config and runtime secrets from env
│   ├── fetchers/                         # Isolated API/profile fetchers with retry & backoff
│   │   ├── http_client.py
│   │   ├── github_fetcher.py
│   │   ├── leetcode_fetcher.py
│   │   ├── codechef_fetcher.py
│   │   ├── skillrack_fetcher.py
│   │   └── hackerrank_fetcher.py
│   ├── processors/
│   │   └── stats_processor.py            # Streaks, monthly totals, language share, idempotency hash
│   ├── generators/
│   │   ├── svg_generator.py              # Dark-themed SVG builders
│   │   └── readme_generator.py           # Marker-scoped README updater
│   └── main.py                           # CLI orchestrator & GitHub Actions step summary writer
└── tests/test_pipeline.py                # Automated test suite
```

## Marker-Scoped README Updates

The generator strictly modifies content between paired HTML comment markers in `README.md`:

- `<!-- AUTO-GENERATED-START: github-stats -->` ... `<!-- AUTO-GENERATED-END: github-stats -->`
- `<!-- AUTO-GENERATED-START: coding-stats -->` ... `<!-- AUTO-GENERATED-END: coding-stats -->`
- `<!-- AUTO-GENERATED-START: activity -->` ... `<!-- AUTO-GENERATED-END: activity -->`

All manually authored sections (About Me, Experience & Recognition, Technical Stack, Featured Projects) are left completely untouched.

## Data Sources & Reliability

| Platform | Integration Method | Notes |
| :--- | :--- | :--- |
| **GitHub** | GraphQL API (primary when token present) + REST API & public contributions calendar (fallback) | Tracks 12M contributions, streaks, active days, monthly velocity, language share, repos, stars, and recent public events. |
| **LeetCode** | Official GraphQL API (`https://leetcode.com/graphql`) | Tracks total solved, Easy/Medium/Hard breakdown, contest rating, contests attended, global ranking, top %, streak, and recent accepted submissions. |
| **SkillRack** | Public Resume Parser (`skillrack.com/faces/resume.xhtml`) | Tracks rank, programs solved, bronze medals, certificates, and language breakdown. |
| **CodeChef** | Public Profile Parser (`codechef.com/users/{username}`) | Tracks rating, highest rating, star tier, problems solved, and contests. |
| **HackerRank** | Public REST Badges API (`/rest/hackers/{username}/badges`) | Tracks verified domain badges and solved counts. |
| **GeeksforGeeks** | Direct profile link only | GFG renders profile stats client-side without an unauthenticated public API; rather than fabricating or shipping stale hardcoded numbers, it is linked directly. |

### Graceful Fallback & Idempotency

1. **Per-Platform Fault Isolation:** Each fetcher executes independently with exponential backoff (`http_client.py`). If a platform experiences a temporary outage or rate limit, its last valid entry in `data/stats_snapshot.json` is preserved (`cached_fallback`) and logged without breaking the build or wiping existing sections.
2. **Idempotent Commits:** `stats_processor.py` computes a deterministic SHA-256 `content_hash` over normalized metrics (excluding volatile timestamps). When metrics have not changed, `last_updated` stays unchanged, generated SVGs/README remain byte-identical, and the GitHub Actions workflow skips creating empty commits.

## Required & Optional GitHub Repository Secrets

- **`GITHUB_TOKEN` (Built-in, Required — No Manual Setup Needed):**
  Automatically provided by GitHub Actions. Used both for querying the GitHub GraphQL/REST API and committing updated files (`permissions: contents: write` is already configured in `update-readme.yml`).
- **`GH_STATS_TOKEN` (Optional Personal Access Token):**
  If you want GitHub GraphQL contribution counts to also include **private repository contributions** (or avoid anonymous rate limits during forks), create a fine-grained or classic PAT with `read:user` scope and add it under **Repository Settings → Secrets and variables → Actions → New repository secret** as `GH_STATS_TOKEN`. Without it, the workflow seamlessly uses the built-in `GITHUB_TOKEN`.

## Enabling & Testing Daily Automation

1. Push the updated repository to GitHub (`main` branch).
2. Open your repository **Actions** tab → ensure workflows are enabled.
3. Click **Daily Profile README Update** → **Run workflow** (`workflow_dispatch`) to trigger an immediate manual verification run.
4. Inspect the workflow logs and **Summary** table to confirm every platform reports `live`.

### Running Locally

```bash
pip install -r requirements.txt
python -m scripts.main --dry-run   # Verify API fetchers without modifying files
python -m scripts.main             # Regenerate SVGs, snapshot, and README markers
pytest -v                          # Run unit & integration tests
```
