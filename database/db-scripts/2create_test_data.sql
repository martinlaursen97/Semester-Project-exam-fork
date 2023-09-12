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

-- gender
INSERT INTO gender (
	gender_type, created_at)
	VALUES('Male', NOW());
INSERT INTO gender (
	gender_type, created_at)
	VALUES('Female', NOW());

-- attribute

INSERT INTO attribute (
	attribute_name, description, created_at)
	VALUES('Intelligence','Gives you more mana and spell power', NOW());
INSERT INTO attribute (
	attribute_name, description, created_at)
	VALUES('Strength','Makes you stronger', NOW());
INSERT INTO attribute (
	attribute_name, description, created_at)
	VALUES('Agility','Gives you crit', NOW());

-- place

INSERT INTO place (
	place_name, created_at)
	VALUES('Fire City', NOW());
INSERT INTO place (
	place_name, created_at)
	VALUES('Forest City', NOW());
INSERT INTO place (
	place_name, created_at)
	VALUES('Mountain City', NOW());

-- relation

INSERT INTO relation (
	user1_id, user2_id,created_at)
	VALUES(1,2, NOW());
INSERT INTO relation (
	user1_id, user2_id,created_at)
	VALUES(1,3, NOW());
INSERT INTO relation (
	user1_id, user2_id,created_at)
	VALUES(2,3, NOW());

-- location

INSERT INTO location (
	x, y, place_id, created_at)
	VALUES(2,3,1, NOW());
INSERT INTO location (
	x, y, place_id, created_at)
	VALUES(4,5,2, NOW());
INSERT INTO location (
	x, y, place_id, created_at)
	VALUES(6,7,3, NOW());

-- base_character

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
    
-- character_location

INSERT INTO character_location  (
	character_id, location_id, created_at)
    VALUES(1, 1, NOW());
INSERT INTO character_location  (
	character_id, location_id, created_at)
    VALUES(2, 1, NOW());
INSERT INTO character_location  (
	character_id, location_id, created_at)
    VALUES(3, 2, NOW());


-- ability

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

-- class_ability
INSERT INTO class_ability  (
	class_id, ability_id, created_at)
    VALUES(1,1, NOW());
INSERT INTO class_ability  (
	class_id, ability_id, created_at)
    VALUES(2,2, NOW());
INSERT INTO class_ability  (
	class_id, ability_id, created_at)
    VALUES(3,3, NOW());

-- character_attribute

INSERT INTO character_attribute  (
	character_id, attribute_id, value,created_at)
    VALUES(1,1,20, NOW());
INSERT INTO character_attribute  (
	character_id, attribute_id, value,created_at)
    VALUES(1,1,20, NOW());
INSERT INTO character_attribute  (
	character_id, attribute_id, value,created_at)
    VALUES(1,1,20, NOW());


