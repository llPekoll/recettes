from playwright.sync_api import Page, sync_playwright, expect

from faker import Faker


def generate_random_username():
    fake = Faker()
    username = "pw_test_" + fake.user_name()
    return username


def generate_random_email():
    fake = Faker()
    email = fake.email()
    return email


def generate_random_password():
    fake = Faker()
    password = fake.password(
        length=10, special_chars=True, digits=True, upper_case=True, lower_case=True
    )
    return password


random_email = generate_random_email()
random_username = generate_random_username()
random_password = generate_random_password()


def test_register_ok(page: Page):
    page.goto("http://127.0.0.1:8000/register/")
    page.locator('[data-test="username"]').click()
    page.locator('[data-test="username"]').fill(random_username)
    page.locator('[data-test="username"]').press("Tab")
    page.locator('[data-test="email"]').fill(random_email)
    page.locator('[data-test="email"]').press("Tab")
    page.locator('[data-test="password1"]').click()
    page.locator('[data-test="password1"]').fill(random_password)
    page.locator('[data-test="password1"]').press("Tab")
    page.locator('[data-test="password2"]').fill(random_password)
    page.locator('[data-test="submit"]').click()
    logo = page.locator('[data-test="logo"]')
    expect(logo).to_have_attribute("href", "/")

    # ---------------------
    url = f"http://127.0.0.1:8000/users/delete/"
    page.route(url, lambda route: route.continue_(method="DELETE"))
    page.goto(url)


def test_register_wrong_username(page: Page):
    pass


def test_register_wrong_email(page: Page):
    pass


def test_register_password_not_match(page: Page):
    pass


def test_register_password_not_long(page: Page):
    pass
