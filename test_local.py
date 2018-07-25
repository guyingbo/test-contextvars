import threading
import asyncio

local = threading.local()


async def main():
    local.var = "main"
    task = asyncio.create_task(sub())
    assert local.var == "main"
    local.var = "main changed"
    await task


async def sub():
    await asyncio.sleep(.1)

    assert local.var == "main changed"

    local.var = "sub"


def test():
    asyncio.run(main())
