import strawberry
from fastapi import APIRouter
from strawberry.asgi import GraphQL

from service.app.generic.graphql.graphql_service import Query, Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app: GraphQL = GraphQL(schema)

routes = APIRouter()
routes.add_route("/graphql", graphql_app)
routes.add_websocket_route("/graphql", graphql_app)
