import { Page, expect } from '@playwright/test';


export const login = async (page: Page, username: string, password: string): Promise<void> => {
    await page.goto("http://localhost:8000/");
    await page.locator('[data-test="login"]').click()
    await page.locator('[data-test="username"]').fill(username)
    await page.locator('[data-test="password"]').fill(password)
    await page.locator('[data-test="submit"]').click()
    await expect(page.locator('[data-test="profile-icon"]')).toBeVisible()
}