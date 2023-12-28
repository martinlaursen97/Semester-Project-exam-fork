import 'cypress-real-events/support';

describe('Login and Character test', () => {
  const pageLoadTime = 1000;
  const loginWaitTime = 3000;
  const createCharacterWaitTime = 2000;
  const enterWorldWaitTime = 2000;
  const numberinY = -200;
 
  beforeEach(() => {
    cy.visit('http://localhost:3000/login');
    cy.wait(pageLoadTime);
  });

  // Login
  it('should login and create a character', () => {
    
    cy.login('user0@example.com', 'password')

    // Create Character
    cy.get('[data-test="nameCharacter"]').should('be.visible').type('Orc')
    cy.get('[data-test="selectClass"]').select('Warrior')
    cy.get('[data-test="selectGender"]').select('other')
    cy.get('[data-test="createCharacter"]').click()
    cy.wait(createCharacterWaitTime)
    
    // Enter World
    cy.get('[data-test="enterWorld"]').first().click()
    cy.wait(enterWorldWaitTime)
    
    for (let i = 0; i < 10; i++) {
      cy.get('[data-test="directionButtonsUp"]').click();
    }
    
    cy.wait(3000)
    
    for (let i = 0; i < 10; i++) {
      cy.get('[data-test="directionButtonsDown"]').click();
    }

    cy.get('[data-test="placeName"]').type('Kea')
    cy.get('[data-test="Xcoordinate"]').type('200')
    for (let i = 0; i < 3; i++) {
    cy.get('[data-test="Ycoordinate"]').type('0').realType('{downarrow}');
    }
    cy.get('[data-test="placeRadius"]').type('75')
    cy.get('[data-test="submitPlace"]').click()
  })
});
