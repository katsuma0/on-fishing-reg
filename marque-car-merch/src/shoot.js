// Rasterize an HTML or SVG file to PNG via the on-disk Chromium.
// usage: node shoot.js <input> <output> [width height]   (fullPage if no w/h)
const { chromium } = require('playwright');
const path = require('path');

const EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

(async () => {
  const [,, input, output, w, h] = process.argv;
  const abs = path.resolve(input);
  const browser = await chromium.launch({ executablePath: EXE, args: ['--no-sandbox'] });
  const viewport = (w && h) ? { width: +w, height: +h } : { width: 1400, height: 1000 };
  const page = await browser.newPage({ viewport, deviceScaleFactor: 2 });
  await page.goto('file://' + abs, { waitUntil: 'load', timeout: 15000 });
  try { await page.evaluate(() => document.fonts && document.fonts.ready); } catch (e) {}
  await page.waitForTimeout(300);
  await page.screenshot({ path: output, fullPage: !(w && h) });
  await browser.close();
  console.log('shot', output);
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
