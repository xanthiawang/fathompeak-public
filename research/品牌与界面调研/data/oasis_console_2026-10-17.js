  /* ======== 绿洲（2026-10-17 第二版）：用户后台里的一页，不是单独的应用 ========
     逻辑（Zixin 10-17 指出第一版使用逻辑有问题后重写）：
       调用 → 绿洲里冒出能量球 → 点一下收进正在长的那棵树；4 份长成。
       长成：送 1 张算力代金券（直接进钱包）+ 开种袋，下一颗种子自动种下。
       营地种满后自动开放溪畔，再种满开放林地；6 个位置都满后，最早的树移入森林。没有手动扩建、选位置、移动。
     原型里，体验中心每发一条消息算一次调用（按所选模型数计）；只存内存，刷新即重来，不发请求、不扣费。
     种袋顺序沿用 Codex 原型：第 1 袋月辉，之后与暖阳交替。插画为 Codex 10-18 交付的 A 版蚀刻（炭黑排线 + 自然淡彩，荒漠绿洲）。 */
  (function(){
    var oaRoot=document.getElementById('oaRoot'); if(!oaRoot) return;
    const WORLD='art/oasis/oasis-world_etched_2026-10-18.webp',GROW='art/oasis/oasis-growth_etched_2026-10-18.webp';
    const SP={sun:{n:'暖阳树',r:'常规',d:'一棵普通的小树，慢慢也能长成一片林子。'},moon:{n:'月辉树',r:'稀有',d:'银绿叶片和月牙果实，给绿洲留一点夜光。'}};
    const STG=['种子','发芽','树苗','成树','成熟'],ZN=['营地','溪畔','林地'],NEED=4;
    /* 坑位与 Codex 蚀刻场景对齐（交付索引 2026-10-18）：每块地前后错开两个坑，树宽 16% 时不重叠 */
    const POS=[[12,78],[24,60],[44,78],[56,60],[76,78],[88,60]],BUB=[[-7,-22],[6,-25],[-1,-30],[9,-15],[-9,-11]];
    const SPROUT='<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 17V9.5M10 11.5C10 8 7.6 6.3 4 6.3c0 3.5 2.4 5.2 6 5.2ZM10 9.5c0-3 2-4.7 5.6-4.7 0 3-2 4.7-5.6 4.7ZM5.5 17h9" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    const fresh=()=>({trees:[],cur:null,bag:false,pending:0,zones:1,draws:0,coupons:0,forest:0,log:[],night:false});
    let s=fresh(),still=false,logAll=false;
    const E=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    const B=(label,a,v='',cls='gray')=>`<button type="button" class="btn ${cls} sm" data-oa="${a}" data-v="${E(v)}">${label}</button>`;
    const L=(label,a,v='')=>`<button type="button" class="bt-a" data-oa="${a}" data-v="${E(v)}">${label}</button>`;
    /* 图集 5 列 × 2 行：列 = 阶段（种子、发芽、树苗、成树、成熟），上行暖阳、下行月辉；接地点在格内 (50%, 90%) */
    const art=t=>`<span class="oa-art${t.type==='moon'?' rare':''}" role="img" aria-label="${SP[t.type].n} · ${STG[t.e]}" style="--col:${t.e*25}%;background-image:url('${GROW}')"></span>`;
    const nm=t=>E(t.name||SP[t.type].n);
    const cur=()=>s.trees.find(t=>t.id===s.cur);
    const tm=iso=>new Date(iso).toLocaleString('zh-CN',{month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'});
    const role=()=>(typeof me!=='undefined'&&me&&me.role)||'personal';
    function note(type,detail,ref){s.log.push({type,detail,ref:ref||'',time:new Date().toISOString()})}
    const dlg=document.getElementById('oaDlg');
    function modal(title,body){document.getElementById('oaDlgT').textContent=title;document.getElementById('oaDlgB').innerHTML=body;if(!dlg.open)dlg.showModal()}
    function close(){if(dlg.open)dlg.close()}
    function plant(type){
      const used=new Set(s.trees.filter(t=>t.slot>=0).map(t=>t.slot)),free=()=>[...Array(s.zones*2).keys()].find(i=>!used.has(i));
      let slot=free(),extra='';
      if(slot===undefined&&s.zones<3){s.zones++;note('开放'+ZN[s.zones-1],ZN[s.zones-2]+'种满了，'+ZN[s.zones-1]+'多了 2 个位置');extra=ZN[s.zones-1]+'开放了。';slot=free()}
      if(slot===undefined){const old=s.trees.filter(t=>t.slot>=0&&t.e===NEED)[0];slot=old.slot;old.slot=-1;s.forest++;note('移入森林',nm(old)+'移入森林，腾出位置；记录都保留',old.id);extra=nm(old)+'移入了森林。'}
      const t={id:'tree-'+(s.trees.length+1),type,e:0,slot,at:new Date().toISOString(),name:''};
      s.trees.push(t);s.cur=t.id;note('种下'+SP[type].n,'种在'+ZN[Math.floor(slot/2)],t.id);
      return {t,extra};
    }
    function collect(){
      const t=cur();if(!t||!s.pending)return false;
      s.pending--;t.e++;note('收取能量','1 份能量 · '+nm(t)+' '+STG[t.e-1]+' → '+STG[t.e],t.id);
      if(t.e===NEED){s.cur=null;s.bag=true;s.coupons++;note(nm(t)+'长成了','送 1 张算力代金券，已放进钱包',t.id);render();
        modal(SP[t.type].n+'长成了',`<div class="oa-reveal">${art(t)}<p>送你 1 张算力代金券，已经放进钱包。</p><p>种袋里有下一颗种子。</p><div class="oa-acts">${B('打开种袋','bag','','black')}</div></div>`);return 'mature'}
      return true;
    }
    function openBag(){
      if(!s.bag)return;const type=s.draws%2===0?'moon':'sun';s.draws++;s.bag=false;const {t,extra}=plant(type);render();
      modal(type==='moon'?'月光落进了种袋':'又一颗暖阳',`<div class="oa-reveal">${art({type,e:NEED})}<span class="oa-tag">${SP[type].r}</span><p>${SP[type].n}种在${ZN[Math.floor(t.slot/2)]}，从种子开始长。${extra}</p><div class="oa-acts">${B('好','close','','black')}</div></div>`);
    }
    function map(){
      const c=cur(),planted=s.trees.filter(t=>t.slot>=0);
      /* 未开放区域：一整片雾，从区域边界起向内渐隐（不压到已开放区域里的树），不画硬分界线；每块地只在顶部放一个小标签 */
      const fog=s.zones<3?`<div class="oa-fog" style="left:${s.zones*100/3}%"></div>`+[1,2].filter(i=>i>=s.zones).map(i=>`<span class="oa-chip" style="left:${i*100/3+100/6}%">${ZN[i]}<span class="oa-chipx"> · ${i===s.zones?'种满'+ZN[i-1]+'后开放':'之后开放'}</span></span>`).join(''):'';
      const trees=planted.map(t=>`<button type="button" class="oa-tree oa-p${t.slot}${t.id===s.cur?' cur':''}" data-oa="tree" data-v="${t.id}" aria-label="${nm(t)}，${STG[t.e]}">${art(t)}<span class="oa-cap">${nm(t)} · ${STG[t.e]}</span></button>`).join('');
      const first=!s.trees.length?`<button type="button" class="oa-plot oa-p0" data-oa="first"><span>＋</span>种下第一颗</button>`:'';
      let bubs='';
      if(c&&s.pending){const [x,y]=POS[c.slot],n=Math.min(s.pending,BUB.length),f=[.35,.5,.7,.88,1][c.e];bubs=BUB.slice(0,n).map(([dx,dy],i)=>{const more=i===n-1&&s.pending>n?s.pending-n+1:1;return `<button type="button" class="oa-bub" style="left:${x+dx}%;top:${y+dy*f}%;animation-delay:${-i*.7}s" data-oa="collect" aria-label="收取 ${more} 份能量"><b class="mono">+${more}</b></button>`}).join('')}
      return `<section class="oa-map" aria-label="绿洲"><div class="oa-maphd"><span>OASIS · 已种 ${s.trees.length} 棵${s.forest?' · 森林 '+s.forest:''}</span><div><button type="button" class="oa-q" data-oa="night" aria-pressed="${s.night}">${s.night?'暮色':'日光'}</button><button type="button" class="oa-q" data-oa="still" aria-pressed="${still}">${still?'已暂停摆动':'暂停摆动'}</button></div></div>
        <div class="oa-world${s.night?' night':''}"><img src="${WORLD}" alt="相连的营地、溪畔和林地">${fog}${trees}${first}${bubs}</div>${foot()}</section>`;
    }
    function foot(){
      const c=cur();let lead,body,actn;
      if(c){lead=c.e?art(c):`<span class="oa-ico">${SPROUT}</span>`;body=`<b>${nm(c)} · ${STG[c.e]}</b><i class="bt-track"><i style="width:${c.e/NEED*100}%"></i></i><span>${s.pending?'有 '+s.pending+' 份能量待收':'再收 '+(NEED-c.e)+' 份能量长成'}</span>`;actn=s.pending?B('收取能量','collect-all','','black'):B('去体验中心','go','play')}
      else if(s.bag){lead=`<span class="oa-ico">${SPROUT}</span>`;body='<b>种袋还没打开</b><span>打开后，下一颗种子会自动种下。</span>';actn=B('打开种袋','bag','','black')}
      else{lead=`<span class="oa-ico">${SPROUT}</span>`;body=`<b>还没有种树</b><span>种下第一颗种子，之后每完成一次调用，它就长大一点。${s.pending?'已经有 '+s.pending+' 份能量在等它。':''}</span>`;actn=B('种下第一颗种子','first','','black')}
      return `<div class="oa-foot">${lead}<div class="oa-fi">${body}</div><div class="oa-fa">${actn}</div></div>`;
    }
    function sources(){
      return `<h3 class="cs-h3">能量从哪来</h3><div class="oa-src">
        <div class="oa-srow"><span class="oa-amt mono">+1</span><div><b>每完成一次调用</b><span class="cs-help">体验中心或 API 的请求完成后，绿洲里多 1 份能量。</span></div>${L('去体验中心','go','play')}</div>
        <div class="oa-srow"><span class="oa-amt mono">+2</span><div><b>绿电时段的批量任务</b><span class="cs-help">不急的任务排到电站绿电富余的时段执行，每完成一批多 2 份。</span></div>${L('了解绿电批量任务','go','batch')}</div>
      </div><p class="cs-fine">原型里，体验中心每发一条消息算一次调用。能量份数是玩法设定，不是计费规则；绿洲不显示具体电站，也不给出减排数字。</p>`;
    }
    function atlas(){
      const cards=Object.keys(SP).map(type=>{const n=s.trees.filter(t=>t.type===type).length;return `<article class="oa-card${n?'':' locked'}">${art({type,e:NEED})}<span class="oa-tag">${SP[type].r}</span><h4>${SP[type].n}</h4><p>${n?SP[type].d:'还没遇到。'}</p><span class="oa-cnt mono">${n?'已种 '+n+' 棵':'—'}</span></article>`}).join('');
      const own=Object.keys(SP).filter(type=>s.trees.some(t=>t.type===type)).length,mem=role()==='member';
      return `<h3 class="cs-h3">图鉴 <span class="oa-cnt mono">${own} / ${Object.keys(SP).length}</span></h3><div class="oa-cards">${cards}</div>
        <p class="cs-fine">每棵树长成时开一个种袋，按公开的顺序出种：第 1 袋月辉，第 2 袋暖阳，之后交替，不是抽奖。每棵树长成还送 1 张算力代金券，${mem?'放进企业钱包，由管理员统一使用':'放进钱包，优先于余额扣费'}；面额待定。${s.coupons&&!mem?' '+L('去钱包看看','go','bill'):''}</p>`;
    }
    function log(){
      if(!s.log.length)return '';
      const ev=s.log.slice().reverse(),show=logAll?ev:ev.slice(0,6);
      return `<h3 class="cs-h3">成长记录</h3><ul class="oa-log">${show.map(e=>`<li><i></i><b>${E(e.type)}</b><time>${tm(e.time)}</time><span>${E(e.detail)}</span></li>`).join('')}</ul>${ev.length>6?`<div class="oa-more">${B(logAll?'收起':'查看全部 '+ev.length+' 条','log-all')}</div>`:''}`;
    }
    function outside(){
      const c=cur(),r=document.getElementById('oaRailT');
      if(r)r.textContent=c?'绿洲 · '+(c.name||SP[c.type].n)+' · '+STG[c.e]+(s.pending?' · '+s.pending+' 份能量待收':''):s.pending?'绿洲 · '+s.pending+' 份能量待收':'绿洲 · 还没有种树';
      const nb=document.querySelector('.cs-nav [data-p="oasis"]');
      if(nb){let b=nb.querySelector('.oa-n');if(s.pending){if(!b){b=document.createElement('span');b.className='bt-n mono oa-n';nb.appendChild(b)}b.textContent=s.pending;b.setAttribute('aria-label',s.pending+' 份能量待收')}else if(b)b.remove()}
      const w=document.getElementById('oaWallet'),e=document.getElementById('oaWalletEmpty');
      if(w){w.hidden=!s.coupons;if(e)e.hidden=!!s.coupons;w.innerHTML=s.coupons?`<div><span>算力代金券 · 来自绿洲 × <span class="mono">${s.coupons}</span><small>每棵树长成送 1 张；下一次付费调用时自动抵扣，优先于余额。面额待定。</small></span><span class="oa-tag">可用</span></div>`:''}
    }
    function render(){oaRoot.classList.toggle('oa-still',still);oaRoot.innerHTML=map()+sources()+atlas()+log();outside()}
    function detail(id){
      const t=s.trees.find(x=>x.id===id);if(!t)return;
      modal(t.name||SP[t.type].n,`<div class="oa-reveal">${art(t)}<span class="oa-tag">${SP[t.type].r} · ${STG[t.e]}${t.slot<0?' · 森林':''}</span></div><div class="cs-f"><label for="oaName">给它起个名字</label><input class="in" id="oaName" maxlength="20" value="${E(t.name)}" placeholder="${SP[t.type].n}"></div><div class="oa-acts">${B('保存','rename',id,'black')}</div>${s.log.filter(e=>e.ref===id).map(e=>`<div class="oa-srcl"><b>${E(e.type)}</b><span>${E(e.detail)}</span><time>${tm(e.time)}</time></div>`).join('')}`);
    }
    function rules(){
      modal('绿洲怎么玩',`<div class="oa-rule"><p>在平台上的每次调用都会变成能量，出现在正在长的那棵树旁边，点一下就收进去。收满 4 份，树从种子长成：种子 → 发芽 → 树苗 → 成树 → 成熟。</p><h4>长成以后</h4><p>送 1 张算力代金券，直接放进钱包；再开一个种袋，下一颗种子自动种下。种袋按公开顺序出种，不是抽奖。</p><h4>地方不够了</h4><p>营地种满后自动开放溪畔，溪畔种满开放林地。6 个位置都满了，最早长成的树会移入森林，图鉴和记录都保留。</p><h4>不显示什么</h4><p>不显示用了哪座电站、各电站价格，也不给出未经核验的减排数字。时段折扣是价格规则，不能单独证明绿电来源。</p></div>`);
    }
    function onClick(e){
      const b=e.target.closest('[data-oa]');if(!b)return;const a=b.dataset.oa,v=b.dataset.v;
      if(a==='close'){close();return}
      if(a==='go'){close();csTab(v);window.scrollTo(0,0);return}
      if(a==='night'){s.night=!s.night;render();return}
      if(a==='still'){still=!still;render();return}
      if(a==='log-all'){logAll=!logAll;render();return}
      if(a==='first'){if(!s.trees.length){plant('sun');render()}return}
      if(a==='collect'){if(collect()===true)render();return}
      if(a==='collect-all'){let r;while(s.pending&&cur()&&(r=collect())===true){}if(r===true)render();return}
      if(a==='bag'){openBag();return}
      if(a==='tree'){detail(v);return}
      if(a==='rename'){const t=s.trees.find(x=>x.id===v),i=document.getElementById('oaName');if(t&&i){t.name=i.value.trim().slice(0,20);close();render()}return}
      if(a==='rules'){rules();return}
      if(a==='reset'){modal('重新开始？',`<p>清空这个预览里的树、能量和代金券。只影响当前页面。</p><div class="oa-acts">${B('重新开始','reset-ok','','black')}${B('取消','close')}</div>`);return}
      if(a==='reset-ok'){s=fresh();close();render();return}
    }
    oaRoot.addEventListener('click',onClick);dlg.addEventListener('click',e=>{if(e.target===dlg){close();return}onClick(e)});
    document.querySelectorAll('[data-oa-top]').forEach(b=>b.addEventListener('click',()=>onClick({target:b})));
    /* 体验中心发出消息 → 绿洲多能量（原型里代替真实调用完成事件）；先于体验中心自己的处理读取输入 */
    document.addEventListener('submit',function(e){if(!e.target||e.target.id!=='xpBox')return;const q=document.getElementById('xpQ');if(!q||!q.value.trim())return;
      const n=Math.max(1,document.querySelectorAll('#xpPills .xp-pill').length);s.pending+=n;note('体验中心发出 '+n+' 次请求','绿洲多了 '+n+' 份能量');render();setTimeout(function(){toast('绿洲多了 '+n+' 份能量。')},60)},true);
    render();
  })();
