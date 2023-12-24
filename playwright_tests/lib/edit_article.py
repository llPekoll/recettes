from playwright.sync_api import expect, Page
import lorem
import os
import time


image_path = os.path.abspath("playwright_tests/lib/fixtures/images/bf.jpg")


def edit_article(page: Page) -> None:
    time.sleep(1)
    page.locator('[data-test="edit-article"]').click()
    page.locator('[data-test="title"]').fill("My Edited article")
    page.locator("#quill-id_content div").first.fill(f"Edited -> {lorem.paragraph()}")
    page.locator('[data-test="image"]').set_input_files(image_path)

    page.locator('[data-test="submit"]').click()
