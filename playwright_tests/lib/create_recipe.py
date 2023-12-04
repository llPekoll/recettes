from playwright.sync_api import Playwright, sync_playwright, expect, Page
import lorem
import os
from pydantic import BaseModel


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
    Ingredient(quantity="13", unit="Kilograme", name="Chocolate"),
    Ingredient(quantity="90", unit="Piece", name="oigons"),
]

steps = [
    Step(title="Melanger"),
    Step(title="astiquer"),
    Step(title="malaxer"),
    Step(title="manger"),
]


def add_ingredient(page: Page, quantity: str, unit: str, name: str) -> None:
    page.locator('[data-test="quantity"]').fill(quantity)
    handle = page.query_selector('[data-test="unit"]')
    handle.select_option(label=unit)
    page.locator('[data-test="ingredient_name"]').fill(name)
    page.locator('[data-test="add-ingredient"]').click()
    expect(page.locator(f'[data-test="ing-{name}"]')).not_to_be_visible()


def add_step(page: Page, title: str) -> None:
    page.locator('[data-test="title-step"]').fill(title)
    page.locator('[data-test="ingredient_name"]').fill(lorem.paragraph())
    page.locator('[data-test="image-step"]').set_input_files(image_path)
    page.locator('[data-test="add-step"]').click()


def create_recipe(page: Page) -> None:
    page.locator('[data-test="create-recipe"]').click()
    page.locator('[data-test="title"]').fill("My recipe")
    handle = page.query_selector('[data-test="category"]')
    handle.select_option(label="Garden")
    page.locator('[data-test="description"]').fill(lorem.paragraph())
    page.locator('[data-test="image-desc"]').set_input_files(image_path)
    handle = page.query_selector('[data-test="origin"]')
    handle.select_option(label="Asia")
    page.locator('[data-test="duration-input"]').fill("2.5")
    handle = page.query_selector('[data-test="duration-select"]')
    handle.select_option(label="Minutes")

    for ing in ings:
        add_ingredient(page, ing.quantity, ing.unit, ing.name)

    for step in steps:
        add_step(page, step.title)
    page.locator('[data-test="is_published"]').click()
    page.locator('[data-test="submit"]').click()
