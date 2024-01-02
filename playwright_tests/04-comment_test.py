from faker import Faker
from playwright.sync_api import sync_playwright
from lib import register, create_article, delete_account, create_recipe, add_comment


fake = Faker()


def generate_random_user():
    return f"pw_{fake.user_name()}"


def generate_random_password():
    return fake.password(
        length=10, special_chars=True, digits=True, upper_case=True, lower_case=True
    )


def generate_random_email():
    return fake.email()


def test_comment_on_recipe():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        username = generate_random_user()
        register(page, username, generate_random_password(), generate_random_email())
        create_recipe(page, basic=True, create=True, publish=True)
        add_comment(page)
        page.goto("http://localhost:8000/en/")
        create_article(page)
        add_comment(page)
        delete_account(page)
        context.close()
        browser.close()

