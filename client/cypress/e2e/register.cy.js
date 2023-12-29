import "cypress-real-events/support";

describe('Register User Test', () => {
  it('Register the user', () => {
    let accessToken;
    cy.intercept("POST", "/api/postgres/auth/register").as(
      "userRegistration"
    );

    cy.visit("http://localhost:3000/login");

    cy.get("a:nth-child(1)").click();

    cy.url().should("eq", "http://localhost:3000/register");

    cy.get("input:first-of-type").click();
    cy.get("input:first-of-type").type("ae12@test.com");

    cy.get("input:nth-of-type(2)").click();
    cy.get("input:nth-of-type(2)").type("password");

    cy.get("input:last-of-type").click();
    cy.get("input:last-of-type").type("password");

    cy.get("button[type='submit']").click();
  

    cy.wait("@userRegistration");

    cy.url().should("eq", "http://localhost:3000/login");
    
    cy.intercept("POST", "api/postgres/auth/login-email").as("userLogin");
    
    cy.get("input[type='email']").clear();
    cy.get("input[type='email']").clear().type("ae12@test.com");
    cy.get("input[type='password']").clear();
    cy.get("input[type='password']").clear().type("password");
    cy.get("button[type='submit']").click();

    cy.get("form").submit();

    cy.wait("@userLogin").then(({ response }) => { // accessToken is for some reason always undefined, which leads to error
      accessToken = response.body.access_token;
    });

    cy.request({
      method: 'DELETE',
      url: '/api/postgres/base-user',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      }
    })

    cy.visit("http://localhost:3000/login");
    cy.get("input[type='email']").clear().type("ae12@test.com");
    cy.get("form").submit();

    cy.checkAlert("Error: Wrong email or password")
  })
})