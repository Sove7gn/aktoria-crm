# Aktoria CRM

Live, view-only copy of the Aktoria CRM: outbound DMs, inbound replies and calls, our posts, and competitor posts.

It reads the Aktoria Google Sheet (published to the web) and refreshes every minute. To change anything (mark DMs sent, book calls), use the CRM on claude.ai or the sheet itself.

To update this page after the CRM changes: `python build.py <path to aktoria-crm.html>`, then commit and push.
