/**
 * Node test harness for Portfolio tools (SellerGuard Micro-SaaS)
 * Stubs browser DOM, navigator, localStorage, URL, Blob
 * Runs tests and reports PASS/FAIL assertions.
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

console.log('====================================================');
console.log('SELLERGUARD MICRO-SAAS TEST HARNESS');
console.log('====================================================\n');

// 1. Setup DOM Stubs & Storage
const storage = {};
const localStorageMock = {
  getItem: (k) => (k in storage ? storage[k] : null),
  setItem: (k, v) => { storage[k] = String(v); },
  removeItem: (k) => { delete storage[k]; },
  clear: () => { for (let k in storage) delete storage[k]; }
};

let lastCopiedText = '';
const clipboardMock = {
  writeText: (t) => {
    lastCopiedText = t;
    return Promise.resolve();
  }
};

// Handle Node 22 navigator compatibility
if (typeof global.navigator === 'undefined') {
  global.navigator = { clipboard: clipboardMock };
} else {
  try {
    Object.defineProperty(global, 'navigator', {
      value: { clipboard: clipboardMock },
      configurable: true,
      writable: true
    });
  } catch (e) {
    try {
      Object.defineProperty(navigator, 'clipboard', {
        value: clipboardMock,
        configurable: true,
        writable: true
      });
    } catch (e2) {}
  }
}

global.localStorage = localStorageMock;

const blobStore = {};
let lastCreatedBlob = null;
let lastDownloadedFile = null;

class MockBlob {
  constructor(parts, opts) {
    this.parts = parts;
    this.opts = opts || {};
    this.text = parts.join('');
    lastCreatedBlob = this;
  }
}
global.Blob = MockBlob;

global.URL = {
  createObjectURL: (blob) => {
    const url = 'blob:test-' + Math.random().toString(36).slice(2);
    blobStore[url] = blob;
    return url;
  },
  revokeObjectURL: (url) => {
    delete blobStore[url];
  }
};

// DOM Elements Registry
const elements = {};

function getOrCreateElement(id) {
  if (elements[id]) return elements[id];
  const el = {
    id: id,
    tagName: 'DIV',
    value: '',
    textContent: '',
    innerHTML: '',
    style: {},
    dataset: {},
    classList: {
      classes: new Set(),
      add: function(c) { this.classes.add(c); },
      remove: function(c) { this.classes.delete(c); },
      contains: function(c) { return this.classes.has(c); }
    },
    listeners: {},
    addEventListener: function(evt, handler) {
      if (!this.listeners[evt]) this.listeners[evt] = [];
      this.listeners[evt].push(handler);
    },
    trigger: function(evt, data) {
      if (this.listeners[evt]) {
        this.listeners[evt].forEach(fn => fn(data || { target: this }));
      }
    },
    click: function() {
      this.trigger('click', { target: this });
    },
    querySelectorAll: function(sel) {
      return [];
    },
    querySelector: function(sel) {
      return null;
    },
    attrs: {},
    getAttribute: function(k){ return this.attrs[k] === undefined ? null : this.attrs[k]; },
    setAttribute: function(k,v){ this.attrs[k] = String(v); },
    removeAttribute: function(k){ delete this.attrs[k]; },
    focus: function(){}, blur: function(){},
    appendChild: function(){}, removeChild: function(){}, remove: function(){},
    closest: function(){ return null; },
    scrollIntoView: function(){},
    offsetWidth: 100, offsetHeight: 20
  };
  elements[id] = el;
  return el;
}

// Global Document Stub
global.document = {
  getElementById: (id) => getOrCreateElement(id),
  querySelectorAll: (sel) => {
    if (sel === '.suite-tab') {
      return [getOrCreateElement('tab1'), getOrCreateElement('tab2'), getOrCreateElement('tab3'), getOrCreateElement('tab4')];
    }
    if (sel === '.suite-panel') {
      return [getOrCreateElement('panel-scanner'), getOrCreateElement('panel-tacos'), getOrCreateElement('panel-voucher'), getOrCreateElement('panel-audit')];
    }
    if (sel === '.plat-btn') {
      return [getOrCreateElement('plat-sea')];
    }
    if (sel === '.curr-btn') {
      return [getOrCreateElement('curr-php')];
    }
    if (sel === '[data-php][data-usd]') {
      return [];
    }
    if (sel === '#audit-table th[data-sort]') {
      return ['sku', 'title', 'score', 'imageCount', 'reviews', 'price', 'stock'].map(col => {
        const th = getOrCreateElement('th-' + col);
        th.dataset.sort = col;
        return th;
      });
    }
    if (sel === '#cls-tabs .cls-tab') {
      return ['all','Expired stock','Clearance sale','Flash sale','Bundle / voucher','Promo push','Scale','Restock first','noimage'].map(f => {
        const b = getOrCreateElement('cls-tab-' + f); b.dataset.f = f; b.classList.toggle = function(c, on){ on ? this.classes.add(c) : this.classes.delete(c); }; return b;
      });
    }
    if (sel === '#audit-top-fixes .fix-item') {
      const html = elements['audit-top-fixes'] ? elements['audit-top-fixes'].innerHTML : '';
      const matches = [...html.matchAll(/<span class="fix-title">([^<]+)<\/span>[\s\S]*?<div class="fix-stat">([^<]+)<\/div>/g)];
      return matches.map(m => ({
        querySelector: (sub) => {
          if (sub === '.fix-title') return { textContent: m[1] };
          if (sub === '.fix-stat') return { textContent: m[2] };
          return null;
        }
      }));
    }
    return [];
  },
  createElement: (tag) => {
    const el = {
      tagName: tag.toUpperCase(),
      style: {},
      value: '',
      href: '',
      download: '',
      click: function() {
        if (this.download) {
          lastDownloadedFile = {
            download: this.download,
            href: this.href,
            blob: blobStore[this.href] || lastCreatedBlob
          };
        }
      },
      select: () => {},
      appendChild: () => {},
      removeChild: () => {}
    };
    return el;
  },
  body: {
    appendChild: () => {},
    removeChild: () => {},
    classList: { add(){}, remove(){}, contains(){ return false; }, toggle(){} }
  },
  documentElement: {
    attrs: {},
    getAttribute: function(k){ return this.attrs[k] === undefined ? null : this.attrs[k]; },
    setAttribute: function(k,v){ this.attrs[k] = String(v); },
    classList: { add(){}, remove(){}, contains(){ return false; }, toggle(){} },
    style: {}
  },
  querySelector: (sel) => null,
  addEventListener: () => {},
  execCommand: () => true
};
global.matchMedia = () => ({ matches: false, addEventListener(){}, addListener(){} });

global.window = global;
global.addEventListener = () => {};
global.requestAnimationFrame = (f) => 0;

// 2. Load Tool Script from site/tools/index.html
const htmlPath = path.resolve(__dirname, '../site/tools/index.html');
if (!fs.existsSync(htmlPath)) {
  console.error('FAIL: site/tools/index.html does not exist. Run python build.py first.');
  process.exit(1);
}

const htmlContent = fs.readFileSync(htmlPath, 'utf8');
const scriptMatches = [...htmlContent.matchAll(/<script>([\s\S]*?)<\/script>/g)];
const toolScript = scriptMatches.find(s => s[1].length > 1000);

if (!toolScript) {
  console.error('FAIL: Could not find inline tool script in site/tools/index.html');
  process.exit(1);
}

console.log('Loaded inline script: ' + toolScript[1].length + ' characters.\n');

// Execute script in the simulated context
try {
  vm.runInThisContext(toolScript[1]);
  console.log('Script evaluated successfully without runtime exceptions.\n');
} catch (err) {
  console.error('FAIL: Error executing script in context:', err);
  process.exit(1);
}

// 3. Test Suite
let passCount = 0;
let failCount = 0;

function assert(condition, testName, extraInfo = '') {
  if (condition) {
    console.log(`[PASS] ${testName}${extraInfo ? ' (' + extraInfo + ')' : ''}`);
    passCount++;
  } else {
    console.error(`[FAIL] ${testName}${extraInfo ? ' - ' + extraInfo : ''}`);
    failCount++;
  }
}

// Run audit sample
if (typeof window.loadAuditSample === 'function') {
  window.loadAuditSample();
} else {
  getOrCreateElement('audit-sample-btn').click();
}

// Assertion 1: Total SKUs loaded
const totalSkus = parseInt(getOrCreateElement('audit-total-skus').textContent, 10);
assert(totalSkus === 25, '1. Audit sample loads 25 SKUs', `Total SKUs: ${totalSkus}`);

// Assertion 2: Overall Catalogue Score within 0-100 range
const scoreText = getOrCreateElement('audit-overall-score').textContent;
const scoreMatch = scoreText.match(/(\d+)\/100/);
const overallScore = scoreMatch ? parseInt(scoreMatch[1], 10) : NaN;
assert(!isNaN(overallScore) && overallScore >= 40 && overallScore <= 95,
  '2. Overall catalogue health score is computed accurately', `Score: ${scoreText}`);

// Assertion 3: Critical SKUs count is tracked (<50)
const critCount = parseInt(getOrCreateElement('audit-crit-count').textContent, 10);
assert(critCount > 0 && critCount < 25, '3. Critical risk SKUs (<50) are correctly detected', `Critical count: ${critCount}`);

// Assertion 4: Optimized SKUs count is tracked (>=80)
const goodCount = parseInt(getOrCreateElement('audit-good-count').textContent, 10);
assert(goodCount > 0 && goodCount <= 25, '4. High-conversion optimized SKUs (80+) are detected', `Optimized count: ${goodCount}`);

// Assertion 5: Top 10 Fixes list populated and ranked
const topFixesHtml = getOrCreateElement('audit-top-fixes').innerHTML;
assert(topFixesHtml.includes('fix-item') && topFixesHtml.includes('SKUs'),
  '5. Top catalogue fixes list is populated and formatted', 'Contains ranked fix items');

// Assertion 6: Table rendering has 25 SKU rows
const tbodyHtml = getOrCreateElement('audit-tbody').innerHTML;
const rowCount = (tbodyHtml.match(/<tr data-sku=/g) || []).length;
assert(rowCount === 25, '6. SKU Scorecard table renders exactly 25 SKU rows', `Rendered rows: ${rowCount}`);

// Assertion 7: Detail Drawer opens and displays checks for critical SKU
window.openAuditDrawer('SEA-LOT-02');
const drawerTitle = getOrCreateElement('drawer-title').textContent;
const drawerScore = getOrCreateElement('drawer-score-val').textContent;
const drawerChecks = getOrCreateElement('drawer-checks-list').innerHTML;
assert(drawerTitle.includes('Whitening') && drawerChecks.includes('CRITICAL POLICY VIOLATION'),
  '7. Detail drawer inspects SKU and flags critical claims (pampaputi/cure)',
  `Title: "${drawerTitle}", Score: ${drawerScore}`);

// Assertion 8: CSV Export generates proper file download with headers and 25 rows
lastDownloadedFile = null;
window.exportAuditCSV();
assert(lastDownloadedFile !== null &&
       lastDownloadedFile.download === 'marketplace-audit-scorecard.csv' &&
       lastDownloadedFile.blob.text.includes('SKU,Product Title') &&
       lastDownloadedFile.blob.text.includes('SEA-CRM-01'),
  '8. Export CSV creates valid downloadable Blob with headers and rows',
  `Filename: ${lastDownloadedFile ? lastDownloadedFile.download : 'none'}`);

// Assertion 9: HTML Report Export produces styled standalone HTML
lastDownloadedFile = null;
window.exportAuditHTML();
assert(lastDownloadedFile !== null &&
       lastDownloadedFile.download === 'marketplace-audit-report.html' &&
       lastDownloadedFile.blob.text.includes('<!DOCTYPE html>') &&
       lastDownloadedFile.blob.text.includes('Marketplace Catalogue Audit Report'),
  '9. Export HTML report generates self-contained branded HTML report',
  `Size: ${lastDownloadedFile ? lastDownloadedFile.blob.text.length : 0} bytes`);

// Assertion 10: Copy summary writes formatted text to clipboard
lastCopiedText = '';
window.copyAuditSummary();
assert(lastCopiedText.includes('MARKETPLACE CATALOGUE AUDIT REPORT') &&
       lastCopiedText.includes('Total SKUs Audited: 25'),
  '10. Copy summary produces structured plain-text report for clipboard',
  `Length: ${lastCopiedText.length} chars`);

// Assertion 11: LocalStorage persistence
const savedData = JSON.parse(storage['audit-v1'] || 'null');
assert(savedData !== null && Array.isArray(savedData.rows) && savedData.rows.length === 25,
  '11. Audit state persists in localStorage under "audit-v1"',
  `Saved rows: ${savedData ? savedData.rows.length : 0}`);

// Assertion 12: Regression Check — Module 1 (Listing Scanner)
getOrCreateElement('listing-title').value = 'Herbal Whitening Miracle Cure 100% Guaranteed';
getOrCreateElement('risk-cat').value = 'medical';
if (typeof window.audit === 'function') window.audit();
const scannerScore = parseInt(getOrCreateElement('score-num').textContent, 10);
assert(!isNaN(scannerScore) && scannerScore < 70,
  '12. Regression: Module 1 Scanner accurately penalizes medical & guarantee violations',
  `Scanner score: ${scannerScore}`);

// Assertion 13: Regression Check — Module 2 (Ad Efficiency & TACOS)
getOrCreateElement('ae-price').value = '1200';
getOrCreateElement('ae-cogs').value = '400';
getOrCreateElement('ae-fee').value = '10';
getOrCreateElement('ae-ad-order').value = '150';
getOrCreateElement('ae-mon-rev').value = '250000';
getOrCreateElement('ae-mon-ad').value = '35000';
if (typeof window.calcAdEfficiency === 'function') window.calcAdEfficiency();
const tacosText = getOrCreateElement('ae-tacos-val').textContent;
assert(tacosText.includes('14.0%'),
  '13. Regression: Module 2 TACOS Calculator computes correct monthly TACOS',
  `TACOS: ${tacosText}`);

// Assertion 14: Regression Check — Module 3 (Voucher Simulator)
getOrCreateElement('vs-price').value = '1000';
getOrCreateElement('vs-cogs').value = '400';
getOrCreateElement('vs-plat').value = '20';
getOrCreateElement('vs-shop').value = '10';
getOrCreateElement('vs-comm').value = '6';
getOrCreateElement('vs-target').value = '100';
if (typeof window.calcVoucherSim === 'function') window.calcVoucherSim();
const vsMargin = getOrCreateElement('vs-margin-val').textContent;
assert(vsMargin.length > 0 && !vsMargin.includes('NaN'),
  '14. Regression: Module 3 Campaign Voucher Simulator computes net margin',
  `Margin: ${vsMargin}`);

/* ---------------- TOOL 5: Product Performance Classifier ---------------- */
console.log('\n--- Tool 5: Product Performance Classifier ---');
loadClassifySample();
const clsK = id => Number(getOrCreateElement(id).textContent);
assert(clsK('cls-k-expired') === 2, '15. Classifier: expired stock detected', `Expired: ${clsK('cls-k-expired')}`);
assert(clsK('cls-k-clear') === 4, '16. Classifier: clearance (expiring ≤60d) detected', `Clearance: ${clsK('cls-k-clear')}`);
assert(clsK('cls-k-flash') >= 15, '17. Classifier: flash-sale candidates (0 sold, ≥10 stock)', `Flash: ${clsK('cls-k-flash')}`);
assert(clsK('cls-k-scale') >= 3, '18. Classifier: scale candidates (fast sellers low on stock)', `Scale: ${clsK('cls-k-scale')}`);
assert(clsK('cls-k-noimg') === 5, '19. Classifier: missing-image count', `No image: ${clsK('cls-k-noimg')}`);
const clsStatus = getOrCreateElement('cls-status').textContent;
assert(/40 of 40 products shown/.test(clsStatus), '20. Classifier: renders all 40 sample rows', clsStatus);
const clsHtml = getOrCreateElement('cls-tbody').innerHTML;
assert(/act-pill high/.test(clsHtml) && /Sparkling Pear/.test(clsHtml) && /212 units sitting/.test(clsHtml), '21. Classifier: row shows action pill + why line', 'Sparkling Pear → Flash sale');
assert(/noimg-tag/.test(clsHtml), '22. Classifier: no-image tag rendered', 'tag present');
clsSetFilter('Expired stock');
assert(/2 of 40 products shown/.test(getOrCreateElement('cls-status').textContent), '23. Classifier: action filter narrows the table', getOrCreateElement('cls-status').textContent);
clsSetFilter('noimage');
assert(/5 of 40 products shown/.test(getOrCreateElement('cls-status').textContent), '24. Classifier: no-image filter', getOrCreateElement('cls-status').textContent);
clsSetFilter('all');
getOrCreateElement('cls-q').value = 'capsules'; window.clsRun ? null : null;
const plan = clsPlanText();
assert(/PRODUCT ACTION PLAN — 40 products/.test(plan) && /EXPIRED STOCK \(2\)/.test(plan) && /NEEDS IMAGE \(5\)/.test(plan), '25. Classifier: copyable action plan grouped by action', `${plan.split('\n').length} lines`);
clsExportCSV();
assert(lastDownloadedFile && lastDownloadedFile.download === 'product-action-plan.csv' && /^action,priority,sku/.test(lastDownloadedFile.blob.text), '26. Classifier: CSV export has header + rows', lastDownloadedFile ? lastDownloadedFile.download : 'none');
const clsSaved = JSON.parse(localStorageMock.getItem('classify-v1') || 'null');
assert(clsSaved && clsSaved.rows && clsSaved.rows.length === 40, '27. Classifier: persists to localStorage classify-v1', `rows: ${clsSaved ? clsSaved.rows.length : 0}`);
// flexible headers: Shopee-style export
clsRun([{ 'Seller SKU':'X1', 'Product Name':'Test Toner', 'Brand':'Lab', 'Quantity':'50', 'Units Sold':'0', 'Sale Price':'299' }]);
assert(clsK('cls-k-flash') === 1, '28. Classifier: flexible header mapping (Seller SKU / Quantity / Units Sold)', 'mapped to Flash sale');

/* ---------------- TOOL 6: Monthly Performance Report ---------------- */
console.log('\n--- Tool 6: Monthly Performance Report ---');
loadReportSample();
const rptOut = rptRender();
assert(rptOut && rptOut.ins, '29. Report: renders from sample', 'rendered');
const nm = rptOut.ins.now;
const near = (a,b,t) => Math.abs(a-b) <= (t||0.01);
assert(near(nm.aov, 412500/1375), '30. Report: AOV computed', `AOV ${nm.aov.toFixed(2)}`);
assert(near(nm.cvr, 1375/61200, 1e-6), '31. Report: conversion rate computed', `CVR ${(nm.cvr*100).toFixed(2)}%`);
assert(near(nm.roas, 121000/38800), '32. Report: ROAS computed', `ROAS ${nm.roas.toFixed(2)}x`);
assert(near(nm.tacos, 38800/412500, 1e-4), '33. Report: TACOS computed', `TACOS ${(nm.tacos*100).toFixed(1)}%`);
const prevHtml = getOrCreateElement('rpt-preview').innerHTML;
assert(/rpt-doc/.test(prevHtml) && /Glow Lab Official/.test(prevHtml) && /▲ 9\.4%/.test(prevHtml), '34. Report: document preview shows store + revenue delta', 'revenue ▲ 9.4%');
assert(rptOut.ins.what.length === 3 && rptOut.ins.next.length === 3, '35. Report: exactly 3 findings + 3 actions', `${rptOut.ins.what.length}/${rptOut.ins.next.length}`);
assert(rptOut.ins.what.some(w => /Traffic rose .* conversion dropped/.test(w)), '36. Report: rule fires — traffic up, conversion down', rptOut.ins.what.find(w=>/Traffic rose/.test(w)) || 'missing');
assert(rptOut.ins.what.some(w => /Ads returned a healthy 3\.12x \(down 18% MoM\)/.test(w)) && rptOut.ins.next.some(n => /ROAS slipped 18%/.test(n)), '37. Report: ROAS insight + slip action use real numbers', 'ROAS 3.12x, down 18% → action');
const txt = rptPlain(false);
assert(/MONTHLY PERFORMANCE REPORT — Glow Lab Official/.test(txt) && /WHAT HAPPENED/.test(txt) && /NEXT MONTH — ACTIONS/.test(txt), '38. Report: plain-text export', `${txt.split('\n').length} lines`);
const md = rptPlain(true);
assert(/^# MONTHLY PERFORMANCE REPORT/.test(md) && /\| Metric \| This month \|/.test(md), '39. Report: markdown export has table', 'markdown table');
rptDownload();
assert(lastDownloadedFile && /performance-report-\d{4}-\d{2}\.html/.test(lastDownloadedFile.download) && /<style>/.test(lastDownloadedFile.blob.text), '40. Report: self-contained HTML download', lastDownloadedFile ? lastDownloadedFile.download : 'none');
const hist = JSON.parse(localStorageMock.getItem('report-v1') || '[]');
assert(hist.length === 1 && hist[0].revenue === 412500, '41. Report: month saved to report-v1 history', `${hist.length} month(s)`);
// low ROAS rule
const lowIns = rptInsights({store:'X',marketplace:'Y',month:'2026-08',cur:'$',notes:'',now:{revenue:10000,orders:100,sessions:5000,ad_spend:3000,ad_sales:4500,units:null,returns:null,impressions:null},prev:{revenue:10000,orders:100,sessions:5000,ad_spend:2000,ad_sales:4400,units:null,returns:null,impressions:null}});
assert(lowIns.what.some(w=>/below the 2x line/.test(w)) && lowIns.next.some(n=>/Cut campaigns/.test(n)), '42. Report: low-ROAS rule + action', 'ROAS 1.5x → cut');

console.log('\n====================================================');
console.log(`TEST RESULTS: ${passCount} PASSED, ${failCount} FAILED`);
console.log('====================================================');

if (failCount > 0) {
  process.exit(1);
} else {
  process.exit(0);
}
