from typing import Any

import graphene


class RootQuery(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    async def resolve_hello(self, info: Any, name: str) -> str:
        return "Hello " + name


schema = graphene.Schema(query=RootQuery, auto_camelcase=False)
