import graphene
from graphene_django import DjangoObjectType
from posts.models import Post
from graphql import GraphQLError
from core.helpers import requires_authentication, get_user, get_decoded_user_id
from users.schema import UserType


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'date_created']


class Query(graphene.ObjectType):
    list_all_posts = graphene.List(PostType)
    list_my_posts = graphene.List(PostType)
    list_users_posts = graphene.List(PostType, id=graphene.ID(required=True))

    @requires_authentication
    def resolve_list_all_posts(self, info):
        return Post.objects.all()

    @requires_authentication
    def resolve_list_my_posts(self, info):
        user_id = info.context.user.id
        user = get_user(user_id)
        return Post.objects.filter(user=user)

    @requires_authentication
    def resolve_list_users_posts(self, info, id):
        user_id = get_decoded_user_id(id)
        user = get_user(user_id)
        return Post.objects.filter(user=user)


class CreatePost(graphene.Mutation):
    class Arguments:
        content = graphene.String(required=True)

    user = graphene.Field(UserType)
    post = graphene.Field(PostType)

    @requires_authentication
    def mutate(self, info, content):
        user_id = info.context.user.id
        user = get_user(user_id)

        post = Post(user=user, content=content)
        post.save()
        return CreatePost(user=user, post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)
        content = graphene.String()

    user = graphene.Field(UserType)
    post = graphene.Field(PostType)

    def mutate(self, info, post_id, **kwargs):
        user_id = info.context.user.id
        user = get_user(user_id)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise GraphQLError('Post not found.')

        for field, value in kwargs.items():
            if value is not None:
                setattr(post, field, value)
        post.save()
        return UpdatePost(user=user, post=post)


class DeletePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)

    success = graphene.Boolean()

    @requires_authentication
    def mutate(self, info, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise GraphQLError('Post not found.')

        post.delete()
        return DeletePost(success=True)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
