from typing import List, Optional

import graphene
from fastapi import Request
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql.execution.base import ResolveInfo
from sqlalchemy import select
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession

from backend.db.models import User


async def _get_engine(info: ResolveInfo) -> AsyncEngine:
    request: Request = info.context["request"]  # type: ignore
    return request.app.state.engine


class UserSchema(SQLAlchemyObjectType):
    class Meta:
        model = User
        exclude_fields = ["password"]


class UsersQuery(graphene.ObjectType):
    users = graphene.List(UserSchema, ids=graphene.List(graphene.Int))

    async def resolve_users(
        self, info: ResolveInfo, ids: Optional[List[int]] = None
    ) -> List[User]:
        engine = await _get_engine(info)
        statement = select(User)
        if ids:
            statement = statement.filter(User.id.in_(ids))
        async with AsyncSession(engine) as session:
            query_result = await session.execute(statement)
        users: List[User] = query_result.scalars().fetchall()
        return users


class RootQuery(UsersQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=RootQuery, auto_camelcase=False)
