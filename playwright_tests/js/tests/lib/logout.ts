import { Page, expect } from '@playwright/test';


export const logout = async (page: Page) => {
    await page.goto("http://localhost:8000/");
    await page.locator('[data-test="profile-icon"]').click()
    await page.locator('[data-test="logout"]').click()
    await expect(page.locator('[data-test="profile-icon"]')).not.toBeVisible()
}