describe('Testing character creation', () => {

  beforeEach(() => {
    cy.visit('http://localhost:3000/characters')
  });

  it('Name is required Alert', () => {
    cy.get('[data-test="createCharacter"]').click();
    cy.checkAlert('Name is required');
  });

  it('Class is required Alert', () => {
    cy.get('[data-test="nameCharacter"]').type('test');
    cy.get('[data-test="createCharacter"]').click();
    cy.checkAlert('Class is required');
  });

  it('Gender is required Alert', () => {
    cy.login('user0@example.com', 'password');
    cy.get('[data-test="nameCharacter"]').type('test');
    cy.get('[data-test="selectClass"]').select('Shaman');
    cy.get('[data-test="createCharacter"]').click();
    cy.checkAlert('Gender is required');
  });

  it('Character created', () => {
    cy.login('user0@example.com', 'password');
    cy.get('[data-test="nameCharacter"]').type('test');
    cy.get('[data-test="selectClass"]').select('Shaman');
    cy.get('[data-test="selectGender"]').select('male');
    cy.get('[data-test="createCharacter"]').click();

    cy.get('[data-test="nameCharacter"]').clear()
    cy.contains('test').should('exist');
  });
});
