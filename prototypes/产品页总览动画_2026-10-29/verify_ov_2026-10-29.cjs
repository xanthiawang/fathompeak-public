// Fallback DOM/behavior audit, not a browser rendering test.
// NODE_PATH=/tmp/ov-dom-qa/node_modules node verify_ov_2026-10-29.cjs
const { JSDOM } = require('jsdom');
const fs = require('node:fs');
const assert = require('node:assert/strict');
const { pathToFileURL } = require('node:url');
(async () => {
  const dom = new JSDOM('<div class="ov-anim" data-layer="0"><img class="ov-original"></div>', {
    url: pathToFileURL(__dirname + '/ov-anim.html').href, runScripts:'outside-only'
  });
  const w = dom.window, d = w.document;
  Object.defineProperty(d, 'currentScript', { value: {src:pathToFileURL(__dirname+'/ov-anim.js').href} });
  Object.defineProperty(d, 'hidden', {value:false, configurable:true});
  let callbacks = new Map(), next = 0, change;
  w.setTimeout = fn => { callbacks.set(++next,fn); return next; };
  w.clearTimeout = id => callbacks.delete(id);
  const media = { matches:false, addEventListener:(_,fn)=>{change=fn;}, removeEventListener:()=>{} };
  w.matchMedia = () => media;
  w.Image = class { set src(url) { assert.ok(fs.existsSync(require('node:url').fileURLToPath(url))); Promise.resolve().then(()=>this.onload()); } };
  let motionPaused = false;
  w.SVGElement.prototype.pauseAnimations = () => { motionPaused = true; };
  w.SVGElement.prototype.unpauseAnimations = () => { motionPaused = false; };
  const root=d.querySelector('.ov-anim'), events=[];
  root.addEventListener('ovlayer',e=>events.push(e.detail.layer));
  w.eval(fs.readFileSync(__dirname+'/ov-anim.js','utf8'));
  w.OvAnimation.init(root);
  await new Promise(resolve=>setImmediate(resolve));
  assert.equal(root.querySelectorAll('.ov-tier').length,4);
  assert.equal(root.querySelectorAll('.ov-flow').length,22);
  assert.equal(root.querySelectorAll('.ov-circuit').length,12);
  assert.equal(root.querySelectorAll('animateMotion').length,22);
  assert.ok(root.hasAttribute('data-ready'));
  assert.equal(motionPaused,false);
  const step=()=>{const [id,fn]=[...callbacks][0];callbacks.delete(id);fn();};
  for(let i=0;i<4;i++)step();
  assert.deepEqual(events,[0,1,2,3,0]);
  const hit=root.querySelector('[data-tier="2"] .ov-hit');
  hit.dispatchEvent(new w.Event('pointerenter'));
  assert.equal(root.dataset.layer,'2');assert.equal(callbacks.size,0);
  assert.ok(root.hasAttribute('data-paused'));
  assert.equal(motionPaused,true);
  hit.dispatchEvent(new w.Event('pointerleave'));
  assert.equal(motionPaused,false);
  assert.equal(callbacks.size,1);step();assert.equal(root.dataset.layer,'3');
  media.matches=true;change();
  assert.equal(callbacks.size,0);assert.equal(root.dataset.layer,'0');assert.equal(motionPaused,true);
  media.matches=false;change();assert.equal(callbacks.size,1);
  Object.defineProperty(d,'hidden',{value:true,configurable:true});
  d.dispatchEvent(new w.Event('visibilitychange'));assert.equal(callbacks.size,0);
  root.ovAnimation.destroy();assert.equal(root.querySelector('.ov-scene'),null);
  const report={date:'2026-10-29',syntax:'passed',dom_checks:'passed',event_sequence:events,
    checks:['four layers','ten pipe circles plus twelve circuit circles','SVG clock pauses and resumes','assets exist','0-1-2-3 cycle','hover selects and pauses','leave resumes','reduced motion stops timer','hidden page stops timer','destroy restores fallback'],
    browser_render:'Not verified by this DOM audit; see README second-round notes',
    note:'DOM test uses simulated image load and timers; PIL independently decodes and checks exported assets. Not a browser render acceptance.'};
  fs.writeFileSync(__dirname+'/verification_round2_2026-10-29.json',JSON.stringify(report,null,2)+'\n');
  console.log(report);
  dom.window.close();
})().catch(error=>{console.error('Overview verification failed:',error);process.exitCode=1;});
