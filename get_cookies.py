import asyncio
from playwright.async_api import async_playwright

URL = "https://trends.google.com/trends/"
OUTPUT_FILE = "google_trends_cookies.txt"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ],
        )
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(URL, wait_until="networkidle")

        cookies = await context.cookies()

        cookie_string = "; ".join(
            [f"{cookie['name']}={cookie['value']}" for cookie in cookies]
        )

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(cookie_string)

        print("Saved cookies to:", OUTPUT_FILE)
        print("Cookie string:")
        print(cookie_string)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
