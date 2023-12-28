it('displays character Name and Race in the world', () => {
  cy.visit('http://localhost:3000/login')

  //login
  cy.login('user0@example.com', 'password');

 

  // Kontroller om navnet, gender og class er synlige
  cy.contains(`Name: Orc`).should('be.visible')
  cy.contains(`Gender: other`).should('be.visible')
  cy.contains(`Class: Warrior`).should('be.visible')

  cy.get('[data-test="enterWorld"]').eq(1).should('be.visible')
  .should('contain', 'Name: yasuo')
  .should('contain', 'Gender: female')
  .should('contain', 'Class: Warrior');

  cy.get('[data-test="enterWorld"]').first().click()
})