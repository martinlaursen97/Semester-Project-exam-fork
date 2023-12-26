describe('Login Page Tests', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/login'); // Replace '/' with the path to your login page
    cy.get('[data-test="e-mail"]').clear();
    cy.get('[data-test="password"]').clear();
  });

  it('Should display the login form', () => {
    cy.get('form').should('be.visible');
    cy.get('[data-test="e-mail"]').should('be.visible');
    cy.get('[data-test="password"]').should('be.visible');
    cy.get('[data-test="loginButton"]').should('be.visible');
  });

  it('Should require email and password', () => {
    cy.get('[data-test="loginButton"]').click();
    cy.checkAlert('Please fill out all fields');
  });

  it('Should validate password length', () => {
    cy.get('[data-test="e-mail"]').type('user0@example.com');
    cy.get('[data-test="password"]').type('short');
    cy.get('[data-test="loginButton"]').click();
    cy.checkAlert('Password must be between 8 and 32 characters');
  });

  it('Should navigate to characters page on successful login', () => {
    cy.intercept('POST', '/auth/login-email').as('loginRequest');

    cy.get('[data-test="e-mail"]').type('user0@example.com');
    cy.get('[data-test="password"]').type('password');
    cy.get('[data-test="loginButton"]').click();
    cy.url().should('include', '/characters');
  });

  it('Should handle invalid credentials', () => {
    cy.intercept('POST', '/auth/login-email', {
      statusCode: 401,
      body: { error: 'Invalid credentials' }
    }).as('failedLoginRequest');
    cy.get('[data-test="e-mail"]').type('user0@example.com');
    cy.get('[data-test="password"]').type('wrongpassword');
    cy.get('[data-test="loginButton"]').click();
    cy.wait(1000);
    cy.checkAlert('Wrong email or password');
  });

  it('Should have a link to the registration page', () => {
    cy.contains('Don\'t have an account?').should('be.visible');
    cy.contains('Register').should('have.attr', 'href', '/register');
  });

  it('Should have a link to the forgot password page', () => {
    cy.contains('Forgot Password').should('have.attr', 'href', '/forgot-password');
  });
});
