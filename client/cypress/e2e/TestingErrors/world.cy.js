it('displays character Name and Race in the world', () => {
  cy.visit('http://localhost:3000/login')

  //login
  cy.get('[data-test="e-mail"]').clear().type('erol-taskiran@hotmail.com')
  cy.get('[data-test="password"]').clear().type(12345678)
  cy.get('[data-test="loginButton"]').click()
  cy.wait(2000)

  cy.get('[data-test="enterWorld"]').click()

  // Kontroller om navnet, gender og class er synlige
  cy.contains(`Name: Yasuo`).should('be.visible')
  cy.contains(`Gender: female`).should('be.visible')
  cy.contains(`Class: Shaman`).should('be.visible')

})