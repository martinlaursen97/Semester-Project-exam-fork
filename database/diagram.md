---
title: RPG example
---
erDiagram
    User {
        int user_id pk
        string first_name
        string last_name
        string email
        string password
        datetime created_at
        }



    Relation {
        int relation_id pk
        int user1_id fk
        int user2_id fk
        datetime created_at

    }


    Character {
        int character_id pk
        int class_id fk
        int user_id fk
        string gender_id fk
        string character_name
        bool alive
        int level
        int xp
        int money
        datetime created_at
    }

    Class {
        int class_id pk
        string class_name
    }

    Gender {
        int gender_id pk
        string gender_type
    }

    Attributes {
        int attribute_id pk
        string attribute_name
        string description
    }


    Character_attribute {
        int character_attribute_id pk
        int character_id fk
        int attribute_id fk
        int value
    }

    Place {
        int plance_id
        string place_name
    }


    Location {
        int location_id pk
        int x
        int y
        int place_id fk
    }



    Character_location{
        int character_location_id pk
        int character_id fk
        int location_id fk
    }

    Ability_type {
        int ability_type_id pk
        string ability_name
        string description
    }

    Ability {
        int ability_id pk
        string name
        int ability_type_id fk
    }

    Class_ability {
        int class_ability_id pk
        int class_id fk
        int ability_id fk
    }



    User |o--o{ Character : has
    Class |o--o{ Character : can_be
    Gender |o--o{ Character : can_be

    Character_attribute |o--o{Character: has
    Character_attribute |o--o{Attributes: has

    Place |o--o{ Location: has
    Character_location |o--o{ Location: is_in
    Character_location |o--o{ Character: is_in

    Ability |o--o{ Class_ability: has
    Class |o--o{ Class_ability: has
    Ability_type |o--o{ Ability: has

    User |o--o{ Relation : has
    User |o--o{ Relation : has_
