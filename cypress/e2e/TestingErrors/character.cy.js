it('handles character creation errors', () => {
    cy.visit('http://localhost:3000/characters')
  
  
  
    // Forsøger at oprette karakter uden et navn
    cy.get('[data-test="nameCharacter"]').clear()
    cy.get('[data-test="createCharacter"]').click()
    //mangler error message
    cy.contains('Name is required').should('be.visible')
  
    // vi forsøger at oprette en karakter uden at vælge klasse og køn
    cy.get('[data-test="nameCharacter"]').type('Yasuo')
    cy.get('[data-test="createCharacter"]').click()
    //mangler error message
    cy.contains('Class is required').should('be.visible')
    cy.contains('Gender is required').should('be.visible')
  })