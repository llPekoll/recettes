from playwright.sync_api import Playwright, sync_playwright, expect, Page


def logout(page: Page) -> None:
    page.locator('[data-test="profile-icon"]').click()
    page.locator('[data-test="logout"]').click()
    expect(page.locator('[data-test="profile-icon"]')).not_to_be_visible()
