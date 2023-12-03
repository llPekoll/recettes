from playwright.sync_api import Playwright, sync_playwright, expect


def login(page, username: str, password: str) -> None:
    page.goto("http://localhost:8000/en/")
    page.locator('[data-test="login"]').click()
    page.locator('[data-test="username"]').fill(username)
    page.locator('[data-test="password"]').fill(password)
    page.locator('[data-test="submit"]').click()
    expect(page.locator('[data-test="profile-icon"]')).to_be_visible()
