from playwright.sync_api import expect, Page
import time


def delete_recipe(page: Page) -> None:
    page.locator('[data-test="delete-recipe"]').click()
    time.sleep(1)
    page.locator(".swal2-confirm").click()
    expect(page.locator('[data-test="profile-icon"]')).to_be_visible()
