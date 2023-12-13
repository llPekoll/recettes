import { test } from '@playwright/test';
import { login, logout, register } from './lib';
import { faker } from '@faker-js/faker';


const username = `pw_${faker.internet.userName()}`
const password = faker.internet.password({ length: 20 })
const randomEmail = faker.internet.email();


test('register', async ({ page }) => {
	await register(page, username, password, randomEmail)
	await logout(page)
	await login(page, username, password)
});
