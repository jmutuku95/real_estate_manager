from api.views.auth import AuthResource
from api.views.board import BoardResource, BoardMembersResource
from api.views.conversation import ConversationResource
from api.views.estate import EstateResource
from api.views.message import MessageResource
from api.views.role import RoleResource, RoleUsersResource
from api.views.user import (
    UserResource, UserRolesResource, UserWalletResource, UserBoardsResource)
from api.views.welcome import WelcomeResource


def add_resources(api):
    """
    Add API resources to routes.
    """

    api.add_resource(
        AuthResource,
        '/api/v1/signin',
        '/api/v1/signin/')

    api.add_resource(
        BoardResource,
        '/api/v1/boards',
        '/api/v1/boards/',
        '/api/v1/boards/<int:board_id>',
        '/api/v1/boards/<int:board_id>/')

    api.add_resource(
        BoardMembersResource,
        '/api/v1/boards/<int:board_id>/members',
        '/api/v1/boards/<int:board_id>/members/'
    )

    api.add_resource(
        ConversationResource,
        '/api/v1/conversations',
        '/api/v1/conversations/',
        '/api/v1/conversations/<int:conversation_id>',
        '/api/v1/conversations/<int:conversation_id>/')

    api.add_resource(
        EstateResource,
        '/api/v1/estates/<int:estate_id>',
        '/api/v1/estates/<int:estate_id>')

    api.add_resource(
        MessageResource,
        '/api/v1/conversations/<int:conversation_id>/messages',
        '/api/v1/conversations/<int:conversation_id>/messages/',
        '/api/v1/conversations/<int:conversation_id>/messages/<int:message_id>',
        '/api/v1/conversations/<int:conversation_id>/messages/<int:message_id>/')

    api.add_resource(
        RoleResource,
        '/api/v1/roles',
        '/api/v1/roles/',
        '/api/v1/roles/<int:role_id>',
        '/api/v1/roles/<int:role_id>/')

    api.add_resource(
        RoleUsersResource,
        '/api/v1/roles/<int:role_id>/users',
        '/api/v1/roles/<int:role_id>/users/')

    api.add_resource(
        UserResource,
        '/api/v1/users',
        '/api/v1/users/',
        '/api/v1/users/<int:user_id>',
        '/api/v1/users/<int:user_id>/')

    api.add_resource(
        UserBoardsResource,
        '/api/v1/users/<int:user_id>/boards',
        '/api/v1/users/<int:user_id>/boards/')

    api.add_resource(
        UserRolesResource,
        '/api/v1/users/<int:user_id>/roles',
        '/api/v1/users/<int:user_id>/roles/')

    api.add_resource(
        UserWalletResource,
        '/api/v1/users/<int:user_id>/wallet',
        '/api/v1/users/<int:user_id>/wallet/')

    api.add_resource(
        WelcomeResource,
        '/',
        '/api/v1',
        '/api/v1/'
    )
    return api
