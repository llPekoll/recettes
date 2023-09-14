from playwright.sync_api import Page, expect

from account.tests.test_register import (
    create_user,
    delete_users,
    random_password,
    random_username,
)


def test_login_valid(page: Page):
    create_user(page)
    page.locator('[data-test="profile"]').click()
    page.locator('[data-test="logout"]').click()
    page.locator('[data-test="login"]').click()
    page.locator('[data-test="username"]').click()
    page.locator('[data-test="username"]').fill(random_username)
    page.locator('[data-test="username"]').press("Tab")
    page.locator('[data-test="password"]').fill(random_password)
    page.locator('[data-test="password"]').press("Tab")
    page.locator('[data-test="submit"]').click()
    profile = page.locator('[data-test="logo"]')
    expect(profile).to_be_visible()
    delete_users(page)


def test_login_wrong_password(page: Page):
    create_user(page)
    page.locator('[data-test="profile"]').click()
    page.locator('[data-test="logout"]').click()
    page.locator('[data-test="login"]').click()
    page.locator('[data-test="username"]').click()
    page.locator('[data-test="username"]').fill(random_username)
    page.locator('[data-test="username"]').press("Tab")
    page.locator('[data-test="password"]').fill(random_password[::-1])
    page.locator('[data-test="password"]').press("Tab")
    page.locator('[data-test="submit"]').click()
    errors = page.locator('[data-test="error"]')
    expect(errors).to_be_visible()
    delete_users(page)
