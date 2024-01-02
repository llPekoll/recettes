from playwright.sync_api import Playwright, sync_playwright, expect, Page
import time

def post_report(page: Page) -> None:
    page.locator('[data-test="report"]').click()
    time.sleep(1)
    page.locator(".swal2-confirm").click()
    page.locator(".swal2-confirm").click()

