import feedparser
from playwright.sync_api import sync_playwright


def fetch_news():
    feed = feedparser.parse("https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en")
    return feed.entries[:5]


def format_tweet(articles):
    tweet = "Top 5 News in India\n\n"
    for i, a in enumerate(articles, 1):
        tweet += f"{i}. {a.title[:80]}\n{a.link}\n\n"
    return tweet[:280]


def post_tweet(tweet_text):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )

        context = browser.new_context(
            storage_state="auth.json",
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        )

        # Patch webdriver detection
        context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        page = context.new_page()

        # Go to home first to verify session is valid
        print("Navigating to x.com home...")
        page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)

        current_url = page.url
        print(f"Current URL: {current_url}")

        if "login" in current_url or "i/flow" in current_url:
            browser.close()
            raise Exception(
                "Session expired or invalid. Re-run setup_auth.py and update AUTH_JSON secret."
            )

        print("Session valid. Opening compose tweet...")

        # Click the compose/tweet button on the home timeline
        page.click('a[href="/compose/tweet"]', timeout=10000)
        page.wait_for_timeout(2000)

        # Type the tweet
        textbox = page.locator('div[data-testid="tweetTextarea_0"]')
        textbox.wait_for(timeout=10000)
        textbox.click()
        textbox.type(tweet_text, delay=30)
        page.wait_for_timeout(1000)

        # Click Post button
        page.click('button[data-testid="tweetButton"]', timeout=10000)
        page.wait_for_timeout(3000)

        print("Tweet posted successfully!")
        browser.close()


if __name__ == "__main__":
    news = fetch_news()
    tweet = format_tweet(news)
    print("Tweet to be posted:\n")
    print(tweet)
    post_tweet(tweet)
    print("Done!")
