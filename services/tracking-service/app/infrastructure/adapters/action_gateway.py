import dataclasses

import motor.motor_asyncio
from bson import ObjectId

from app.application.interfaces.action_interface import ActionReader, ActionSaver
from app.domain.entities.action_entity import Action


class ActionGateway(
    ActionSaver,
    ActionReader,
):
    def __init__(
        self,
        collection: motor.motor_asyncio.AsyncIOMotorCollection,
    ) -> None:
        self.collection = collection

    async def save(self, action: Action) -> Action | None:
        action_dict = dataclasses.asdict(action)
        if "_id" in action_dict and action_dict["_id"] is None:
            del action_dict["_id"]
        result = await self.collection.insert_one(action_dict)
        if result.inserted_id:
            action._id = str(result.inserted_id)
            return action
        return None

    async def read_by_id(self, _id: str) -> Action | None:
        action_data = await self.collection.find_one({"_id": ObjectId(_id)})
        if action_data:
            return Action(**action_data)
        return None
