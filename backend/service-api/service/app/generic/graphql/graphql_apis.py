import strawberry
from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter

from service.app.generic.graphql.graphql_service import Query, Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app: GraphQLRouter = GraphQLRouter(schema)

routes = APIRouter()
routes.include_router(graphql_app, prefix="/graphql")
