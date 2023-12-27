from playwright.sync_api import Playwright, sync_playwright, expect, Page


def post_report(page: Page) -> None:
    page.locator('[data-test="post-report"]').click()

