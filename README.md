# Aktoria CRM

Live, view-only copy of the Aktoria CRM: outbound DMs, inbound replies and calls, our posts, and competitor posts.

It reads the Aktoria Google Sheet (published to the web) and refreshes every minute. To change anything (mark DMs sent, book calls), use the CRM on claude.ai or the sheet itself.

The page is the Claude Design "Aktoria CRM" design (design export in `Desktop/Aktoria/design/`) wired to the sheet:
- `index.html` is generated: `python src/build_app.py` merges the design file with `src/logic.js` (page logic). Edit `src/logic.js`, not `index.html`.
- `data.js` loads the sheet (Sheets connector on claude.ai, the published CSVs elsewhere) and does every save (passcode-protected on this public page).
- `support.js` and `aktoria-tokens.css` come unchanged from the design.
- `legacy/` is the previous CRM, kept as a fallback.
