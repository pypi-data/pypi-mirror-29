#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

import asyncio
import logging
import functools

from uamqp import receiver



_logger = logging.getLogger(__name__)


class MessageReceiverAsync(receiver.MessageReceiver):

    async def __aenter__(self):
        await self.open_async()
        return self

    async def __aexit__(self, *args):
        await self._destroy_async()

    async def _destroy_async(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, functools.partial(self._destroy))

    async def open_async(self, on_message_received):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, functools.partial(self.open, on_message_received))

    async def close_async(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, functools.partial(self.close))
