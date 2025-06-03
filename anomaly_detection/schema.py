import graphene
from model.schema import Query as model_query
from model.schema import Mutation as model_mutation

class Query(model_query, graphene.ObjectType):
    pass

class Mutation(model_mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)