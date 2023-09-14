DROP TABLE IF EXISTS base_user CASCADE;
DROP TABLE IF EXISTS character_attribute CASCADE;
DROP TABLE IF EXISTS ability_type CASCADE;
DROP TABLE IF EXISTS base_class CASCADE;
DROP TABLE IF EXISTS attribute CASCADE;
DROP TABLE IF EXISTS place CASCADE;
DROP TABLE IF EXISTS relation CASCADE;
DROP TABLE IF EXISTS base_character CASCADE;
DROP TABLE IF EXISTS character_location CASCADE;
DROP TABLE IF EXISTS gender CASCADE;
DROP TABLE IF EXISTS ability CASCADE;
DROP TABLE IF EXISTS class_ability CASCADE;


CREATE TABLE base_user (
        id INT GENERATED ALWAYS AS IDENTITY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(50) NOT NULL,
        created_at DATE NOT NULL,
        PRIMARY KEY(id)
);

CREATE TABLE ability_type (
	id INT GENERATED ALWAYS AS IDENTITY,
	name VARCHAR(20) NOT NULL UNIQUE,
	description VARCHAR(200) NOT NULL,
	created_at DATE NOT NULL,
	PRIMARY KEY(id)
);


CREATE TABLE base_class (
	id INT GENERATED ALWAYS AS IDENTITY,
	name VARCHAR(20) NOT NULL UNIQUE,
	created_at DATE NOT NULL,
	PRIMARY KEY(id)
);


CREATE TABLE gender (
	id INT GENERATED ALWAYS AS IDENTITY,
	gender_type VARCHAR(20) NOT NULL UNIQUE,
	created_at DATE NOT NULL,
	PRIMARY KEY(id)
);


CREATE TABLE attribute (
	id INT GENERATED ALWAYS AS IDENTITY,
	attribute_name VARCHAR(20) NOT NULL UNIQUE,
	description VARCHAR(200)NOT NULL,
	created_at DATE NOT NULL,
	PRIMARY KEY(id)

);


CREATE TABLE place (
	id INT GENERATED ALWAYS AS IDENTITY,
	place_name VARCHAR(20) NOT NULL,
	radius INT NOT NULL,
	x INT NOT NULL,
	y INT NOT NULL,
	created_at DATE NOT NULL,
	PRIMARY KEY(id)
);



CREATE TABLE relation (
        id INT GENERATED ALWAYS AS IDENTITY,
        user1_id int NOT NULL,
        user2_id int NOT NULL,
        created_at DATE NOT NULL,
        PRIMARY KEY(id),
        CONSTRAINT fk_user1_user FOREIGN KEY(user1_id) REFERENCES base_user(id) ON
		DELETE CASCADE,
	  	CONSTRAINT fk_user2_user FOREIGN KEY(user2_id) REFERENCES base_user(id) ON
		DELETE CASCADE
);



CREATE TABLE base_character(
	id INT GENERATED ALWAYS AS IDENTITY,
	class_id INT NOT NULL,
	user_id INT NOT NULL,
	gender_id INT NOT NULL,
	character_name VARCHAR(20) NOT NULL,
	alive BOOL NOT NULL,
	LEVEL INT NOT NULL,
	xp INT NOT NULL,
	money INT NOT NULL,
	created_at DATE NOT NULL,
	PRIMARY KEY(id),
	CONSTRAINT fk_class_chararacter FOREIGN KEY(class_id) REFERENCES base_class(id) ON
	DELETE CASCADE,
	CONSTRAINT fk_user_chararacter FOREIGN KEY(user_id) REFERENCES base_user(id) ON
	DELETE CASCADE,
	CONSTRAINT fk_gender_chararacter FOREIGN KEY(gender_id) REFERENCES gender(id) ON
	DELETE CASCADE
);


CREATE TABLE character_location (
	id INT GENERATED ALWAYS AS IDENTITY,
	character_id INT NOT NULL,
	x INT NOT NULL,
	y INT NOT NULL,
	created_at DATE NOT NULL,
	PRIMARY KEY(id),
	CONSTRAINT fk_character_char_location FOREIGN KEY(character_id) REFERENCES base_character(id) ON
	DELETE CASCADE
);


CREATE TABLE ability(
	id INT GENERATED ALWAYS AS IDENTITY,
	name VARCHAR(20) NOT NULL UNIQUE,
	ability_type_id int NOT NULL,
	created_at DATE NOT NULL,
	PRIMARY KEY(id),
	CONSTRAINT fk_ability_type FOREIGN KEY(ability_type_id) REFERENCES ability_type(id) ON
	DELETE CASCADE
);


CREATE TABLE class_ability(
	id INT GENERATED ALWAYS AS IDENTITY,
	class_id INT NOT NULL,
	ability_id int NOT NULL,
	created_at DATE NOT NULL,
	PRIMARY KEY(id),
	CONSTRAINT fk_class_ability FOREIGN KEY(class_id) REFERENCES base_class(id) ON
	DELETE CASCADE,
	CONSTRAINT fk_ability_class_ability FOREIGN KEY(ability_id) REFERENCES ability(id) ON
	DELETE CASCADE
);


CREATE TABLE character_attribute (
	id INT GENERATED ALWAYS AS IDENTITY,
	character_id INT NOT NULL,
	attribute_id INT NOT NULL,
	value int NOT NULL,
	created_at DATE NOT NULL,
	PRIMARY KEY(id),
	CONSTRAINT fk_character_attribute FOREIGN KEY(character_id) REFERENCES base_character(id) ON
	DELETE CASCADE,
	CONSTRAINT fk_attribute_attribute FOREIGN KEY(attribute_id) REFERENCES attribute(id) ON
	DELETE CASCADE
);

-- Functions
CREATE OR REPLACE FUNCTION public.calculate_distance(x1 integer, y1 integer, x2 integer, y2 integer)
	RETURNS double precision
	LANGUAGE plpgsql
AS $function$
BEGIN
	RETURN sqrt((x2 - x1) ^ 2 + (y2 - y1) ^ 2);
END;
$function$
;


CREATE OR REPLACE FUNCTION public.get_character_location(bc_id integer)
	RETURNS TABLE(character_id integer, x integer, y integer)
	LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY (
        SELECT
            bc.id,
            cl.x,
            cl.y
        FROM character_location cl
        JOIN base_character bc on cl.id = bc.id
        where bc.id = bc_id
    );
END
$function$
;


CREATE OR REPLACE FUNCTION public.get_character_place(bc_id integer)
RETURNS VARCHAR(50)
LANGUAGE plpgsql
AS $function$
DECLARE
    character_location RECORD;
    character_place VARCHAR(50);
BEGIN
    SELECT character_id, x, y
    INTO character_location
    FROM public.get_character_location(bc_id);

    IF character_location IS NULL THEN
        RETURN 'Wilderness';
    ELSE
        SELECT place_name
        INTO character_place
        FROM place
        WHERE public.calculate_distance(character_location.x, character_location.y, x, y) <= radius;

        IF character_place IS NULL THEN
            RETURN 'Wilderness';
        ELSE
            RETURN character_place;
        END IF;
    END IF;
END;
$function$
;


CREATE OR REPLACE FUNCTION public.check_place_overlap()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $function$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM place p
        WHERE p.id <> NEW.id
        AND public.calculate_distance(NEW.x, NEW.y, p.x, p.y) <= NEW.radius
    ) THEN
        RAISE EXCEPTION 'New place overlaps with an existing place';
    END IF;
    RETURN NEW;
END;
$function$
;


-- Triggers
CREATE TRIGGER check_place_overlap_trigger
BEFORE INSERT ON place
FOR EACH ROW
EXECUTE FUNCTION public.check_place_overlap();
