#!/usr/bin/env python3


import asyncio
import functools

import gv_rpc.settings as rpc_settings


class Connector:

    def __init__(self, exposedobject, loop, redispool, channelname):
        self.localobject = exposedobject
        self.loop = loop
        self.redispool = redispool
        self.channelname = channelname
        asyncio.ensure_future(self.__listen_for_calls())

    async def __listen_for_calls(self):
        requestchannel = (await self.redispool.subscribe(self.channelname))[0]
        while await requestchannel.wait_message():
            call = await requestchannel.get_json()
            asyncio.ensure_future(self.__call_received(call))

    async def __call_received(self, call):
        data = await self.loop.run_in_executor(None,
                                               functools.partial(
                                                   self.__remote_to_local(call.get('function', '')),
                                                   *call.get('args', []), **call.get('kwargs', {})
                                               )
        )
        with await self.redispool as pub:
            await pub.publish_json(
                self.channelname + ':' + call.get('key'),
                {'data': data}
            )

    def __remote_to_local(self, funcname):
        try:
            func = getattr(self.localobject, funcname)
        except AttributeError:
            func = Connector.__idle
        return func

    @staticmethod
    def __idle():
        return None


class DbConnector(Connector):

    def __init__(self, exposedobject, loop, redispool):
        super().__init__(exposedobject, loop, redispool, rpc_settings.RPC_DB_CHANNEL)
