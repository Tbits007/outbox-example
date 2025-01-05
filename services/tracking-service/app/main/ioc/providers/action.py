from dishka import AnyOf, Provider, Scope, provide

from app.application.interactors.action_interactors import CreateActionInteractor, GetActionInteractor
from app.application.interfaces import action_interface
from app.infrastructure.adapters.action_gateway import ActionGateway


class ActionProvider(Provider):
    action_gateway = provide(
        ActionGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            action_interface.ActionReader,
            action_interface.ActionSaver,
        ],
    )

    get_action_interactor = provide(GetActionInteractor, scope=Scope.REQUEST)
    create_action_interactor = provide(CreateActionInteractor, scope=Scope.REQUEST)
