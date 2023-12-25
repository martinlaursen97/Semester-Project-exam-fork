describe('Login and Character test', () => {
  const pageLoadTime = 1000;
  const loginWaitTime = 3000;
  const createCharacterWaitTime = 2000;
  const enterWorldWaitTime = 2000;
 
  beforeEach(() => {
    cy.visit('http://localhost:3000/login');
    cy.wait(pageLoadTime);
  });

  it('should login and create a character', () => {
    // Login
    cy.get('[data-test="e-mail"]').clear().type('erol-taskiran@hotmail.com')
    cy.get('[data-test="password"]').clear().type(12345678)
    cy.get('[data-test="loginButton"]').click()
    cy.wait(loginWaitTime)

    // Create Character
    cy.get('[data-test="nameCharacter"]').should('be.visible').type('Yasuo')
    cy.get('[data-test="selectClass"]').select('Shaman')
    cy.get('[data-test="selectGender"]').select('female')
    cy.get('[data-test="createCharacter"]').click()
    cy.wait(createCharacterWaitTime)
    
    // Enter World
    cy.get('[data-test="enterWorld"]').click()
    cy.wait(enterWorldWaitTime)
    
    for (let i = 0; i < 10; i++) {
      cy.get('[data-test="directionButtonsUp"]').click();
    }
    
    cy.wait(10000)
    
    for (let i = 0; i < 10; i++) {
      cy.get('[data-test="directionButtonsDown"]').click();
    }
  })
});
