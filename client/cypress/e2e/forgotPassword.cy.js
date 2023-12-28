import "cypress-real-events/support";

it("Forget password success", () => {
  cy.visit("http://localhost:3000/login");
  cy.get("a:nth-child(3)").click();
  cy.get("input").click();
  cy.get("input").type("user0@example.com");

  const button = cy.get("button:nth-child(2)");
  button.should("contain", "Reset Password");
  button.click();

  cy.get("form").submit();


  cy.on("window:alert", (text) => {
    expect(text).to.contains("Check your email for a reset link");
  });

  cy.wait(1000);

  cy.url().should("eq", "http://localhost:3000/login");
});
