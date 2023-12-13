import { Page, expect } from '@playwright/test';

export const register = async (page: Page, username: string, password: string, email: string) => {
    await page.goto('http://localhost:8000/en/');
    await page.locator('[data-test="register"]').click();
    await page.locator('[data-test="username"]').fill(username);
    await page.locator('[data-test="email"]').fill(email);
    await page.locator('[data-test="password1"]').fill(password);
    await page.locator('[data-test="password2"]').fill(password);
    await page.locator('[data-test="submit"]').click();
    await expect(page.locator('[data-test="profile-icon"]')).toBeVisible();
}