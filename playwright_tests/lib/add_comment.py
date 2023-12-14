from playwright.sync_api import expect, Page
import lorem


def add_comment(page: Page) -> None:
    page.locator('[data-test="input-comment"]').fill(lorem.paragraph())
    page.locator('[data-test="add-comment"]').click()
    comment_elements = page.locator('[data-test^="comment-"]')
    assert comment_elements.count() > 0, "No comments found"
