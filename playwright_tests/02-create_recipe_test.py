from faker import Faker
from playwright.sync_api import Playwright, sync_playwright, expect, Page
from lib import register, create_recipe

fake = Faker()


def generate_random_user():
    return f"pw_{fake.user_name()}"


def generate_random_password():
    return fake.password(
        length=10, special_chars=True, digits=True, upper_case=True, lower_case=True
    )


def generate_random_email():
    return fake.email()


def generate_recipe_name():
    return fake.email()


def test_recipe():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        username = generate_random_user()
        recipe_name = generate_random_email()
        print(f"register {username}")
        register(page, username, generate_random_password(), generate_random_email())
        create_recipe(page, True, True, False)
        context.close()
        browser.close()
