CREATE OR REPLACE FUNCTION create_character_location()
RETURNS TRIGGER AS $$
DECLARE
    new_location_id UUID;
BEGIN
    -- Create a new CharacterLocation entry with the supplied id
    INSERT INTO character_location (id, x, y, created_at)
    VALUES (NEW.id, 0, 0, NOW());

    -- Update the character_location_id in the character table
    UPDATE character
    SET character_location_id = NEW.id
    WHERE id = NEW.id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER character_insert_trigger
AFTER INSERT
ON character
FOR EACH ROW
EXECUTE FUNCTION create_character_location();

CREATE OR REPLACE FUNCTION public.calculate_distance(x1 integer, y1 integer, x2 integer, y2 integer)
	RETURNS double precision
	LANGUAGE plpgsql
AS $function$
BEGIN
	RETURN sqrt((x2 - x1) ^ 2 + (y2 - y1) ^ 2);
END;
$function$
;


CREATE OR REPLACE FUNCTION public.get_character_location(c_id UUID)
	RETURNS TABLE(character_id UUID, x integer, y integer)
	LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY (
        SELECT
            c.id,
            cl.x,
            cl.y
        FROM character_location cl
        JOIN character c on cl.id = c.id
        where c.id = c_id
    );
END
$function$
;



CREATE OR REPLACE FUNCTION public.get_character_place(c_id UUID)
RETURNS VARCHAR(50)
LANGUAGE plpgsql
AS $function$
DECLARE
    character_location RECORD;
    character_place VARCHAR(50);
BEGIN
    SELECT character_id, x, y
    INTO character_location
    FROM public.get_character_location(c_id);

    IF character_location IS NULL THEN
        RETURN 'Wilderness';
    ELSE
        SELECT name
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
        AND public.calculate_distance(NEW.x, NEW.y, p.x, p.y) <= NEW.radius + p.radius
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


-- Views
CREATE OR REPLACE VIEW character_details_view AS
SELECT
    c.id AS character_id,
    c.character_name,
    c.gender AS gender,
    bc.name AS class_name,
    public.get_character_place(c.id) AS place_name,
    c.alive,
    c.level,
    c.xp,
    c.money
FROM
    character c
JOIN
    base_class bc ON c.base_class_id = bc.id;
    
-- Stored Procedures
CREATE OR REPLACE PROCEDURE sp_insert_relation(p_user1_id UUID, p_user2_id UUID)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_user1_id = p_user2_id THEN
        RAISE NOTICE 'A user can''t be in a relation with itself.';
        RETURN;
    END IF;
    -- Check relation already exists
    IF NOT EXISTS (SELECT 1 FROM relation WHERE (user1_id = p_user1_id AND user2_id = p_user2_id) OR (user1_id = p_user2_id AND user2_id = p_user1_id)) THEN
        INSERT INTO relation (user1_id, user2_id, created_at) VALUES (p_user1_id, p_user2_id, CURRENT_DATE);
    ELSE
        RAISE NOTICE 'The relation already exists between user1_id % and user2_id %', p_user1_id, p_user2_id;
    END IF;
END;
$$;