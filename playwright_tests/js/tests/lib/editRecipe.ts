import { Page, expect } from '@playwright/test';
import { faker } from '@faker-js/faker';
import { sleep } from './tools';


interface Ingredient {
    quantity: string;
    unit: string;
    name: string;
};

interface Step {
    title: string;
};

const image_path = "playwright_tests/tests/lib/fixtures/images/bf.jpg"

const ings: Ingredient[] = [
    { quantity: "2.5", unit: "Spoon", name: "citron" },
    { quantity: "1", unit: "Liter", name: "citron" },
    { quantity: "5", unit: "Kilograme", name: "Chocolate" },
    { quantity: "90", unit: "Piece", name: "oigons" },
];

const steps: Step[] = [
    { title: "Melanger" },
    { title: "astiquer" },
    { title: "malaxer" },
    { title: "manger" },
];

const addIngredient = async (page: Page, quantity: string, unit: string, name: string): Promise<void> => {
    await page.locator('[data-test="quantity"]').focus()
    await page.locator('[data-test="quantity"]').fill(quantity)
    const handle = page.locator('[data-test="unit"]')
    await handle.selectOption({ label: unit })
    await page.locator('[data-test="ingredient_name"]').fill(name)
    await page.locator('[data-test="add-ingredient"]').click()
    await expect(page.locator(`[data-test="ing-${name}"]`)).toBeVisible()
};

const addStep = async (page: Page, title: string): Promise<void> => {
    await page.locator('[data-test="title-step"]').focus()
    await page.locator('[data-test="title-step"]').fill(title)
    await page.locator("#quill-id_instruction div").first().fill(faker.lorem.paragraph())
    await page.locator('[data-test="image-step"]').setInputFiles(image_path)
    await page.locator('[data-test="add-step"]').click()
    await expect(page.locator(`[data-test="step-${title}"]`)).toBeVisible()
}


export const editRecipe = async (page: Page): Promise<void> => {
    await page.locator('[data-test="edit-recipe"]').click()
    await page.locator('[data-test="title"]').fill("José Martins")
    let handle = page.locator('[data-test="category"]')
    handle.selectOption({ label: "Garden" })
    page.locator('[data-test="description"]').fill(faker.lorem.paragraph())
    page.locator('[data-test="image-desc"]').setInputFiles(image_path)
    handle = page.locator('[data-test="origin"]')
    await handle.selectOption({ label: "Asia" })
    page.locator('[data-test="duration-input"]').fill("2.5")
    handle = page.locator('[data-test="duration-select"]')
    handle.selectOption({ label: "Minutes" })
    for (let ing of ings) {
        await addIngredient(page, ing.quantity, ing.unit, ing.name)
        await sleep(1000);
    }

    for (let step of steps) {
        await addStep(page, step.title)
        await sleep(1000);
    }
    await page.locator("tags").getByRole("textbox").click()
    await page.locator("tags").getByRole("textbox").fill("victorine")
    await page.locator("tags").getByRole("textbox").press("Tab")
    await page.locator("tags").getByRole("textbox").fill("j'y peux rien")
    await page.locator("tags").getByRole("textbox").press("Tab")
    await page.locator("tags").getByRole("textbox").fill("je suis comme ça")
    await page.locator("tags").getByRole("textbox").press("Tab")
    await page.locator('[data-test="is_published"]').click()
    await page.locator('[data-test="submit"]').click()
    expect(page.locator('[data-test="title-recipe"]')).toBe("José Martins")

}