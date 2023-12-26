it('handles login errors', () => {
    cy.visit('http://localhost:3000/login')
  
    // Forsøger at ligge en '@' efter en '@'
    cy.get('[data-test="e-mail"]').clear().type('testemail@example@.com')
    cy.get('[data-test="password"]').clear().type('validPassword')
    cy.get('[data-test="loginButton"]').click()
    cy.contains(/Den del, der kommer efter "@", må ikke indeholde symbolet "@"./i).should('exist')
    cy.wait(5000)
    // Forsøger at logge in med forkert e-mail
    cy.get('[data-test="e-mail"]').clear().type('testemail@example.com')
    cy.get('[data-test="password"]').clear().type('validPassword')
    cy.get('[data-test="loginButton"]').click()
    //mangler error message
    cy.contains('Invalid email or password').should('be.visible')
  
    // Forsøger her at logge ind med forkert adgangskode
    cy.get('[data-test="e-mail"]').clear().type('valid-email@example.com')
    cy.get('[data-test="password"]').clear().type('invalidPassword')
    cy.get('[data-test="loginButton"]').click()
    //mangler error message
    cy.contains('Invalid email or password').should('be.visible')
  })
  