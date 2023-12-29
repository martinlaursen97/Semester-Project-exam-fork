| Endpoint                                         | Method   | Summary                 | Description                                      |
|:-------------------------------------------------|:---------|:------------------------|:-------------------------------------------------|
| /api/postgres/auth/login-email                   | POST     | Login                   | Login by email and password.                     |
| /api/postgres/auth/register                      | POST     | Register                | Register by email and password.                  |
| /api/postgres/auth/forgot-password               | POST     | Forgot Password         | Forgot password.                                 |
| /api/postgres/auth/reset-password                | POST     | Reset Password          | Reset password.                                  |
| /api/postgres/base-users                         | DELETE   | Delete Current User     | Delete current user.                             |
| /api/postgres/characters                         | GET      | Characters Me           | My characters.                                   |
| /api/postgres/characters                         | POST     | Create Character        | Create character.                                |
| /api/postgres/characters/place/{character_id}    | GET      | Character Place Details | Get place of character.                          |
| /api/postgres/character-locations/{character_id} | PATCH    | Move Character          | Move character.                                  |
| /api/postgres/base-classes                       | GET      | Get Classes             | Get all classes.                                 |
| /api/postgres/places                             | GET      | Get Places              | Get all places.                                  |
| /api/postgres/places                             | POST     | Create Place            | Create place.                                    |
| /api/neo4j/auth/register                         | POST     | Register                | Register by email and password.                  |
| /api/neo4j/auth/login-email                      | POST     | Login                   | Login by email and password.                     |
| /api/neo4j/auth/forgot-password                  | POST     | Forgot Password         | Forgot password.                                 |
| /api/neo4j/auth/reset-password                   | POST     | Reset Password          | Reset password.                                  |
| /api/neo4j/relations                             | POST     | Create Friend Request   | Create friend request.                           |
| /api/neo4j/characters                            | GET      | Characters Me           | Get characters for logged in user.               |
| /api/neo4j/characters                            | POST     | Create Character        | Create character.                                |
| /api/neo4j/characters/{character_id}             | PATCH    | Update Character        | Update character.                                |
| /api/neo4j/characters/{character_id}             | DELETE   | Delete Character        | Delete character if user owns.                   |
| /api/neo4j/items/                                | POST     | Add Item                | Create an item in the db.                        |
| /api/neo4j/items/character                       | POST     | Add Item To Character   | Add item to character.                           |
| /api/neo4j/items/equip                           | POST     | Equip Item To Character | Equip item to character.                         |
| /api/neo4j/items/{character_id}/items            | GET      | Get Character Items     | Return items on character.                       |
| /api/mongodb/auth/login-email                    | POST     | Login                   | Login by email and password.                     |
| /api/mongodb/auth/register                       | POST     | Register                | Create a new user.                               |
| /api/mongodb/auth/me                             | GET      | Get Me                  | Get the current user.                            |
| /api/mongodb/base-users/add-friend               | POST     | Add Friend              | Add a friend to the current user.                |
| /api/mongodb/base-users/remove-friend            | DELETE   | Remove Friend           | Remove a friend from the current user.           |
| /api/mongodb/characters                          | POST     | Create Character        | Create a character for the current user.         |
| /api/mongodb/base-classes                        | POST     | Create Class            | Create a class for the current user.             |
| /api/mongodb/base-classes/{class_id}/add-ability | PATCH    | Add Ability             | Add an ability to a class.                       |
| /api/monitoring/health                           | GET      | Health Check            | Checks the health of a project.                  |
|                                                  |          |                         |                                                  |
|                                                  |          |                         | It returns 200 if the project is healthy.        |
| /api/monitoring/health-mongodb                   | GET      | Mongodb Check           | Checks the health of the mongodb.                |
|                                                  |          |                         |                                                  |
|                                                  |          |                         | It returns 200 if the mongodb is healthy.        |
| /api/monitoring/health-neo4j                     | GET      | Neo4J Check             | Checks the health of the Neo4j database.         |
|                                                  |          |                         |                                                  |
|                                                  |          |                         | It returns 200 if the Neo4j database is healthy. |