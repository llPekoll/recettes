from playwright.sync_api import Playwright, sync_playwright, expect, Page
import lorem
import os


def create_recipe(page: Page) -> None:
    page.locator('[data-test="create-recipe"]').click()
    page.locator('[data-test="title"]').fill("My recipe")
    handle = page.query_selector('[data-test="category"]')
    handle.select_option(label="Garden")
    page.locator('[data-test="description"]').fill(lorem.paragraph())
    image_path = os.path.abspath("playwright_tests/lib/fixtures/images/bf.jpg")
    page.locator('[data-test="image-desc"]').set_input_files(image_path)
    handle = page.query_selector('[data-test="origin"]')
    handle.select_option(label="Asia")
    page.locator('[data-test="duration-input"]').fill("2.5")
    handle = page.query_selector('[data-test="duration-select"]')
    handle.select_option(label="Minute")
    page.locator('[data-test="quantity"]').fill("2.5")
    handle = page.query_selector('[data-test="unit"]')
    handle.select_option(label="Spoon")
    page.locator('[data-test="ingredient_name"]').fill("citron")
    page.locator('[data-test="add-ingredient"]').click()
