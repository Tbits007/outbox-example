from dishka import AnyOf, Provider, Scope, provide

from app.application.interactors.user_interactors import GetUserInteractor, UpdateUserInteractor
from app.application.interfaces import user_interface
from app.infrastructure.adapters.user_gateway import UserGateway


class UserProvider(Provider):
    user_gateway = provide(
        UserGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            user_interface.UserReader,
            user_interface.UserSaver,
            user_interface.UserUpdater,
        ],
    )

    get_user_interactor = provide(GetUserInteractor, scope=Scope.REQUEST)
    update_user_Interactor = provide(UpdateUserInteractor, scope=Scope.REQUEST)
