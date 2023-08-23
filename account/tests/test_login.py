from playwright.sync_api import Page, expect
from .test_register import create_user


def test_login_valid(page: Page):
    create_user(page)
    page.goto("http://127.0.0.1:8000/")
    page.locator('[data-test="profile"]').click()
    page.locator('[data-test="logout"]').click()
    page.wait_for_timeout(1000)
    page.locator('[data-test="logout"]').click()
    page.locator('[data-test="login"]').click()
