#!/usr/bin/env python3
"""Generate downtown-preparedness/index.html"""
import base64, os

SYT_B64 = open('/tmp/syt_b64.txt').read().strip()
FT_B64  = open('/tmp/ft_b64.txt').read().strip()
SYT_SRC = f"data:image/png;base64,{SYT_B64}"
FT_SRC  = f"data:image/png;base64,{FT_B64}"

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Downtown Educational Preparedness Initiative</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
/* ===== DESIGN TOKENS ===== */
:root {{
  --white: #FFFFFF;
  --black: #000000;
  --blue:  #008AFC;
  --red:   #F50B0B;
  --font-hero: 'Anton', Arial Black, sans-serif;
  --font-label: Arial Black, Arial, sans-serif;
  --font-body: 'Montserrat', Arial, sans-serif;
  --nav-h: 56px;
  --search-h: 48px;
  --bar-h: 104px; /* nav + search */
  --footer-h: 64px;
  --transition: 150ms ease;
}}

/* ===== RESET ===== */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; }}
body {{
  font-family: var(--font-body);
  background: var(--white);
  color: var(--black);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}}
a {{ color: inherit; text-decoration: none; }}
button {{ cursor: pointer; font-family: var(--font-body); border: none; background: none; }}

/* ===== STICKY TOP BAR ===== */
#topbar {{
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 1000;
  background: var(--black);
}}

/* nav row */
#navbar {{
  height: var(--nav-h);
  display: flex;
  align-items: center;
  padding: 0 16px;
  gap: 8px;
  border-bottom: 2px solid var(--blue);
}}
#nav-brand {{
  font-family: var(--font-hero);
  font-size: 14px;
  color: var(--blue);
  letter-spacing: 1px;
  white-space: nowrap;
  flex-shrink: 0;
}}
#nav-links {{
  display: flex;
  align-items: center;
  gap: 2px;
  overflow-x: auto;
  flex: 1;
  scrollbar-width: none;
}}
#nav-links::-webkit-scrollbar {{ display: none; }}
.nav-group-label {{
  font-family: var(--font-label);
  font-size: 8px;
  color: var(--blue);
  text-transform: uppercase;
  letter-spacing: 1px;
  padding: 0 6px;
  white-space: nowrap;
  opacity: 0.7;
}}
.nav-btn {{
  font-family: var(--font-body);
  font-size: 11px;
  font-weight: 600;
  color: var(--white);
  background: transparent;
  border: 1px solid transparent;
  padding: 4px 8px;
  white-space: nowrap;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: color var(--transition), border-color var(--transition), background var(--transition);
}}
.nav-btn:hover {{ color: var(--blue); border-color: var(--blue); }}
.nav-btn.active {{ background: var(--blue); color: var(--white); border-color: var(--blue); }}

#hamburger {{
  display: none;
  flex-direction: column;
  gap: 5px;
  padding: 8px;
  margin-left: auto;
}}
#hamburger span {{
  display: block;
  width: 24px;
  height: 2px;
  background: var(--white);
  transition: transform var(--transition), opacity var(--transition);
}}
#hamburger.open span:nth-child(1) {{ transform: translateY(7px) rotate(45deg); }}
#hamburger.open span:nth-child(2) {{ opacity: 0; }}
#hamburger.open span:nth-child(3) {{ transform: translateY(-7px) rotate(-45deg); }}

/* Mobile drawer */
#nav-drawer {{
  display: none;
  position: fixed;
  top: var(--nav-h);
  left: 0; right: 0;
  background: var(--black);
  border-bottom: 2px solid var(--blue);
  z-index: 999;
  max-height: calc(100vh - var(--nav-h));
  overflow-y: auto;
  padding: 8px 0 16px;
}}
#nav-drawer.open {{ display: block; }}
.drawer-group-label {{
  font-family: var(--font-label);
  font-size: 9px;
  color: var(--blue);
  text-transform: uppercase;
  letter-spacing: 1px;
  padding: 12px 16px 4px;
  opacity: 0.7;
}}
.drawer-btn {{
  display: block;
  width: 100%;
  text-align: left;
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 600;
  color: var(--white);
  padding: 10px 24px;
  border-bottom: 1px solid #1a1a1a;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}}
.drawer-btn:hover {{ background: #111; color: var(--blue); }}
.drawer-btn.active {{ color: var(--blue); border-left: 3px solid var(--blue); }}

/* search row */
#searchbar {{
  height: var(--search-h);
  display: flex;
  align-items: center;
  padding: 0 16px;
  gap: 8px;
  background: #111;
  border-bottom: 1px solid #222;
}}
#search-input {{
  flex: 1;
  height: 32px;
  background: #1a1a1a;
  border: 1px solid #333;
  color: var(--white);
  font-family: var(--font-body);
  font-size: 13px;
  padding: 0 12px;
  outline: none;
  transition: border-color var(--transition);
}}
#search-input:focus {{ border-color: var(--blue); }}
#search-input::placeholder {{ color: #555; }}
#search-clear {{
  color: #555;
  font-size: 16px;
  padding: 4px 8px;
  display: none;
}}
#search-clear.visible {{ display: block; color: var(--white); }}
#search-results {{
  position: absolute;
  top: calc(var(--bar-h) - 2px);
  left: 16px; right: 16px;
  background: var(--black);
  border: 1px solid var(--blue);
  z-index: 998;
  display: none;
  max-height: 280px;
  overflow-y: auto;
}}
#search-results.open {{ display: block; }}
.search-item {{
  display: block;
  padding: 10px 16px;
  font-size: 13px;
  color: var(--white);
  border-bottom: 1px solid #1a1a1a;
  cursor: pointer;
  font-family: var(--font-body);
}}
.search-item:hover {{ background: var(--blue); color: var(--white); }}
.search-item strong {{ color: var(--blue); }}
.search-item:hover strong {{ color: var(--white); }}
.search-none {{ padding: 12px 16px; font-size: 12px; color: #888; }}

/* ===== MAIN CONTENT ===== */
#main {{
  margin-top: var(--bar-h);
  margin-bottom: var(--footer-h);
  flex: 1;
}}
section.panel {{
  display: none;
  min-height: calc(100vh - var(--bar-h) - var(--footer-h));
  padding: 48px 24px 64px;
  animation: fadeIn var(--transition) ease;
}}
section.panel.active {{ display: block; }}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: translateY(0); }} }}

/* ===== FOOTER ===== */
#site-footer {{
  position: fixed;
  bottom: 0; left: 0; right: 0;
  height: var(--footer-h);
  background: var(--black);
  border-top: 2px solid var(--blue);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  z-index: 900;
}}
/* LOGO SWAP POINTS — replace <img> src with real file path when ready */
.footer-logo-syt {{
  height: 36px;
  width: auto;
  display: block;
  /* swap: <img src="logo-syt.png" alt="SYT.FYI"> */
}}
.footer-logo-ft {{
  height: 36px;
  width: auto;
  display: block;
  /* swap: <img src="logo-firetactic.png" alt="FireTactic"> */
}}
.footer-tagline {{
  font-family: var(--font-label);
  font-size: 9px;
  color: var(--white);
  text-transform: uppercase;
  letter-spacing: 1.5px;
  text-align: center;
  flex: 1;
  padding: 0 8px;
}}

/* ===== REUSABLE COMPONENTS ===== */
.container {{ max-width: 1100px; margin: 0 auto; }}

.section-tag {{
  font-family: var(--font-label);
  font-size: 10px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--blue);
  margin-bottom: 12px;
}}
h1.hero {{
  font-family: var(--font-hero);
  font-size: clamp(2rem, 6vw, 5rem);
  text-transform: uppercase;
  line-height: 1;
  color: var(--black);
  margin-bottom: 24px;
}}
h2.section-title {{
  font-family: var(--font-hero);
  font-size: clamp(1.5rem, 4vw, 2.8rem);
  text-transform: uppercase;
  line-height: 1.05;
  color: var(--black);
  margin-bottom: 20px;
}}
h3.card-title {{
  font-family: var(--font-label);
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 8px;
}}
p.body {{ font-size: 15px; line-height: 1.7; margin-bottom: 16px; }}
p.lead {{ font-size: 17px; font-weight: 600; line-height: 1.6; margin-bottom: 20px; }}

.divider {{
  height: 3px;
  background: var(--blue);
  margin: 32px 0;
}}
.divider-sm {{
  height: 2px;
  background: var(--black);
  margin: 20px 0;
}}

/* Cards */
.card-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
  margin-top: 24px;
}}
.card {{
  border: 2px solid var(--black);
  padding: 20px;
  background: var(--white);
}}
.card.blue {{ background: var(--blue); color: var(--white); border-color: var(--blue); }}
.card.black {{ background: var(--black); color: var(--white); border-color: var(--black); }}
.card.red {{ background: var(--red); color: var(--white); border-color: var(--red); }}
.card p {{ font-size: 13px; line-height: 1.5; margin-top: 6px; }}

/* Color blocks */
.block-row {{
  display: flex;
  flex-direction: column;
  gap: 0;
  margin: 32px 0;
}}
.block {{
  padding: 20px 28px;
  font-family: var(--font-hero);
  font-size: clamp(1.4rem, 4vw, 2.6rem);
  text-transform: uppercase;
  letter-spacing: 1px;
}}
.block.blue {{ background: var(--blue); color: var(--white); }}
.block.red {{ background: var(--red); color: var(--white); }}
.block.black {{ background: var(--black); color: var(--white); }}

/* Checklist */
.checklist {{ list-style: none; margin-top: 16px; }}
.checklist li {{
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
  font-size: 14px;
  font-weight: 500;
}}
.checklist li::before {{
  content: '▶';
  color: var(--blue);
  font-size: 10px;
  margin-top: 3px;
  flex-shrink: 0;
}}

/* Timeline */
.timeline {{ margin-top: 32px; position: relative; }}
.timeline::before {{
  content: '';
  position: absolute;
  left: 24px;
  top: 0; bottom: 0;
  width: 2px;
  background: var(--blue);
}}
.timeline-step {{
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
  padding-left: 8px;
  position: relative;
}}
.step-num {{
  width: 36px;
  height: 36px;
  background: var(--black);
  color: var(--white);
  font-family: var(--font-hero);
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 2px solid var(--blue);
  z-index: 1;
}}
.step-content h4 {{
  font-family: var(--font-label);
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 4px;
}}
.step-content p {{ font-size: 13px; color: #444; line-height: 1.5; }}

/* Accordion (FAQ) */
.accordion {{ margin-top: 16px; }}
.accordion-item {{ border: 2px solid var(--black); margin-bottom: 4px; }}
.accordion-btn {{
  width: 100%;
  text-align: left;
  padding: 14px 18px;
  font-family: var(--font-label);
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: var(--white);
  border: none;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background var(--transition), color var(--transition);
}}
.accordion-btn:hover {{ background: var(--black); color: var(--white); }}
.accordion-btn.open {{ background: var(--blue); color: var(--white); }}
.accordion-arrow {{ font-size: 12px; transition: transform var(--transition); }}
.accordion-btn.open .accordion-arrow {{ transform: rotate(180deg); }}
.accordion-body {{
  display: none;
  padding: 14px 18px;
  font-size: 14px;
  line-height: 1.6;
  border-top: 1px solid #eee;
  background: #fafafa;
}}
.accordion-body.open {{ display: block; }}

/* Number steps */
.num-steps {{ margin-top: 24px; }}
.num-step {{
  display: flex;
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 20px;
  border-left: 4px solid var(--blue);
  padding: 12px 16px;
  background: #f8f8f8;
}}
.num-step .num {{
  font-family: var(--font-hero);
  font-size: 2rem;
  color: var(--blue);
  line-height: 1;
  min-width: 40px;
}}
.num-step h4 {{
  font-family: var(--font-label);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 4px;
}}
.num-step p {{ font-size: 13px; line-height: 1.5; }}

/* Banner */
.banner {{
  padding: 18px 24px;
  font-family: var(--font-label);
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 1px;
  border: 2px solid var(--black);
  margin: 24px 0;
}}
.banner.blue {{ background: var(--blue); color: var(--white); border-color: var(--blue); }}
.banner.black {{ background: var(--black); color: var(--white); }}
.banner.red {{ background: var(--red); color: var(--white); border-color: var(--red); }}

/* Photo placeholder */
.photo-placeholder {{
  background: #e8e8e8;
  border: 2px dashed #bbb;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #888;
  font-size: 12px;
  font-family: var(--font-label);
  text-transform: uppercase;
  letter-spacing: 1px;
  text-align: center;
  padding: 24px;
  gap: 8px;
}}
.photo-placeholder .icon {{ font-size: 32px; }}

/* Fictional example styles */
.fictional-badge {{
  display: inline-block;
  background: var(--red);
  color: var(--white);
  font-family: var(--font-label);
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 2px;
  padding: 4px 12px;
  margin-bottom: 20px;
}}

/* Two-col layout */
.two-col {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-top: 24px;
}}
@media (max-width: 768px) {{ .two-col {{ grid-template-columns: 1fr; }} }}

/* Info table */
.info-table {{ width: 100%; border-collapse: collapse; margin-top: 16px; }}
.info-table td {{
  padding: 10px 14px;
  border: 1px solid #ddd;
  font-size: 13px;
  vertical-align: top;
}}
.info-table td:first-child {{
  font-family: var(--font-label);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: #f0f0f0;
  width: 35%;
  font-weight: 700;
}}

/* Summer timeline */
.summer-bar {{
  display: flex;
  margin-top: 24px;
  border: 2px solid var(--black);
  overflow: hidden;
}}
.summer-phase {{
  flex: 1;
  padding: 16px 10px;
  text-align: center;
  border-right: 2px solid var(--black);
}}
.summer-phase:last-child {{ border-right: none; }}
.summer-phase.blue {{ background: var(--blue); color: var(--white); }}
.summer-phase.black {{ background: var(--black); color: var(--white); }}
.summer-phase .month {{
  font-family: var(--font-label);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 6px;
  opacity: 0.8;
}}
.summer-phase .phase-name {{
  font-family: var(--font-hero);
  font-size: 1rem;
  text-transform: uppercase;
}}
@media (max-width: 600px) {{ .summer-bar {{ flex-direction: column; }} .summer-phase {{ border-right: none; border-bottom: 2px solid var(--black); }} }}

/* Flow diagram */
.flow-diagram {{ margin-top: 32px; }}
.flow-box {{
  border: 2px solid var(--black);
  padding: 14px 20px;
  text-align: center;
  font-family: var(--font-label);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
  background: var(--white);
  margin: 0 auto 4px;
  max-width: 280px;
}}
.flow-box.blue {{ background: var(--blue); color: var(--white); border-color: var(--blue); }}
.flow-box.black {{ background: var(--black); color: var(--white); }}
.flow-arrow {{ text-align: center; font-size: 20px; color: var(--blue); line-height: 1.2; margin: 4px 0; }}
.flow-branches {{
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 8px;
}}
.flow-branch {{
  border: 2px solid var(--black);
  padding: 12px 16px;
  text-align: center;
  font-family: var(--font-label);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
  min-width: 120px;
}}

/* Closing statement */
.closing-statement {{
  font-family: var(--font-hero);
  font-size: clamp(1.4rem, 4vw, 2.4rem);
  text-transform: uppercase;
  text-align: center;
  padding: 40px 24px;
  background: var(--black);
  color: var(--white);
  margin-top: 40px;
  letter-spacing: 2px;
}}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {{
  #nav-links {{ display: none; }}
  #hamburger {{ display: flex; }}
  .card-grid {{ grid-template-columns: 1fr 1fr; }}
  section.panel {{ padding: 32px 16px 72px; }}
  .footer-tagline {{ font-size: 7px; }}
}}
@media (max-width: 480px) {{
  .card-grid {{ grid-template-columns: 1fr; }}
  .footer-tagline {{ display: none; }}
}}
@media (min-width: 1100px) {{
  .card-grid {{ grid-template-columns: repeat(4, 1fr); }}
  section.panel {{ padding: 56px 48px 80px; }}
}}

/* ===== PRINT ===== */
@media print {{
  #topbar, #site-footer, #nav-drawer {{ display: none !important; }}
  #main {{ margin: 0; }}
  section.panel {{ display: none !important; padding: 0; }}
  section.panel.active {{ display: block !important; min-height: auto; }}
  .accordion-body {{ display: block !important; }}
  * {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
}}

/* ===== SVG HUB/SPOKE (Ecosystem) ===== */
#ecosystem-svg {{ width: 100%; max-width: 640px; display: block; margin: 0 auto; }}
</style>
</head>
<body>

<!-- ===== TOP BAR ===== -->
<div id="topbar">
  <nav id="navbar">
    <span id="nav-brand">DEPI</span>
    <div id="nav-links">
      <!-- GROUP: Initiative -->
      <span class="nav-group-label">Initiative</span>
      <button class="nav-btn" data-section="home">Home</button>
      <button class="nav-btn" data-section="about">About Tony</button>
      <button class="nav-btn" data-section="overview">Overview</button>
      <button class="nav-btn" data-section="why-edu">Why Edu Facilities</button>
      <button class="nav-btn" data-section="why-downtown">Why Downtown</button>
      <button class="nav-btn" data-section="ecosystem">Ecosystem</button>
      <button class="nav-btn" data-section="challenges">Challenges</button>
      <!-- GROUP: Programs -->
      <span class="nav-group-label">Programs</span>
      <button class="nav-btn" data-section="pilot">Pilot Program</button>
      <button class="nav-btn" data-section="pilot-benefits">Pilot Benefits</button>
      <!-- GROUP: Platforms -->
      <span class="nav-group-label">Platforms</span>
      <button class="nav-btn" data-section="syt360">SYT.360</button>
      <button class="nav-btn" data-section="sytpro">SYT.PRO</button>
      <button class="nav-btn" data-section="firetactic">FireTactic</button>
      <!-- GROUP: Operations -->
      <span class="nav-group-label">Operations</span>
      <button class="nav-btn" data-section="school-example">School Example</button>
      <button class="nav-btn" data-section="responder">Responder View</button>
      <button class="nav-btn" data-section="school-police">School Police</button>
      <button class="nav-btn" data-section="emergency">Emergency Planning</button>
      <button class="nav-btn" data-section="resources">Prep Resources</button>
      <!-- GROUP: Future -->
      <span class="nav-group-label">Future</span>
      <button class="nav-btn" data-section="summer">Summer</button>
      <button class="nav-btn" data-section="digital-twin">Digital Twin</button>
      <button class="nav-btn" data-section="overhead">Overhead Imagery</button>
      <button class="nav-btn" data-section="grants">Grant Opportunities</button>
      <!-- GROUP: Action -->
      <span class="nav-group-label">Action</span>
      <button class="nav-btn" data-section="faq">FAQ</button>
      <button class="nav-btn" data-section="next-steps">Next Steps</button>
      <button class="nav-btn" data-section="contact">Contact</button>
    </div>
    <button id="hamburger" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </nav>

  <!-- search row -->
  <div id="searchbar">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#555" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
    <input id="search-input" type="text" placeholder="Search sections… (school, pilot, fire rescue, responder…)" autocomplete="off">
    <button id="search-clear" aria-label="Clear">&times;</button>
  </div>
  <div id="search-results"></div>
</div>

<!-- Mobile drawer -->
<div id="nav-drawer">
  <div class="drawer-group-label">Initiative</div>
  <button class="drawer-btn" data-section="home">Home</button>
  <button class="drawer-btn" data-section="about">About Tony</button>
  <button class="drawer-btn" data-section="overview">Initiative Overview</button>
  <button class="drawer-btn" data-section="why-edu">Why Educational Facilities</button>
  <button class="drawer-btn" data-section="why-downtown">Why Downtown Miami</button>
  <button class="drawer-btn" data-section="ecosystem">Educational Ecosystem</button>
  <button class="drawer-btn" data-section="challenges">Current Challenges</button>
  <div class="drawer-group-label">Programs</div>
  <button class="drawer-btn" data-section="pilot">Pilot Program</button>
  <button class="drawer-btn" data-section="pilot-benefits">Pilot School Benefits</button>
  <div class="drawer-group-label">Platforms</div>
  <button class="drawer-btn" data-section="syt360">SYT.360</button>
  <button class="drawer-btn" data-section="sytpro">SYT.PRO</button>
  <button class="drawer-btn" data-section="firetactic">FireTactic</button>
  <div class="drawer-group-label">Operations</div>
  <button class="drawer-btn" data-section="school-example">School Example</button>
  <button class="drawer-btn" data-section="responder">Responder View</button>
  <button class="drawer-btn" data-section="school-police">School Police View</button>
  <button class="drawer-btn" data-section="emergency">Emergency Planning</button>
  <button class="drawer-btn" data-section="resources">Preparedness Resources</button>
  <div class="drawer-group-label">Future</div>
  <button class="drawer-btn" data-section="summer">Summer Opportunity</button>
  <button class="drawer-btn" data-section="digital-twin">Digital Twin</button>
  <button class="drawer-btn" data-section="overhead">Overhead Imagery</button>
  <button class="drawer-btn" data-section="grants">Grant Opportunities</button>
  <div class="drawer-group-label">Action</div>
  <button class="drawer-btn" data-section="faq">FAQ</button>
  <button class="drawer-btn" data-section="next-steps">Next Steps</button>
  <button class="drawer-btn" data-section="contact">Contact</button>
</div>

<!-- ===== MAIN CONTENT ===== -->
<main id="main">

<!-- ==================== SECTION 1: HOME ==================== -->
<section class="panel" id="sec-home">
<div class="container">
  <div class="section-tag">Downtown Educational Preparedness Initiative</div>
  <h1 class="hero">Downtown Educational<br>Preparedness Initiative</h1>
  <p class="lead">Create a repeatable preparedness framework that improves operational awareness, facility familiarization, emergency planning, and responder coordination before emergencies occur.</p>
  <div class="divider"></div>
  <div class="block-row">
    <div class="block blue">One Source of Truth</div>
    <div class="block red">Two Perspectives</div>
    <div class="block black">Safer Outcomes</div>
  </div>
  <div class="divider"></div>
  <!-- Connected nodes visual -->
  <h3 class="card-title" style="margin-bottom:20px;">A Collaborative Network</h3>
  <div style="overflow-x:auto;">
  <svg viewBox="0 0 620 260" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:620px;display:block;margin:0 auto;" aria-label="Stakeholder network diagram">
    <!-- lines -->
    <line x1="310" y1="130" x2="110" y2="60"  stroke="#008AFC" stroke-width="1.5" opacity="0.5"/>
    <line x1="310" y1="130" x2="510" y2="60"  stroke="#008AFC" stroke-width="1.5" opacity="0.5"/>
    <line x1="310" y1="130" x2="80"  y2="190" stroke="#008AFC" stroke-width="1.5" opacity="0.5"/>
    <line x1="310" y1="130" x2="540" y2="190" stroke="#008AFC" stroke-width="1.5" opacity="0.5"/>
    <line x1="310" y1="130" x2="200" y2="230" stroke="#008AFC" stroke-width="1.5" opacity="0.5"/>
    <line x1="310" y1="130" x2="420" y2="230" stroke="#008AFC" stroke-width="1.5" opacity="0.5"/>
    <!-- center -->
    <rect x="245" y="105" width="130" height="50" fill="#000"/>
    <text x="310" y="127" text-anchor="middle" fill="#008AFC" font-family="Arial Black" font-size="9" font-weight="700" letter-spacing="1">PREPAREDNESS</text>
    <text x="310" y="143" text-anchor="middle" fill="#FFF" font-family="Arial Black" font-size="9" font-weight="700" letter-spacing="1">INITIATIVE</text>
    <!-- nodes -->
    <rect x="55"  y="38"  width="110" height="34" fill="#F50B0B"/><text x="110" y="58"  text-anchor="middle" fill="#FFF" font-family="Arial Black" font-size="9">SCHOOL ADMIN</text>
    <rect x="455" y="38"  width="110" height="34" fill="#008AFC"/><text x="510" y="58"  text-anchor="middle" fill="#FFF" font-family="Arial Black" font-size="9">SCHOOL POLICE</text>
    <rect x="20"  y="170" width="120" height="34" fill="#000"/><text x="80"  y="190" text-anchor="middle" fill="#FFF" font-family="Arial Black" font-size="9">FIRE RESCUE</text>
    <rect x="478" y="170" width="100" height="34" fill="#000"/><text x="528" y="190" text-anchor="middle" fill="#FFF" font-family="Arial Black" font-size="9">EMS</text>
    <rect x="140" y="213" width="120" height="34" fill="#008AFC"/><text x="200" y="234" text-anchor="middle" fill="#FFF" font-family="Arial Black" font-size="9">LAW ENFORCE.</text>
    <rect x="358" y="213" width="104" height="34" fill="#F50B0B"/><text x="410" y="234" text-anchor="middle" fill="#FFF" font-family="Arial Black" font-size="9">FACILITIES</text>
  </svg>
  </div>
  <div class="banner blue" style="margin-top:32px;text-align:center;font-size:13px;">
    We can start with one school — evaluate the process — learn from it — and determine what comes next.
  </div>
</div>
</section>

<!-- ==================== SECTION 2: ABOUT TONY ==================== -->
<section class="panel" id="sec-about">
<div class="container">
  <div class="section-tag">About the Presenter</div>
  <h2 class="section-title">About Tony Prol</h2>
  <div class="two-col">
    <div>
      <!-- LOGO SWAP: replace div with <img src="tony-photo.jpg" alt="Tony Prol" style="width:100%;border:2px solid #000;"> -->
      <div class="photo-placeholder" style="height:280px;">
        <span class="icon">👤</span>
        <span>Photo — Tony Prol</span>
        <span style="font-size:10px;color:#aaa;">Swap: &lt;img src="tony-photo.jpg"&gt;</span>
      </div>
    </div>
    <div>
      <h3 class="card-title" style="color:var(--blue);font-size:18px;">Tony Prol</h3>
      <div class="divider-sm"></div>
      <table class="info-table">
        <tr><td>Title</td><td>Miami Beach Firefighter / Paramedic</td></tr>
        <tr><td>Company</td><td>Founder &amp; CEO — SYT.FYI</td></tr>
        <tr><td>Foundation</td><td>President &amp; Executive Director — First In Safety Foundation</td></tr>
        <tr><td>Location</td><td>Downtown Miami Office</td></tr>
      </table>
    </div>
  </div>
  <div class="divider"></div>
  <h3 class="card-title">Focus Areas</h3>
  <div class="card-grid" style="grid-template-columns:repeat(auto-fill,minmax(160px,1fr));">
    <div class="card blue"><h3 class="card-title">Preparedness</h3><p>Building proactive preparedness frameworks before emergencies occur.</p></div>
    <div class="card black"><h3 class="card-title">Responder Coordination</h3><p>Improving how responders access and share critical facility information.</p></div>
    <div class="card"><h3 class="card-title">Operational Awareness</h3><p>Ensuring all stakeholders share a single source of truth.</p></div>
    <div class="card"><h3 class="card-title">Educational Facilities</h3><p>Specialized focus on schools, colleges, and universities.</p></div>
    <div class="card blue"><h3 class="card-title">Community Safety</h3><p>Partnerships that serve the whole community — not just one agency.</p></div>
  </div>
  <div class="banner black" style="margin-top:32px;">
    This initiative is about preparedness and partnership — not technology. Technology is a tool, not the goal.
  </div>
</div>
</section>

<!-- ==================== SECTION 3: INITIATIVE OVERVIEW ==================== -->
<section class="panel" id="sec-overview">
<div class="container">
  <div class="section-tag">What We Are Building</div>
  <h2 class="section-title">Initiative Overview</h2>
  <p class="lead">This initiative starts with educational facilities in Downtown Miami and Brickell — evaluating preparedness, improving facility familiarization, strengthening responder awareness, and documenting lessons learned.</p>
  <div class="divider"></div>
  <h3 class="card-title">Objective</h3>
  <p class="body">Build a repeatable preparedness framework that any educational institution — from a single charter school to a large university — can evaluate, adopt, and scale through genuine partnership with public safety agencies.</p>
  <div class="card-grid" style="grid-template-columns:repeat(3,1fr);margin-top:32px;">
    <div class="card black" style="text-align:center;">
      <div style="font-family:var(--font-hero);font-size:3rem;color:var(--blue);">01</div>
      <h3 class="card-title" style="color:var(--white);">Scalable</h3>
      <p style="color:#ccc;">A framework built to grow — from one school to an entire district.</p>
    </div>
    <div class="card blue" style="text-align:center;">
      <div style="font-family:var(--font-hero);font-size:3rem;color:var(--white);">02</div>
      <h3 class="card-title">Collaborative</h3>
      <p>Built in partnership with schools, public safety, and the broader community.</p>
    </div>
    <div class="card" style="text-align:center;border:2px solid var(--black);">
      <div style="font-family:var(--font-hero);font-size:3rem;color:var(--red);">03</div>
      <h3 class="card-title">Starts With One School</h3>
      <p>No pressure, no commitment. One visit, one evaluation, one set of lessons learned.</p>
    </div>
  </div>
  <div class="divider"></div>
  <div class="banner blue">
    We evaluate. We learn. We document. We decide together what comes next.
  </div>
</div>
</section>

<!-- ==================== SECTION 4: WHY EDUCATIONAL FACILITIES ==================== -->
<section class="panel" id="sec-why-edu">
<div class="container">
  <div class="section-tag">The Case for Educational Facilities</div>
  <h2 class="section-title">Why Educational Facilities</h2>
  <div class="banner black">
    Educational facilities present unique preparedness, occupancy, reunification, and responder coordination challenges that require dedicated planning and collaboration.
  </div>
  <div class="card-grid" style="margin-top:32px;">
    <div class="card blue"><h3 class="card-title">K-12 Schools</h3><p>High-density populations, complex ingress/egress, reunification requirements, and regular occupancy changes.</p></div>
    <div class="card"><h3 class="card-title">Charter Schools</h3><p>Independent governance structures often operate with limited preparedness infrastructure and staff turnover.</p></div>
    <div class="card black"><h3 class="card-title">Private Schools</h3><p>Varied facilities, independent safety programs, and limited direct coordination with public safety agencies.</p></div>
    <div class="card blue"><h3 class="card-title">Colleges</h3><p>Open campuses, adult populations, multiple buildings, and complex multi-agency coordination needs.</p></div>
    <div class="card"><h3 class="card-title">Universities</h3><p>Large footprints, residential populations, research facilities, and hospital/clinic adjacencies.</p></div>
    <div class="card black"><h3 class="card-title">Trade Schools</h3><p>Industrial equipment, specialized hazards, and populations unfamiliar with emergency procedures.</p></div>
  </div>
  <div class="divider"></div>
  <h3 class="card-title">Why This Matters</h3>
  <ul class="checklist">
    <li>Staff turnover disrupts institutional knowledge every year</li>
    <li>Responding agencies may have outdated or no facility information</li>
    <li>Reunification and assembly area documentation is often inconsistent</li>
    <li>Emergency contacts change and rarely reach the right responder in time</li>
    <li>Multiple agencies respond but rarely share a single information source</li>
  </ul>
</div>
</section>

<!-- ==================== SECTION 5: WHY DOWNTOWN MIAMI ==================== -->
<section class="panel" id="sec-why-downtown">
<div class="container">
  <div class="section-tag">The Pilot Geography</div>
  <h2 class="section-title">Why Downtown Miami</h2>
  <p class="lead">Downtown Miami and Brickell offer an ideal environment to evaluate a preparedness initiative: concentrated institutions, multiple public safety agencies, and a walkable geography that creates a natural feedback loop.</p>
  <div class="divider"></div>
  <div class="card-grid">
    <div class="card black"><h3 class="card-title" style="color:var(--blue);">01</h3><h3 class="card-title" style="color:var(--white);">Dense Urban Environment</h3><p style="color:#ccc;">High building concentration means responder familiarization is critical.</p></div>
    <div class="card blue"><h3 class="card-title">02</h3><h3 class="card-title">High Building Concentration</h3><p>Multiple educational facilities within a compact, navigable area.</p></div>
    <div class="card"><h3 class="card-title">03</h3><h3 class="card-title">Multiple Educational Institutions</h3><p>MDCPS schools, charter schools, MDC, FIU, and private institutions all within proximity.</p></div>
    <div class="card black"><h3 class="card-title" style="color:var(--blue);">04</h3><h3 class="card-title" style="color:var(--white);">Shared Public Safety Resources</h3><p style="color:#ccc;">Fire, EMS, law enforcement, and school police all serve the same zone.</p></div>
    <div class="card blue"><h3 class="card-title">05</h3><h3 class="card-title">Walkable Ecosystem</h3><p>Proximity allows for in-person evaluation, relationship-building, and rapid iteration.</p></div>
    <div class="card"><h3 class="card-title">06</h3><h3 class="card-title">Local Support Presence</h3><p>Tony's Downtown Miami office provides direct, on-the-ground coordination.</p></div>
    <div class="card black"><h3 class="card-title" style="color:var(--blue);">07</h3><h3 class="card-title" style="color:var(--white);">Fast Feedback Loop</h3><p style="color:#ccc;">Compact geography accelerates learning, documentation, and evaluation.</p></div>
    <div class="card blue"><h3 class="card-title">08</h3><h3 class="card-title">Scalable Pilot Zone</h3><p>Lessons learned here can be replicated to any urban or suburban district.</p></div>
  </div>
</div>
</section>

<!-- ==================== SECTION 6: EDUCATIONAL ECOSYSTEM ==================== -->
<section class="panel" id="sec-ecosystem">
<div class="container">
  <div class="section-tag">The Network</div>
  <h2 class="section-title">Educational Ecosystem</h2>
  <p class="lead">The initiative is designed to serve the full spectrum of educational institutions in the Downtown Miami area — starting with one partner, growing through trust and demonstrated value.</p>
  <div class="divider"></div>

  <!-- Hub-and-spoke SVG -->
  <svg id="ecosystem-svg" viewBox="0 0 640 360" xmlns="http://www.w3.org/2000/svg" aria-label="Educational ecosystem hub and spoke diagram">
    <!-- spokes -->
    <line x1="320" y1="180" x2="130" y2="60"  stroke="#008AFC" stroke-width="1.5" opacity="0.6"/>
    <line x1="320" y1="180" x2="510" y2="60"  stroke="#008AFC" stroke-width="1.5" opacity="0.6"/>
    <line x1="320" y1="180" x2="80"  y2="200" stroke="#008AFC" stroke-width="1.5" opacity="0.6"/>
    <line x1="320" y1="180" x2="560" y2="200" stroke="#008AFC" stroke-width="1.5" opacity="0.6"/>
    <line x1="320" y1="180" x2="160" y2="310" stroke="#008AFC" stroke-width="1.5" opacity="0.6"/>
    <line x1="320" y1="180" x2="480" y2="310" stroke="#008AFC" stroke-width="1.5" opacity="0.6"/>
    <line x1="320" y1="180" x2="320" y2="330" stroke="#008AFC" stroke-width="1.5" opacity="0.6"/>
    <!-- center hub -->
    <rect x="215" y="148" width="210" height="64" fill="#000"/>
    <text x="320" y="170" text-anchor="middle" fill="#008AFC" font-family="Arial Black" font-size="9" letter-spacing="1.5">DOWNTOWN EDUCATIONAL</text>
    <text x="320" y="184" text-anchor="middle" fill="#FFF" font-family="Arial Black" font-size="9" letter-spacing="1.5">PREPAREDNESS INITIATIVE</text>
    <text x="320" y="200" text-anchor="middle" fill="#F50B0B" font-family="Arial Black" font-size="8" letter-spacing="1">DOWNTOWN MIAMI · BRICKELL</text>
    <!-- spoke nodes — hover via CSS class -->
    <g class="eco-node" data-label="MDCPS">
      <rect x="60"  y="38"  width="140" height="36" fill="#008AFC"/>
      <text x="130" y="60" text-anchor="middle" fill="#FFF" font-family="Arial Black" font-size="10">MDCPS</text>
    </g>
    <g class="eco-node" data-label="Academica">
      <rect x="440" y="38"  width="140" height="36" fill="#F50B0B"/>
      <text x="510" y="60" text-anchor="middle" fill="#FFF" font-family="Arial Black" font-size="10">ACADEMICA</text>
    </g>
    <g class="eco-node" data-label="Charter Schools">
      <rect x="10"  y="178" width="140" height="36" fill="#000"/>
      <text x="80"  y="200" text-anchor="middle" fill="#FFF" font-family="Arial Black" font-size="9">CHARTER SCHOOLS</text>
    </g>
    <g class="eco-node" data-label="Miami Dade College">
      <rect x="490" y="178" width="140" height="36" fill="#000"/>
      <text x="560" y="196" text-anchor="middle" fill="#008AFC" font-family="Arial Black" font-size="9">MIAMI DADE</text>
      <text x="560" y="208" text-anchor="middle" fill="#FFF" font-family="Arial Black" font-size="9">COLLEGE</text>
    </g>
    <g class="eco-node" data-label="FIU">
      <rect x="90"  y="290" width="140" height="36" fill="#008AFC"/>
      <text x="160" y="312" text-anchor="middle" fill="#FFF" font-family="Arial Black" font-size="10">FIU</text>
    </g>
    <g class="eco-node" data-label="Private Schools">
      <rect x="410" y="290" width="140" height="36" fill="#F50B0B"/>
      <text x="480" y="312" text-anchor="middle" fill="#FFF" font-family="Arial Black" font-size="9">PRIVATE SCHOOLS</text>
    </g>
    <g class="eco-node" data-label="Future Partners">
      <rect x="245" y="318" width="150" height="30" fill="#222"/>
      <text x="320" y="337" text-anchor="middle" fill="#888" font-family="Arial Black" font-size="8">FUTURE PARTNERS</text>
    </g>
  </svg>

  <div class="banner blue" style="text-align:center;margin-top:24px;">
    Starting With One School. Growing Through Partnership.
  </div>
</div>
</section>

<!-- ==================== SECTION 7: CURRENT CHALLENGES ==================== -->
<section class="panel" id="sec-challenges">
<div class="container">
  <div class="section-tag">The Problem We Are Solving</div>
  <h2 class="section-title">Current Challenges</h2>
  <p class="lead">Before we can improve preparedness, we need to understand the barriers that exist today across educational facilities and the agencies that serve them.</p>
  <div class="card-grid">
    <div class="card red"><h3 class="card-title">Information Silos</h3><p>Critical facility data exists in isolation — one agency can't see what another knows.</p></div>
    <div class="card black"><h3 class="card-title">Multiple Documents</h3><p>Emergency plans live in binders, shared drives, email threads, and outdated PDFs — no single source.</p></div>
    <div class="card"><h3 class="card-title">Facility Familiarization</h3><p>Responding units often have never been inside the building they're responding to.</p></div>
    <div class="card blue"><h3 class="card-title">Turnover</h3><p>Staff changes mean institutional knowledge walks out the door every year — along with safety context.</p></div>
    <div class="card black"><h3 class="card-title">Emergency Access</h3><p>Gates, lock boxes, utility access, and entry points are often unknown until arrival on scene.</p></div>
    <div class="card red"><h3 class="card-title">Building Complexity</h3><p>Multi-story, multi-wing, multi-building campuses create confusion under time pressure.</p></div>
    <div class="card"><h3 class="card-title">Responder Awareness</h3><p>AED locations, assembly areas, reunification zones — not documented or not accessible in the field.</p></div>
    <div class="card blue"><h3 class="card-title">Coordination Challenges</h3><p>Multiple responding agencies arrive with different information, creating confusion and gaps.</p></div>
  </div>
  <div class="banner black" style="margin-top:32px;">
    These are not hypothetical problems. They are documented, real, and addressable through preparedness.
  </div>
</div>
</section>

<!-- ==================== SECTION 8: PILOT PROGRAM ==================== -->
<section class="panel" id="sec-pilot">
<div class="container">
  <div class="section-tag">The Approach</div>
  <h2 class="section-title">Pilot Program</h2>
  <p class="lead">The pilot is designed to be low-risk, high-value, and educational for every participant. It starts with one school and one visit.</p>
  <div class="divider"></div>
  <div class="timeline">
    <div class="timeline-step">
      <div class="step-num">1</div>
      <div class="step-content"><h4>School Selection</h4><p>Identify one willing educational institution in Downtown Miami or Brickell to serve as the pilot partner.</p></div>
    </div>
    <div class="timeline-step">
      <div class="step-num">2</div>
      <div class="step-content"><h4>SYT.360 Visit</h4><p>Conduct a no-cost, on-site preparedness visit to document the facility, contacts, utilities, and critical information.</p></div>
    </div>
    <div class="timeline-step">
      <div class="step-num">3</div>
      <div class="step-content"><h4>Preparedness Review</h4><p>Review existing emergency plans, identify gaps, and document the current state of preparedness.</p></div>
    </div>
    <div class="timeline-step">
      <div class="step-num">4</div>
      <div class="step-content"><h4>School Profile</h4><p>Build a complete operational profile of the facility — accessible to the school and approved downstream partners.</p></div>
    </div>
    <div class="timeline-step">
      <div class="step-num">5</div>
      <div class="step-content"><h4>Responder Familiarization</h4><p>Share relevant facility information with verified responders — Fire Rescue, EMS, Law Enforcement, School Police.</p></div>
    </div>
    <div class="timeline-step">
      <div class="step-num">6</div>
      <div class="step-content"><h4>Lessons Learned</h4><p>Document what worked, what didn't, and what all parties learned from the process.</p></div>
    </div>
    <div class="timeline-step">
      <div class="step-num">7</div>
      <div class="step-content"><h4>Expansion Evaluation</h4><p>Based on feedback from all partners, jointly determine whether and how to expand the initiative.</p></div>
    </div>
  </div>
  <div class="closing-statement">It starts with one school.</div>
</div>
</section>

<!-- ==================== SECTION 9: PILOT BENEFITS ==================== -->
<section class="panel" id="sec-pilot-benefits">
<div class="container">
  <div class="section-tag">What the Pilot School Receives</div>
  <h2 class="section-title">Pilot School Benefits</h2>
  <div class="banner blue">At no cost to the school. No commitment beyond participation. No obligation beyond honesty.</div>
  <ul class="checklist" style="margin-top:24px;">
    <li><strong>SYT.360 Visit</strong> — A professional on-site preparedness visit conducted by Tony Prol</li>
    <li><strong>Preparedness Review</strong> — A documented review of the school's current preparedness posture</li>
    <li><strong>School Operational Profile</strong> — A complete, structured facility profile for internal and responder use</li>
    <li><strong>Emergency Planning Support</strong> — Resources and guidance to improve existing emergency plans</li>
    <li><strong>Overhead Documentation</strong> — Aerial imagery and documentation of the school site</li>
    <li><strong>Responder Familiarization</strong> — Approved facility information delivered to verified responding agencies</li>
    <li><strong>School Police Familiarization</strong> — Dedicated familiarization session with School Police personnel</li>
    <li><strong>Two-Year SYT.PRO Access</strong> — Full platform access for evaluation and feedback purposes</li>
    <li><strong>Lessons Learned Report</strong> — A formal written report documenting findings and recommendations</li>
  </ul>
  <div class="banner black" style="margin-top:32px;">
    The pilot school's feedback shapes every future decision. Their experience is the roadmap.
  </div>
</div>
</section>

<!-- ==================== SECTION 10: SYT.360 ==================== -->
<section class="panel" id="sec-syt360">
<div class="container">
  <div class="section-tag">SYT.FYI</div>
  <h2 class="section-title">SYT.360</h2>
  <div class="banner blue" style="font-size:16px;padding:20px 24px;">No-Cost Preparedness Visit</div>
  <p class="body" style="margin-top:20px;">The SYT.360 visit is a structured, on-site assessment conducted by a trained preparedness professional. It is not an inspection — it is a collaborative documentation process designed to capture what exists and identify what is missing.</p>
  <div class="divider"></div>
  <h3 class="card-title">What a SYT.360 Visit Covers</h3>
  <div class="card-grid" style="grid-template-columns:repeat(auto-fill,minmax(200px,1fr));margin-top:20px;">
    <div class="card"><h3 class="card-title">Facility Walkthrough</h3><p>Physical tour of the entire facility — every entrance, wing, and critical space.</p></div>
    <div class="card blue"><h3 class="card-title">Emergency Contacts</h3><p>Key personnel, roles, and how to reach them — documented and current.</p></div>
    <div class="card black"><h3 class="card-title">AED Documentation</h3><p>Location, model, and condition of every AED on campus.</p></div>
    <div class="card"><h3 class="card-title">Utility Documentation</h3><p>Gas, electric, and water shutoff locations — clearly mapped and described.</p></div>
    <div class="card blue"><h3 class="card-title">Assembly Areas</h3><p>Primary and alternate assembly zones — mapped and documented.</p></div>
    <div class="card"><h3 class="card-title">Reunification Areas</h3><p>Student-parent reunification zones — aligned with existing plans or newly established.</p></div>
    <div class="card black"><h3 class="card-title">Existing Plan Review</h3><p>Review of current emergency operations plans, evacuation procedures, and safety documents.</p></div>
    <div class="card"><h3 class="card-title">Floor Plans</h3><p>Documentation of available floor plans and identification of gaps.</p></div>
    <div class="card blue"><h3 class="card-title">Overhead Documentation</h3><p>Aerial imagery and site documentation of the school grounds and surroundings.</p></div>
    <div class="card"><h3 class="card-title">School Profile</h3><p>Compilation of all gathered information into a structured, usable operational profile.</p></div>
  </div>
</div>
</section>

<!-- ==================== SECTION 11: SYT.PRO ==================== -->
<section class="panel" id="sec-sytpro">
<div class="container">
  <div class="section-tag">SYT.FYI Platform</div>
  <h2 class="section-title">SYT.PRO</h2>
  <div class="banner blue" style="font-size:16px;padding:20px 24px;">Enhanced School Preparedness Platform</div>
  <p class="body" style="margin-top:20px;">SYT.PRO is the school-facing platform where all preparedness information lives — organized, accessible, and controlled entirely by the school.</p>
  <div class="divider"></div>
  <div class="card-grid" style="grid-template-columns:repeat(auto-fill,minmax(200px,1fr));">
    <div class="card black"><h3 class="card-title" style="color:var(--blue);">School Dashboard</h3><p style="color:#ccc;">A centralized view of the school's preparedness posture — contacts, documents, and status at a glance.</p></div>
    <div class="card"><h3 class="card-title">Document Repository</h3><p>A structured, searchable library of emergency plans, floor plans, and preparedness documents.</p></div>
    <div class="card blue"><h3 class="card-title">Preparedness Resources</h3><p>Curated resources, templates, and guidance to help schools improve their preparedness programs.</p></div>
    <div class="card"><h3 class="card-title">Operational Profile</h3><p>The school's complete facility and operational profile — maintained, current, and ready to share.</p></div>
    <div class="card black"><h3 class="card-title" style="color:var(--blue);">Facility Information</h3><p style="color:#ccc;">AED locations, utilities, access points, assembly areas — all in one place.</p></div>
    <div class="card blue"><h3 class="card-title">Emergency Planning Resources</h3><p>Tools and templates to support or improve the school's existing emergency operations plans.</p></div>
    <div class="card"><h3 class="card-title">Responder Familiarization Support</h3><p>Manage what information is shared with which responding agencies — school controls access.</p></div>
  </div>
  <div class="banner red" style="margin-top:32px;">
    Pilot schools receive two years of access for evaluation and feedback purposes.
  </div>
</div>
</section>

<!-- ==================== SECTION 12: FIRETACTIC ==================== -->
<section class="panel" id="sec-firetactic">
<div class="container">
  <div class="section-tag">First In Safety Foundation</div>
  <h2 class="section-title">FireTactic</h2>
  <div class="banner blue" style="font-size:14px;padding:16px 24px;">Verified Responder Platform — Operated by First In Safety Foundation</div>
  <p class="body" style="margin-top:20px;">FireTactic is the responder-facing platform — purpose-built for public safety professionals who need reliable, pre-incident facility information when they need it most.</p>
  <div class="divider"></div>
  <div class="two-col">
    <div>
      <h3 class="card-title" style="color:var(--blue);">Who Uses FireTactic</h3>
      <ul class="checklist" style="margin-top:12px;">
        <li>School Police — campus-specific familiarization and coordination</li>
        <li>Fire Rescue — pre-incident planning and structural awareness</li>
        <li>EMS — access, AED locations, and critical contact information</li>
        <li>Law Enforcement — tactical awareness and facility familiarity</li>
      </ul>
    </div>
    <div>
      <h3 class="card-title" style="color:var(--red);">Platform Capabilities</h3>
      <ul class="checklist" style="margin-top:12px;">
        <li>Pre-Incident Planning — document and distribute facility profiles</li>
        <li>Training — use facility data for tabletop and field exercises</li>
        <li>Familiarization — help responders know a building before they enter it</li>
        <li>Responder Notes — agency-specific annotations and operational notes</li>
        <li>Operational Awareness — shared, current, verified facility information</li>
      </ul>
    </div>
  </div>
  <div class="divider"></div>
  <div class="card-grid" style="grid-template-columns:repeat(3,1fr);">
    <div class="card" style="border:2px solid var(--blue);text-align:center;padding:24px;">
      <div style="font-family:var(--font-hero);font-size:2rem;color:var(--blue);">VERIFIED</div>
      <p style="margin-top:8px;font-size:12px;">All users are identity-verified public safety professionals</p>
    </div>
    <div class="card" style="border:2px solid var(--red);text-align:center;padding:24px;">
      <div style="font-family:var(--font-hero);font-size:2rem;color:var(--red);">CONTROLLED</div>
      <p style="margin-top:8px;font-size:12px;">Schools decide what information is shared and with whom</p>
    </div>
    <div class="card black" style="text-align:center;padding:24px;">
      <div style="font-family:var(--font-hero);font-size:2rem;color:var(--white);">CURRENT</div>
      <p style="margin-top:8px;font-size:12px;color:#ccc;">Information is maintained and updated by the school</p>
    </div>
  </div>
  <div class="banner black" style="margin-top:32px;">
    First In Safety Foundation operates FireTactic as part of its mission to improve responder preparedness and community safety.
  </div>
</div>
</section>

<!-- ==================== SECTION 13: SCHOOL EXAMPLE ==================== -->
<section class="panel" id="sec-school-example">
<div class="container">
  <div class="fictional-badge">⚠ Fictional Example — For Illustration Purposes Only</div>
  <div class="section-tag">What a School Profile Looks Like</div>
  <h2 class="section-title">Brickell Bay Preparatory Academy</h2>
  <p style="font-size:12px;color:#888;margin-bottom:24px;">This is a fictional school created to demonstrate the format of a real operational profile. All names, contacts, and details are invented.</p>

  <div class="two-col">
    <div>
      <!-- SWAP: <img src="school-exterior.jpg" alt="School exterior photo"> -->
      <div class="photo-placeholder" style="height:200px;">
        <span class="icon">🏫</span>
        <span>School Exterior Photo</span>
        <span style="font-size:10px;color:#aaa;">Swap: &lt;img src="school-exterior.jpg"&gt;</span>
      </div>
    </div>
    <div>
      <!-- SWAP: <img src="school-aerial.jpg" alt="Aerial view of school"> -->
      <div class="photo-placeholder" style="height:200px;">
        <span class="icon">✈</span>
        <span>Aerial / Overhead View</span>
        <span style="font-size:10px;color:#aaa;">Swap: &lt;img src="school-aerial.jpg"&gt;</span>
      </div>
    </div>
  </div>

  <div class="divider"></div>

  <div class="two-col">
    <div>
      <table class="info-table">
        <tr><td>School Name</td><td>Brickell Bay Preparatory Academy <span style="color:var(--red);font-size:10px;">(FICTIONAL)</span></td></tr>
        <tr><td>Address</td><td>100 Brickell Bay Drive, Miami, FL 33131 <span style="color:var(--red);font-size:10px;">(FICTIONAL)</span></td></tr>
        <tr><td>Type</td><td>Charter School, Grades K-8</td></tr>
        <tr><td>Enrollment</td><td>Approx. 420 students</td></tr>
        <tr><td>Main Entrance</td><td>North side of building — Brickell Bay Dr. Buzzer access, security camera, lobby check-in.</td></tr>
        <tr><td>Secondary Entrance</td><td>East side — staff badge access only. Loading dock on south side, chain-link gate.</td></tr>
      </table>
    </div>
    <div>
      <table class="info-table">
        <tr><td>Assembly Area</td><td>Northwest parking lot — marked with yellow paint. Capacity: 500+.</td></tr>
        <tr><td>Reunification</td><td>Southeast corner of adjacent park — parent/student reunification zone.</td></tr>
        <tr><td>AED #1</td><td>Main lobby — left of reception desk, green cabinet</td></tr>
        <tr><td>AED #2</td><td>2nd floor hallway — near Room 212, wall-mounted</td></tr>
        <tr><td>AED #3</td><td>Gymnasium — east wall, near bleachers</td></tr>
        <tr><td>Gas Shutoff</td><td>SE exterior mechanical room — orange valve, marked with sign</td></tr>
        <tr><td>Electric</td><td>Basement utility room B1 — main panel labeled "MAIN"</td></tr>
        <tr><td>Water</td><td>NE exterior — behind HVAC units, blue valve</td></tr>
      </table>
    </div>
  </div>

  <div class="divider"></div>

  <div class="two-col">
    <div>
      <h3 class="card-title">Emergency Contacts <span style="color:var(--red);font-size:10px;">(FICTIONAL)</span></h3>
      <table class="info-table" style="margin-top:12px;">
        <tr><td>Principal</td><td>Dr. Maria Sanchez — Principal</td></tr>
        <tr><td>Asst. Principal</td><td>Mr. David Torres — Operations</td></tr>
        <tr><td>Safety Coord.</td><td>Ms. Angela Rivera</td></tr>
        <tr><td>Facilities</td><td>Mr. Carlos Gomez</td></tr>
        <tr><td>After Hours</td><td>[Building Security — Placeholder]</td></tr>
      </table>
    </div>
    <div>
      <h3 class="card-title">Documents On File</h3>
      <ul class="checklist" style="margin-top:12px;">
        <li>Emergency Operations Plan (2024)</li>
        <li>Evacuation Procedures — All Hazards</li>
        <li>Floor Plans — Ground &amp; 2nd Floor</li>
        <li>Assembly Area Map</li>
        <li>Reunification Protocol</li>
        <li>Utility Map</li>
      </ul>
    </div>
  </div>

  <div class="divider"></div>

  <div class="two-col">
    <div>
      <div class="card blue">
        <h3 class="card-title">Responder Notes</h3>
        <p>Main entrance requires buzzer release from office. North parking lot gate is padlocked after hours — key on Knox box at main entrance. Basement stairwell at northwest corner — only access to utility room during event. No elevator. Building is fully sprinklered — panel in basement B1.</p>
      </div>
    </div>
    <div>
      <div class="card black">
        <h3 class="card-title" style="color:var(--blue);">School Police Notes</h3>
        <p style="color:#ccc;">SRO assigned: Officer [Name Placeholder]. Office located Room 101, main lobby left of entry. Two camera systems — main lobby and exterior perimeter. Access to camera system through front office. Lockdown protocol: doors key-lock, no external handle release.</p>
      </div>
    </div>
  </div>

  <div class="banner red" style="margin-top:32px;">
    ⚠ This is a fictional example. All names, addresses, contacts, and operational details are invented for illustration purposes only.
  </div>
</div>
</section>

<!-- ==================== SECTION 14: RESPONDER VIEW ==================== -->
<section class="panel" id="sec-responder">
<div class="container">
  <div class="section-tag">How Information Flows</div>
  <h2 class="section-title">Responder View</h2>
  <p class="lead">The school is always the source of truth. Information flows downstream only with the school's knowledge and approval.</p>
  <div class="divider"></div>
  <div class="flow-diagram">
    <div class="flow-box black" style="max-width:320px;padding:20px;">
      <div style="font-family:var(--font-hero);font-size:1.1rem;color:var(--blue);">School Administration</div>
      <div style="font-size:11px;color:#aaa;margin-top:4px;font-family:var(--font-body);">Owns and controls all information</div>
    </div>
    <div class="flow-arrow">↓</div>
    <div class="flow-box blue" style="max-width:320px;">
      <div style="font-family:var(--font-hero);font-size:1rem;">SYT.PRO Platform</div>
      <div style="font-size:11px;opacity:0.8;margin-top:4px;font-family:var(--font-body);">School reviews, approves, and manages shared information</div>
    </div>
    <div class="flow-arrow">↓</div>
    <div class="flow-box black" style="max-width:320px;">
      <div style="font-family:var(--font-hero);font-size:1rem;color:var(--blue);">FireTactic</div>
      <div style="font-size:11px;color:#aaa;margin-top:4px;font-family:var(--font-body);">Verified responder platform — First In Safety Foundation</div>
    </div>
    <div class="flow-arrow">↓</div>
    <div class="flow-branches">
      <div class="flow-branch" style="background:var(--red);color:#fff;border-color:var(--red);">School Police</div>
      <div class="flow-branch" style="background:var(--blue);color:#fff;border-color:var(--blue);">Fire Rescue</div>
      <div class="flow-branch" style="background:var(--black);color:#fff;">EMS</div>
      <div class="flow-branch">Law Enforcement</div>
    </div>
  </div>
  <div class="divider"></div>
  <div class="two-col" style="margin-top:24px;">
    <div class="card blue">
      <h3 class="card-title">The School Controls Access</h3>
      <p>The school determines which agencies receive which information. Nothing flows without school awareness and approval.</p>
    </div>
    <div class="card black">
      <h3 class="card-title" style="color:var(--blue);">Responders Get What They Need</h3>
      <p style="color:#ccc;">Verified responders access current, accurate facility information before an incident — not for the first time during one.</p>
    </div>
  </div>
  <div class="banner black" style="margin-top:32px;">
    The goal is familiar responders — not surprised ones.
  </div>
</div>
</section>

<!-- ==================== SECTION 15: SCHOOL POLICE VIEW ==================== -->
<section class="panel" id="sec-school-police">
<div class="container">
  <div class="section-tag">Dedicated Focus</div>
  <h2 class="section-title">School Police View</h2>
  <div class="banner blue" style="font-size:14px;padding:18px 24px;margin-bottom:32px;">
    School Police play a critical role in preparedness, facility awareness, responder coordination, and emergency response.
  </div>
  <p class="body">School Police are often the first point of contact in any campus emergency — and yet they frequently lack the same level of pre-incident documentation that mutual-aid responders expect from other environments. This initiative directly addresses that gap.</p>
  <div class="divider"></div>
  <div class="card-grid" style="grid-template-columns:repeat(auto-fill,minmax(240px,1fr));">
    <div class="card black">
      <h3 class="card-title" style="color:var(--blue);">Facility Familiarization</h3>
      <p style="color:#ccc;">School Police officers gain documented, structured access to facility information — floor plans, access points, AED locations, utility locations — in a format purpose-built for operational use. Not a binder. Not a PDF. A live profile.</p>
    </div>
    <div class="card blue">
      <h3 class="card-title">Shared Awareness with Mutual Aid</h3>
      <p>When Fire Rescue, EMS, or Law Enforcement arrives on a school campus, they need to share situational awareness with School Police immediately. This initiative creates a common operating picture so everyone is working from the same source.</p>
    </div>
    <div class="card">
      <h3 class="card-title">Documentation Continuity Through Turnover</h3>
      <p>Officers rotate. Staff changes. School resource officers are reassigned. When that happens, the institutional knowledge about a campus shouldn't leave with them. A maintained operational profile ensures continuity regardless of personnel changes.</p>
    </div>
    <div class="card black">
      <h3 class="card-title" style="color:var(--blue);">Pre-Incident Planning Support</h3>
      <p style="color:#ccc;">School Police benefit from the same pre-incident planning tools available to all verified responders — enabling proactive familiarization, tabletop exercise support, and coordinated emergency response planning before an incident occurs.</p>
    </div>
  </div>
  <div class="banner red" style="margin-top:32px;">
    School Police deserve the same quality of pre-incident information as any other responding agency. This initiative helps make that a reality.
  </div>
</div>
</section>

<!-- ==================== SECTION 16: EMERGENCY PLANNING ==================== -->
<section class="panel" id="sec-emergency">
<div class="container">
  <div class="section-tag">Core Documentation</div>
  <h2 class="section-title">Emergency Planning</h2>
  <p class="lead">Effective emergency planning requires documentation of the right information — organized, current, and accessible to those who need it.</p>
  <div class="divider"></div>
  <div class="card-grid" style="grid-template-columns:repeat(auto-fill,minmax(200px,1fr));">
    <div class="card blue">
      <h3 class="card-title">Emergency Contacts</h3>
      <p>Key personnel, roles, alternates, and after-hours contacts — documented, current, and accessible.</p>
    </div>
    <div class="card black">
      <h3 class="card-title" style="color:var(--blue);">Assembly Areas</h3>
      <p style="color:#ccc;">Primary and alternate assembly areas — mapped, marked, and documented with capacity information.</p>
    </div>
    <div class="card red">
      <h3 class="card-title">Reunification Areas</h3>
      <p>Student-parent reunification zones — clearly defined, documented, and communicated to all parties.</p>
    </div>
    <div class="card">
      <h3 class="card-title">Utilities</h3>
      <p>Gas, electric, and water shutoffs — location, access method, and responsible party documented.</p>
    </div>
    <div class="card blue">
      <h3 class="card-title">Access Points</h3>
      <p>Every entrance, exit, and access point — including locked doors, codes, Knox boxes, and gate access.</p>
    </div>
    <div class="card black">
      <h3 class="card-title" style="color:var(--blue);">Critical Information</h3>
      <p style="color:#ccc;">AED locations, hazardous materials, special needs populations, and structural considerations.</p>
    </div>
    <div class="card">
      <h3 class="card-title">Documents</h3>
      <p>Emergency operations plans, evacuation procedures, floor plans — centralized and version-controlled.</p>
    </div>
  </div>
  <div class="banner black" style="margin-top:32px;">
    The best emergency plan is one that exists, is current, and is known by the people who need it.
  </div>
</div>
</section>

<!-- ==================== SECTION 17: PREPAREDNESS RESOURCES ==================== -->
<section class="panel" id="sec-resources">
<div class="container">
  <div class="section-tag">Resource Library</div>
  <h2 class="section-title">Preparedness Resources</h2>
  <p class="lead">Schools receive access to a curated library of preparedness resources — organized by type and ready to use or adapt.</p>
  <div class="divider"></div>
  <div class="card-grid" style="grid-template-columns:repeat(auto-fill,minmax(200px,1fr));">
    <div class="card blue">
      <div style="font-size:28px;margin-bottom:8px;">📋</div>
      <h3 class="card-title">Policies</h3>
      <p>Sample safety and emergency policies aligned with Florida school safety requirements.</p>
      <div style="margin-top:12px;padding:6px 10px;background:rgba(255,255,255,0.2);font-size:10px;font-family:var(--font-label);letter-spacing:1px;">Resource Placeholder</div>
    </div>
    <div class="card black">
      <div style="font-size:28px;margin-bottom:8px;">📁</div>
      <h3 class="card-title" style="color:var(--blue);">Plans</h3>
      <p style="color:#ccc;">Emergency operations plan templates and all-hazards plan frameworks.</p>
      <div style="margin-top:12px;padding:6px 10px;background:rgba(255,255,255,0.1);font-size:10px;font-family:var(--font-label);letter-spacing:1px;color:#888;">Resource Placeholder</div>
    </div>
    <div class="card">
      <div style="font-size:28px;margin-bottom:8px;">🗺</div>
      <h3 class="card-title">Maps</h3>
      <p>Floor plan templates, site layout guides, and mapping resources for preparedness documentation.</p>
      <div style="margin-top:12px;padding:6px 10px;background:#f0f0f0;font-size:10px;font-family:var(--font-label);letter-spacing:1px;">Resource Placeholder</div>
    </div>
    <div class="card blue">
      <div style="font-size:28px;margin-bottom:8px;">🎓</div>
      <h3 class="card-title">Training</h3>
      <p>Training resources, tabletop exercise guides, and drill planning materials.</p>
      <div style="margin-top:12px;padding:6px 10px;background:rgba(255,255,255,0.2);font-size:10px;font-family:var(--font-label);letter-spacing:1px;">Resource Placeholder</div>
    </div>
    <div class="card black">
      <div style="font-size:28px;margin-bottom:8px;">📄</div>
      <h3 class="card-title" style="color:var(--blue);">Procedures</h3>
      <p style="color:#ccc;">Standard operating procedures for lockdown, evacuation, shelter-in-place, and reunification.</p>
      <div style="margin-top:12px;padding:6px 10px;background:rgba(255,255,255,0.1);font-size:10px;font-family:var(--font-label);letter-spacing:1px;color:#888;">Resource Placeholder</div>
    </div>
    <div class="card">
      <div style="font-size:28px;margin-bottom:8px;">✅</div>
      <h3 class="card-title">Checklists</h3>
      <p>Preparedness audit checklists, pre-event verification lists, and post-incident documentation templates.</p>
      <div style="margin-top:12px;padding:6px 10px;background:#f0f0f0;font-size:10px;font-family:var(--font-label);letter-spacing:1px;">Resource Placeholder</div>
    </div>
  </div>
  <div class="banner blue" style="margin-top:32px;">
    Resources are curated through the SYT.PRO platform and accessible to all participating schools.
  </div>
</div>
</section>

<!-- ==================== SECTION 18: SUMMER OPPORTUNITY ==================== -->
<section class="panel" id="sec-summer">
<div class="container">
  <div class="section-tag">Strategic Timing</div>
  <h2 class="section-title">Summer Opportunity</h2>
  <div class="block-row">
    <div class="block blue" style="font-size:clamp(1rem,3vw,1.6rem);">Summer provides a unique opportunity to conduct preparedness reviews, facility familiarization, documentation, and pilot evaluations before students return.</div>
  </div>
  <p class="body">Schools are often most accessible during summer months — reduced occupancy, administrative availability, and time to complete documentation without disrupting the school day. This is the ideal window to conduct a SYT.360 visit, build the school's operational profile, and complete responder familiarization before the fall semester begins.</p>
  <div class="divider"></div>
  <h3 class="card-title">Summer Preparedness Window</h3>
  <div class="summer-bar" style="margin-top:20px;">
    <div class="summer-phase blue">
      <div class="month">June</div>
      <div class="phase-name">Site Visit</div>
      <p style="font-size:11px;margin-top:6px;opacity:0.85;">SYT.360 preparedness visit and facility walkthrough</p>
    </div>
    <div class="summer-phase black">
      <div class="month">June — July</div>
      <div class="phase-name">Review</div>
      <p style="font-size:11px;margin-top:6px;color:#aaa;">Preparedness review, gap identification, plan evaluation</p>
    </div>
    <div class="summer-phase blue">
      <div class="month">July</div>
      <div class="phase-name">Documentation</div>
      <p style="font-size:11px;margin-top:6px;opacity:0.85;">Profile build, overhead imagery, document upload</p>
    </div>
    <div class="summer-phase black">
      <div class="month">August</div>
      <div class="phase-name">Familiarization</div>
      <p style="font-size:11px;margin-top:6px;color:#aaa;">Responder familiarization before students return</p>
    </div>
  </div>
  <div class="banner red" style="margin-top:32px;text-align:center;">
    Students return in August. The window to prepare is now.
  </div>
</div>
</section>

<!-- ==================== SECTION 19: DIGITAL TWIN ==================== -->
<section class="panel" id="sec-digital-twin">
<div class="container">
  <div class="section-tag">Future Capability</div>
  <h2 class="section-title">Digital Twin</h2>
  <p class="lead">The future of facility familiarization extends beyond floor plans and photos. Digital twin technology offers responders the ability to virtually walk a building before they ever set foot inside.</p>
  <div class="divider"></div>
  <div style="border:3px solid var(--black);padding:40px;text-align:center;margin:24px 0;background:#f8f8f8;">
    <div style="font-family:var(--font-hero);font-size:clamp(1.2rem,4vw,2rem);text-transform:uppercase;margin-bottom:12px;">Future Digital Twin Demonstration</div>
    <div style="font-family:var(--font-body);font-size:13px;color:#888;font-style:italic;">No live model required for this demonstration.<br>This space is reserved for future digital twin content.</div>
    <!-- SWAP: embed Matterport iframe or 3D viewer here -->
    <div style="margin-top:24px;padding:60px 20px;border:2px dashed #ccc;color:#bbb;font-family:var(--font-label);font-size:11px;letter-spacing:1px;">
      DIGITAL TWIN EMBED PLACEHOLDER<br>
      <span style="font-size:9px;">Swap: Matterport embed, photogrammetry viewer, or 3D model</span>
    </div>
  </div>
  <h3 class="card-title">Future Capabilities</h3>
  <div class="card-grid" style="grid-template-columns:repeat(auto-fill,minmax(180px,1fr));margin-top:20px;">
    <div class="card black"><h3 class="card-title" style="color:var(--blue);">Matterport</h3><p style="color:#ccc;">3D virtual walkthroughs of school facilities for remote familiarization.</p></div>
    <div class="card blue"><h3 class="card-title">Photogrammetry</h3><p>Photogrammetric models from standard photography — scalable and accessible.</p></div>
    <div class="card"><h3 class="card-title">Gaussian Splats</h3><p>Emerging photorealistic 3D capture technology for high-fidelity virtual environments.</p></div>
    <div class="card black"><h3 class="card-title" style="color:var(--blue);">Reality Capture</h3><p style="color:#ccc;">LiDAR and laser scanning for precise structural documentation.</p></div>
    <div class="card blue"><h3 class="card-title">3D Familiarization</h3><p>Responders navigate a virtual facility before responding to a real incident.</p></div>
    <div class="card"><h3 class="card-title">Training</h3><p>Use 3D models for tabletop exercises, scenario planning, and team drills.</p></div>
    <div class="card black"><h3 class="card-title" style="color:var(--blue);">Emergency Planning</h3><p style="color:#ccc;">Walk through evacuation routes, access points, and staging areas virtually.</p></div>
  </div>
  <div class="banner blue" style="margin-top:32px;">
    This capability is on the roadmap — not a requirement for the pilot. Preparedness first. Technology second.
  </div>
</div>
</section>

<!-- ==================== SECTION 20: OVERHEAD IMAGERY ==================== -->
<section class="panel" id="sec-overhead">
<div class="container">
  <div class="section-tag">Aerial Documentation</div>
  <h2 class="section-title">Overhead Imagery</h2>
  <p class="lead">Aerial and overhead documentation provides a perspective that ground-level photography cannot — and one that responders rely on for situational awareness before and during an incident.</p>
  <div class="divider"></div>
  <div class="two-col" style="margin-bottom:32px;">
    <!-- SWAP: <img src="drone-school.jpg" alt="Drone photo of school campus"> -->
    <div class="photo-placeholder" style="height:240px;">
      <span class="icon">🚁</span>
      <span>Drone / Aerial Photography</span>
      <span style="font-size:10px;color:#aaa;">Swap: &lt;img src="drone-school.jpg"&gt;</span>
    </div>
    <!-- SWAP: <img src="school-aerial-map.jpg" alt="School aerial map view"> -->
    <div class="photo-placeholder" style="height:240px;">
      <span class="icon">🛰</span>
      <span>School Aerial Overview</span>
      <span style="font-size:10px;color:#aaa;">Swap: &lt;img src="school-aerial-map.jpg"&gt;</span>
    </div>
  </div>
  <h3 class="card-title">Why Overhead Imagery Matters</h3>
  <div class="card-grid" style="grid-template-columns:repeat(auto-fill,minmax(200px,1fr));">
    <div class="card blue"><h3 class="card-title">Emergency Access Routes</h3><p>Identify approach paths, staging areas, and potential obstructions from above.</p></div>
    <div class="card black"><h3 class="card-title" style="color:var(--blue);">Assembly Areas</h3><p style="color:#ccc;">Confirm and document assembly zones relative to building exits and surrounding streets.</p></div>
    <div class="card"><h3 class="card-title">Responder Orientation</h3><p>Give arriving units a bird's-eye view of the campus before they arrive on scene.</p></div>
    <div class="card blue"><h3 class="card-title">Building Familiarization</h3><p>Overhead context helps responders understand building layout, adjacencies, and perimeter.</p></div>
  </div>
</div>
</section>

<!-- ==================== SECTION 21: GRANT OPPORTUNITIES ==================== -->
<section class="panel" id="sec-grants">
<div class="container">
  <div class="section-tag">Future Funding Pathways</div>
  <h2 class="section-title">Grant Opportunities</h2>
  <p class="lead">Preparedness initiatives like this one are supported by a growing number of federal, state, and private funding programs designed to improve school safety and emergency management.</p>
  <div class="divider"></div>
  <div class="card-grid">
    <div class="card blue">
      <h3 class="card-title">Preparedness Grants</h3>
      <p>Federal and state programs supporting school preparedness planning, documentation, and training.</p>
    </div>
    <div class="card black">
      <h3 class="card-title" style="color:var(--blue);">Safety Grants</h3>
      <p style="color:#ccc;">School safety improvement grants available through FEMA, DHS, and state emergency management agencies.</p>
    </div>
    <div class="card red">
      <h3 class="card-title">Emergency Management Grants</h3>
      <p>Local and regional emergency management funding to support collaborative preparedness programs.</p>
    </div>
    <div class="card">
      <h3 class="card-title">Public Safety Grants</h3>
      <p>Law enforcement and fire service grant programs that support pre-incident planning and responder familiarization.</p>
    </div>
    <div class="card blue">
      <h3 class="card-title">Foundation Funding</h3>
      <p>Private and community foundation support for educational safety and community preparedness initiatives.</p>
    </div>
    <div class="card black">
      <h3 class="card-title" style="color:var(--blue);">Partnership Opportunities</h3>
      <p style="color:#ccc;">Collaborative funding through joint applications with school districts, municipalities, and public safety agencies.</p>
    </div>
  </div>
  <div class="banner black" style="margin-top:32px;">
    Identifying the right funding pathways is part of the lessons learned process. The pilot informs the funding strategy.
  </div>
</div>
</section>

<!-- ==================== SECTION 22: FAQ ==================== -->
<section class="panel" id="sec-faq">
<div class="container">
  <div class="section-tag">Questions &amp; Answers</div>
  <h2 class="section-title">Frequently Asked Questions</h2>
  <div class="divider"></div>
  <div class="accordion">
    <div class="accordion-item">
      <button class="accordion-btn">Who owns the information? <span class="accordion-arrow">▼</span></button>
      <div class="accordion-body">The school owns all information. All data, documentation, and profiles are the property of the school. SYT.FYI and First In Safety Foundation are facilitators — not custodians.</div>
    </div>
    <div class="accordion-item">
      <button class="accordion-btn">Who controls access to the information? <span class="accordion-arrow">▼</span></button>
      <div class="accordion-body">The school controls all access. The school determines what information is made available, to which agencies, and under what conditions. Nothing is shared without school awareness and approval.</div>
    </div>
    <div class="accordion-item">
      <button class="accordion-btn">Can one school participate? <span class="accordion-arrow">▼</span></button>
      <div class="accordion-body">Yes. The entire initiative is designed to start with one school. There is no minimum, no commitment to expand, and no obligation beyond the pilot evaluation itself.</div>
    </div>
    <div class="accordion-item">
      <button class="accordion-btn">Can multiple schools participate simultaneously? <span class="accordion-arrow">▼</span></button>
      <div class="accordion-body">Yes. Multiple schools can participate in the pilot. Each school's profile is independent, and participation by one school does not affect or obligate another.</div>
    </div>
    <div class="accordion-item">
      <button class="accordion-btn">Who uses FireTactic? <span class="accordion-arrow">▼</span></button>
      <div class="accordion-body">FireTactic is used by verified responders only — School Police, Fire Rescue, EMS, and Law Enforcement — through the First In Safety Foundation. Access requires identity verification and is managed by the Foundation.</div>
    </div>
    <div class="accordion-item">
      <button class="accordion-btn">How does the pilot program work? <span class="accordion-arrow">▼</span></button>
      <div class="accordion-body">The pilot follows seven steps: (1) School Selection, (2) SYT.360 Visit, (3) Preparedness Review, (4) School Profile Build, (5) Responder Familiarization, (6) Lessons Learned Documentation, (7) Expansion Evaluation. Every step is collaborative and documented.</div>
    </div>
    <div class="accordion-item">
      <button class="accordion-btn">What happens after the pilot? <span class="accordion-arrow">▼</span></button>
      <div class="accordion-body">After the pilot, all parties receive a Lessons Learned Report documenting findings, gaps, successes, and recommendations. Together, the school, public safety partners, and initiative team evaluate whether and how to expand — on their terms, on their timeline.</div>
    </div>
    <div class="accordion-item">
      <button class="accordion-btn">What does the pilot school have to do? <span class="accordion-arrow">▼</span></button>
      <div class="accordion-body">Participate honestly. Allow a facility visit. Review the profile and provide feedback. That's it. No financial commitment, no long-term obligation, no software implementation required beyond the pilot period.</div>
    </div>
    <div class="accordion-item">
      <button class="accordion-btn">Is this a sales presentation? <span class="accordion-arrow">▼</span></button>
      <div class="accordion-body">No. This is a preparedness initiative. The goal is to build a framework that genuinely improves preparedness, responder familiarization, and facility awareness. Technology supports the mission — it is not the mission.</div>
    </div>
  </div>
</div>
</section>

<!-- ==================== SECTION 23: NEXT STEPS ==================== -->
<section class="panel" id="sec-next-steps">
<div class="container">
  <div class="section-tag">How We Move Forward</div>
  <h2 class="section-title">Next Steps</h2>
  <p class="lead">Moving forward requires one willing school, one visit, and one commitment to honest evaluation. Everything else follows from there.</p>
  <div class="divider"></div>
  <div class="num-steps">
    <div class="num-step">
      <div class="num">1</div>
      <div><h4>Identify School</h4><p>Identify one educational institution in the Downtown Miami or Brickell area willing to serve as a pilot partner.</p></div>
    </div>
    <div class="num-step">
      <div class="num">2</div>
      <div><h4>Schedule Visit</h4><p>Coordinate a SYT.360 preparedness visit with school administration — no disruption to the school day required.</p></div>
    </div>
    <div class="num-step">
      <div class="num">3</div>
      <div><h4>Conduct Evaluation</h4><p>Complete the on-site preparedness visit, facility walkthrough, documentation, and existing plan review.</p></div>
    </div>
    <div class="num-step">
      <div class="num">4</div>
      <div><h4>Review Findings</h4><p>Share the completed school profile and preparedness review with school administration for review and feedback.</p></div>
    </div>
    <div class="num-step">
      <div class="num">5</div>
      <div><h4>Document Lessons Learned</h4><p>Compile a formal Lessons Learned Report capturing what worked, what needs improvement, and what all parties learned.</p></div>
    </div>
    <div class="num-step">
      <div class="num">6</div>
      <div><h4>Discuss Expansion</h4><p>Review the lessons learned with all stakeholders and jointly determine whether, when, and how to expand the initiative.</p></div>
    </div>
  </div>
  <div class="closing-statement">It starts with one school.</div>
</div>
</section>

<!-- ==================== SECTION 24: CONTACT ==================== -->
<section class="panel" id="sec-contact">
<div class="container" style="max-width:700px;">
  <div class="section-tag">Get In Touch</div>
  <h2 class="section-title">Contact</h2>
  <div class="divider"></div>
  <table class="info-table" style="margin-bottom:32px;">
    <tr><td>Name</td><td><strong>Tony Prol</strong></td></tr>
    <tr><td>Title</td><td>Founder &amp; CEO — SYT.FYI</td></tr>
    <tr><td>Foundation</td><td>President &amp; Executive Director — First In Safety Foundation</td></tr>
    <tr><td>Location</td><td>Downtown Miami, Florida</td></tr>
    <tr><td>Email</td><td><span style="color:var(--blue);">[EMAIL PLACEHOLDER — fill in before sharing]</span></td></tr>
    <tr><td>Phone</td><td><span style="color:var(--blue);">[PHONE PLACEHOLDER — fill in before sharing]</span></td></tr>
    <tr><td>Website</td><td><span style="color:var(--blue);">SYT.FYI</span></td></tr>
  </table>
  <div class="closing-statement" style="font-size:clamp(1rem,3vw,1.6rem);letter-spacing:3px;">
    Preparedness First.<br>Technology Second.<br>Partnership Always.
  </div>
</div>
</section>

</main>

<!-- ===== FOOTER ===== -->
<footer id="site-footer">
  <!-- LOGO SWAP: Replace <img> src with real file path. Current: embedded base64 -->
  <img class="footer-logo-syt" src="{SYT_SRC}" alt="SYT.FYI — Property Intelligence" title="SYT.FYI">
  <span class="footer-tagline">Preparedness First. Technology Second. Partnership Always.</span>
  <!-- LOGO SWAP: Replace <img> src with real file path. Current: embedded base64 -->
  <img class="footer-logo-ft" src="{FT_SRC}" alt="FireTactic" title="FireTactic">
</footer>

<script>
// ===== SECTION MAP =====
const SECTIONS = [
  {{ id:'home',          el:'sec-home',          title:'Home',                    keys:['home','homepage','start','overview main'] }},
  {{ id:'about',         el:'sec-about',          title:'About Tony',              keys:['tony','about','prol','firefighter','paramedic','founder','ceo','miami beach'] }},
  {{ id:'overview',      el:'sec-overview',       title:'Initiative Overview',     keys:['initiative','overview','objective','scalable','collaborative','pillars'] }},
  {{ id:'why-edu',       el:'sec-why-edu',        title:'Why Educational Facilities', keys:['educational','facilities','k-12','k12','charter','private','college','university','trade school'] }},
  {{ id:'why-downtown',  el:'sec-why-downtown',   title:'Why Downtown Miami',      keys:['downtown','miami','brickell','geography','urban','zone','pilot zone'] }},
  {{ id:'ecosystem',     el:'sec-ecosystem',      title:'Educational Ecosystem',   keys:['ecosystem','mdcps','academica','miami dade college','mdc','fiu','hub','spoke','network','partners'] }},
  {{ id:'challenges',    el:'sec-challenges',     title:'Current Challenges',      keys:['challenges','problems','silos','turnover','complexity','coordination','gaps','barrier'] }},
  {{ id:'pilot',         el:'sec-pilot',          title:'Pilot Program',           keys:['pilot','program','steps','timeline','selection','visit','syt360','360 visit','lessons','expansion'] }},
  {{ id:'pilot-benefits',el:'sec-pilot-benefits', title:'Pilot School Benefits',   keys:['benefits','pilot benefits','school benefits','what school gets','access','report','two year','2 year'] }},
  {{ id:'syt360',        el:'sec-syt360',         title:'SYT.360',                 keys:['syt360','syt.360','360','no cost','free visit','walkthrough','aed','utility','assembly','floor plan','profile'] }},
  {{ id:'sytpro',        el:'sec-sytpro',         title:'SYT.PRO',                 keys:['sytpro','syt.pro','platform','dashboard','repository','documents','preparedness platform'] }},
  {{ id:'firetactic',    el:'sec-firetactic',     title:'FireTactic',              keys:['firetactic','fire tactic','first in safety','foundation','responder platform','verified','training','pre-incident','pre incident'] }},
  {{ id:'school-example',el:'sec-school-example', title:'School Example',          keys:['school example','brickell bay','example','demo','fictional','sample','profile example','what it looks like'] }},
  {{ id:'responder',     el:'sec-responder',      title:'Responder View',          keys:['responder','responder view','flow','information flow','fire rescue','ems','law enforcement','downstream'] }},
  {{ id:'school-police', el:'sec-school-police',  title:'School Police View',      keys:['school police','police','sro','resource officer','school police view','famil'] }},
  {{ id:'emergency',     el:'sec-emergency',      title:'Emergency Planning',      keys:['emergency','planning','emergency planning','contacts','assembly','reunification','utilities','access','documents'] }},
  {{ id:'resources',     el:'sec-resources',      title:'Preparedness Resources',  keys:['resources','library','policies','plans','maps','training','procedures','checklists','resource library'] }},
  {{ id:'summer',        el:'sec-summer',         title:'Summer Opportunity',      keys:['summer','opportunity','june','july','august','summer window','timing','before school'] }},
  {{ id:'digital-twin',  el:'sec-digital-twin',   title:'Digital Twin',            keys:['digital twin','twin','matterport','3d','photogrammetry','gaussian','splat','lidar','reality capture','virtual'] }},
  {{ id:'overhead',      el:'sec-overhead',       title:'Overhead Imagery',        keys:['overhead','aerial','drone','imagery','photography','bird','map view','site view'] }},
  {{ id:'grants',        el:'sec-grants',         title:'Grant Opportunities',     keys:['grant','grants','funding','fema','dhs','foundation funding','partnership funding','money'] }},
  {{ id:'faq',           el:'sec-faq',            title:'FAQ',                     keys:['faq','questions','who owns','controls','one school','multiple schools','how does','what happens','after pilot'] }},
  {{ id:'next-steps',    el:'sec-next-steps',     title:'Next Steps',              keys:['next steps','steps','move forward','how to start','action','identify','schedule','expand'] }},
  {{ id:'contact',       el:'sec-contact',        title:'Contact',                 keys:['contact','tony','email','phone','reach','get in touch'] }},
];

// ===== ROUTER =====
function showSection(id) {{
  const sec = SECTIONS.find(s => s.id === id) || SECTIONS[0];
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-btn, .drawer-btn').forEach(b => b.classList.remove('active'));
  const el = document.getElementById(sec.el);
  if (el) el.classList.add('active');
  document.querySelectorAll(`[data-section="${{sec.id}}"]`).forEach(b => b.classList.add('active'));
  window.scrollTo(0, 0);
  if (location.hash !== '#' + sec.id) history.pushState(null, '', '#' + sec.id);
  closeDrawer();
}}

function getHashId() {{
  const h = location.hash.replace('#','');
  return SECTIONS.find(s => s.id === h) ? h : 'home';
}}

window.addEventListener('popstate', () => showSection(getHashId()));
document.addEventListener('DOMContentLoaded', () => showSection(getHashId()));

// ===== NAV BUTTONS =====
document.querySelectorAll('.nav-btn, .drawer-btn').forEach(btn => {{
  btn.addEventListener('click', () => showSection(btn.dataset.section));
}});

// ===== HAMBURGER / DRAWER =====
const hamburger = document.getElementById('hamburger');
const drawer = document.getElementById('nav-drawer');
function closeDrawer() {{
  hamburger.classList.remove('open');
  drawer.classList.remove('open');
}}
hamburger.addEventListener('click', () => {{
  hamburger.classList.toggle('open');
  drawer.classList.toggle('open');
}});

// ===== SEARCH =====
const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');
const searchClear = document.getElementById('search-clear');

function searchSections(query) {{
  if (!query.trim()) return [];
  const q = query.toLowerCase();
  return SECTIONS.filter(s =>
    s.title.toLowerCase().includes(q) ||
    s.keys.some(k => k.includes(q))
  ).slice(0, 8);
}}

function renderResults(query) {{
  const results = searchSections(query);
  if (!query.trim()) {{
    searchResults.classList.remove('open');
    return;
  }}
  searchResults.classList.add('open');
  if (results.length === 0) {{
    searchResults.innerHTML = '<div class="search-none">No section found — try: <strong>pilot</strong>, <strong>school example</strong>, <strong>responder</strong></div>';
    return;
  }}
  searchResults.innerHTML = results.map(s =>
    `<div class="search-item" data-id="${{s.id}}"><strong>${{s.title}}</strong></div>`
  ).join('');
  searchResults.querySelectorAll('.search-item').forEach(item => {{
    item.addEventListener('click', () => {{
      showSection(item.dataset.id);
      searchInput.value = '';
      searchResults.classList.remove('open');
      searchClear.classList.remove('visible');
    }});
  }});
}}

searchInput.addEventListener('input', () => {{
  const val = searchInput.value;
  searchClear.classList.toggle('visible', val.length > 0);
  renderResults(val);
}});

searchInput.addEventListener('keydown', e => {{
  if (e.key === 'Enter') {{
    const results = searchSections(searchInput.value);
    if (results.length > 0) {{
      showSection(results[0].id);
      searchInput.value = '';
      searchResults.classList.remove('open');
      searchClear.classList.remove('visible');
    }}
  }}
  if (e.key === 'Escape') {{
    searchResults.classList.remove('open');
    searchInput.blur();
  }}
}});

searchClear.addEventListener('click', () => {{
  searchInput.value = '';
  searchClear.classList.remove('visible');
  searchResults.classList.remove('open');
  searchInput.focus();
}});

document.addEventListener('click', e => {{
  if (!e.target.closest('#searchbar') && !e.target.closest('#search-results')) {{
    searchResults.classList.remove('open');
  }}
}});

// ===== FAQ ACCORDION =====
document.querySelectorAll('.accordion-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    const body = btn.nextElementSibling;
    const isOpen = btn.classList.contains('open');
    // close all
    document.querySelectorAll('.accordion-btn').forEach(b => {{
      b.classList.remove('open');
      b.nextElementSibling.classList.remove('open');
    }});
    if (!isOpen) {{
      btn.classList.add('open');
      body.classList.add('open');
    }}
  }});
}});
</script>
</body>
</html>"""

os.makedirs('/home/user/mbfd-cism-support/downtown-preparedness', exist_ok=True)
with open('/home/user/mbfd-cism-support/downtown-preparedness/index.html', 'w') as f:
    f.write(HTML)
print(f"Written: {len(HTML):,} chars")
