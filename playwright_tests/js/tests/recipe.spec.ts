import { test } from '@playwright/test';
import { createRecipe, editRecipe, register } from './lib';
import { faker } from '@faker-js/faker';


const username = `pw_${faker.internet.userName()}`;
const password = faker.internet.password({ length: 20 });
const randomEmail = faker.internet.email();


test('Create Recipe', async ({ page }) => {
	await register(page, username, password, randomEmail);
	await createRecipe(page, false, false);
});


test('Edit Recipe', async ({ page }) => {
	await register(page, username, password, randomEmail);
	await createRecipe(page, true, false);
	await editRecipe(page);
});

