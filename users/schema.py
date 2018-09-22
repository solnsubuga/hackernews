import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String()
        username = graphene.String()
        password = graphene.String()

    def mutate(self, info, email, username, password):
        user = get_user_model()(
            email=email,
            username=username,
        )

        user.set_password = password
        user.save()
        return CreateUser(user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()
