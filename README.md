# PEP 567 -- Context Variables

## References

* [PEP 567](https://www.python.org/dev/peps/pep-0567/)
* [contextvars python 实现](https://github.com/MagicStack/contextvars)
* [immutables](https://github.com/MagicStack/immutables)
* [HAMT](https://en.wikipedia.org/wiki/Hash_array_mapped_trie)
* [pydecimal](https://github.com/python/cpython/blob/master/Lib/_pydecimal.py)
* [cpython context](https://github.com/python/cpython/blob/41cb0baea96a80360971908a0bd79d9d40dd5e44/Python/context.c)

## Introduction

~~~Python
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
    await asyncio.sleep(1)

    assert local.var == "main changed"

    local.var = "sub"


def test():
    asyncio.run(main())
~~~

## Usage
