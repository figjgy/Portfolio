// Harness for the site assistant's retrieval brain.
// Pulls the real KB + scoring code out of the BUILT page and asks it questions,
// so what is tested is exactly what ships.
const fs = require('fs');
const html = fs.readFileSync('site/index.html', 'utf8');

const start = html.indexOf('var KB=[');
const end   = html.indexOf('var CHIPS=');
if (start < 0 || end < 0) { console.error('FAIL: could not find the brain in the built page'); process.exit(1); }
let code = html.slice(start, end);
code = code.replace(/'%\(up\)s'/g, "''");           // build-time token
const sandbox = {};
new Function('sandbox', code + '\nsandbox.score=score;sandbox.kbAnswer=kbAnswer;sandbox.KB=KB;')(sandbox);

const cases = [
  ['what did you do for margegold',        'margegold-jewelry'],
  ['tell me about the kpick website',      'kpick-website'],
  ['do you do 3d renders',                 null],
  ['exhibit booth',                        'philmed-expo-2026'],
  ['who is kibo',                          'kibo'],
  ['telegram bot',                         null],
  ['ads for foreign clients',              'ads-creatives'],
  ['anong ginawa mo sa shopee',            null],
  ['may video editing ka ba',              null],
  ['what is your education',               'b:education'],
  ['sino ka',                              'x:who'],
  ['content calendar',                     'content-calendar-system'],
  ['tarpaulin printing',                   'banners-tarpaulins'],
  ['sungshim korean supplier sourcing',    'brand-sourcing'],
  ['what do people say about you',         null],
];

let pass = 0, soft = 0;
console.log('QUESTION'.padEnd(38), 'MATCHED');
console.log('-'.repeat(86));
for (const [q, want] of cases) {
  const hit = sandbox.score(q);
  const got = hit ? hit.doc.id : '(no match -> falls back to keywords)';
  const ok  = want ? got.includes(want) : !!hit;
  if (ok) pass++; else soft++;
  console.log(q.padEnd(38), (ok ? '  ' : 'x ') + got + (hit ? '  score ' + hit.score.toFixed(1) : ''));
}

// things that must NOT be answered from the KB - they are "do something" intents
const mustMiss = ['how much do you charge', 'magkano', 'can i talk to jamie', 'i want to hire you'];
console.log('\nThese must fall through to the intent rules (price / contact):');
for (const q of mustMiss) {
  const hard = /rate|price|cost|quote|how much|magkano|presyo|budget|hire|start|begin|book|whats ?app|contact|talk to|email|message you/i.test(q);
  console.log('  ' + (hard ? 'ok  ' : 'X   ') + q);
  if (hard) pass++; else soft++;
}
console.log('\n' + pass + ' ok, ' + soft + ' to look at');
