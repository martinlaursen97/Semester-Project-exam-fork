const baseApiUrl = "http://localhost:8080/api/postgres";
const baseClientUrl = "http://localhost:3000";

function generateRandomString(length) {
    const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let result = "";
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

Cypress.Commands.add("checkAlert", (expectedText) => {
    cy.on("window:alert", (text) => {
        expect(text).to.equal(expectedText);
    });
});

Cypress.Commands.add("login", (email, password) => {
    cy.visit(`${baseClientUrl}/login`);
    cy.intercept("POST", `${baseApiUrl}/auth/login-email`).as("loginRequest");
    cy.get("[data-test='e-mail']").clear().type(email);
    cy.get("[data-test='password']").clear().type(password);
    cy.get("[data-test='loginButton']").click();
    cy.wait("@loginRequest")
});


Cypress.Commands.add("registerAndGetToken", (email, password) => {
    cy.request({
        method: "POST",
        url: `${baseApiUrl}/auth/register`,
        body: {
            email,
            password
        }
    }).then(response => {
        expect(response.status).to.eq(201);
    });

    cy.request({
        method: "POST",
        url: `${baseApiUrl}/auth/login-email`,
        body: {
            email,
            password
        }
    }).then(response => {
        expect(response.body.data).to.have.property("access_token");
        const accessToken = response.body.data.access_token;
        return accessToken;
    });
});


Cypress.Commands.add("deleteCurrentUser", (accessToken) => {
    cy.request({
        method: "DELETE",
        url: `${baseApiUrl}/base-users`,
        headers: {
            "Authorization": `Bearer ${accessToken}`,
        }
    }).then(response => {
        expect(response.status).to.eq(200);
    });
});


Cypress.Commands.add("createCharacter", (characterName) => {
    cy.intercept("POST", `${baseApiUrl}/characters`).as("characterCreation");

    cy.get('[data-test="nameCharacter"]').type(characterName);
    cy.get('[data-test="selectClass"]').select("Warrior");
    cy.get('[data-test="selectGender"]').select("male");;
    cy.get('[data-test="createCharacter"]').click();

    cy.wait("@characterCreation").then(({ response }) => {
        expect(response.statusCode).to.eq(201);
    });
});