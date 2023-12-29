import { generateRandomString } from "../support/utils";

describe("Test world", () => {

  const userEmail = `${generateRandomString(10)}@test.com`;
  const characterName = `Character${generateRandomString(10)}`;
  const userPassword = "password";
  let accessToken = "";

  beforeEach(() => {
    cy.setCookie("access_token", accessToken);
    cy.visit("http://localhost:3000/characters");

    cy.intercept("GET", "http://localhost:8080/api/postgres/places").as("getPlaces");
    cy.get("[data-test=\"enterWorld\"]").first().click()
    cy.get("[data-test=\"enterWorld\"]").first().click()
    cy.wait("@getPlaces");
  });

  before(() => {
    cy.registerAndGetToken(userEmail, userPassword).then((token) => {
      accessToken = token;
    });
    cy.login(userEmail, userPassword);
    cy.createCharacter(characterName);
  });

  it("Should select a point on the canvas", () => {
    cy.get("canvas").click(250, 250);
    cy.get(".info-box").should("be.visible");

  });

  it("Should display the character name", () => {
    cy.get("canvas").click(250, 250);
    cy.get(".info-box").should("contain", `"character_name": "${characterName}",`);
    cy.get(".info-box").should("contain", "character_location");
    cy.get(".info-box").should("contain", "money");
    cy.get(".info-box").should("contain", "xp");
    cy.get(".info-box").should("contain", "level");
  });

  it("Should move the character", () => {
    cy.get("canvas").click(250, 250);
    for (let i = 1; i < 10; i++) {
      cy.get("[data-test=\"directionButtonsUp\"]").click();
      if (i > 1) {
        cy.get(".info-box").should("contain", `"y": -${i * 10}`)
      }
    }
  });

  after(() => {
    if (accessToken) {
      cy.deleteCurrentUser(accessToken);
    }
  });
});
