from dishka import AnyOf, Provider, Scope, provide

from app.application.interactors.outbox_interactor import OutboxRelayInteractor
from app.application.interfaces import outbox_interface
from app.infrastructure.adapters.outbox_gateway import OutboxGateway


class OutboxProvider(Provider):
    outbox_gateway = provide(
        OutboxGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            outbox_interface.OutboxReader,
            outbox_interface.OutboxSaver,
            outbox_interface.OutboxUpdater,
        ],
    )

    outbox_interactor = provide(OutboxRelayInteractor, scope=Scope.REQUEST)
