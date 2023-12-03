from playwright.sync_api import Playwright, sync_playwright, expect


def register(page, username: str, password: str, email: str) -> None:
    page.goto("http://localhost:8000/en/")
    page.locator('[data-test="register"]').click()
    page.locator('[data-test="username"]').fill(username)
    page.locator('[data-test="email"]').fill(email)
    page.locator('[data-test="password1"]').fill(password)
    page.locator('[data-test="password2"]').fill(password)
    page.locator('[data-test="submit"]').click()
    expect(page.locator('[data-test="profile-icon"]')).to_be_visible()
