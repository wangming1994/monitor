from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).parent
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True)
    page = browser.new_page(viewport={'width':2400,'height':510}, device_scale_factor=1)
    errors=[]
    requests=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    page.on('request',lambda r: requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
    # This managed Chromium blocks file:// navigation via its enterprise policy.
    # Loading the exact file contents checks the self-contained document offline.
    page.set_content((ROOT/'index.html').read_text(),wait_until='networkidle')
    expect(page.get_by_role('heading', name='黑龙江省交易集团数智化大屏',exact=True)).to_be_visible()
    assert page.locator('.panel').count()==10
    assert page.locator('.china-map').count()==1
    expect(page.locator('#market-cells')).to_contain_text('走访对接数量')
    page.get_by_role('tab',name='财务指标',exact=True).click()
    expect(page.locator('#market-cells')).to_contain_text('预算完成率')
    page.get_by_role('tab',name='市场开拓',exact=True).click()
    expect(page.locator('#market-cells')).to_contain_text('走访对接数量')
    page.locator('.metric').first.hover()
    expect(page.locator('#tip')).to_be_visible()
    page.mouse.move(0,0)
    expect(page.locator('#tip')).not_to_be_visible()
    page.screenshot(path='/workspace/dashboard-wide.png')
    print('Panel overflow:',page.locator('.panel').evaluate_all('(els)=>els.map(e=>({name:e.querySelector("h2")?.textContent,height:e.clientHeight,scroll:e.scrollHeight})).filter(e=>e.scroll>e.height+3)'))
    for w,h in [(2048,431),(1440,900),(390,844)]:
        page.set_viewport_size({'width':w,'height':h})
        page.wait_for_timeout(100)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth && document.documentElement.scrollHeight<=innerHeight')
        box=page.locator('#board').bounding_box()
        assert box['width']<=w+1 and box['height']<=h+1
        if w==2048:page.screenshot(path='/workspace/dashboard-preview.png')
    assert not errors, errors
    assert not requests, requests
    browser.close()
    print('PASS: 10 panels, inline China SVG, both metric tabs, hover tooltip, responsive 2400/2048/1440/390 layouts; no runtime errors or network requests.')
