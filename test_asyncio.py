import asyncio
import contextvars

var = contextvars.ContextVar("var")


async def main():
    var.set("main")
    task = asyncio.create_task(sub())
    assert var.get() == "main"
    var.set("main changed")
    await task


async def sub():
    await asyncio.sleep(.1)

    assert var.get() == "main"

    var.set("sub")


def test():
    asyncio.run(main())
