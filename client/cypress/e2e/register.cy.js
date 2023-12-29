import "cypress-real-events/support";

describe("User Registration and Login Workflow", () => {
  const baseApiUrl = "http://localhost:8080/api/postgres"
  const baseClientUrl = "http://localhost:3000"

  const userEmail = "ae12@test.com";
  const userPassword = "password";
  let accessToken = "";

  it("Registers a new user", () => {
    cy.intercept("POST", `${baseApiUrl}/auth/register`).as("userRegistration");

    cy.visit(`${baseClientUrl}/login`);
    cy.get("a:nth-child(1)").click();
    cy.url().should("include", "/register");

    cy.get("input[type='email']").type(userEmail);
    cy.get("input[type='password']:first").type(userPassword);
    cy.get("input[type='password']:last").type(userPassword);
    cy.get("button[type='submit']").click();

    cy.wait("@userRegistration");
    cy.url().should("include", "/login");
  });

  it("Logs in the registered user", () => {
    cy.intercept("POST", `${baseApiUrl}/auth/login-email`).as("userLogin");

    cy.visit(`${baseClientUrl}/login`);
    cy.get("input[type='email']").clear().type(userEmail);
    cy.get("input[type='password']").clear().type(userPassword);
    cy.get("button[type='submit']").click();

    cy.wait("@userLogin").then(({ response }) => {
      accessToken = response.body.data.access_token;
    });
  });

  after(() => {
    if (accessToken) {
      cy.request({
        method: "DELETE",
        url: `${baseApiUrl}/base-users`,
        headers: {
          "Authorization": `Bearer ${accessToken}`,
        }
      });
    }
  });
});
