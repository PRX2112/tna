"""
🔐 FIRST TIME SETUP — Run this script ONCE locally to generate auth.json
This saves your Twitter login session so the bot can post without re-logging in.
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://twitter.com/login")

    print("👉 Log in to Twitter manually in the browser window...")
    print("✅ Once logged in, come back here and press ENTER to save session.")
    input()

    context.storage_state(path="auth.json")
    browser.close()
    print("\n✅ auth.json saved! Upload it to your GitHub repo as a secret or file.")
