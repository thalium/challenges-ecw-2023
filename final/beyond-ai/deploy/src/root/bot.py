from playwright.sync_api import sync_playwright
from os.path import isfile, dirname, join
import subprocess

def getApplications():
    output = subprocess.run(['/root/database-interact.sh', '-s'], stdout=subprocess.PIPE)
    if output.stdout == b'':
        return []
    return output.stdout.decode().strip().split('\n') # ['3', '4']

def setSeen(id):
    subprocess.run(['/root/database-interact.sh', f'-u {id}'], stdout=subprocess.PIPE)
    return

def checkHosts():
    # in case the /etc/hosts file is overwritten, we add the hostname pointing to 127.0.0.1
    hosts = open('/etc/hosts', 'r').read()
    if target not in hosts :
        open('/etc/hosts', 'a').write(f'127.0.0.1 {target}')
    return

target = 'beyond-ai.ecw'
timeout = 3000
username = 'beyond-admin'
password = 'gEJ7fo%9LT1#7q#D3U'

checkHosts()
applications = getApplications()

if len(applications) > 0:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        context.set_default_timeout(timeout)
        page = context.new_page()
        page.goto(f'http://{target}/wp-login.php')
        page.locator('#user_login').fill(username)
        page.locator('#user_pass').fill(password)
        page.locator('#wp-submit').click()
        
        for id in applications:
            page.goto(f'http://{target}/?ai-recruitment&application={id}')
            page.wait_for_load_state('networkidle')
            setSeen(id)
        page.close()
else:
    print('[-] No applications...')
