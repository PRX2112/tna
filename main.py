import feedparser
from playwright.sync_api import sync_playwright


def fetch_news():
    feed = feedparser.parse("https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en")
    return feed.entries[:5]


def format_tweet(articles):
    tweet = "Top 5 News in India 🇮🇳\n\n"
    for i, a in enumerate(articles, 1):
        tweet += f"{i}. {a.title[:80]}\n{a.link}\n\n"
    return tweet[:280]


def post_tweet(tweet_text):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Load saved login session
        context = browser.new_context(storage_state="auth.json")
        page = context.new_page()

        page.goto("https://twitter.com/compose/tweet")
        page.wait_for_timeout(5000)

        page.fill('div[role="textbox"]', tweet_text)
        page.click('div[data-testid="tweetButtonInline"]')

        page.wait_for_timeout(5000)
        browser.close()


if __name__ == "__main__":
    news = fetch_news()
    tweet = format_tweet(news)
    print("Tweet to be posted:\n")
    print(tweet)
    post_tweet(tweet)
    print("\n✅ Tweet posted successfully!")
