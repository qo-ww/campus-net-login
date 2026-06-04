#!/usr/bin/python3
"""
校园网自动联网 - 农职大
读取 配置.txt 中的账号信息，自动登录校园网
"""
import time, os, sys, requests
from datetime import datetime
from playwright.sync_api import sync_playwright

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---- 读取配置 ----
CFG_FILE = os.path.join(SCRIPT_DIR, "配置.txt")
USER = ""; PASS = ""; ISP = "@telecom"
if os.path.exists(CFG_FILE):
    with open(CFG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or "=" not in line: continue
            k, v = line.split("=", 1)
            k = k.strip(); v = v.strip().split("#")[0].strip()
            if k == "学号": USER = v
            elif k == "密码": PASS = v
            elif k == "运营商":
                v = v.replace("电信","@telecom").replace("联通","@unicom").replace("移动","@cmcc").replace("校园网","@campus")
                ISP = v

if not USER or not PASS:
    print("错误：请先编辑 配置.txt 填入学号和密码！")
    input("按回车退出...")
    sys.exit(1)

USERNAME = USER + ISP
LOG_FILE = os.path.join(SCRIPT_DIR, "network.log")
LOGIN_API = "http://10.10.10.2:801/eportal/?c=ACSetting&a=Login&url=drappal"
PORTAL_URL = "http://10.10.10.2/"
CHECK_URL = "http://www.baidu.com"
CHECK_INTERVAL = 5
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
HEADLESS = "--show" not in sys.argv

def log(msg):
    now = datetime.now().strftime("%H:%M:%S")
    line = "[%s] %s" % (now, msg)
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except: pass

def is_online():
    try:
        r = requests.get(CHECK_URL, timeout=5, allow_redirects=True)
        if "10.10.10.2" in r.url.lower() or "eportal" in r.url.lower():
            return False
        return r.status_code == 200 and len(r.text) > 500
    except: return False

def api_login():
    data = {"DDDDD": USERNAME, "upass": PASS, "R1": "0", "R2": "0", "R3": "3",
            "R6": "0", "para": "00", "0MKKey": "123456", "v6ip": ""}
    try:
        r = requests.post(LOGIN_API, data=data, timeout=15)
        log("API: " + str(r.status_code))
        return True
    except Exception as e:
        log("API err: " + str(e)[:60])
        return False

def browser_login():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="msedge", headless=HEADLESS, executable_path=EDGE_PATH)
            page = browser.new_page(viewport={"width": 640, "height": 960})
            page.goto(PORTAL_URL, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(6000)
            body = page.inner_text("body")
            if "注销" in body:
                page.evaluate("wc()")
                page.wait_for_timeout(2000)
                page.evaluate("""() => { document.querySelectorAll('a').forEach(a => { if ((a.innerText||'').trim()==='\u786e\u5b9a') a.click(); }); }""")
                page.wait_for_timeout(8000)
            page.evaluate("""([u, p, isp]) => {
                let un = document.querySelector('input[name="DDDDD"]');
                if (un) { un.value = u; un.dispatchEvent(new Event('input',{bubbles:true})); }
                let pw = document.querySelector('input[name="upass"]');
                if (pw) { pw.value = p; pw.dispatchEvent(new Event('input',{bubbles:true})); }
                let s = document.querySelector('select[name="ISP_select"]');
                if (s) { s.value = isp; s.dispatchEvent(new Event('change',{bubbles:true})); }
            }""", [USER, PASS, ISP])
            page.wait_for_timeout(500)
            btn = page.query_selector('input[value="登录"]')
            if btn: btn.click(force=True)
            else: page.evaluate("ee(1)")
            page.wait_for_timeout(10000)
            browser.close()
            return True
    except Exception as e:
        log("Browser err: " + str(e)[:80])
        return False

def do_login():
    api_login()
    time.sleep(4)
    if is_online(): return
    browser_login()
    time.sleep(4)

def main():
    log("=" * 30)
    log("Campus Auto Login | " + USERNAME)
    if not is_online():
        do_login()
    fail_count = 0; cooldown = 0
    while True:
        if cooldown > 0: cooldown -= CHECK_INTERVAL
        if is_online():
            if fail_count > 0: fail_count = 0; cooldown = 0
        else:
            fail_count += 1
            if cooldown <= 0: do_login(); cooldown = 60
            else: log("OFFLINE (cooldown %ds)" % cooldown)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()