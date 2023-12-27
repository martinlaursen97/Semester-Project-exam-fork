it('displays character Name and Race in the world', () => {
  cy.visit('http://localhost:3000/login')

  //login
  cy.get('[data-test="e-mail"]').clear().type('user0@example.com')
  cy.get('[data-test="password"]').clear().type('password')
  cy.get('[data-test="loginButton"]').click()
  cy.wait(2000)

  cy.get('[data-test="enterWorld"]').click()

  // Kontroller om navnet, gender og class er synlige
  cy.contains(`Name: Orc`).should('be.visible')
  cy.contains(`Gender: other`).should('be.visible')
  cy.contains(`Class: Warrior`).should('be.visible')

})