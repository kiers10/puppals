# import graphene
# from graphene_django.utils import get_schema
# from users.schema import Query as UsersQuery, Mutation as UsersMutation
# from pets.schema import Query as PetsQuery, Mutation as PetsMutation

# # Combine the queries from all apps
# queries = [
#     UsersQuery,
#     PetsQuery,
# ]

# # Combine the mutations from all apps
# mutations = [
#     UsersMutation,
#     PetsMutation,
# ]

# schema = get_schema()
# schema = graphene.Schema(query=queries, mutation=mutations)
