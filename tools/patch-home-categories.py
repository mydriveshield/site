import sys, json, pathlib
site = pathlib.Path(sys.argv[1]); pages = json.load(open(pathlib.Path(__file__).with_name("pages.json")))
f = site/"index.html"; s = f.read_text()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:60], s.count(old))
    s = s.replace(old, new)
labels = {"caravan":"Caravan Warranty","jetski":"Jetski Warranty","marine":"Marine Warranty","motorbike":"Motorbike Warranty","motorhome":"Motorhome Warranty","machinery":"Machinery Warranty","truck":"Truck Warranty"}
# 1. category labels + callback intro
rep("let callbackSource = '';", "let callbackSource = '';\n// New categories (quote by callback until the online quote flow is built)\nconst CAT_LABELS = " + json.dumps(labels) + ";")
rep("  else if(from === 'absolute') intro.textContent", "  else if(CAT_LABELS[from]) intro.textContent = 'Leave your details and a MyDriveShield consultant will call you within one business day with a quote for the Integrity ' + CAT_LABELS[from] + '. In the notes, tell us the make, model, year and hours or kilometres.';\n  else if(from === 'absolute') intro.textContent")
rep("if(instantBox) instantBox.style.display = (from === 'endurance') ? 'none' : 'block';", "if(instantBox) instantBox.style.display = (from === 'endurance' || CAT_LABELS[from]) ? 'none' : 'block';")
# 2. lead product label
rep("  const product = callbackSource==='roadside' ? 'Roadside Assistance ONLY (3 or 5 Star — confirm on call)'", "  const product = CAT_LABELS[callbackSource] ? CAT_LABELS[callbackSource]+' (quote request — confirm details on call)'\n                : callbackSource==='roadside' ? 'Roadside Assistance ONLY (3 or 5 Star — confirm on call)'")
rep("const est = (callbackSource!=='roadside' && (", "const est = (callbackSource!=='roadside' && !CAT_LABELS[callbackSource] && (")
# 3. deep link ?callback=<key>
rep("  // Deep links from product pages: /#quote?start=warranty|endurance|roadside", "  // Deep links from the new category pages: /?callback=caravan|jetski|marine|motorbike|motorhome|machinery|truck#quote\n  (function(){\n    const m = (location.search||'').match(/callback=([a-z]+)/);\n    if(!m || !CAT_LABELS[m[1]]) return;\n    showCallback(m[1]);\n    setTimeout(()=>document.getElementById('quote').scrollIntoView(), 50);\n  })();\n  // Deep links from product pages: /#quote?start=warranty|endurance|roadside")
# 4. tile row under the intent cards
short = {"caravan":"Caravans","jetski":"Jet skis","marine":"Boats","motorbike":"Motorbikes","motorhome":"Motorhomes","machinery":"Machinery","truck":"Trucks"}
tiles = "".join('<a class="cat-tile" href="/%s/"><b>%s</b><span>from $%s</span></a>' % (p["slug"], short[p["key"]], format(p["frm"], ",")) for p in pages)
row = '    <div class="cat-row" aria-labelledby="cat-title">\n      <h3 id="cat-title">Not a car? We also arrange Integrity warranties for</h3>\n      <div class="cat-grid">' + tiles + '</div>\n      <p class="cat-note">Prices include GST. Each page shows who qualifies, every claim limit and every price.</p>\n    </div>\n'
rep('  </div>\n  <div class="trust">', row + '  </div>\n  <div class="trust">')
css = """  .cat-row{max-width:980px;margin:30px auto 0;text-align:center}
  .cat-row h3{font-size:18px;margin-bottom:14px}
  .cat-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:10px}
  .cat-tile{display:flex;flex-direction:column;gap:2px;border:1.5px solid var(--line);border-radius:14px;padding:14px 8px;background:#fff;box-shadow:var(--shadow-sm);transition:.2s}
  .cat-tile:hover,.cat-tile:focus-visible{border-color:var(--orange);transform:translateY(-2px);box-shadow:var(--shadow)}
  .cat-tile b{color:var(--navy);font-size:15.5px}
  .cat-tile span{color:var(--muted);font-size:13px}
  .cat-note{color:var(--muted);font-size:13.5px;margin-top:12px}
  @media(max-width:900px){.cat-grid{grid-template-columns:repeat(4,1fr)}}
  @media(max-width:520px){.cat-grid{grid-template-columns:repeat(2,1fr)}}
"""
rep("  .intent-more a{color:var(--navy);font-weight:700;text-decoration:underline;text-underline-offset:3px}\n", "  .intent-more a{color:var(--navy);font-weight:700;text-decoration:underline;text-underline-offset:3px}\n" + css)
f.write_text(s)
c = site/"assets/site.css"; t = c.read_text()
anchor = "  .intent-more a{color:var(--navy);font-weight:700;text-decoration:underline;text-underline-offset:3px}\n"
assert t.count(anchor) == 1
t = t.replace(anchor, anchor + css) + "\n.tbl-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}\n.tbl-scroll .cmp{min-width:520px}\n"
c.write_text(t)
print("home patched")
