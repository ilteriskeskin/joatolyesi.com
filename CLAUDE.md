# Joryu — Project Instructions

## What this is
Practice tracking + structured training platform for solo martial artists
(jo, bokken, kata practitioners — aikido/iaido/kobudo). Side project of
İlteriş Keskin (@joryu.art). Goal: supplemental income via freemium
subscriptions, one-time digital programs, and equipment affiliate links.

Read BRIEF.md before starting any task. It contains the full business plan,
current phase, and landing page spec. TODO.md tracks known gaps, launch
blockers, and the feature roadmap — check it before proposing new work.

## Current phase
Phase 1: App MVP. Phase 0 (landing + waitlist) shipped and stays live at `/`.
In scope now:
- User accounts: email + password, signed session cookie (no OAuth, no magic links)
- Daily practice log + streak (free tier)
- Kata & suburi video library (a few free, rest Pro)
- 30-day structured program engine (Pro)
- Pro subscription via Lemon Squeezy hosted checkout + webhooks
  (no card data touches our server, no LS API calls — buy links + webhooks only)
- PWA: manifest + service worker (installable, basic offline shell)
- Profiles & community ("GitHub for martial artists"): username, bio,
  discipline (branş), opt-in public profile with practice stats + activity
  heatmap, practitioner search. Public pages viewable logged-out.
- Kata library defaults to the user's discipline, switchable to others/all
Schema changes go through Alembic migrations from now on (no create_all).

## Stack
- Backend: FastAPI (Python 3.12), PostgreSQL, SQLAlchemy 2.x, Alembic
- Frontend: HTMX + Alpine.js, Tailwind CSS (CDN is fine for Phase 0)
- Templates: Jinja2
- Deploy target: single VPS with Docker Compose (owner is a DevOps engineer;
  keep Dockerfile + compose.yml simple and production-ready)
- No React, no Next.js, no SPA frameworks. Keep it server-rendered.

## Conventions
- Type hints everywhere, Pydantic v2 models for all request/response schemas
- Async SQLAlchemy sessions; never block the event loop (owner has been
  burned by this in production — no sync HTTP calls inside async routes)
- Env config via pydantic-settings; every field must have a matching env var
  documented in .env.example
- Keep dependencies minimal. Justify every new package.
- Turkish comments are fine; code identifiers in English.

## i18n
Two languages from day one: Turkish (primary/default) and English.
Simple approach for Phase 0: one template, strings from a dict/JSON per
locale, ?lang= query param + cookie. No heavyweight i18n library.

## Style / brand
- Dark, atmospheric, minimal — matches @joryu.art content aesthetic
  (dojo at dusk, wood, ink). Not a generic SaaS gradient template.
- Fonts: one serif display + one clean sans. No emoji in UI.
- Mobile-first: traffic comes from Instagram/TikTok bio links.

## What NOT to do
- No native app — PWA only
- No one-time program sales yet (subscription first; one-time comes later)
- No equipment affiliate pages yet
- No email sending (verification, reminders) yet — collect and store only
- Analytics is Google Analytics 4 (G-54NX2S2Z01), gtag in base + landing;
  don't add other trackers
- Don't add features not in BRIEF.md without asking
