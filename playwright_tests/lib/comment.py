from playwright.sync_api import Playwright, sync_playwright, expect, Page
import lorem

def add_comment(page: Page) -> None:
    page.locator("#quill-id_comment div").first.fill(lorem.paragraph())
    page.locator('[data-test="add-comment"]').click()


def delete_comment(page: Page) -> None:
    page.locator('[data-test="delete-comment"]').first()
