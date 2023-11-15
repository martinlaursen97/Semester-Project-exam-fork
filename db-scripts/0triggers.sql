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