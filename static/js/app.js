:root {
  --bg: #0b1020;
  --panel: #131d32;
  --card: #f5f7ff;
  --text: #edf3ff;
  --muted: #b5c4e5;
  --primary: #7c9cff;
  --accent: #65d6a5;
  --warning: #f5c76d;
  --shadow: rgba(17, 24, 39, 0.35);
}

* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
  background: linear-gradient(180deg, #0d1326 0%, #121929 100%);
  color: var(--text);
}

a { color: inherit; }
.container { width: min(1100px, calc(100% - 32px)); margin: 0 auto; }
.topbar {
  position: sticky; top: 0; z-index: 10; backdrop-filter: blur(10px);
  background: rgba(11,16,32,0.75); border-bottom: 1px solid rgba(255,255,255,0.08);
}
.nav { display: flex; justify-content: space-between; align-items: center; min-height: 72px; }
.brand { font-size: 1.2rem; font-weight: 700; }
nav { display: flex; gap: 18px; flex-wrap: wrap; }
nav a { color: var(--muted); text-decoration: none; }
.hero { padding: 90px 0 50px; }
.hero-grid { display: grid; grid-template-columns: 1.5fr 0.9fr; gap: 32px; align-items: center; }
.eyebrow { text-transform: uppercase; letter-spacing: 0.12em; color: var(--accent); font-size: 0.8rem; font-weight: 700; }
h1 { font-size: clamp(2.4rem, 4vw, 4rem); line-height: 1.08; margin: 0 0 16px; }
.hero-copy p { color: var(--muted); font-size: 1.08rem; line-height: 1.8; }
.cta-row { display: flex; gap: 16px; flex-wrap: wrap; margin-top: 24px; }
.btn {
  display: inline-flex; align-items: center; justify-content: center; border: none; border-radius: 999px;
  padding: 14px 22px; font-weight: 700; cursor: pointer; text-decoration: none; transition: 0.2s ease;
}
.btn.primary { background: var(--primary); color: #fff; }
.btn.secondary { background: transparent; border: 1px solid rgba(255,255,255,0.18); color: var(--text); }
.hero-panel { display: grid; gap: 18px; }
.stat-box, .feature-grid article, .product-card, .panel, .summary-card {
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 22px; box-shadow: var(--shadow);
}
.stat-box span { display: block; color: var(--muted); margin-bottom: 10px; }
.stat-box strong { font-size: 2rem; }
.section { padding: 80px 0; }
.section.alt { background: rgba(255,255,255,0.02); }
.section-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 28px; }
.section-head a { color: var(--accent); text-decoration: none; }
.feature-grid, .product-grid, .summary-grid, .panel-grid { display: grid; gap: 20px; }
.feature-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.product-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.product-card img { width: 100%; height: 200px; object-fit: cover; border-radius: 12px; margin-bottom: 16px; }
.product-card h3, .feature-grid h3, .panel h3 { margin: 0 0 8px; }
.product-card p, .feature-grid p, .panel p { color: var(--muted); line-height: 1.7; }
.product-meta { display: flex; justify-content: space-between; align-items: center; margin-top: 18px; }
.price-tag { font-weight: 700; color: var(--warning); }
.tag { background: rgba(101,214,165,0.15); color: var(--accent); border-radius: 999px; padding: 8px 12px; font-size: 0.8rem; }
.summary-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); margin-bottom: 28px; }
.summary-card strong { display: block; margin-top: 8px; font-size: 1.7rem; }
.panel-grid { grid-template-columns: 1.2fr 0.8fr; }
.bar-chart { display: grid; gap: 12px; }
.bar-row { display: grid; grid-template-columns: 90px 1fr 48px; align-items: center; gap: 12px; }
.bar-track { background: rgba(255,255,255,0.06); height: 14px; border-radius: 999px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, var(--primary), var(--accent)); }
.idea-list { padding-left: 18px; color: var(--muted); line-height: 1.8; }
.footer { padding: 28px 0 60px; color: var(--muted); }
.auth-body { display: grid; place-items: center; min-height: 100vh; }
.auth-card { width: min(420px, calc(100% - 32px)); background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 28px; }
.auth-card form, .panel form, .ai-copy-form { display: grid; gap: 14px; }
input, textarea, select, button { font: inherit; }
input, textarea, select {
  width: 100%; padding: 12px 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.12); background: rgba(12,18,30,0.6); color: var(--text);
}
textarea { min-height: 100px; resize: vertical; }
.error { color: #ff9ca9; }
.admin-page { padding: 48px 0 80px; }
.admin-grid { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 20px; margin-bottom: 28px; }
.generated-copy { margin-top: 18px; padding: 18px; border-radius: 12px; background: rgba(255,255,255,0.04); color: var(--muted); }
@media (max-width: 900px) {
  .hero-grid, .feature-grid, .product-grid, .summary-grid, .panel-grid, .admin-grid { grid-template-columns: 1fr; }
  nav { gap: 10px; }
}
