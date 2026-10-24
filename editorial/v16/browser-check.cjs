const {chromium}=require('playwright');
const fs=require('fs');
const path=require('path');
(async()=>{
 const root=path.resolve(__dirname,'../..');
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||'/usr/bin/chromium',args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1360,height:1000}});const errors=[];await page.route('**/account-config.json',r=>r.fulfill({json:{enabled:false}}));page.on('pageerror',e=>errors.push(String(e)));
 await page.goto('http://127.0.0.1:4173/?course=maths&stage=P1',{waitUntil:'networkidle'});
 await page.locator('[data-only-chapter="7"]').click();
 await page.waitForSelector('.question-card');
 const ids=[];let pages=0;
 do{
  pages++;ids.push(...await page.locator('.question-card').evaluateAll(es=>es.map(e=>e.dataset.qid)));
  for(const button of await page.locator('.answer-toggle').all())await button.click();
  for(const detail of await page.locator('.answer-source-details').all())await detail.evaluate(e=>e.open=true);
  await page.waitForFunction(()=>[...document.querySelectorAll('.rewrite-figure img')].every(i=>i.complete&&i.naturalWidth>0));
  if(await page.locator('.katex-error').count())throw Error('KaTeX error');
  if(pages===1)await page.screenshot({path:path.join(root,'editorial/v16/browser-desktop.png'),fullPage:false});
  const next=page.locator('[data-action="next"]');if(await next.isDisabled())break;
  await next.click();
 }while(pages<10);
 if(ids.length!==21||new Set(ids).size!==21)throw Error('chapter pool: '+JSON.stringify(ids));
 if(ids.some(id=>['15','27','35','36'].some(n=>id===`P1-C07-R${n}`)))throw Error('withdrawn question in practice');
 // A real one-part question used to fail bank validation. Verify it loads and opens in the UI.
 await page.goto('http://127.0.0.1:4173/?course=maths&stage=P1&q=P1-C07-R25',{waitUntil:'networkidle'});
 await page.waitForSelector('#card-P1-C07-R25');await page.locator('.answer-toggle').click();
 await page.setViewportSize({width:390,height:844});
 await page.screenshot({path:path.join(root,'editorial/v16/browser-mobile.png'),fullPage:true});
 const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);if(overflow)throw Error('mobile horizontal overflow');
 if(errors.length)throw Error(errors.join('\n'));
 fs.writeFileSync(path.join(root,'editorial/v16/browser-checks.json'),JSON.stringify({status:'passed',mode:'local-only config intercepted in test browser; production auth unchanged',chapterPool:ids,pages,mathErrors:0,pageErrors:errors,mobileHorizontalOverflow:overflow,onePartQuestion:'P1-C07-R25'},null,2)+'\n');
 await browser.close();console.log('PASS browser: all 21 chapter questions, answers and figures; one-part question; mobile layout');
})().catch(e=>{console.error(e);process.exit(1)});
