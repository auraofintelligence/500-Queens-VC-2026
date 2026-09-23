const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs');
const assert=require('node:assert/strict');
const base=process.env.SITE_BASE||'http://127.0.0.1:8768/';
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 const page=await browser.newPage({viewport:{width:390,height:844},acceptDownloads:true});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const pages=fs.readdirSync('.').filter(p=>p.endsWith('.html')&&p!=='404.html');
 for(const width of (process.argv.includes('--interactions-only')?[]:[390,1440])){
  await page.setViewportSize({width,height:900});
  for(const path of pages){
   const response=await page.goto(base+path,{waitUntil:'networkidle'});assert.equal(response.status(),200,path);
   await page.evaluate(async()=>{await Promise.all([...document.images].map(i=>{i.loading='eager';return i.decode().catch(()=>{});}));});
   const state=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,broken:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length,h1:document.querySelectorAll('h1').length}));
   assert.equal(state.overflow,false,`${path} overflows at ${width}`);assert.equal(state.broken,0,`${path} broken image at ${width}`);assert.equal(state.h1,1,path);
  }
  console.log(`PASS: ${pages.length} pages at ${width}px: no overflow, missing images or heading errors`);
 }
 await page.goto(base+'catalogue.html');
 assert.equal(await page.locator('[data-search]:visible').count(),120);
 await page.locator('#catalogue-search').fill('care');assert.ok(await page.locator('[data-search]:visible').count()>0);assert.ok(await page.locator('[data-search]:visible').count()<120);
 await page.locator('#catalogue-search').fill('zzz-no-match');assert.equal(await page.locator('[data-search]:visible').count(),0);assert.equal(await page.locator('.no-results').isVisible(),true);
 await page.locator('#catalogue-search').fill('');await page.locator('#catalogue-sector').selectOption({index:1});assert.ok(await page.locator('[data-search]:visible').count()>0);
 await page.goto(base+'references.html');assert.equal(await page.locator('[data-search]:visible').count(),27);await page.locator('#document-search').fill('planning');assert.equal(await page.locator('[data-search]:visible').count(),1);
 await page.goto(base+'ventures.html');assert.equal(await page.locator('[data-search]:visible').count(),18);await page.locator('#venture-search').fill('solar');assert.ok(await page.locator('[data-search]:visible').count()>0);
 await page.goto(base+'capital.html');assert.match(await page.locator('#budget-output').innerText(),/30,000,000/);await page.locator('#budget-intake').fill('200');assert.match(await page.locator('#budget-output').innerText(),/55,000,000/);await page.locator('#budget-setup').fill('250000');assert.match(await page.locator('#budget-output').innerText(),/55,250,000/);await page.locator('#budget-intake').fill('-1');assert.match(await page.locator('#budget-output').innerText(),/Check inputs/);await page.getByRole('button',{name:'Restore the 2021 guide'}).click();await page.waitForFunction(()=>document.querySelector('#budget-output').textContent.includes('30,000,000'));assert.match(await page.locator('#budget-output').innerText(),/30,000,000/);
 await page.goto(base+'join.html');await page.getByRole('button',{name:'Build an enterprise'}).click();assert.equal(await page.locator('#path-link').getAttribute('href'),'ventures.html');await page.locator('#interest-note').fill('I would like to explore community energy.');const [download]=await Promise.all([page.waitForEvent('download'),page.getByRole('button',{name:'Download my note'}).click()]);await download.saveAs('work/downloaded-note.txt');assert.ok(fs.readFileSync('work/downloaded-note.txt','utf8').includes('community energy'));
 await page.getByRole('button',{name:'Explore ☰'}).click();assert.equal(await page.locator('#explore-menu').isVisible(),true);await page.keyboard.press('Escape');assert.equal(await page.locator('#explore-menu').isVisible(),false);
 await page.emulateMedia({reducedMotion:'reduce'});assert.equal(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior),'auto');
 console.log('PASS: catalogue and project filters; 27 reference search; calculator inputs/reset; pathway choices; local note download; menu; reduced motion');
 await page.emulateMedia({reducedMotion:'no-preference'});
 for(const path of ['index','ai-queens','capital','join']){await page.setViewportSize({width:390,height:844});await page.goto(base+path+'.html',{waitUntil:'networkidle'});await page.screenshot({path:`work/${path}-phone-viewport.png`});}
 await page.setViewportSize({width:1440,height:1000});await page.goto(base+'index.html',{waitUntil:'networkidle'});await page.screenshot({path:'work/final-desktop-viewport.png'});
 assert.deepEqual(errors,[],'Browser errors');await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
