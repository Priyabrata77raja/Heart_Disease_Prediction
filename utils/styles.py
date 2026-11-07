CSS = """
<style>
:root{--navy:#061A33;--deep:#092746;--burg:#48152B;--crim:#F52246;--coral:#FF465C;--bg:#F4F7FB;--blue:#EAF3FC;--muted:#64748B}
html,body,[class*="css"],.stApp{font-family:'Inter','Segoe UI',system-ui,sans-serif}
.stApp{background:var(--bg);color:#0f2442}
[data-testid="stHeader"]{background:transparent}
[data-testid="stSidebarNav"],[data-testid="stToolbar"],#MainMenu,footer{display:none!important}
.block-container{padding-top:1.2rem;max-width:1400px}
/* Sidebar */
[data-testid="stSidebar"]{background:linear-gradient(180deg,#061A33,#092746);border-right:1px solid #ffffff14}
[data-testid="stSidebar"] *{color:#fff}
[data-testid="stSidebar"] [role="radiogroup"]{gap:4px}
[data-testid="stSidebar"] [role="radiogroup"] label{border-radius:10px;padding:9px 12px;transition:all .2s;width:100%}
[data-testid="stSidebar"] [role="radiogroup"] label>div:first-child{display:none}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{background:#ffffff1a}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){background:linear-gradient(90deg,#F52246,#d4143a);box-shadow:0 6px 16px #F5224655}
[data-testid="stSidebar"] [role="radiogroup"] label p{font-size:14px;font-weight:600}
.brand{display:flex;align-items:center;gap:10px;margin:4px 0 18px}
.brand b{font-size:23px;line-height:1}.brand span{font-size:11px;color:#9fb3cc}
.side-foot{display:flex;gap:10px;align-items:center;border-top:1px solid #ffffff1f;padding-top:14px;margin-top:22px;font-size:12px;color:#b9c9de}
/* Hero */
.hero{border-radius:24px;padding:38px 36px;min-height:420px;color:#fff;position:relative;overflow:hidden;
 background:radial-gradient(circle at 85% 20%,#F5224633,transparent 50%),linear-gradient(120deg,#061A33,#092746 55%,#48152B);
 border:1px solid #ffffff22;box-shadow:0 18px 45px #061a3340;display:flex;flex-direction:column;justify-content:center}
.eyebrow{font-size:12px;letter-spacing:2.2px;font-weight:800;color:#ffb3c0}
.hero h1{font-size:clamp(44px,5.5vw,72px);line-height:1.05;margin:14px 0 6px;font-weight:800;color:#fff;padding:0}
.hero h1 span{color:var(--crim)}
.hero h3{color:#fff;font-weight:500;font-size:21px;margin:0 0 14px}
.hero p{color:#cfdcec;line-height:1.7;font-size:15px;max-width:520px}
.hero-art{border-radius:24px;overflow:hidden;min-height:420px;position:relative;display:flex;align-items:center;justify-content:center;
 background:radial-gradient(ellipse at 55% 45%,#8e203c 0%,#48152B 40%,#061A33 85%);border:1px solid #ffffff22;box-shadow:0 18px 45px #061a3340}
.hero-art img{max-height:420px;max-width:100%;object-fit:contain;position:relative;mask-image:radial-gradient(ellipse at center,#000 62%,transparent 98%);-webkit-mask-image:radial-gradient(ellipse at center,#000 62%,transparent 98%)}
.hero-art svg{position:absolute;left:0;right:0;top:50%;width:100%;transform:translateY(-50%);filter:drop-shadow(0 0 8px #F52246)}
.feat{background:linear-gradient(145deg,#092746,#0b2f55);border:1px solid #ffffff1c;border-radius:16px;padding:16px;color:#fff;display:flex;gap:12px;align-items:center;transition:all .2s;box-shadow:inset 0 -2px 0 #F5224655}
.feat:hover{transform:translateY(-3px);box-shadow:0 10px 24px #061a3340,inset 0 -2px 0 #F52246}
.feat i{font-style:normal;font-size:26px}.feat b{font-size:13px;line-height:1.3}
/* Cards */
.head{display:flex;align-items:center;gap:14px;margin:4px 0 4px}
.head .ic{font-size:34px}.head h2{margin:0;font-size:28px;font-weight:800;color:#0f2442;padding:0}
.sub{color:var(--muted);font-size:14px;margin:0 0 18px 0}
.card{background:#fff;border:1px solid #e3eaf3;border-radius:16px;padding:18px;box-shadow:0 6px 20px #16304f0f;height:100%;transition:all .2s}
.card:hover{transform:translateY(-3px);box-shadow:0 12px 28px #16304f1a}
.card .ic{font-size:30px;width:52px;height:52px;display:flex;align-items:center;justify-content:center;background:#fff0f3;border-radius:50%;margin-bottom:10px}
.card h4{margin:0 0 6px;font-size:16px;color:#0f2442}.card p{margin:0;color:var(--muted);font-size:13.5px;line-height:1.6}
.chip{display:inline-block;background:#fff0f3;color:#c01237;border-radius:20px;padding:3px 10px;font-size:11px;font-weight:700;margin-bottom:6px}
.ph{height:140px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:52px;background:linear-gradient(135deg,#EAF3FC,#fde7ec);margin-bottom:10px}
.banner{border-radius:18px;overflow:hidden;min-height:200px;padding:30px 34px;border:1px solid #dbe7f4;background:linear-gradient(90deg,#EAF3FCf2 45%,#EAF3FC66),var(--img) right center/cover no-repeat}
.banner h1{margin:8px 0;font-size:32px;color:#0f2442;line-height:1.25;padding:0}.banner small{color:var(--muted)}
.emer{background:linear-gradient(145deg,#fff0f3,#fff);border:1px solid #ffd0d9;border-radius:18px;padding:24px;text-align:center}
.emer .n{font-size:64px;font-weight:800;color:#d4143a;line-height:1.1}
.warn{background:#fff1f3;border:1px solid #ffc4cf;border-left:5px solid var(--crim);border-radius:12px;padding:14px 16px;color:#7a1226;font-size:14px}
.metric{background:#fff;border:1px solid #e3eaf3;border-radius:16px;padding:16px;text-align:center;box-shadow:0 6px 20px #16304f0f}
.metric .l{font-size:12px;color:var(--muted);font-weight:700;letter-spacing:.5px}.metric .v{font-size:26px;font-weight:800;color:#0f2442;margin-top:4px}
.metric .v.na{font-size:16px;color:#94a3b8;font-weight:600;padding:6px 0}
.result{border-radius:16px;padding:22px;text-align:center}
.result.pos{background:#fff1f3;border:1px solid #ffc4cf}.result.neg{background:#eefaf3;border:1px solid #bfe8cf}.result.idle{background:var(--blue);border:1px solid #d3e4f6}
.result h3{margin:6px 0;font-size:24px;padding:0}.result p{color:#475569;font-size:14px}
.disc{background:#fff8e6;border:1px solid #f4d68a;border-radius:12px;padding:12px 16px;color:#7a5a14;font-size:12.5px;line-height:1.6;margin-top:18px}
.foot{text-align:center;color:#8593a6;font-size:11.5px;padding:20px 0 4px}
/* Streamlit widgets */
div.stButton>button,div[data-testid="stFormSubmitButton"]>button{border-radius:11px;font-weight:700;padding:.6rem 1rem;transition:all .2s}
div.stButton>button[kind="primary"],div[data-testid="stFormSubmitButton"]>button{background:linear-gradient(90deg,#F52246,#FF465C);color:#fff;border:0;box-shadow:0 8px 18px #F5224640}
div.stButton>button[kind="primary"]:hover,div[data-testid="stFormSubmitButton"]>button:hover{transform:translateY(-2px);filter:brightness(1.06);color:#fff}
div.stButton>button[kind="secondary"]{background:transparent;border:1px solid #F52246;color:#F52246}
.hero-btns div.stButton>button[kind="secondary"]{color:#fff}
div[data-baseweb="tab-list"]{gap:10px}
button[data-baseweb="tab"]{background:#fff;border:1px solid #dbe3ee;border-radius:12px;padding:10px 20px;font-weight:700}
button[data-baseweb="tab"][aria-selected="true"]{background:linear-gradient(90deg,#F52246,#FF465C);color:#fff;border-color:transparent}
button[data-baseweb="tab"][aria-selected="true"] p{color:#fff}
div[data-baseweb="tab-highlight"],div[data-baseweb="tab-border"]{display:none}
[data-testid="stVerticalBlockBorderWrapper"]{border-radius:16px}
[data-testid="stImage"] img{border-radius:12px;height:140px;object-fit:cover;width:100%}
@media (max-width:768px){.hero{padding:26px 20px;min-height:auto}.hero-art{min-height:300px}.banner{padding:22px}.banner h1{font-size:24px}}

.topbar{display:flex;justify-content:flex-end;align-items:center;gap:8px;color:#0f2442;font-weight:600;font-size:14px;margin:-6px 4px 10px}
.st-key-hero{border-radius:22px;border:1px solid #ffffff22;box-shadow:0 18px 45px #061a3340;overflow:hidden;padding:0;
 background:radial-gradient(circle at 90% 30%,#F5224655,transparent 55%),linear-gradient(110deg,#061A33 0%,#092746 45%,#48152B 100%)}
.st-key-hero [data-testid="stHorizontalBlock"]{gap:0;align-items:center}
.st-key-hero [data-testid="stVerticalBlock"]{gap:.4rem}
.herotxt{padding:30px 10px 0 34px;color:#fff}
.badge{display:inline-block;border:1.5px solid #ffffff55;border-radius:30px;padding:7px 16px;font-size:12px;font-weight:700;letter-spacing:.4px;background:#ffffff0d}
.badge b{color:#FF465C}
.herotxt h1{font-size:clamp(44px,5.6vw,76px);font-weight:800;line-height:1.05;margin:16px 0 4px;color:#fff;padding:0}
.herotxt h1 span{color:#F52246}
.herotxt h3{font-size:clamp(20px,2.4vw,30px);font-weight:400;color:#fff;margin:0 0 14px}
.herotxt p{color:#dbe5f2;font-size:15.5px;line-height:1.65;max-width:560px;margin:0}
.heroimg{padding:0;line-height:0}
.heroimg img{width:100%;height:100%;min-height:340px;object-fit:cover;display:block;
 -webkit-mask-image:linear-gradient(90deg,transparent 0%,#000 28%);mask-image:linear-gradient(90deg,transparent 0%,#000 28%)}
.st-key-hero_btns{padding:0 0 26px 34px}
.st-key-start button{background:linear-gradient(90deg,#d4143a,#F52246)!important;color:#fff!important;border:0!important;box-shadow:0 8px 20px #F5224655}
.st-key-explore button{background:transparent!important;color:#fff!important;border:1.5px solid #ffffff66!important}
.st-key-explore button:hover{border-color:#F52246!important;background:#F5224626!important}
.fcard{text-align:center;padding:6px 6px 0}
.fcard .ic{width:58px;height:58px;border-radius:50%;background:linear-gradient(145deg,#ffe3e8,#ffc9d3);display:flex;align-items:center;justify-content:center;font-size:28px;margin:0 auto 8px;box-shadow:0 6px 14px #F5224626}
.fcard h4{margin:0 0 6px;font-size:18px;color:#0f2442}.fcard p{margin:0;color:#475569;font-size:13.5px;line-height:1.55;min-height:42px}
[class*="st-key-fc_"]{background:#fff;border:1px solid #e8edf5;border-radius:18px;box-shadow:0 8px 24px #16304f14;padding:14px 10px 6px;transition:all .2s}
[class*="st-key-fc_"]:hover{transform:translateY(-4px);box-shadow:0 14px 30px #F5224626}
[class*="st-key-fc_"] button{background:transparent!important;border:0!important;color:#F52246!important;font-weight:800;box-shadow:none!important;width:100%}
.glow [class*="st-key-fc_"]{box-shadow:0 0 0 2px #F52246,0 10px 28px #F5224655}
.dbar{display:flex;align-items:center;gap:16px;border-radius:16px;padding:18px 24px;margin-top:18px;color:#fff;border:1px solid #ffffff1c;
 background:linear-gradient(100deg,#061A33,#0a2342 60%,#48152B);box-shadow:0 10px 26px #061a3340}
.dbar .x{flex:none;width:46px;height:46px;border-radius:50%;background:#F52246;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:24px}
.dbar b{color:#FF465C;font-size:17px}.dbar p{margin:2px 0 0;font-size:13.5px;color:#e2eaf5;line-height:1.55}
.dbar svg{flex:none;margin-left:auto;opacity:.9}
.sidelogo img{width:100%}
.side-box{margin-top:26px;border-top:1px solid #ffffff1f;padding:16px 4px 0;display:flex;gap:10px;align-items:center;font-size:13px}
.side-box small{color:#c9d6e8}
</style>
"""

LOGO = """<svg width="44" height="44" viewBox="0 0 44 44"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF465C"/><stop offset="1" stop-color="#d4143a"/></linearGradient></defs>
<path d="M22 40 C8 29 3 21 3 14 C3 8 8 4 13 4 C17 4 20 6 22 9 C24 6 27 4 31 4 C36 4 41 8 41 14 C41 21 36 29 22 40Z" fill="url(#lg)"/>
<path d="M6 22 H15 L18 14 L23 30 L27 19 L29 22 H38" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>"""

ECG = """<svg viewBox="0 0 600 120" preserveAspectRatio="none" height="120"><path d="M0 60 H170 L190 60 L205 25 L225 100 L245 40 L260 60 H600" fill="none" stroke="#FF465C" stroke-width="3" stroke-linejoin="round" opacity=".85"/></svg>"""

DBAR_ECG = """<svg width="190" height="60" viewBox="0 0 190 60"><path d="M0 34 H40 L48 34 L55 14 L63 52 L71 24 L78 34 H100 C100 20 112 14 124 20 C130 14 148 16 148 30 C148 42 124 52 124 52 C124 52 100 42 100 34" fill="none" stroke="#FF465C" stroke-width="2.4" stroke-linejoin="round"/></svg>"""

DARK = """
<style>
.stApp{background:#121317;color:#e8edf5}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#3b1020 0%,#2a0d18 100%);border-right:1px solid #ffffff12}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){background:rgba(45,212,191,.13);border:1px solid #2dd4bf77;box-shadow:0 0 18px #2dd4bf26}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p{color:#5eead4}
.topbar{color:#e8edf5}
.head h2{color:#fff}.sub{color:#9aa4b2}
.st-key-hero{background:radial-gradient(circle at 88% 30%,#F5224633,transparent 55%),linear-gradient(110deg,#2b0c18 0%,#3b101f 55%,#240b15 100%);border:1px solid #ffffff14}
.st-key-start button{background:linear-gradient(90deg,#2dd4bf,#5eead4)!important;color:#06231f!important;box-shadow:0 8px 20px #2dd4bf40}
.st-key-explore button{border:1.5px solid #ffffff55!important}
[class*="st-key-fc_"]{background:#1d1a21;border:1px solid #ffffff14;border-radius:14px;box-shadow:inset 0 -2px 0 #F5224666;padding:10px 12px 4px}
[class*="st-key-fc_"]:hover{box-shadow:0 12px 26px #F5224633,inset 0 -2px 0 #F52246}
[class*="st-key-fc_"] button{color:#FF465C!important;padding:.1rem .4rem;justify-content:flex-start;font-size:13px}
.mini{display:flex;gap:12px;align-items:center;color:#fff}.mini i{font-style:normal;font-size:28px}.mini b{font-size:13.5px;line-height:1.3}
.st-key-feat_row{padding:0 26px 26px}
.st-key-hero .st-key-feat_row [data-testid="stHorizontalBlock"]{gap:.8rem;align-items:stretch}
.card{background:#1b1e24;border:1px solid #2a2e37;box-shadow:none}
.card:hover{border-color:#F5224688;box-shadow:0 12px 28px #F5224626}
.card .ic{background:#F5224626}
.card h4{color:#fff}.card p{color:#9aa4b2}
.fcard h4{color:#fff}.fcard p{color:#9aa4b2}
.chip{background:#F5224626;color:#ff8a9a}
.ph{background:linear-gradient(135deg,#3a1220,#1b1e24)}
[data-testid="stVerticalBlockBorderWrapper"]{background:#1b1e24;border-color:#2a2e37!important}
h4 span,.stMarkdown h4{color:#fff}
.banner{border:1px solid #2a2e37;background:linear-gradient(90deg,#1b1e24f5 42%,#1b1e2466),var(--img) right center/cover no-repeat}
.banner h1{color:#fff}.banner small{color:#9aa4b2}
.emer{background:linear-gradient(145deg,#3a1220,#1b1e24);border:1px solid #5a1a28;color:#fff}
.emer .n{color:#ff465c}.emer p{color:#e8b4bd!important}
.warn{background:#2b1016;border:1px solid #5a1a28;border-left:5px solid #F52246;color:#ffc4cf}
.metric{background:#1b1e24;border-color:#2a2e37;box-shadow:none}.metric .v{color:#fff}.metric .l{color:#9aa4b2}
.result p{color:#cbd5e1}.result.idle{background:#1f2630;border:1px solid #2a3a4d}
.result.pos{background:#2b1016;border:1px solid #5a1a28}.result.neg{background:#10291c;border:1px solid #1f5a3a}
.dbar{background:linear-gradient(100deg,#2b1016,#1b1e24 70%);border:1px solid #5a1a28}
button[data-baseweb="tab"]{background:#1b1e24;border:1px solid #2a2e37;color:#cbd5e1}
button[data-baseweb="tab"][aria-selected="true"]{background:linear-gradient(90deg,#d4143a,#F52246);color:#fff}
[data-testid="stExpander"]{border:1px solid #F5224677;border-radius:10px;background:transparent}
[data-testid="stExpander"] summary p{color:#FF465C;font-weight:700}
div.stButton>button[kind="secondary"]{border-color:#F5224688}
.foot{color:#6b7685}
</style>
"""
