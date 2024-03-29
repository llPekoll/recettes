# from faker import Faker
# from playwright.sync_api import Page, expect


# def generate_random_username():
#     fake = Faker()
#     username = "pw_test_" + fake.user_name()
#     return username


# def generate_random_email():
#     fake = Faker()
#     email = fake.email()
#     return email


# def generate_random_password():
#     fake = Faker()
#     password = fake.password(
#         length=10, special_chars=True, digits=True, upper_case=True, lower_case=True
#     )
#     return password


# random_email = generate_random_email()
# random_username = generate_random_username()
# random_password = generate_random_password()


# def delete_users(page: Page):
#     url = "http://127.0.0.1:3000/users/delete/"
#     page.route(url, lambda route: route.continue_(method="DELETE"))
#     page.goto(url)


# def create_user(page: Page, password_Type="valid"):
#     page.goto("http://127.0.0.1:3000/register/")
#     page.locator('[data-test="username"]').fill(random_username)
#     page.locator('[data-test="email"]').fill(random_email)
#     page.locator('[data-test="password1"]').click()
#     if password_Type == "valid":
#         page.locator('[data-test="password1"]').fill(random_password)
#     elif password_Type == "missmatch":
#         page.locator('[data-test="password1"]').fill(random_password)
#     elif password_Type == "too_short":
#         page.locator('[data-test="password1"]').fill("233")
#     if password_Type == "valid":
#         page.locator('[data-test="password2"]').fill(random_password)
#     elif password_Type == "missmatch":
#         page.locator('[data-test="password2"]').fill(random_password[::-1])
#     elif password_Type == "too_short":
#         page.locator('[data-test="password2"]').fill("233")
#     page.locator('[data-test="submit"]').click()


# def test_register_valid(page: Page, password_Type="valid"):
#     create_user(page, "valid")
#     logo = page.locator('[data-test="logo"]')
#     expect(logo).to_have_attribute("href", "/")
#     delete_users(page)


# def test_register_wrong_username(page: Page):
#     create_user(page)
#     page.goto("http://127.0.0.1:3000/register/")
#     page.wait_for_timeout(1000)
#     page.locator('[data-test="username"]').fill(random_username)
#     page.locator('[data-test="password2"]').click()
#     already_taken = page.locator('[data-test="already-taken"]')
#     expect(already_taken).to_be_visible()
#     delete_users(page)


# def test_register_wrong_email(page: Page):
#     create_user(page)
#     page.goto("http://127.0.0.1:3000/register/")
#     page.wait_for_timeout(1000)
#     page.locator('[data-test="email"]').fill(random_email)
#     page.locator('[data-test="password2"]').click()
#     already_taken = page.locator('[data-test="already-taken"]')
#     expect(already_taken).to_be_visible()
#     delete_users(page)


# def test_register_password_missmatch(page: Page):
#     create_user(page, "missmatch")
#     page.wait_for_timeout(1000)
#     error = page.locator('[data-test="error"]')
#     expect(error).to_be_visible()
#     delete_users(page)


# def test_register_password_not_long(page: Page):
#     create_user(page, "missmatch")
#     page.wait_for_timeout(1000)
#     error = page.locator('[data-test="error"]')
#     expect(error).to_be_visible()
#     delete_users(page)
