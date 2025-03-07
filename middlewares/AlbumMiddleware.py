import asyncio
from typing import Callable, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message


# Middleware for handler receive photos album
class AlbumMiddleware(BaseMiddleware):

    def __init__(self, latency: Union[int, float] = 0.1):

        # init latency and album data dictionary
        self.latency = latency
        self.album_data = {}

    # main middleware logic
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]
    ) -> Any:

        # if event hasn't media group, pass it
        if not event.media_group_id:
            return await handler(event, data)

        # collect messages of the same media group
        total_before = self.collect_album_message(event)

        # wait for a specified latency time
        await asyncio.sleep(self.latency)

        # check the total number of messages after latency
        total_after = len(self.album_data[event.media_group_id]["messages"])

        # if new messages were added during the latency. exit
        if total_after != total_before:
            return

        # sort the album messages by message_id and add to data
        album_messages = self.album_data[event.media_group_id]["messages"]
        album_messages.sort(key=lambda x: x.message_id)
        data["album"] = album_messages

        # call the original handler with custom data["album"]
        await handler(event, data)

        # remove the media group from tracking to free up memory
        del self.album_data[event.media_group_id]

    def collect_album_message(self, event: Message):

        # checking if media group exists in album data
        if event.media_group_id not in self.album_data:

            # create a new entity for the media group
            self.album_data[event.media_group_id] = {"messages": []}

        # append the new message to the media group
        self.album_data[event.media_group_id]["messages"].append(event)

        # return the total number of messages in the current media group
        return len(self.album_data[event.media_group_id]["messages"])
