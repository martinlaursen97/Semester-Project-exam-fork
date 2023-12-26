it('it display the Name, Gender and Character', () => {
    cy.visit('http://localhost:3000/login')
    
    //login
    cy.get('[data-test="e-mail"]').clear().type('erol-taskiran@hotmail.com')
    cy.get('[data-test="password"]').clear().type(12345678)
    cy.wait(1000)
    cy.get('[data-test="loginButton"]').click()
    cy.wait(2000)

    cy.get('[data-test="nameCharacter"]').should('be.visible').type('Yasuo');
      
    //kigger efter om dropdown menuen indeholder male,female og other
    cy.get('[data-test="selectClass"]').should('include', 'Warrior');
    cy.get('[data-test="selectClass"]').should('include', 'Mage');
    cy.get('[data-test="selectClass"]').should('include', 'Shaman');

    //kigger efter om dropdown menuen indeholder male,female og other
    cy.get('[data-test="selectGender"]').should('contain', 'male');
    cy.get('[data-test="selectGender"]').should('contain', 'female');
    cy.get('[data-test="selectGender"]').should('contain', 'other');
   
    cy.wait(1000);

})