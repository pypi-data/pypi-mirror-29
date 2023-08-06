#!/usr/bin/env python3


import asyncio
import atexit
import threading

from gv_application.application import GVApplication, run_in_thread, stop
from gv_rpc.client import Client
from .settings import *


class Fake(GVApplication):

    def __init__(self):
        super().__init__('fake', '/Users/vadimbertrand/Work/gtl-ville/gv-common/fake.log')
        self.rpcclient = None

    def init_from_thread(self, loop, redisaddr):
        super().init_from_thread(loop, redisaddr)
        self.__set_rpcclient(RPC_DB_CHANNEL)
        asyncio.ensure_future(self.__rpc_calls())
        super().run()

    def __set_rpcclient(self, channelname):
        if self.redispool is None:
            self.logger.error('No redis pool. return.')
            return

        self.rpcclient = Client(self.loop, self.redispool, channelname)

    async def __rpc_calls(self):
        cp = await self.rpcclient.get_cp()
        print(('cp', cp))


# Create and run application in a background thread
fake = Fake()
threading.Thread(target=run_in_thread,
                 args=(fake, ('127.0.0.1', 6379)),
                 daemon=True).start()

# Register exit cleanup
atexit.register(stop, fake)

print('Asyncio background thread started.')
print('To gracefully close the application use exit() command or CTRL-C interrupt')
