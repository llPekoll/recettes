from faker import Faker
from playwright.sync_api import sync_playwright
from lib import register, login, logout, delete_account

fake = Faker()


def generate_random_user():
    return f"pw_{fake.user_name()}"


def generate_random_password():
    return fake.password(
        length=10, special_chars=True, digits=True, upper_case=True, lower_case=True
    )


def generate_random_email():
    return fake.email()


def test_login_register():
    with sync_playwright() as playwright:
        username = generate_random_user()
        password = generate_random_password()
        email = generate_random_email()
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print(f"register {username}")
        register(page, username, password, email)
        context.close()
        browser.close()

        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        print("login")
        login(page, username, password)

        print("logout")
        logout(page)
        context.close()
        browser.close()


def test_delete_account():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        username = generate_random_user()
        password = generate_random_password()
        print(f"register {username}")
        register(page, username, password, generate_random_email())
        delete_account(page)
        context.close()
        browser.close()
