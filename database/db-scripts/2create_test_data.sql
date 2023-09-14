-- Base user
INSERT INTO base_user (
	first_name, last_name,email,password,created_at)
	VALUES('ob','Hansen','mail@mail.com','password',NOW());

INSERT INTO base_user (
	first_name, last_name,email,password,created_at)
	VALUES('Bob','random','mail1@mail.com','password',NOW());

INSERT INTO base_user (
	first_name, last_name,email,password,created_at)
	VALUES('Henning','Ven','mail2@mail.com','password',NOW());

-- Ability Type
INSERT INTO ability_type (
	name, description, created_at)
	VALUES('Frost','Slows enemies for 30%', NOW());
INSERT INTO ability_type (
	name, description, created_at)
	VALUES('Fire','Burns enemies', NOW());
INSERT INTO ability_type (
	name, description, created_at)
	VALUES('Arcane','Hits harder', NOW());
INSERT INTO ability_type (
	name, description, created_at)
	VALUES('Melee','Very strong', NOW());

-- Base class
INSERT INTO base_class (
	name, created_at)
	VALUES('Mage', NOW());

INSERT INTO base_class (
	name, created_at)
	VALUES('Priest', NOW());
INSERT INTO base_class (
	name, created_at)
	VALUES('Shaman', NOW());
INSERT INTO base_class (
	name, created_at)
	VALUES('ADC', NOW());
INSERT INTO base_class (
	name, created_at)
	VALUES('Warrior', NOW());
INSERT INTO base_class (
	name, created_at)
	VALUES('Druid', NOW());

-- Gender
INSERT INTO gender (
	gender_type, created_at)
	VALUES('Male', NOW());
INSERT INTO gender (
	gender_type, created_at)
	VALUES('Female', NOW());

-- Attribute
INSERT INTO attribute (
	attribute_name, description, created_at)
	VALUES('Intelligence','Gives you more mana and spell power', NOW());
INSERT INTO attribute (
	attribute_name, description, created_at)
	VALUES('Strength','Makes you stronger', NOW());
INSERT INTO attribute (
	attribute_name, description, created_at)
	VALUES('Agility','Gives you crit', NOW());

-- Place
INSERT INTO place (
	place_name, radius, x, y, created_at)
	VALUES('Fire City', 4, 0, 10, NOW());
INSERT INTO place (
	place_name, radius, x, y, created_at)
	VALUES('Forest City', 4, 10, 0, NOW());
INSERT INTO place (
	place_name, radius, x, y, created_at)
	VALUES('Mountain City', 4, -10, 0, NOW());

-- Relation
INSERT INTO relation (
	user1_id, user2_id,created_at)
	VALUES(1,2, NOW());
INSERT INTO relation (
	user1_id, user2_id,created_at)
	VALUES(1,3, NOW());
INSERT INTO relation (
	user1_id, user2_id,created_at)
	VALUES(2,3, NOW());

-- Base_character
INSERT INTO base_character  (
	class_id, user_id, gender_id, character_name, alive, level, xp, money, created_at)
    VALUES(1,1,1,'Humble gaming', true, 9000, 99999, 999999, NOW());
INSERT INTO base_character  (
	class_id, user_id, gender_id, character_name, alive, level, xp, money, created_at)
    VALUES(2,1,1,'Gamer', true, 9000, 99999, 999999, NOW());
INSERT INTO base_character  (
	class_id, user_id, gender_id, character_name, alive, level, xp, money, created_at)
    VALUES(3,1,1,'sniger', true, 9000, 99999, 999999, NOW());
INSERT INTO base_character  (
	class_id, user_id, gender_id, character_name, alive, level, xp, money, created_at)
    VALUES(4,1,1,'Moshizzl3', true, 9000, 99999, 999999, NOW());
    
-- Character_location
INSERT INTO character_location  (
	character_id, x, y, created_at)
    VALUES(1, 1, 5, NOW());
INSERT INTO character_location  (
	character_id, x, y, created_at)
    VALUES(2, 5, 1, NOW());
INSERT INTO character_location  (
	character_id, x, y, created_at)
    VALUES(3, -5, 1, NOW());
INSERT INTO character_location  (
	character_id, x, y, created_at)
	VALUES(4, 30, 20, NOW());


-- Ability
INSERT INTO ability  (
	name, ability_type_id, created_at)
    VALUES('Frost Ball', 1, NOW());
INSERT INTO ability  (
	name, ability_type_id, created_at)
    VALUES('Fire Ball', 2, NOW());
INSERT INTO ability  (
	name, ability_type_id, created_at)
    VALUES('Arcane Blast', 3, NOW());
INSERT INTO ability  (
	name, ability_type_id, created_at)
    VALUES('Execute', 4, NOW());

-- Class_ability
INSERT INTO class_ability  (
	class_id, ability_id, created_at)
    VALUES(1,1, NOW());
INSERT INTO class_ability  (
	class_id, ability_id, created_at)
    VALUES(2,2, NOW());
INSERT INTO class_ability  (
	class_id, ability_id, created_at)
    VALUES(3,3, NOW());

-- Character_attribute
INSERT INTO character_attribute  (
	character_id, attribute_id, value,created_at)
    VALUES(1,1,20, NOW());
INSERT INTO character_attribute  (
	character_id, attribute_id, value,created_at)
    VALUES(1,1,20, NOW());
INSERT INTO character_attribute  (
	character_id, attribute_id, value,created_at)
    VALUES(1,1,20, NOW());
