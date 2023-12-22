-- Base users
INSERT INTO base_user (id, email, password, status, created_at) 
SELECT gen_random_uuid(), i::text, i::text, 'active', now()  -- Note that the password is not hashed
FROM generate_series(1, 100) as t(i);


-- Relations
-- This will create:
-- * 3 relations for each base user
DO $$
DECLARE 
    user_id UUID;
BEGIN
    FOR user_id IN SELECT id FROM base_user LOOP
        FOR i IN 1..3 LOOP
            INSERT INTO relation (id, user1_id, user2_id, created_at)
            SELECT 
                gen_random_uuid(), 
                user_id, 
                (SELECT id FROM base_user WHERE id != user_id ORDER BY RANDOM() LIMIT 1), 
                now()
            ON CONFLICT (user1_id, user2_id) DO NOTHING;
        END LOOP;
    END LOOP;
END 
$$;


-- Abilities and ability types
-- This will create:
-- * 5 ability types
-- * 5 abilities for each ability type
WITH at AS (
    INSERT INTO ability_type (id, name, description, created_at)
    SELECT gen_random_uuid(), md5(random()::text), md5(random()::text), now()
    FROM generate_series(1, 5) as i
    RETURNING id
)
INSERT INTO ability (id, name, description, ability_type_id, created_at)
SELECT gen_random_uuid(), md5(random()::text), md5(random()::text), at.id, now()
FROM at
CROSS JOIN generate_series(1, 5) as i;


-- Base classes
-- This will create:
-- * 5 base classes
INSERT INTO base_class (id, name, description, created_at)
VALUES (gen_random_uuid(), 'Warrior', 'A strong and powerful warrior', now()),
       (gen_random_uuid(), 'Mage', 'A wise and powerful mage', now()),
       (gen_random_uuid(), 'Rogue', 'A sneaky and powerful rogue', now()),
       (gen_random_uuid(), 'Priest', 'A holy and powerful priest', now()),
       (gen_random_uuid(), 'Paladin', 'A holy and powerful paladin', now());


-- Class abilities
-- This will create:
-- * 5 class abilities for each base class
INSERT INTO class_ability (id, base_class_id, ability_id, created_at)
SELECT gen_random_uuid(), bc.id, a.id, now()
FROM base_class bc
CROSS JOIN ability a;


-- Character locations
-- This will create:
-- * 300 character locations
INSERT INTO character_location (id, x, y, created_at)
SELECT gen_random_uuid(), (random() * 1000)::int, (random() * 1000)::int, now()
FROM generate_series(1, 300) as i;


-- Characters
-- This will create:
-- * 3 characters for each base user
WITH bu AS (
    SELECT id FROM base_user
)
INSERT INTO character (
    id, gender, character_name, alive, level, xp, money, 
    base_class_id, user_id, character_location_id, created_at
)
SELECT gen_random_uuid(), 'male', md5(random()::text), true, 1, 0, 0, 
    (SELECT id FROM base_class ORDER BY RANDOM() LIMIT 1), bu.id, null, now()
FROM base_user bu
CROSS JOIN generate_series(1, 3) as i;


-- Attributes
-- This will create:
-- * 5 attributes
INSERT INTO attribute (id, name, description, created_at)
VALUES (gen_random_uuid(), 'Strength', 'Strength is a measure of physical power', now()),
       (gen_random_uuid(), 'Agility', 'Agility is a measure of physical finesse', now()),
       (gen_random_uuid(), 'Intellect', 'Intellect is a measure of mental power', now()),
       (gen_random_uuid(), 'Spirit', 'Spirit is a measure of faith and willpower', now()),
       (gen_random_uuid(), 'Stamina', 'Stamina is a measure of physical endurance', now());


-- Character attributes
-- This will create:
-- * 5 character attributes for each character
INSERT INTO character_attribute (id, value, character_id, attribute_id, created_at)
SELECT gen_random_uuid(), (random() * 100)::int, c.id, a.id, now()
FROM character c
CROSS JOIN attribute a;

-- Places
-- This will create:
-- * 5 non-overlapping places
INSERT INTO place(id, name, description, radius, x, y, created_at)
VALUES
    (gen_random_uuid(), 'Stormwind', 'The capital of the Alliance', 50, 50, 50, now()),
    (gen_random_uuid(), 'Ironforge', 'The capital of the Dwarves', 40, -110, -100, now()),
    (gen_random_uuid(), 'Darnassus', 'The capital of the Night Elves', 30, -200, 200, now()),
    (gen_random_uuid(), 'Exodar', 'The capital of the Draenei', 60, 150, -180, now()),
    (gen_random_uuid(), 'Orgrimmar', 'The capital of the Horde', 70, -25, 200, now());