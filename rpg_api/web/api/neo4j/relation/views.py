from fastapi import APIRouter
from rpg_api.db.neo4j.dependencies import Neo4jSession
from rpg_api.web.dtos.neo4j.neo4j_dtos import (
    NeoBaseUserDTO,
    NeoUserCreateDTO,
)
from rpg_api.web.daos.base_user_dao import NeoBaseUserDAO
from rpg_api.utils import dtos
from rpg_api.web.api.neo4j.auth.auth_dependencies import GetCurrentUser
from rpg_api import exceptions as rpg_exc
from rpg_api.services.email_service.email_dependencies import GetEmailService
from rpg_api.web.api.neo4j.auth.token_store import token_store
from rpg_api.settings import settings
from datetime import datetime


router = APIRouter()


@router.post(
    "",
)
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
