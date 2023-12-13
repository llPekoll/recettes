from playwright.sync_api import Playwright, sync_playwright, expect, Page

from .create_recipe import create_recipe


def edit_recipe(page: Page) -> None:
    page.locator('[data-test="edit-recipe"]').click()
    create_recipe(page, False, False, True)
