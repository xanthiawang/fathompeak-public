(() => {
  const toHex = (c) => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(s => parseFloat(s)); if (p.length === 4 && p[3] < 0.5) return null; return '#' + p.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase(); };
  const q = (s) => [...document.querySelectorAll(s)];
  const txt = (e) => (e.innerText || e.textContent || '').trim().replace(/\s+/g, ' ');
  const scripts = q('script[src]').map(s => s.src.toLowerCase());
  const libs = ['gsap', 'three', 'lottie', 'framer', 'motion', 'spline', 'rive', 'swiper', 'aos', 'locomotive', 'lenis', 'anime', 'webgl', 'unity', 'particles'].filter(k => scripts.some(s => s.includes(k)));
  let keyframes = 0, animated = 0;
  for (const sh of document.styleSheets) { let rules; try { rules = sh.cssRules; } catch (e) { continue; } for (const r of rules || []) if (r.type === 7) keyframes++; }
  for (const el of q('body *').slice(0, 4000)) { const cs = getComputedStyle(el); if (cs.animationName && cs.animationName !== 'none') animated++; }
  const ctas = q('a,button').filter(e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); const t = txt(e); return t && t.length < 24 && r.width > 60 && r.height > 28 && r.top < innerHeight * 1.5 && toHex(cs.backgroundColor); }).map(e => txt(e) + ' [' + toHex(getComputedStyle(e).backgroundColor) + ']');
  const inputs = q('input,select,textarea').filter(e => e.type !== 'hidden').map(e => (e.type || e.tagName.toLowerCase()) + ':' + (e.placeholder || e.name || e.id || '')).slice(0, 12);
  const tables = q('table').length;
  const priceHits = (document.body.innerText.match(/[¥$￥]\s?\d+(\.\d+)?/g) || []).slice(0, 12);
  const perM = (document.body.innerText.match(/(每|\/|per )\s?(百万|1M|M|million)\s?(tokens?|词元)/gi) || []).length;
  const hero = document.querySelector('h1') || q('h2')[0];
  return JSON.stringify({
    url: location.href, title: document.title, bodyFont: getComputedStyle(document.body).fontFamily.split(',')[0],
    counts: { video: q('video').length, canvas: q('canvas').length, svg: q('svg').length, img: q('img').length, lottie: q('lottie-player,[data-lottie],dotlottie-player').length, iframe: q('iframe').length, tables, inputs: inputs.length, keyframes, animatedNow: animated },
    libs, hasScrollReveal: !!(window.IntersectionObserver && (scripts.some(s => /aos|reveal|scroll/.test(s)) || keyframes > 5)),
    nav: [...new Set(q('header a, nav a').map(txt).filter(t => t && t.length < 18))].slice(0, 18),
    ctas: [...new Set(ctas)].slice(0, 10), inputs, h1: hero ? txt(hero).slice(0, 120) : null,
    h2: q('h2').map(txt).filter(Boolean).slice(0, 12), priceHits, perMillionMentions: perM,
    imgAlt: q('img').map(i => (i.alt || '').trim()).filter(Boolean).slice(0, 10),
    bodyText: document.body.innerText.replace(/\s+/g, ' ').slice(0, 2500)
  });
})()
