"""Build aktoria-crm-site/index.html from the Claude Design file (export lives in Desktop/Aktoria/design/).

The design markup, styles and runtime stay as designed. This script only:
- adds the document head bits (title, robots), data.js and the page logic (logic.js, inlined);
- replaces the design's sample-data script with a one-line hand-off to that logic;
- swaps the few hard-coded sample texts in the template for bindings, and adds the few slots the real data needs
  (connection notice, DM pause note and Pause/Resume button, "show more" buttons, empty states, save-on-blur for notes and call date).
Every replacement must match exactly once, so a changed design fails loudly instead of silently.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = r"C:\Users\Reyansh\Desktop\Aktoria\design\Aktoria CRM.dc.html"
OUT = os.path.join(os.path.dirname(HERE), "index.html")  # the site root, served by GitHub Pages

src = open(DESIGN, encoding="utf-8").read()
logic = open(os.path.join(HERE, "logic.js"), encoding="utf-8").read()
assert "</script" not in logic

def rep(old, new, count=1):
    global src
    n = src.count(old)
    if n != count:
        sys.exit("expected %d match(es), found %d for:\n%s" % (count, n, old[:200]))
    src = src.replace(old, new)

# ---------- head, runtime hand-off ----------
rep('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<script src="./support.js"></script>\n</head>',
    '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '<meta name="robots" content="noindex">\n<title>Aktoria CRM</title>\n'
    '<script src="./data.js"></script>\n<script>\n' + logic + '\n</script>\n<script src="./support.js"></script>\n'
    '<script>\n'
    '// If this host blocks the runtime\'s compile step (no eval), hand it the logic class directly.\n'
    '(function(){var n=0,t=setInterval(function(){n++;if(n>200){clearInterval(t);return;}\n'
    '  if(!window.__dcRegistry||!window.__dcRootName||!window.DCLogic||!window.AK_LOGIC)return;\n'
    '  var e=window.__dcRegistry[window.__dcRootName()];if(!e)return;\n'
    '  if(e.Logic){clearInterval(t);return;}\n'
    '  if(e.logicError){clearInterval(t);e.Logic=window.AK_LOGIC(window.DCLogic,window.React);e.logicError=null;window.__dcSetProps(window.__dcRootName(),null);}\n'
    '},50);})();\n</script>\n</head>')
s0 = src.index('<script type="text/x-dc" data-dc-script')
s1 = src.index('>', s0) + 1
s2 = src.index('</script>', s1)
src = src[:s1] + "\nconst Component=window.AK_LOGIC(DCLogic,React);\n" + src[s2:]

# ---------- chrome ----------
rep('<span>10:42</span>', '<span>{{ phoneTime }}</span>')

# connection notice (no data yet, connector needs approval, sheet not published...) and stale-range note
rep('<sc-if value="{{ loading }}">\n<div style="display:flex; flex-direction:column; gap:var(--s-6);">',
    '<sc-if value="{{ gate.on }}">\n'
    '<div style="display:flex; flex-direction:column; align-items:center; gap:10px; padding:var(--s-9) var(--s-5); text-align:center; border-radius:var(--r-lg); background:var(--glass); border:1px solid var(--glass-edge); box-shadow:var(--shadow-md), var(--hi);">\n'
    '<span style="width:52px; height:52px; border-radius:50%; border:1.5px dashed var(--hairline-strong);"></span>\n'
    '<span style="font-size:var(--fs-lg); font-weight:600;">{{ gate.title }}</span>\n'
    '<span style="font-size:var(--fs-sm); color:var(--ink-3); max-width:420px;">{{ gate.body }}</span>\n'
    '<div style="display:flex; gap:8px; flex-wrap:wrap; justify-content:center;">\n'
    '<button onClick="{{ gate.go }}" style="margin-top:6px; height:var(--btn-h); padding:0 16px; border:0; border-radius:var(--r-btn); background:var(--ink); color:#fff; font-size:var(--fs-sm); font-weight:500; cursor:pointer;">{{ gate.cta }}</button>\n'
    '<sc-if value="{{ gate.hasSheet }}"><button onClick="{{ gate.sheet }}" style="margin-top:6px; height:var(--btn-h); padding:0 16px; border:0; border-radius:var(--r-btn); background:var(--glass-strong); box-shadow:var(--shadow-sm), var(--hi); font-size:var(--fs-sm); font-weight:500; cursor:pointer;">Open the Google Sheet ↗</button></sc-if>\n'
    '</div>\n</div>\n</sc-if>\n'
    '<sc-if value="{{ hasStale }}"><span style="font-size:var(--fs-xs); color:var(--warn-ink); padding:8px 12px; border-radius:var(--r-md); background:var(--warn-soft); box-shadow:inset 0 0 0 1px var(--warn-line);">{{ stale }}</span></sc-if>\n\n'
    '<sc-if value="{{ loading }}">\n<div style="display:flex; flex-direction:column; gap:var(--s-6);">')

# ---------- home ----------
rep('<sc-if value="{{ home.allDone }}">\n<div style="padding:var(--s-8) var(--s-4);',
    '<sc-if value="{{ home.hasMoreTodo }}"><button onClick="{{ home.moreTodo }}" style="width:100%; height:44px; border:0; border-top:1px solid var(--hairline); background:transparent; font-size:var(--fs-sm); font-weight:500; color:var(--ink-2); cursor:pointer; transition:background var(--dur), color var(--dur);" style-hover="background:rgba(255,255,255,.7); color:var(--ink);">Show {{ home.moreTodoN }} more</button></sc-if>\n'
    '<sc-if value="{{ home.allDone }}">\n<div style="padding:var(--s-8) var(--s-4);')
rep('<section style="display:flex; flex-direction:column; gap:var(--s-3);">\n<div style="display:flex; align-items:center; gap:10px;">\n<h2 style="margin:0; font-size:var(--fs-lg); font-weight:600; letter-spacing:-0.015em;">Competitors posted something new</h2>',
    '<sc-if value="{{ home.hasAlerts }}">\n<section style="display:flex; flex-direction:column; gap:var(--s-3);">\n<div style="display:flex; align-items:center; gap:10px;">\n<h2 style="margin:0; font-size:var(--fs-lg); font-weight:600; letter-spacing:-0.015em;">Competitors posted something new</h2>')
rep('</sc-for>\n</div>\n</section>\n\n<section style="display:flex; flex-direction:column; gap:var(--s-3);">\n<div style="display:flex; align-items:center; gap:8px;">\n<h2 style="margin:0; font-size:var(--fs-lg); font-weight:600; letter-spacing:-0.015em;">Questions for the founders</h2>',
    '</sc-for>\n</div>\n</section>\n</sc-if>\n\n<sc-if value="{{ home.hasFq }}">\n<section style="display:flex; flex-direction:column; gap:var(--s-3);">\n<div style="display:flex; align-items:center; gap:8px;">\n<h2 style="margin:0; font-size:var(--fs-lg); font-weight:600; letter-spacing:-0.015em;">Questions for the founders</h2>')
rep('</sc-for>\n</div>\n</section>\n\n<section style="display:flex; flex-direction:column; gap:var(--s-3);">\n<div style="display:flex; align-items:center; gap:8px;">\n<h2 style="margin:0; font-size:var(--fs-lg); font-weight:600; letter-spacing:-0.015em;">Pilot goals</h2>',
    '</sc-for>\n</div>\n</section>\n</sc-if>\n\n<section style="display:flex; flex-direction:column; gap:var(--s-3);">\n<div style="display:flex; align-items:center; gap:8px;">\n<h2 style="margin:0; font-size:var(--fs-lg); font-weight:600; letter-spacing:-0.015em;">Pilot goals</h2>')
rep('{{ g.v }} <span style="color:var(--ink-4);">/ 1,000</span>', '{{ g.v }} <span style="color:var(--ink-4);">/ {{ g.tgt }}</span>')
rep('<span style="font-size:var(--fs-xs); color:var(--ink-3);">4 this week. Goal is 5.</span>', '<span style="font-size:var(--fs-xs); color:var(--ink-3);">{{ home.inqText }}</span>')

# ---------- our posts: post type filter under the status tabs ----------
rep('</sc-for>\n</div>\n</div>\n\n<div style="display:flex; flex-direction:column; gap:var(--s-5);">\n<sc-for list="{{ posts.list }}" as="p">',
    '</sc-for>\n</div>\n</div>\n'
    '<div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:calc(-1 * var(--s-2));">\n<sc-for list="{{ posts.types }}" as="c">'
    '<button onClick="{{ c.go }}" style="display:inline-flex; align-items:center; gap:6px; height:30px; padding:0 12px; border-radius:var(--r-pill); border:1px solid {{ c.bd }}; background:{{ c.bg }}; color:{{ c.fg }}; font-size:var(--fs-sm); font-weight:500; cursor:pointer; white-space:nowrap;">{{ c.label }}'
    '<span style="font-family:var(--font-mono); font-size:var(--fs-3xs); padding:1px 6px; border-radius:var(--r-pill); background:{{ c.cbg }};">{{ c.count }}</span></button>'
    '</sc-for>\n'
    '<sc-if value="{{ posts.canAdd }}"><button onClick="{{ posts.toggleAdd }}" style="margin-left:auto; display:inline-flex; align-items:center; height:30px; padding:0 14px; border-radius:var(--r-pill); border:1px solid var(--ink); background:#fff; color:var(--ink); font-size:var(--fs-sm); font-weight:500; cursor:pointer;">{{ posts.addLabel }}</button></sc-if>\n'
    '</div>\n'
    '<sc-if value="{{ posts.addOpen }}">\n'
    '<div style="display:flex; flex-direction:column; gap:10px; padding:var(--s-4); border-radius:var(--r-lg); background:#fff; box-shadow:var(--shadow-sm), inset 0 0 0 1px var(--hairline);">\n'
    '<span style="font-size:var(--fs-md); font-weight:600;">Add a post we wrote ourselves</span>\n'
    '<span style="font-size:var(--fs-xs); color:var(--ink-3);">Paste its link if it is already live and it gets tracked like the rest. Posts written straight on X are also added by the tracker on its own.</span>\n'
    '<div style="display:flex; flex-wrap:wrap; gap:8px;">\n'
    '<select value="{{ posts.f.account }}" onChange="{{ posts.on.account }}" aria-label="Account" style="height:36px; padding:0 12px; border:0; border-radius:var(--r-btn); background:#fff; box-shadow:inset 0 0 0 1px var(--hairline-strong); font-size:var(--fs-sm); outline:none;"><option value="Karan">Karan</option><option value="Shreenabh">Shreenabh</option><option value="Aktoria">Aktoria page</option></select>\n'
    '<select value="{{ posts.f.type }}" onChange="{{ posts.on.type }}" aria-label="Post type" style="height:36px; padding:0 12px; border:0; border-radius:var(--r-btn); background:#fff; box-shadow:inset 0 0 0 1px var(--hairline-strong); font-size:var(--fs-sm); outline:none;"><option value="Own post">Type: other</option><option value="Lead magnet">Lead magnet</option><option value="Founder story">Founder story</option><option value="Data post">Data post</option><option value="Tagging post">Tagging post</option></select>\n'
    '<select value="{{ posts.f.status }}" onChange="{{ posts.on.status }}" aria-label="Status" style="height:36px; padding:0 12px; border:0; border-radius:var(--r-btn); background:#fff; box-shadow:inset 0 0 0 1px var(--hairline-strong); font-size:var(--fs-sm); outline:none;"><option value="To post">To post</option><option value="Scheduled">Scheduled</option><option value="Posted">Already posted</option></select>\n'
    '<input type="date" value="{{ posts.f.date }}" onChange="{{ posts.on.date }}" aria-label="Date" style="height:36px; padding:0 12px; border:0; border-radius:var(--r-btn); background:#fff; box-shadow:inset 0 0 0 1px var(--hairline-strong); font-size:var(--fs-sm); outline:none;">\n'
    '<input value="{{ posts.f.time }}" onChange="{{ posts.on.time }}" placeholder="Time, e.g. 8:30 PM" aria-label="Time" style="height:36px; padding:0 12px; border:0; border-radius:var(--r-btn); background:#fff; box-shadow:inset 0 0 0 1px var(--hairline-strong); font-size:var(--fs-sm); outline:none; width:150px;">\n'
    '</div>\n'
    '<input value="{{ posts.f.link }}" onChange="{{ posts.on.link }}" placeholder="Link on X, if it is live (x.com/.../status/...)" aria-label="Link" style="height:36px; padding:0 12px; border:0; border-radius:var(--r-btn); background:#fff; box-shadow:inset 0 0 0 1px var(--hairline-strong); font-size:var(--fs-sm); outline:none;">\n'
    '<textarea value="{{ posts.f.text }}" onChange="{{ posts.on.text }}" placeholder="The post text" rows="4" style="padding:10px 12px; border:0; border-radius:var(--r-btn); background:#fff; box-shadow:inset 0 0 0 1px var(--hairline-strong); font-size:var(--fs-sm); font-family:inherit; resize:vertical; outline:none;"></textarea>\n'
    '<div style="display:flex; gap:8px;"><button onClick="{{ posts.saveAdd }}" style="height:36px; padding:0 16px; border:0; border-radius:var(--r-btn); background:var(--ink); color:#fff; font-size:var(--fs-sm); font-weight:500; cursor:pointer;">{{ posts.saveLabel }}</button>'
    '<button onClick="{{ posts.toggleAdd }}" style="height:36px; padding:0 12px; border:0; border-radius:var(--r-btn); background:transparent; color:var(--ink-2); font-size:var(--fs-sm); cursor:pointer;">Cancel</button></div>\n'
    '</div>\n</sc-if>\n'
    '\n<div style="display:flex; flex-direction:column; gap:var(--s-5);">\n<sc-for list="{{ posts.list }}" as="p">')

rep('<div style="flex:2 1 300px; display:flex; flex-direction:column; gap:4px;"><span style="font-size:var(--fs-2xs); color:var(--ink-3);">What we changed</span><span style="font-size:var(--fs-md); line-height:1.5;">{{ cmp.changed }}</span></div>\n', '')

# ---------- sidebar: a visible Refresh button above Open sheet ----------
rep('<a href="#" onClick="{{ openSheet }}"',
    '<button onClick="{{ refresh }}" title="Reload the sheet now and pull new numbers and replies from X" style="display:flex; align-items:center; justify-content:center; gap:6px; height:32px; padding:0 12px; border:0; border-radius:var(--r-btn); background:var(--ink); color:#fff; font-size:var(--fs-xs); font-weight:500; cursor:pointer;">Refresh now</button>\n'
    '<a href="#" onClick="{{ openSheet }}"')

# ---------- calendar: 3 a day, x to take a post off, + to add one, drag to reorder or move ----------
rep('<span style="display:flex; align-items:center; gap:6px;">5 a day\n', '<span style="display:flex; align-items:center; gap:6px;">3 a day\n')
rep('Each account aims for 5 posts a day. The five small bars in every day fill up as posts get planned, scheduled and posted.',
    'Each account posts 3 a day. Press + to pick from the drafts, drag posts to reorder a day or move them to another day, and × to take one off the calendar (it stays in Our posts).')
rep('<span style="font-family:var(--font-mono); font-size:var(--fs-3xs); color:{{ c.cfg }}; white-space:nowrap;">{{ c.count }}</span>\n</div>\n<sc-for list="{{ c.posts }}" as="p">\n<div onClick="{{ p.open }}" style="display:flex; flex-direction:column; gap:4px; padding:7px 8px; border-radius:9px; background:rgba(255,255,255,.8); box-shadow:inset 0 0 0 1px var(--hairline); cursor:pointer;',
    '<span style="font-family:var(--font-mono); font-size:var(--fs-3xs); color:{{ c.cfg }}; white-space:nowrap;">{{ c.count }}</span>\n'
    '<sc-if value="{{ c.canAdd }}"><button onClick="{{ c.add }}" title="Add a post to this day" style="width:20px; height:20px; border:0; border-radius:6px; display:grid; place-items:center; background:#fff; box-shadow:inset 0 0 0 1px var(--hairline-strong); font-size:14px; line-height:1; color:var(--ink); cursor:pointer;">+</button></sc-if>\n'
    '</div>\n<sc-for list="{{ c.posts }}" as="p">\n'
    '<div onClick="{{ p.open }}" draggable="{{ p.drag }}" onDragStart="{{ p.start }}" onDragOver="{{ c.over }}" onDrop="{{ p.dropOn }}" style="display:flex; flex-direction:column; gap:4px; padding:7px 8px; border-radius:9px; background:rgba(255,255,255,.8); box-shadow:inset 0 0 0 1px var(--hairline); cursor:{{ p.cur }};')
rep('<span style="margin-left:auto; display:inline-flex; align-items:center; height:16px; padding:0 5px; border-radius:4px; font-size:9.5px; font-weight:600; white-space:nowrap; background:{{ p.sbg }}; color:{{ p.sfg }};">{{ p.st }}</span>\n</div>\n<span style="font-size:11.5px;',
    '<span style="margin-left:auto; display:inline-flex; align-items:center; height:16px; padding:0 5px; border-radius:4px; font-size:9.5px; font-weight:600; white-space:nowrap; background:{{ p.sbg }}; color:{{ p.sfg }};">{{ p.st }}</span>\n'
    '<sc-if value="{{ p.canX }}"><button onClick="{{ p.x }}" title="Take off the calendar (keeps the post)" style="width:16px; height:16px; border:0; border-radius:4px; display:grid; place-items:center; background:transparent; font-size:13px; line-height:1; color:var(--ink-3); cursor:pointer;" style-hover="background:var(--n-soft); color:var(--ink);">×</button></sc-if>\n'
    '</div>\n<span style="font-size:11.5px;')
rep('<div style="min-height:158px; padding:8px; border-left:1px solid var(--hairline);',
    '<div onDragOver="{{ c.over }}" onDrop="{{ c.drop }}" style="min-height:158px; padding:8px; border-left:1px solid var(--hairline);')
rep('<sc-if value="{{ wide }}">\n<div style="border-radius:var(--r-lg); background:var(--glass); backdrop-filter:var(--blur); -webkit-backdrop-filter:var(--blur); border:1px solid var(--glass-edge); box-shadow:var(--shadow-md), var(--hi); overflow:hidden; opacity:{{ E.op }}; transform:{{ E.t }}; transition:opacity 500ms var(--ease) 60ms, transform 500ms var(--ease) 60ms;">\n<div style="overflow-x:auto;">\n<div style="display:grid; grid-template-columns:140px repeat(7, minmax(112px, 1fr)); min-width:930px;">',
    '<sc-if value="{{ cal.pick.open }}">\n'
    '<div style="display:flex; flex-direction:column; gap:10px; padding:var(--s-4); border-radius:var(--r-lg); background:#fff; box-shadow:var(--shadow-md), inset 0 0 0 1px var(--hairline);">\n'
    '<div style="display:flex; align-items:center; gap:10px;"><span style="font-size:var(--fs-md); font-weight:600;">{{ cal.pick.title }}</span>'
    '<button onClick="{{ cal.pick.close }}" style="margin-left:auto; height:30px; padding:0 12px; border:0; border-radius:var(--r-btn); background:var(--n-soft); font-size:var(--fs-xs); cursor:pointer;">Close</button></div>\n'
    '<div style="display:flex; flex-wrap:wrap; gap:6px;"><sc-for list="{{ cal.pick.kinds }}" as="k"><button onClick="{{ k.go }}" style="display:inline-flex; align-items:center; gap:6px; height:28px; padding:0 11px; border-radius:var(--r-pill); border:1px solid {{ k.bd }}; background:{{ k.bg }}; color:{{ k.fg }}; font-size:var(--fs-xs); font-weight:500; cursor:pointer;">{{ k.label }} <span style="font-family:var(--font-mono); font-size:var(--fs-3xs);">{{ k.count }}</span></button></sc-for></div>\n'
    '<sc-if value="{{ cal.pick.empty }}"><span style="font-size:var(--fs-sm); color:var(--ink-3);">No drafts left for this account. New ones arrive tonight.</span></sc-if>\n'
    '<div style="display:flex; flex-direction:column; max-height:420px; overflow-y:auto; border-radius:var(--r-md); box-shadow:inset 0 0 0 1px var(--hairline);">\n'
    '<sc-for list="{{ cal.pick.items }}" as="it"><div style="display:flex; align-items:center; gap:12px; padding:10px 12px; border-bottom:1px solid var(--hairline);">'
    '<div style="flex:1; min-width:0; display:flex; flex-direction:column; gap:3px;"><span style="font-size:var(--fs-3xs); color:var(--ink-3);">{{ it.type }} · {{ it.when }}<sc-if value="{{ it.hasNeeds }}"> · {{ it.needs }}</sc-if></span>'
    '<span style="font-size:var(--fs-sm); line-height:1.4;">{{ it.line }}</span></div>'
    '<button onClick="{{ it.add }}" style="flex:0 0 auto; height:30px; padding:0 14px; border:0; border-radius:var(--r-btn); background:var(--ink); color:#fff; font-size:var(--fs-xs); font-weight:500; cursor:pointer;">Add</button></div></sc-for>\n'
    '</div>\n</div>\n</sc-if>\n\n'
    '<sc-if value="{{ wide }}">\n<div style="border-radius:var(--r-lg); background:var(--glass); backdrop-filter:var(--blur); -webkit-backdrop-filter:var(--blur); border:1px solid var(--glass-edge); box-shadow:var(--shadow-md), var(--hi); overflow:hidden; opacity:{{ E.op }}; transform:{{ E.t }}; transition:opacity 500ms var(--ease) 60ms, transform 500ms var(--ease) 60ms;">\n<div style="overflow-x:auto;">\n<div style="display:grid; grid-template-columns:140px repeat(7, minmax(112px, 1fr)); min-width:930px;">')

# ---------- send today ----------
rep('<span style="font-size:var(--fs-lg); font-weight:600;">Everything for today is sent</span>',
    '<span style="font-size:var(--fs-lg); font-weight:600;">{{ send.clearTitle }}</span>')
rep('<sc-if value="{{ is.send }}">\n<sc-if value="{{ send.hasRes }}">',
    '<sc-if value="{{ is.send }}">\n'
    '<div style="display:flex; align-items:center; gap:10px; padding:12px 14px; border-radius:var(--r-lg); background:var(--glass-faint); border:1px dashed var(--hairline-strong); font-size:var(--fs-sm); color:var(--ink-2); opacity:{{ E.op }}; transition:opacity 500ms var(--ease);">'
    '<span style="width:8px; height:8px; flex:0 0 8px; border-radius:50%; background:{{ send.holdDot }};"></span><span style="flex:1 1 auto;">{{ send.hold }}</span>'
    '<button onClick="{{ send.togglePause }}" style="flex:0 0 auto; padding:6px 12px; border-radius:var(--r-md); border:1px solid var(--hairline-strong); background:#fff; color:var(--ink); font-size:var(--fs-sm); font-weight:500; cursor:pointer;">{{ send.pauseLabel }}</button></div>\n'
    '<sc-if value="{{ send.hasRes }}">')
rep('<span style="font-size:var(--fs-xs); color:var(--ink-3);">Yesterday · Wed 28 Oct</span>', '<span style="font-size:var(--fs-xs); color:var(--ink-3);">{{ send.res.day }}</span>')
rep('line-height:1; font-variant-numeric:tabular-nums;">52</span><span style="font-size:var(--fs-sm); color:var(--ink-2);">sent</span>',
    'line-height:1; font-variant-numeric:tabular-nums;">{{ send.res.sent }}</span><span style="font-size:var(--fs-sm); color:var(--ink-2);">sent on X</span>')
rep('<div style="display:flex; flex-direction:column; gap:8px; flex:1 1 240px; min-width:0;">\n<span style="display:flex; align-items:center; gap:6px; font-size:var(--fs-xs); color:var(--ink-3);">Couldn’t send',
    '<sc-if value="{{ send.res.hasCant }}">\n<div style="display:flex; flex-direction:column; gap:8px; flex:1 1 240px; min-width:0;">\n<span style="display:flex; align-items:center; gap:6px; font-size:var(--fs-xs); color:var(--ink-3);">Couldn’t send')
rep('color:var(--bad-ink); font-variant-numeric:tabular-nums;">6</span>\n<div style="display:flex; flex-direction:column; gap:4px; font-size:var(--fs-xs); color:var(--ink-2);">\n<span><b style="font-family:var(--font-mono); font-weight:500;">4</b> · their DMs need a passcode</span>\n<span><b style="font-family:var(--font-mono); font-weight:500;">2</b> · they only take DMs from people they follow</span>\n</div>\n</div>\n</div>',
    'color:var(--bad-ink); font-variant-numeric:tabular-nums;">{{ send.res.cant }}</span>\n<div style="display:flex; flex-direction:column; gap:4px; font-size:var(--fs-xs); color:var(--ink-2);">\n<sc-for list="{{ send.res.why }}" as="w"><span><b style="font-family:var(--font-mono); font-weight:500;">{{ w.n }}</b> · {{ w.label }}</span></sc-for>\n</div>\n</div>\n</div>\n</sc-if>')
rep('<span style="font-size:var(--fs-xs); color:var(--ink-3);">Each account, yesterday</span>', '<span style="font-size:var(--fs-xs); color:var(--ink-3);">Each account, {{ send.res.dayLow }}</span>')
rep('<span style="font-size:var(--fs-sm); font-weight:500; color:var(--ink-2);">Skipped for now: {{ send.skipN }} seed-stage people</span>',
    '<span style="font-size:var(--fs-sm); font-weight:500; color:var(--ink-2);">{{ send.skipLabel }}</span>')
rep('Seed and pre-seed companies rarely have budget for remote operators yet. They stay out of the list unless you choose Send anyway.',
    'Seed and pre-seed companies rarely have budget for remote operators yet, and unclear funding is checked first. They stay out of the list unless you choose Send anyway.')
rep('<span style="font-size:var(--fs-sm); color:var(--ink-3); max-width:340px;">Tomorrow’s list appears after the sheet updates at 7:00.</span>',
    '<span style="font-size:var(--fs-sm); color:var(--ink-3); max-width:340px;">{{ send.clearText }}</span>')

# ---------- pipeline ----------
rep('<option value="Any channel">Any channel</option><option value="X">X</option><option value="LinkedIn">LinkedIn</option>',
    '<option value="Any channel">Any channel</option><option value="X">X</option><option value="LinkedIn">LinkedIn</option><option value="Email">Email</option>')
rep('<sc-if value="{{ col.empty }}">',
    '<sc-if value="{{ col.hasMore }}"><button onClick="{{ col.more }}" style="height:32px; border:0; border-radius:var(--r-btn); background:rgba(255,255,255,.7); box-shadow:var(--shadow-xs), inset 0 0 0 1px var(--hairline); font-size:var(--fs-xs); font-weight:500; color:var(--ink-2); cursor:pointer;" style-hover="background:#fff; color:var(--ink);">Show {{ col.moreN }} more</button></sc-if>\n<sc-if value="{{ col.empty }}">')
rep('</button>\n</sc-for>\n</div>\n<span style="display:inline-flex; align-items:center; gap:6px; height:24px; padding:0 9px; border-radius:var(--r-pill); font-size:var(--fs-2xs); font-weight:500; white-space:nowrap; background:{{ c.stage.bg }}; color:{{ c.stage.fg }}; box-shadow:{{ c.stage.bd }};" title="Furthest stage reached by anyone at this company"><span style="width:6px; height:6px; border-radius:50%; background:{{ c.stageDot }};"></span>{{ c.stage.label }}</span>\n</div>\n</sc-for>\n</div>',
    '</button>\n</sc-for>\n</div>\n<span style="display:inline-flex; align-items:center; gap:6px; height:24px; padding:0 9px; border-radius:var(--r-pill); font-size:var(--fs-2xs); font-weight:500; white-space:nowrap; background:{{ c.stage.bg }}; color:{{ c.stage.fg }}; box-shadow:{{ c.stage.bd }};" title="Furthest stage reached by anyone at this company"><span style="width:6px; height:6px; border-radius:50%; background:{{ c.stageDot }};"></span>{{ c.stage.label }}</span>\n</div>\n</sc-for>\n'
    '<sc-if value="{{ pipe.cosHasMore }}"><button onClick="{{ pipe.cosMore }}" style="width:100%; height:44px; border:0; border-top:1px solid var(--hairline); background:transparent; font-size:var(--fs-sm); font-weight:500; color:var(--ink-2); cursor:pointer;" style-hover="background:rgba(255,255,255,.7); color:var(--ink);">Show {{ pipe.cosMoreN }} more</button></sc-if>\n</div>')
rep('<span style="font-size:var(--fs-sm); color:var(--ink-3);">{{ t.about }} {{ t.n }} tested side by side.</span>', '<span style="font-size:var(--fs-sm); color:var(--ink-3);">{{ t.about }}</span>')

# ---------- our posts ----------
rep('Where this post ranks among everything {{ p.rankOf }} has posted, by views. #1 is their biggest post ever.',
    '{{ p.tipText }}')
# "What we changed" moves into that "i" (team ask 29 Oct: no text on the card that isn't useful)
rep('<div style="display:flex; gap:10px; padding:12px var(--s-5); border-top:1px solid var(--hairline); font-size:var(--fs-sm); line-height:1.5;">\n'
    '<span style="flex:0 0 auto; font-weight:600;">What we changed</span>\n'
    '<span style="color:var(--ink-2); text-wrap:pretty;">{{ p.changed }}</span>\n</div>\n', '')
rep('<span style="margin-top:auto; font-family:var(--font-mono); font-size:var(--fs-2xs); color:var(--ink-3);">{{ p.cViews }} views · {{ p.cLikes }} likes</span>',
    '<span style="margin-top:auto; font-family:var(--font-mono); font-size:var(--fs-2xs); color:var(--ink-3);">{{ p.cNums }}</span>')
rep('placeholder="Paste the link to the post on X"', 'placeholder="{{ p.linkPh }}"')
rep('<span style="font-size:var(--fs-sm); color:var(--ink-3); max-width:340px;">Pick one of the posts below to copy next and it lands here.</span>',
    '<span style="font-size:var(--fs-sm); color:var(--ink-3); max-width:340px;">{{ posts.emptyText }}</span>')
rep('<section style="display:flex; flex-direction:column; gap:var(--s-3); opacity:{{ E.op }}; transition:opacity 500ms var(--ease) 200ms;">\n<div style="display:flex; align-items:baseline; gap:10px; flex-wrap:wrap;">\n<h2 style="margin:0; font-size:var(--fs-lg); font-weight:600; letter-spacing:-0.015em;">10 best posts to copy next</h2>',
    '<sc-if value="{{ posts.hasBest }}">\n<section style="display:flex; flex-direction:column; gap:var(--s-3); opacity:{{ E.op }}; transition:opacity 500ms var(--ease) 200ms;">\n<div style="display:flex; align-items:baseline; gap:10px; flex-wrap:wrap;">\n<h2 style="margin:0; font-size:var(--fs-lg); font-weight:600; letter-spacing:-0.015em;">10 best posts to copy next</h2>')
rep('cursor:pointer; transition:all var(--dur);" style-hover="transform:translateY(-1px); background:#fff;">Plan a copy</button></sc-if>\n</div>\n</sc-for>\n</div>\n</section>\n</sc-if>',
    'cursor:pointer; transition:all var(--dur);" style-hover="transform:translateY(-1px); background:#fff;">{{ b.planLabel }}</button></sc-if>\n</div>\n</sc-for>\n</div>\n</section>\n</sc-if>\n</sc-if>')
rep('<span style="margin-top:auto; font-family:var(--font-mono); font-size:var(--fs-xs); color:var(--ink-3);">{{ cmp.cViews }} views · {{ cmp.cLikes }} likes</span>',
    '<span style="margin-top:auto; font-family:var(--font-mono); font-size:var(--fs-xs); color:var(--ink-3);">{{ cmp.cNums }}</span>')

# ---------- post tracker ----------
rep('<span style="margin-left:auto; font-size:var(--fs-xl); font-weight:500; letter-spacing:-0.03em;">1.28M</span>\n<span style="font-size:var(--fs-2xs); color:var(--ok-ink);">+18% on last week</span>\n</div>\n<svg viewBox="-8 -8 616 186"',
    '<span style="margin-left:auto; font-size:var(--fs-xl); font-weight:500; letter-spacing:-0.03em;">{{ trk.total }}</span>\n<span style="font-size:var(--fs-2xs); color:var(--ok-ink);">{{ trk.totalD }}</span>\n</div>\n'
    '<sc-if value="{{ trk.noChart }}"><span style="padding:var(--s-6) 0; text-align:center; font-size:var(--fs-sm); color:var(--ink-3);">The chart fills in after the tracker’s second check. It runs every 3 hours.</span></sc-if>\n'
    '<sc-if value="{{ trk.hasChart }}">\n<svg viewBox="-8 -8 616 186"')
rep('<div style="display:flex; justify-content:space-between; font-family:var(--font-mono); font-size:var(--fs-3xs); color:var(--ink-3);"><span>{{ trk.chart.l0 }}</span><span>{{ trk.chart.l1 }}</span><span>{{ trk.chart.l2 }}</span></div>',
    '<div style="display:flex; justify-content:space-between; font-family:var(--font-mono); font-size:var(--fs-3xs); color:var(--ink-3);"><span>{{ trk.chart.l0 }}</span><span>{{ trk.chart.l1 }}</span><span>{{ trk.chart.l2 }}</span></div>\n</sc-if>')
rep('<h2 style="margin:0; font-size:var(--fs-lg); font-weight:600; letter-spacing:-0.015em;">What did well and why</h2>',
    '<h2 style="margin:0; font-size:var(--fs-lg); font-weight:600; letter-spacing:-0.015em;">What did well and why</h2>\n<sc-if value="{{ trk.noTop }}"><span style="font-size:var(--fs-sm); color:var(--ink-3);">Shows up once a post has 30 or more views.</span></sc-if>')
rep('<h2 style="margin:0; font-size:var(--fs-lg); font-weight:600; letter-spacing:-0.015em;">Patterns so far</h2>',
    '<h2 style="margin:0; font-size:var(--fs-lg); font-weight:600; letter-spacing:-0.015em;">Patterns so far</h2>\n<sc-if value="{{ trk.noPat }}"><span style="font-size:var(--fs-sm); color:var(--ink-3);">Patterns show up once a few more posts have 30 or more views.</span></sc-if>')
rep('<span style="font-family:var(--font-mono); font-size:var(--fs-3xs); color:var(--ok-ink);">{{ r.delta }} since last check</span>',
    '<span style="font-family:var(--font-mono); font-size:var(--fs-3xs); color:var(--ok-ink);">{{ r.deltaLabel }}</span>')

# ---------- people to DM ----------
rep('<span style="font-size:var(--fs-lg); font-weight:600;">Everyone here has a message</span>', '<span style="font-size:var(--fs-lg); font-weight:600;">{{ pdm.emptyTitle }}</span>')
rep('</article>\n</sc-for>\n</div>\n<sc-if value="{{ pdm.empty }}">',
    '</article>\n</sc-for>\n</div>\n<sc-if value="{{ pdm.hasMore }}"><button onClick="{{ pdm.more }}" style="height:40px; border:0; border-radius:var(--r-btn); background:var(--glass-strong); box-shadow:var(--shadow-sm), var(--hi); font-size:var(--fs-sm); font-weight:500; color:var(--ink-2); cursor:pointer;" style-hover="background:#fff; color:var(--ink);">Show {{ pdm.moreN }} more</button></sc-if>\n<sc-if value="{{ pdm.empty }}">')

# ---------- competitors ----------
rep('<span style="font-size:var(--fs-xs); color:var(--ink-3);">Showing 12 of 35 accounts. The rest are in the sheet under Competitors.</span>',
    '<span style="font-size:var(--fs-xs); color:var(--ink-3);">{{ comp.shownNote }}</span>')
rep('<div style="display:flex; align-items:baseline; gap:10px; flex-wrap:wrap;"><span style="font-size:var(--fs-sm); font-weight:600;">Views per post, last 30 days</span><span style="font-size:var(--fs-xs); color:var(--ink-3);">Spikes are the posts worth copying</span></div>\n<div style="display:flex; gap:10px;">',
    '<div style="display:flex; align-items:baseline; gap:10px; flex-wrap:wrap;"><span style="font-size:var(--fs-sm); font-weight:600;">{{ comp.d.chart.label }}</span><span style="font-size:var(--fs-xs); color:var(--ink-3);">Spikes are the posts worth copying</span></div>\n'
    '<sc-if value="{{ comp.d.noChart }}"><span style="padding:var(--s-5) 0; font-size:var(--fs-sm); color:var(--ink-3);">Fewer than 2 of their saved posts are from the last 30 days, so there’s no chart yet.</span></sc-if>\n'
    '<sc-if value="{{ comp.d.hasChart }}">\n<div style="display:flex; gap:10px;">')
rep('<span>30 days ago</span><span>Biggest: {{ comp.d.chart.peakL }}</span><span>Today</span></div>\n</div>\n</div>\n</div>',
    '<span>30 days ago</span><span>Biggest: {{ comp.d.chart.peakL }}</span><span>Today</span></div>\n</div>\n</div>\n</sc-if>\n</div>')
rep('<h2 style="margin:0; font-size:var(--fs-lg); font-weight:600; letter-spacing:-0.015em;">Their 6 biggest posts, and our copies</h2>',
    '<h2 style="margin:0; font-size:var(--fs-lg); font-weight:600; letter-spacing:-0.015em;">Their 6 biggest posts, and our copies</h2>\n<sc-if value="{{ comp.d.noTop }}"><span style="font-size:var(--fs-sm); color:var(--ink-3);">No posts saved yet. They arrive with the next refresh.</span></sc-if>')
rep('<span style="margin-left:auto; font-family:var(--font-mono); font-size:var(--fs-3xs); color:var(--ink-3);">{{ t.views }} views</span>',
    '<span style="margin-left:auto; font-family:var(--font-mono); font-size:var(--fs-3xs); color:var(--ink-3);">{{ t.viewsL }}</span>')
rep('<span style="margin-top:auto; font-family:var(--font-mono); font-size:var(--fs-3xs); color:var(--ink-4);">{{ t.likes }} likes</span>',
    '<span style="margin-top:auto; font-family:var(--font-mono); font-size:var(--fs-3xs); color:var(--ink-4);">{{ t.likesL }}</span>')
rep('<div style="display:flex; flex-direction:column; gap:8px; padding:12px; border-radius:var(--r-md); background:var(--in-soft); box-shadow:inset 0 0 0 1px var(--in-line);">',
    '<div onClick="{{ t.openCopy }}" style="display:flex; flex-direction:column; gap:8px; padding:12px; border-radius:var(--r-md); background:var(--in-soft); box-shadow:inset 0 0 0 1px var(--in-line); cursor:pointer;">')
rep('font-size:var(--fs-2xs); font-weight:500; cursor:pointer; transition:all var(--dur);" style-hover="transform:translateY(-1px); background:#fff;">Plan a copy</button>',
    'font-size:var(--fs-2xs); font-weight:500; cursor:pointer; transition:all var(--dur);" style-hover="transform:translateY(-1px); background:#fff;">{{ t.planLabel }}</button>')
rep('<span style="display:flex; gap:14px; font-family:var(--font-mono); font-size:var(--fs-2xs); color:var(--ink-2); white-space:nowrap;"><span>{{ r.views }} views</span><span>{{ r.likes }} likes</span>',
    '<span style="display:flex; gap:14px; font-family:var(--font-mono); font-size:var(--fs-2xs); color:var(--ink-2); white-space:nowrap;"><span>{{ r.views }}</span><span>{{ r.likes }}</span>')

# ---------- contact panel ----------
rep('background:var(--n-soft); color:var(--ink-2);">Owner: {{ cp.owner }}</span>', 'background:var(--n-soft); color:var(--ink-2);">{{ cp.ownerLabel }}</span>')
rep('<sc-for list="{{ cp.actions }}" as="a">\n<button onClick="{{ a.fn }}" style="height:var(--btn-h-sm); padding:0 12px; border:0; border-radius:var(--r-btn); font-size:var(--fs-xs); font-weight:500; cursor:pointer; white-space:nowrap; background:{{ a.bg }}; color:{{ a.fg }}; box-shadow:{{ a.sh }}; transition:transform var(--dur-fast) var(--ease), filter var(--dur), background var(--dur);" style-hover="transform:translateY(-1px); filter:brightness(1.06);" style-active="transform:scale(.97);">{{ a.label }}</button>\n</sc-for>\n</div>\n</sc-if>\n</div>',
    '<sc-for list="{{ cp.actions }}" as="a">\n<button onClick="{{ a.fn }}" style="height:var(--btn-h-sm); padding:0 12px; border:0; border-radius:var(--r-btn); font-size:var(--fs-xs); font-weight:500; cursor:pointer; white-space:nowrap; background:{{ a.bg }}; color:{{ a.fg }}; box-shadow:{{ a.sh }}; transition:transform var(--dur-fast) var(--ease), filter var(--dur), background var(--dur);" style-hover="transform:translateY(-1px); filter:brightness(1.06);" style-active="transform:scale(.97);">{{ a.label }}</button>\n</sc-for>\n</div>\n</sc-if>\n'
    '<sc-if value="{{ cp.saveHint }}"><span style="font-size:var(--fs-2xs); color:var(--ink-3);">{{ cp.saveHint }}</span></sc-if>\n</div>')
rep('<div style="display:flex; flex-direction:column; gap:8px;">\n<span style="font-size:var(--fs-2xs); font-weight:600; letter-spacing:var(--tr-caps); text-transform:uppercase; color:var(--ink-3);">How to reach them</span>',
    '<sc-if value="{{ cp.hasReach }}">\n<div style="display:flex; flex-direction:column; gap:8px;">\n<span style="font-size:var(--fs-2xs); font-weight:600; letter-spacing:var(--tr-caps); text-transform:uppercase; color:var(--ink-3);">How to reach them</span>')
rep('<span style="color:var(--ink-3);">↗</span>\n</a>\n</sc-for>\n</div>\n</div>',
    '<span style="color:var(--ink-3);">↗</span>\n</a>\n</sc-for>\n</div>\n</div>\n</sc-if>')
rep('<input type="datetime-local" value="{{ cp.callAt }}" onChange="{{ cp.setCall }}"',
    '<input type="datetime-local" sc-camel-value="{{ cp.callAt }}" onChange="{{ cp.setCall }}" onBlur="{{ cp.saveCall }}" disabled="{{ cp.ro }}"')
rep('<textarea value="{{ cp.note }}" onChange="{{ cp.setNote }}" rows="3"',
    '<textarea value="{{ cp.note }}" onChange="{{ cp.setNote }}" onBlur="{{ cp.saveNote }}" disabled="{{ cp.ro }}" rows="3"')

# ---------- toast (errors get a red mark and may wrap) ----------
rep('display:grid; place-items:center; background:var(--ok); font-size:10px;">✓</span>\n<span style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{{ toast.msg }}</span>',
    'display:grid; place-items:center; background:{{ toast.icBg }}; font-size:10px;">{{ toast.ic }}</span>\n<span style="white-space:{{ toast.ws }}; overflow:hidden; text-overflow:ellipsis;">{{ toast.msg }}</span>')

# ---------- bound SVG geometry ----------
# The browser parses the raw template before the runtime replaces it, and logs an error for every SVG attribute
# that holds "{{ ... }}". The runtime reads "sc-camel-<name>" as "<name>", so the rendered SVG is identical.
import re
t0, t1 = src.index("<x-dc>"), src.index("</x-dc>")
tpl, n = re.subn(r' (d|points|cx|cy|r)="\{\{', r' sc-camel-\1="{{', src[t0:t1])
assert n >= 10, n
src = src[:t0] + tpl + src[t1:]

open(OUT, "w", encoding="utf-8", newline="\n").write(src)
print("wrote", OUT, len(src), "bytes")
