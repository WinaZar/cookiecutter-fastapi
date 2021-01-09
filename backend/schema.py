from typing import List

import graphene
from fastapi import Request
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql.execution.base import ResolveInfo
from sqlalchemy import select
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession

from backend.db.models import User


async def _get_engine(info: ResolveInfo) -> AsyncEngine:
    request: Request = info.context["request"]
    return request.app.state.engine


class UserSchema(SQLAlchemyObjectType):
    class Meta:
        model = User
        exclude_fields = ["password"]


class RootQuery(graphene.ObjectType):
    all_users = graphene.List(UserSchema)

    async def resolve_all_users(self, info: ResolveInfo) -> List[User]:
        engine = await _get_engine(info)
        async with AsyncSession(engine) as session:
            query_result = await session.execute(select(User))
        users: List[User] = query_result.scalars().fetchall()
        return users


schema = graphene.Schema(query=RootQuery, auto_camelcase=False)
