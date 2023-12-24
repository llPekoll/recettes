from playwright.sync_api import expect, Page
import time


def delete_article(page: Page) -> None:
    page.locator('[data-test="delete-article"]').click()
    time.sleep(1)
    page.locator(".swal2-confirm").click()
    expect(page.locator('[data-test="profile-icon"]')).to_be_visible()
