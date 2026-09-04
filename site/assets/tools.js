/* tools.js — client-side e-commerce tools for static site
   Features:
   - Live exchange rate (exchangerate.host) with localStorage cache + manual refresh
   - Currency toggle (USD <-> PHP) for pricing panel
   - Tab UI loader for modules: scanner, tacos, voucher, bulk CSV
   - Simple validators and calculators (deterministic, no external libs)
   - CSV parser (browser-only) with summary download
*/

(function(){
  'use strict';
  // Configuration
  var RATE_KEY = 'jl_rate_usd_php';
  var RATE_TTL = 1000 * 60 * 60; // 1 hour
  var FALLBACK_RATE = 55.0; // PHP per USD
  var RATE_API = 'https://api.exchangerate.host/latest?base=USD&symbols=PHP';
  var WHATSAPP_TEXT = encodeURIComponent("Hi Jamie! I tested your Listing Scanner and I'd like to book a Storefront & Compliance Overhaul for my shop.");
  var VIP_WHATSAPP = 'https://wa.me/639394886685?text=' + WHATSAPP_TEXT;

  // Helpers
  function qs(sel,ctx){return (ctx||document).querySelector(sel)}
  function qsa(sel,ctx){return Array.prototype.slice.call((ctx||document).querySelectorAll(sel))}

  // Rate fetcher with cache
  function saveRate(obj){try{localStorage.setItem(RATE_KEY,JSON.stringify(obj))}catch(e){} }
  function loadRate(){try{return JSON.parse(localStorage.getItem(RATE_KEY) || 'null')}catch(e){return null}}

  function fetchRateFromNetwork(){
    return fetch(RATE_API).then(function(r){
      if(!r.ok) throw new Error('Network error');
      return r.json();
    }).then(function(j){
      if(!j || !j.rates || !j.rates.PHP) throw new Error('Invalid response');
      var out = {rate: Number(j.rates.PHP), timestamp: Date.now()};
      saveRate(out); return out;
    });
  }

  function getRate(){
    return new Promise(function(resolve){
      var cached = loadRate();
      if(cached && (Date.now() - cached.timestamp) < RATE_TTL){ resolve(cached); return }
      fetchRateFromNetwork().then(resolve).catch(function(){
        if(cached) return resolve(cached);
        resolve({rate:FALLBACK_RATE,timestamp:Date.now(),fallback:true});
      });
    });
  }

  // UI wiring
  function updateRateNote(el,rateObj){
    if(!el) return;
    var txt='1 USD = ' + (rateObj.rate||FALLBACK_RATE).toFixed(2) + ' PHP';
    var time = new Date((rateObj.timestamp||Date.now()));
    txt += ' · updated ' + time.toLocaleTimeString();
    if(rateObj.fallback) txt += ' (using fallback)';
    el.textContent = txt;
  }

  function applyCurrencyToPricing(rateObj,cur){
    var panel = qs('#pricing-panel'); if(!panel) return;
    panel.innerHTML='';
    var proUsd = 19; var agencyUsd=49; // canonical USD prices
    if(cur==='USD'){
      panel.innerHTML = '<div class="meta">Pro Seller Plan — $'+proUsd+' / month</div><div class="meta" style="margin-top:.5rem">Agency & Multi‑Shop — $'+agencyUsd+' / month</div>';
    }else{
      var r = rateObj.rate || FALLBACK_RATE;
      var proPhp = Math.round(proUsd * r);
      var agencyPhp = Math.round(agencyUsd * r);
      panel.innerHTML = '<div class="meta">Pro Seller Plan — ₱'+proPhp+' / month</div><div class="meta" style="margin-top:.5rem">Agency & Multi‑Shop — ₱'+agencyPhp+' / month</div>';
    }
  }

  // Tab loader
  function loadTabContent(name){
    var target = qs('#tab-content'); if(!target) return;
    if(name==='scanner') return renderScanner(target);
    if(name==='tacos') return renderTacos(target);
    if(name==='voucher') return renderVoucher(target);
    if(name==='bulk') return renderBulk(target);
    target.innerHTML='<p class="muted">Unknown tab</p>';
  }

  // Module renderers
  function renderScanner(root){
    root.innerHTML='';
    var wr = document.createElement('div');
    wr.innerHTML = '\n      <label class="eyebrow">Platform</label>\n      <div style="margin:.5rem 0 1rem"><select id="scanner-platform"><option value="amazon">Amazon (US/UK)</option><option value="shopify">Shopify / Google Shopping</option><option value="tiktok">TikTok Shop</option><option value="etsy">Etsy</option><option value="sea">Shopee & Lazada (SEA)</option></select></div>\n      <label class="eyebrow">Title</label>\n      <input id="scanner-title" style="width:100%;padding:.6rem;margin-top:.35rem;border-radius:8px;border:1px solid var(--edge);background:transparent;color:var(--ink)">\n      <div class="meta" style="margin-top:.45rem" id="title-count"></div>\n      <label class="eyebrow" style="margin-top:1rem">Tags / keywords (comma separated)</label>\n      <input id="scanner-tags" style="width:100%;padding:.6rem;margin-top:.35rem;border-radius:8px;border:1px solid var(--edge);background:transparent;color:var(--ink)">\n      <div style="margin-top:1rem;display:flex;gap:.5rem"><button id="scanner-run" class="tool-btn">Run check</button><button id="scanner-sanitize" class="tool-btn">Auto‑Sanitize</button></div>\n      <div id="scanner-result" style="margin-top:1rem"></div>\n    ';
    root.appendChild(wr);
    var title = qs('#scanner-title'); var platform = qs('#scanner-platform'); var tags = qs('#scanner-tags'); var result = qs('#scanner-result'); var count = qs('#title-count');

    function platformRules(p){
      if(p==='amazon') return {max:200,banWords:['best','#1','top seller','guarantee','cure']};
      if(p==='shopify') return {max:60,metaMax:160,banWords:[]};
      if(p==='tiktok') return {max:120,banWords:['instant','miracle','cure','guarantee']};
      if(p==='etsy') return {max:140,tagLimit:13,banWords:[]};
      if(p==='sea') return {max:255,banWords:['pampaputi','pinakamura','pm']};
      return {max:100,banWords:[]};
    }

    function check(){
      var p = platform.value; var t = title.value||''; var tk = (tags.value||'').split(',').map(function(s){return s.trim().toLowerCase()}).filter(Boolean);
      var rules = platformRules(p); var messages=[];
      if(rules.max && t.length>rules.max) messages.push('Title length exceeds ' + rules.max + ' characters ('+t.length+')');
      rules.banWords.forEach(function(w){ if(t.toLowerCase().indexOf(w)!==-1 || tk.indexOf(w)!==-1) messages.push('Contains potentially prohibited term: "'+w+'"')});
      if(p==='etsy' && tk.length> (rules.tagLimit||13)) messages.push('Etsy allows max '+rules.tagLimit+' tags — you have '+tk.length);
      // basic show
      if(messages.length===0){ result.innerHTML='<div class="pill-in" style="display:inline-block;padding:.6rem 1rem;border-radius:12px">No immediate issues detected</div>' }
      else { result.innerHTML = '<ul class="meta" style="margin:0;padding-left:1rem">'+messages.map(function(m){return '<li>'+m+'</li>'}).join('')+'</ul>' }
    }

    title.addEventListener('input',function(){ var p=platform.value; var rules=platformRules(p); count.textContent = (title.value||'').length + ' / ' + rules.max + ' characters'; });
    qs('#scanner-run').addEventListener('click',check);
    qs('#scanner-sanitize').addEventListener('click',function(){
      var p=platform.value; var rules=platformRules(p); var t = (title.value||'').slice(0,rules.max); ;
      // naive sanitize: remove banned words
      rules.banWords.forEach(function(w){ var re=new RegExp('\\b'+w+'\\b','ig'); t = t.replace(re,'').trim() });
      title.value = t; count.textContent = title.value.length + ' / ' + rules.max + ' characters';
      showToast('Title auto‑sanitized');
    });

  }

  function renderTacos(root){
    root.innerHTML = '\n      <label class="eyebrow">Selling price</label>\n      <input id="tacos-price" type="number" step="0.01" style="width:100%;padding:.6rem;margin-top:.35rem;border-radius:8px;border:1px solid var(--edge);background:transparent;color:var(--ink)">\n      <div style="display:flex;gap:.5rem;margin-top:1rem"><div style="flex:1"><label class="eyebrow">COGS</label><input id="tacos-cost" type="number" step="0.01" style="width:100%;padding:.6rem;border-radius:8px;border:1px solid var(--edge);background:transparent;color:var(--ink)"></div><div style="flex:1"><label class="eyebrow">Ad spend (period)</label><input id="tacos-ad" type="number" step="0.01" style="width:100%;padding:.6rem;border-radius:8px;border:1px solid var(--edge);background:transparent;color:var(--ink)"></div></div>\n      <div style="display:flex;gap:.5rem;margin-top:1rem"><div style="flex:1"><label class="eyebrow">Platform fee %</label><input id="tacos-fee" type="number" step="0.1" value="10" style="width:100%;padding:.6rem;border-radius:8px;border:1px solid var(--edge);background:transparent;color:var(--ink)"></div><div style="flex:1"><label class="eyebrow">Units sold (period)</label><input id="tacos-units" type="number" step="1" value="1" style="width:100%;padding:.6rem;border-radius:8px;border:1px solid var(--edge);background:transparent;color:var(--ink)"></div></div>\n      <div style="margin-top:1rem"><button id="tacos-run" class="tool-btn">Calculate</button></div>\n      <div id="tacos-result" style="margin-top:1rem"></div>\n    ';
    var run = qs('#tacos-run'); var res = qs('#tacos-result');
    run.addEventListener('click',function(){
      var price = parseFloat(qs('#tacos-price').value)||0; var cost = parseFloat(qs('#tacos-cost').value)||0; var ad = parseFloat(qs('#tacos-ad').value)||0; var fee = parseFloat(qs('#tacos-fee').value)||0; var units = parseInt(qs('#tacos-units').value)||1;
      // contribution margin per unit = price - cost - (platform fee) - (ad per unit)
      var platformCut = price * (fee/100);
      var adPerUnit = (units>0)?(ad/units):ad;
      var contribution = price - cost - platformCut - adPerUnit;
      var totalRevenue = price * units; var tacos = (ad / totalRevenue) * 100 || 0; // percent
      var breakevenROAS = (ad>0)?((cost + platformCut) / (ad/units)) : 0; // simplified
      var status = (contribution>0)?'<span style="color:var(--acc-text)">Healthy & Profitable</span>':'<span style="color:#ef4444">High Risk / Negative</span>';
      res.innerHTML = '<div class="pattern"><div><b>Contribution margin per unit</b><div class="meta">'+contribution.toFixed(2)+'</div></div><div><b>TACOS %</b><div class="meta">'+tacos.toFixed(2)+'%</div></div><div><b>Break‑even ROAS</b><div class="meta">'+(breakevenROAS?breakevenROAS.toFixed(2):'—')+'</div></div><div><b>Status</b><div class="meta">'+status+'</div></div></div>';
    });
  }

  function renderVoucher(root){
    root.innerHTML='';
    root.innerHTML = '\n      <div style="display:grid;gap:.6rem"><label class="eyebrow">Regular price</label><input id="v-reg" type="number" step="0.01" style="padding:.6rem;border-radius:8px;border:1px solid var(--edge);background:transparent;color:var(--ink)">\n      <div style="display:flex;gap:.5rem"><div style="flex:1"><label class="eyebrow">Flash sale %</label><input id="v-flash" type="number" value="0" step="0.1" style="width:100%;padding:.6rem;border-radius:8px;border:1px solid var(--edge);background:transparent;color:var(--ink)"></div><div style="flex:1"><label class="eyebrow">Store voucher %</label><input id="v-store" type="number" value="0" step="0.1" style="width:100%;padding:.6rem;border-radius:8px;border:1px solid var(--edge);background:transparent;color:var(--ink)"></div></div>\n      <div style="display:flex;gap:.5rem;margin-top:0.5rem"><div style="flex:1"><label class="eyebrow">Platform voucher %</label><input id="v-platform" type="number" value="0" step="0.1" style="width:100%;padding:.6rem;border-radius:8px;border:1px solid var(--edge);background:transparent;color:var(--ink)"></div><div style="flex:1"><label class="eyebrow">Platform fee %</label><input id="v-fee" type="number" value="10" step="0.1" style="width:100%;padding:.6rem;border-radius:8px;border:1px solid var(--edge);background:transparent;color:var(--ink)"></div></div>\n      <label class="eyebrow">COGS</label><input id="v-cost" type="number" step="0.01" style="padding:.6rem;border-radius:8px;border:1px solid var(--edge);background:transparent;color:var(--ink)">\n      <div style="margin-top:1rem"><button id="v-run" class="tool-btn">Simulate</button></div>\n      <div id="v-result" style="margin-top:1rem"></div></div>\n    ';
    qs('#v-run').addEventListener('click',function(){
      var p = parseFloat(qs('#v-reg').value)||0; var flash = parseFloat(qs('#v-flash').value)||0; var store = parseFloat(qs('#v-store').value)||0; var plat = parseFloat(qs('#v-platform').value)||0; var fee = parseFloat(qs('#v-fee').value)||0; var cost = parseFloat(qs('#v-cost').value)||0;
      // Apply flash sale then vouchers (rough simulation)
      var afterFlash = p * (1 - flash/100);
      var afterStore = afterFlash * (1 - store/100);
      var finalCheckout = afterStore * (1 - plat/100); // buyer pays after platform voucher
      var platformCut = finalCheckout * (fee/100);
      var netPayout = finalCheckout - platformCut;
      var negative = (netPayout < cost);
      var html = '<div class="pattern"><div><b>Final checkout price</b><div class="meta">'+finalCheckout.toFixed(2)+'</div></div><div><b>Net payout</b><div class="meta">'+netPayout.toFixed(2)+'</div></div>';
      if(negative) html += '<div style="padding:1rem;background:rgba(255,0,0,.05);border-left:3px solid #ef4444"><b style="color:#ef4444">Negative Margin Alert</b><div class="meta">Net payout is below COGS</div></div>';
      html += '</div>';
      qs('#v-result').innerHTML = html;
    });
  }

  // CSV parser (simple)
  function csvParse(text){
    var lines = text.split(/\r?\n/).filter(Boolean);
    var head = lines.shift().split(',').map(function(h){return h.trim().toLowerCase()});
    return lines.map(function(l){var parts = l.split(','); var obj={}; head.forEach(function(h,i){obj[h]= (parts[i]||'').trim()}); return obj});
  }
  function renderBulk(root){
    root.innerHTML='';
    root.innerHTML = '\n      <p class="meta">Upload a CSV of your catalog. Template: sku,name,price,cost,platform</p>\n      <div style="display:flex;gap:.5rem"><input id="bulk-file" type="file" accept=".csv"></div>\n      <div style="margin-top:1rem"><button id="bulk-run" class="tool-btn">Run bulk scan</button> <a id="bulk-template" class="tool-btn" href="/site/tools/sample-bulk.csv" download>Download template</a></div>\n      <div id="bulk-result" style="margin-top:1rem"></div>\n    ';
    qs('#bulk-run').addEventListener('click',function(){
      var f = qs('#bulk-file').files && qs('#bulk-file').files[0]; if(!f){ showToast('Select a CSV file first'); return }
      var reader = new FileReader(); reader.onload = function(e){
        try{
          var rows = csvParse(e.target.result);
          var warnings = [];
          rows.forEach(function(r,i){ var price = parseFloat(r.price)||0; var cost = parseFloat(r.cost)||0; if(price<cost) warnings.push({row:i+2,sku:r.sku,message:'Price below cost'}); });
          var out = '<div class="pattern"><div><b>Rows</b><div class="meta">'+rows.length+'</div></div><div><b>Warnings</b><div class="meta">'+warnings.length+'</div></div></div>';
          if(warnings.length) out += '<ul class="meta">'+warnings.map(function(w){return '<li>Row '+w.row+': '+w.message+' (sku: '+(w.sku||'')+')</li>'}).join('')+'</ul>';
          qs('#bulk-result').innerHTML = out;
        }catch(err){ showToast('Failed to parse CSV'); }
      }; reader.readAsText(f);
    });
  }

  // Initialize
  function init(){
    var rateNote = qs('#rate-note'); var curUsd = qs('#cur-usd'); var curPhp = qs('#cur-php'); var vip = qs('#vip-book');
    // tab wiring
    qsa('[data-tab]').forEach(function(b){ b.addEventListener('click', function(){ qsa('[data-tab]').forEach(function(x){x.classList.remove('on')}); b.classList.add('on'); loadTabContent(b.dataset.tab); }); });
    // default active
    var first = qs('[data-tab]'); if(first){ first.classList.add('on'); loadTabContent(first.dataset.tab); }

    // currency toggles
    curUsd.addEventListener('click',function(){ getRate().then(function(r){ applyCurrencyToPricing(r,'USD'); updateRateNote(rateNote,r); }); curUsd.classList.add('on'); curPhp.classList.remove('on'); });
    curPhp.addEventListener('click',function(){ getRate().then(function(r){ applyCurrencyToPricing(r,'PHP'); updateRateNote(rateNote,r); }); curPhp.classList.add('on'); curUsd.classList.remove('on'); });

    vip.addEventListener('click',function(){ window.open(VIP_WHATSAPP,'_blank') });

    // initial rate load
    getRate().then(function(r){ updateRateNote(rateNote,r); applyCurrencyToPricing(r,'PHP'); curPhp.classList.add('on'); }).catch(function(){ updateRateNote(rateNote,{rate:FALLBACK_RATE,timestamp:Date.now(),fallback:true}); applyCurrencyToPricing({rate:FALLBACK_RATE},'PHP'); curPhp.classList.add('on'); });

  }

  // small toast helper relies on global showToast from site
  if(typeof showToast!=='function') window.showToast = function(m){ alert(m) };

  // attach on DOM ready
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();

  // expose getRate for debugging
  window.jl_tools_getRate = getRate;
})();
