import graphene
from graphene_django import DjangoObjectType
from pets.models import Pet
from graphql import GraphQLError
from core.helpers import requires_authentication, get_decoded_user_id, get_user
from pets.helpers import verify_breed_is_allowed


class PetType(DjangoObjectType):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'breed', 'age']


class Query(graphene.ObjectType):
    list_users_pets = graphene.List(PetType, id=graphene.ID(required=True))

    @requires_authentication
    def resolve_list_users_pets(self, info, id):
        user_id = get_decoded_user_id(id)
        owner = get_user(user_id)
        return Pet.objects.filter(owner=owner)


class CreatePet(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        breed = graphene.String(required=True)
        age = graphene.Int(required=True)

    pet = graphene.Field(PetType)

    @requires_authentication
    def mutate(self, info, name, breed, age):
        verify_breed_is_allowed(breed)

        owner_id = info.context.user.id
        owner = get_user(owner_id)

        pet = Pet(owner=owner, name=name, breed=breed, age=age)
        pet.save()
        return CreatePet(pet=pet)


class UpdatePet(graphene.Mutation):
    class Arguments:
        pet_id = graphene.ID(required=True)
        name = graphene.String()
        breed = graphene.String()
        age = graphene.Int()

    pet = graphene.Field(PetType)

    @requires_authentication
    def mutate(self, info, pet_id, **kwargs):
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            raise GraphQLError('Pet not found.')

        for field, value in kwargs.items():
            if field == 'breed':
                verify_breed_is_allowed(value)
            if value is not None:
                setattr(pet, field, value)
        pet.save()
        return UpdatePet(pet=pet)


class DeletePet(graphene.Mutation):
    class Arguments:
        pet_id = graphene.ID(required=True)

    success = graphene.Boolean()

    @requires_authentication
    def mutate(self, info, pet_id):
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            raise GraphQLError('Pet not found.')

        pet.delete()
        return DeletePet(success=True)


class Mutation(graphene.ObjectType):
    create_pet = CreatePet.Field()
    update_pet = UpdatePet.Field()
    delete_pet = DeletePet.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
