from playwright.sync_api import Playwright, sync_playwright, expect
from playwright.sync_api import Page
import time


def delete_account(page: Page) -> None:
    page.locator('[data-test="profile-icon"]').click()
    page.locator('[data-test="my-profile"]').click()
    page.locator('[data-test="delete-account"]').click()
    time.sleep(1)
    page.locator('input[data-test="delete-input"][type="text"]').fill(
        "I want to delete"
    )
    page.locator(".swal2-confirm").click()
    expect(page.locator('[data-test="login"]')).to_be_visible()
