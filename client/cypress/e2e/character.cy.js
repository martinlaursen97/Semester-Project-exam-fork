import { generateRandomString } from "../support/utils";

describe("Testing character creation", () => {
  const userPassword = "password";
  const characterClass = "Warrior";
  const characterGender = "male";
  const characterName = `Character${generateRandomString(10)}`;
  const userEmail = `${generateRandomString(10)}@test.com`;
  let accessToken = "";

  beforeEach(() => {
    cy.setCookie("access_token", accessToken);
    cy.visit("http://localhost:3000/characters");
  });

  before(() => {
    cy.registerAndGetToken(userEmail, userPassword).then((token) => {
      accessToken = token;
    });
  });

  it("Name is required Alert", () => {
    cy.get('[data-test="createCharacter"]').click();
    cy.checkAlert("Name is required");
  });

  it("Class is required Alert", () => {
    cy.get('[data-test="nameCharacter"]').type(characterName);
    cy.get('[data-test="createCharacter"]').click();
    cy.checkAlert("Class is required");
  });

  it("Gender is required Alert", () => {
    cy.get('[data-test="nameCharacter"]').type(characterName);
    cy.get('[data-test="selectClass"]').select(characterClass);
    cy.get('[data-test="createCharacter"]').click();
    cy.checkAlert("Gender is required");
  });

  it("Character created", () => {
    cy.intercept("POST", "http://localhost:8080/api/postgres/characters").as("characterCreation");

    cy.get('[data-test="nameCharacter"]').type(characterName);
    cy.get('[data-test="selectClass"]').select(characterClass);
    cy.get('[data-test="selectGender"]').select(characterGender);;
    cy.get('[data-test="createCharacter"]').click();

    cy.wait("@characterCreation").then(({ response }) => {
      expect(response.statusCode).to.eq(201);
    });

    cy.get('[data-test="nameCharacter"]').clear();
    cy.contains(characterName).should("exist");
  });

  it("Creates a new character when name is already taken", () => {
    cy.intercept("POST", "http://localhost:8080/api/postgres/characters").as("characterCreation");

    cy.get('[data-test="nameCharacter"]').type(characterName);
    cy.get('[data-test="selectClass"]').select(characterClass);
    cy.get('[data-test="selectGender"]').select(characterGender);
    cy.get('[data-test="createCharacter"]').click();

    cy.wait("@characterCreation").then(({ response }) => {
      expect(response.statusCode).to.eq(403);
    });

    cy.checkAlert("Character name already taken");
  });

  it("Check displays name", () => {
    cy.get('[data-test="nameCharacter"]').should("be.visible").type(characterName);

  });

  it("Contains classes", () => {
    const classes = ["Warrior", "Mage", "Shaman"];
    classes.forEach(className => {
      cy.get('[data-test="selectClass"]').find("option").contains(className).should("exist");
    });
  });

  it("Contains genders", () => {
    const genders = ['male', 'female', 'other'];
    genders.forEach(gender => {
      cy.get('[data-test="selectGender"]').find('option').contains(gender).should('exist');
    });
  });

  it("Name too short", () => {
    const shortName = "\0";
    cy.get('[data-test="nameCharacter"]').type(shortName);
    cy.get('[data-test="createCharacter"]').click();
    cy.checkAlert("Name must be between 1 and 50 characters");
  });

  it("Name too long", () => {
    const longName = generateRandomString(51);
    cy.get('[data-test="nameCharacter"]').type(longName);
    cy.get('[data-test="createCharacter"]').click();
    cy.checkAlert("Name must be between 1 and 50 characters");
  });

  after(() => {
    if (accessToken) {
      cy.deleteCurrentUser(accessToken);
    }
  });
});
