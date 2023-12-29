import { generateRandomString } from "../support/utils.js";

describe("Login Page Tests", () => {
  const userEmail = `${generateRandomString(10)}@test.com`;
  const userPassword = "password";
  let accessToken = "";

  before(() => {
    cy.registerAndGetToken(userEmail, userPassword).then((token) => {
      accessToken = token;
    });
  });


  beforeEach(() => {
    cy.visit("http://localhost:3000/login");
    cy.get('[data-test="e-mail"]').clear();
    cy.get('[data-test="password"]').clear();
  });

  it("Should display the login form", () => {
    cy.get("form").should("be.visible");
    cy.get('[data-test="e-mail"]').should("be.visible");
    cy.get('[data-test="password"]').should("be.visible");
    cy.get('[data-test="loginButton"]').should("be.visible");
  });

  it("Should require email and password", () => {
    cy.get('[data-test="loginButton"]').click();
    cy.checkAlert("Please fill out all fields");
  });

  it("Should validate password length short", () => {
    cy.get('[data-test="e-mail"]').type(userEmail);
    cy.get('[data-test="password"]').type("short");
    cy.get('[data-test="loginButton"]').click();
    cy.checkAlert("Password must be between 8 and 32 characters");
  });

  it("Should validate password length long", () => {
    cy.get('[data-test="e-mail"]').type(userEmail);
    cy.get('[data-test="password"]').type("longpasswordlongpasswordlongpasswordlongpassword");
    cy.get('[data-test="loginButton"]').click();
    cy.checkAlert("Password must be between 8 and 32 characters");
  });

  it("Should navigate to characters page on successful login", () => {
    cy.intercept("POST", "/auth/login-email").as("loginRequest");
    cy.get('[data-test="e-mail"]').type(userEmail);
    cy.get('[data-test="password"]').type(userPassword);
    cy.get('[data-test="loginButton"]').click();
    cy.url().should("include", "/characters");
  });

  it("Should handle invalid credentials", () => {
    cy.get('[data-test="e-mail"]').type(userEmail);
    cy.get('[data-test="password"]').type("wrongpassword");
    cy.get('[data-test="loginButton"]').click();
    cy.checkAlert("Wrong email or password");
  });

  it("Should have a link to the registration page", () => {
    cy.contains("Don't have an account?").should("be.visible");
    cy.contains("Register").should("have.attr", "href", "/register");
  });

  it("Should have a link to the forgot password page", () => {
    cy.contains("Forgot Password").should("have.attr", "href", "/forgot-password");
  });

  after(() => {
    if (accessToken) {
      cy.deleteCurrentUser(accessToken);
    }
  });
});
