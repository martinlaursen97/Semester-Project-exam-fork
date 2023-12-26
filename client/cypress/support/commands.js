// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })
Cypress.Commands.add('checkAlert', (expectedText) => {
    cy.on('window:alert', (text) => {
        expect(text).to.equal(expectedText);
    });
});

Cypress.Commands.add('login', (email, password) => {
    cy.visit('http://localhost:3000/login')
    cy.get('[data-test="e-mail"]').clear().type(email)
    cy.get('[data-test="password"]').clear().type(password)
    cy.get('[data-test="loginButton"]').click()
});
