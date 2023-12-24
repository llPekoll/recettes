from playwright.sync_api import Playwright, sync_playwright, expect, Page
import lorem
import os
from pydantic import BaseModel
import time


class Ingredient(BaseModel):
    quantity: str
    unit: str
    name: str


class Step(BaseModel):
    title: str


image_path = os.path.abspath("playwright_tests/lib/fixtures/images/bf.jpg")

ings = [
    Ingredient(quantity="2.5", unit="Spoon", name="citron"),
    Ingredient(quantity="1", unit="Liter", name="citron"),
    Ingredient(quantity="5", unit="Kilograme", name="Chocolate"),
    Ingredient(quantity="90", unit="Piece", name="oigons"),
]

steps = [
    Step(title="Melanger"),
    Step(title="astiquer"),
    Step(title="malaxer"),
    Step(title="manger"),
]


def add_ingredient(page: Page, quantity: str, unit: str, name: str) -> None:
    page.locator('[data-test="quantity"]').focus()
    page.locator('[data-test="quantity"]').fill(quantity)
    handle = page.query_selector('[data-test="unit"]')
    handle.select_option(label=unit)
    page.locator('[data-test="ingredient_name"]').fill(name)
    page.locator('[data-test="add-ingredient"]').click()
    expect(page.locator(f'[data-test="ing-{name}"]')).to_be_visible()


def add_step(page: Page, title: str) -> None:
    page.locator('[data-test="title-step"]').focus()
    page.locator('[data-test="title-step"]').fill(title)
    page.locator("#quill-id_instruction div").first.fill(lorem.paragraph())
    page.locator('[data-test="image-step"]').set_input_files(image_path)
    page.locator('[data-test="add-step"]').click()
    expect(page.locator(f'[data-test="step-{title}"]')).to_be_visible()


def create_recipe(page: Page, basic: bool, create: bool, publish: bool) -> None:
    if create:
        page.locator('[data-test="create-recipe"]').click()

    page.locator('[data-test="title"]').fill("My recipe")
    page.locator('[data-test="description"]').fill(lorem.paragraph())

    if not basic:
        handle = page.query_selector('[data-test="category"]')
        handle.select_option(label="Garden")
        page.locator('[data-test="image-desc"]').set_input_files(image_path)
        handle = page.query_selector('[data-test="origin"]')
        handle.select_option(label="Asia")
        page.locator('[data-test="duration-input"]').fill("2.5")
        handle = page.query_selector('[data-test="duration-select"]')
        handle.select_option(label="Minutes")

        for ing in ings:
            add_ingredient(page, ing.quantity, ing.unit, ing.name)
            time.sleep(1)

        for step in steps:
            add_step(page, step.title)
            time.sleep(1)

        # add tags add links
        page.locator("tags").get_by_role("textbox").click()
        page.locator("tags").get_by_role("textbox").fill("victorine")
        page.locator("tags").get_by_role("textbox").press("Tab")
        page.locator("tags").get_by_role("textbox").fill("j'y peux rien")
        page.locator("tags").get_by_role("textbox").press("Tab")
        page.locator("tags").get_by_role("textbox").fill("je suis comme ça")
        page.locator("tags").get_by_role("textbox").press("Tab")

    if publish:
        page.locator('[data-test="is_published"]').click()
    page.locator('[data-test="submit"]').click()
