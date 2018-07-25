import contextvars
import asyncio

var = contextvars.ContextVar("var", default="default")


async def main():
    var.set("init")
    token = var.set("main")
    task = asyncio.create_task(sub())
    await task
    assert var.get() == "main"
    var.reset(token)
    assert var.get() == "init"


async def sub():
    await asyncio.sleep(.1)

    assert var.get() == "main"

    var.set("sub")


def test():
    asyncio.run(main())
