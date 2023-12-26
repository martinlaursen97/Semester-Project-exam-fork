describe('Testing load characters page', () => {
    beforeEach(() => {
        cy.login('user0@example.com', 'password');
    });

    it('Check displays name', () => {
        cy.get('[data-test="nameCharacter"]').should('be.visible').type('test');
    });

    it('Contains classes', () => {
        const classes = ['Warrior', 'Mage', 'Shaman'];
        classes.forEach(className => {
            cy.get('[data-test="selectClass"]').find('option').contains(className).should('exist');
        });
    });

    it('Contains genders', () => {
        const genders = ['male', 'female', 'other'];
        genders.forEach(gender => {
            cy.get('[data-test="selectGender"]').find('option').contains(gender).should('exist');
        });
    });
});