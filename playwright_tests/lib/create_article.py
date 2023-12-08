from playwright.sync_api import Playwright, sync_playwright, expect, Page
import lorem
import os
from pydantic import BaseModel
import time


image_path = os.path.abspath("playwright_tests/lib/fixtures/images/bf.jpg")


def create_article(page: Page) -> None:
    page.locator('[data-test="create-article"]').click()
    page.locator('[data-test="title"]').fill("My article")
    page.locator("#quill-id_content div").first.fill(lorem.paragraph())
    page.locator('[data-test="image"]').set_input_files(image_path)

    # add tags add links
    page.locator("tags").get_by_role("textbox").click()
    page.locator("tags").get_by_role("textbox").fill("victorine")
    page.locator("tags").get_by_role("textbox").press("Tab")
    page.locator("tags").get_by_role("textbox").fill("j'y peux rien")
    page.locator("tags").get_by_role("textbox").press("Tab")
    page.locator("tags").get_by_role("textbox").fill("je suis comme ça")
    page.locator("tags").get_by_role("textbox").press("Tab")

    page.locator('[data-test="is_published"]').click()
    page.locator('[data-test="submit"]').click()
