import "cypress-real-events/support";

it("Forget password success", () => {
  cy.visit("http://localhost:3000/login");
  cy.get("a:nth-child(3)").click();
  cy.get("input").click();
  cy.get("input").type("user0@example.com");

  const button = cy.get("button:nth-child(2)");
  button.should("contain", "Reset Password");
  button.click();

  cy.intercept("POST", "/api/postgres/auth/forgot-password").as(
    "passwordReset"
  );

  cy.get("form").submit();

  cy.checkAlert("Check your email for a reset link");

  // Wait for the request to complete before proceeding
  cy.wait("@passwordReset");

  cy.url().should("eq", "http://localhost:3000/login");
});
