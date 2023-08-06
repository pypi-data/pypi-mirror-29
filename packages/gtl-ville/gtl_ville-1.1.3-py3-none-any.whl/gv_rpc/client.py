#!/usr/bin/env python3


import json
import secrets
import string

import aioredis

import gv_rpc.settings as rpc_settings


def random_string():
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))


class RpcWrapper:

    def __init__(self, remote_call, *args, **kwargs):
        self.remote_call = remote_call
        self.funcname = args[:]
        self.kwargs = kwargs.copy()

    def __call__(self, *args, **kwargs):
        if kwargs and self.kwargs:
            kw = self.kwargs.copy()
            kw.update(kwargs)
        else:
            kw = kwargs or self.kwargs
        return self.remote_call(*(self.funcname + args), **kw)


class Client:

    def __init__(self, loop, redispool, channelname):
        self.loop = loop
        self.redispool = redispool
        self.channelname = channelname

    async def __redis_call(self, funcname, *args, **kwargs):
        key = random_string()
        replychannel = aioredis.pubsub.Receiver(loop=self.loop)
        await self.redispool.subscribe(replychannel.channel(self.channelname + ':' + key))

        with await self.redispool as pub:
            await pub.publish_json(
                self.channelname,
                {'function': funcname, 'args': args, 'kwargs': kwargs, 'key': key}
            )

        data = None
        if await replychannel.wait_message():
            data = (await replychannel.get(encoding='UTF-8', decoder=json.loads))[1].get('data')

        replychannel.stop()
        return data

    def __getattr__(self, funcname):
        return RpcWrapper(self.__redis_call, funcname)


class DbClient(Client):

    def __init__(self, loop, redispool):
        super().__init__(loop, redispool, rpc_settings.RPC_DB_CHANNEL)
