from fastapi import APIRouter
from rpg_api.db.neo4j.dependencies import Neo4jSession
from rpg_api.web.daos.base_user_dao import NeoBaseUserDAO
from rpg_api.utils import dtos
from rpg_api.web.api.neo4j.auth.auth_dependencies import GetCurrentUser
from rpg_api import exceptions as rpg_exc


router = APIRouter()


@router.post("", status_code=201)
async def create_friend_request(
    current_user: GetCurrentUser,
    session: Neo4jSession,
    input_dto: dtos.NeoBaseUserRelationshipInputDTO,
) -> dtos.EmptyDefaultResponse:
    """Create friend request."""
    dao = NeoBaseUserDAO(session=session)

    try:
        await dao.create_relationship(
            rel_dto=dtos.NeoBaseUserRelationshipDTO(
                node1_id=int(current_user.id),
                node2_id=input_dto.friend_id,
                relationship_type=input_dto.relationship_type,
                relationship_props=input_dto.relationship_props,
            )
        )
    except Exception as e:
        print(e)
        raise rpg_exc.HttpUnprocessableEntity()

    return dtos.EmptyDefaultResponse()
