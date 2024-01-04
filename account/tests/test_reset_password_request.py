# from account.tests.test_register import (
#     create_user,
#     delete_users,
#     generate_random_email,
#     random_email,
# )
# from playwright.sync_api import Page, expect

# new_email = generate_random_email()


# def test_reset_password_request_ok(page: Page):
#     create_user(page)
#     page.wait_for_timeout(1000)
#     page.goto("http://127.0.0.1:8000/reset-password/")
#     page.locator('[data-test="email"]').fill(random_email)
#     page.locator('[data-test="submit"]').click()
#     validation = page.locator('[data-test="email-sent"]')
#     expect(validation).to_be_visible()
#     delete_users(page)


# def test_reset_password_request_email_not_found(page: Page):
#     create_user(page)
#     page.goto("http://127.0.0.1:8000/reset-password/")
#     page.locator('[data-test="email"]').fill(new_email)
#     page.locator('[data-test="submit"]').click()
#     error = page.locator('[data-test="email-not-found"]')
#     expect(error).to_be_visible()
#     delete_users(page)
