# Design brief: Aktoria CRM

Design a clean, calm web app for the Aktoria growth team. It's an internal CRM plus content dashboard for an agency running X (Twitter) growth and outbound for Aktoria Robotics (YC S26). Aktoria is a teleoperation company: it supplies software and trained remote operators who take over robots when they get stuck, and it collects teleoperation data that it sells to labs training robot foundation models.

The app already exists and works; the data comes live from a Google Sheet. I need a better design: layout, navigation, components and visual system. The engineering stays as it is.

## Who uses it
- **The agency team** (3–4 people, daily, on laptops and phones): send DMs, track posts, schedule content.
- **Aktoria's two founders** (view only, a few times a week): want to see at a glance what's going out, what's working and who replied.
- Nobody is technical. Every label must be plain English. No jargon, no acronyms without words, no "MQL / SQL / ICP" in the UI.

## House style (must keep)
- White background, near-black text, one accent colour per section (Outbound blue, Inbound green, Midbound purple). Calm, editorial, lots of whitespace, nothing flashy. Geist / Geist Mono are fine.
- **At most 10 rows per screen** before "Show more". Keep screens short.
- Works on a phone (375px): no sideways scrolling on the main layout; tables can scroll inside their own box.
- Every screen answers "what do I do next?" at the top.

## Navigation (current structure, please improve)
- **Home**: today at a glance.
- **Outbound** (DMs we send): *Send today*, *Pipeline*. Pipeline has tabs inside: Board · People · Companies · DM templates.
- **Inbound** (replies and calls): *Replies*, *Calls*.
- **Midbound** (posts that warm buyers up): *Calendar*, *Our posts*, *Post tracker*, *People to DM*, *Competitors*. Our posts has Posts · Photos tabs; Competitors has Competitors · All their posts tabs.
- **Top bar**: an owner switch (Everyone / Karan / Shreenabh / Aktoria company page), search, and a "View only · updated 10:42" status with an "Open sheet" link.

## Screens and what's on them

**Home**
- Date header.
- Three section cards (Outbound: to send today and follow-ups due; Inbound: replies waiting and calls booked; Midbound: posts planned and new competitor posts).
- A "Do these first" list (replies, then follow-ups due, then calls).
- "Competitors posted something new" alerts.
- Founder questions waiting for a WhatsApp answer, with a copy button.
- Pilot goals progress (followers per account vs 1,000 target; inbound inquiries per week).

**Send today (Outbound)**
- The latest day's X DMs: sent count, couldn't-send count and reason (for example "their DMs need a passcode"), and per-account progress like "Shreenabh 30 of 30".
- Groups below: Follow-ups due, Send today, Find their handle first.
- Each person row: name, company, role, funding stage pill (Series B, Public, Seed: skip…), next step pill, and quick actions (Copy message · Mark sent).

**Pipeline**
- *Board*: kanban columns To send → Sent → Follow-up 1 sent → Follow-up 2 sent → Replied → Call booked → Customer, plus Closed. Drag to change stage. Empty follow-up columns are hidden.
- *People*: a sortable table (Priority, Name + role, Company, Funding stage, Owner, Channel, Stage, Next step, Fit, Likely to buy) with filters (stage, next step, type, channel, funding: Series A or later / Seed or pre-seed / Unknown).
- *Companies*: one row per company with all its contacts and the furthest stage reached.
- *DM templates*: each template's opener and 2 follow-ups, and its sent, replies, reply rate and verdict ("Need 10+ sends", "Double down", "Rewrite"). A/B test versions (e.g. S2 / S2B / S2C) sit side by side.
- *Contact panel* (slides in from the right): stage selector and next-step buttons, how to reach them (LinkedIn, X), "Most likely to buy from Aktoria", the DM result, funding stage with source, why now, the messages (first message, follow-up 1 "not yet, send on 31 Oct", follow-up 2) with Copy buttons, a dates timeline, a call date picker and notes.

**Replies / Calls (Inbound)**
- Lists of people who replied (reply now) and calls booked (prep the call), each with the contact panel.

**Calendar (Midbound)**
- Week view: rows are accounts, columns are Mon–Sun.
- Each cell lists that day's posts with time, first line and a status pill (Posted / Scheduled / To post), plus "3 of 5" against the 5-a-day target.
- Previous / This week / Next week controls.

**Our posts**
- Tabs: To post · Scheduled · Posted · Later.
- Each post card shows **side by side**: the competitor's original (who, rank like "#1 of 13 for Adamo", their views and likes) and our version (account, time, status, our numbers once live), plus "What we changed", media needed with a Drive folder link, and any founder question.
- Buttons: Copy our version · Mark as scheduled · Mark as posted (paste the X link) · "It's live: add the link".
- A full-screen side-by-side view.
- Below: "10 best posts to copy next" (the biggest posts in the space by views).

**Post tracker**
- Totals: posts tracked, views, engagement, engagement per 1K views, people to DM.
- "This week" grid: accounts × Mon–Fri cells coloured green, yellow or red (5 posts and engagement up / fewer posts or flat / nothing posted or engagement down by more than half).
- Traction charts: total views over time, followers per account vs the 1,000 goal.
- "What did well and why": the top 3 posts with plain reasons ("1.4× Shreenabh's usual engagement", "copies Maxinsights' #1 post", "3 reposts").
- "Patterns so far": best post type, account and hour.
- "Every post" table with a sparkline trend and "+230 since last check".

**People to DM**
- People who replied to or quoted our posts, robotics people first.
- Each card: name, handle, followers, fit (Robotics leader / Robotics / Investor / Other / Not a buyer), DMs open, their bio, what they said and on which post, a ready message with Copy, links, and Mark messaged.
- Tabs: To message · Messaged · All.

**Competitors**
- About 35 accounts grouped by how close they are (same thing as us / overlaps on data / overlaps on software / big robotics account like Figure, Unitree, Tesla Optimus).
- Each competitor page: followers, posting rate, typical engagement, best post type, and a **graph**. Their 6 biggest posts sit in a row across the top, each with an arrow down to our copy of it (account, status, our views), or an empty dashed circle "Not copied yet". Below that: their best posts of all time, latest posts, who runs it, and our copies.
- "All their posts": a filterable list of ~600 competitor posts with rank pills and engagement.

## What I'd like from you
1. A visual system: colour tokens (light theme only is fine), type scale, spacing, radii, and components (nav, sub-tabs, KPI tiles, tables, pills/status chips, list rows, cards, the side-by-side post comparison, the contact panel, kanban cards, the week grid, the calendar cell, the graph view, empty states, toasts, buttons).
2. Designs for Home, Send today, Pipeline (Board + People + contact panel), Calendar, Our posts (card + full-screen compare), Post tracker, People to DM, and a Competitor page with the graph. Each at desktop (1280px) and phone (375px).
3. Ideas to cut noise: what to merge, hide behind a click, or drop. The team's main complaint is "too much noise". Home and Send today should feel like a to-do list, not a dashboard.
4. Deliver as HTML/CSS (one file or a small design system file plus page mockups) using CSS custom properties for every colour and size, so I can drop it into the existing app.
