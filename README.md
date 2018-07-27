# PEP 567 -- Context Variables Test

1. 介绍PEP
2. PEP 550 and PEP 568
3. asyncio today & tomorrow

## References

* [PEP 567](https://www.python.org/dev/peps/pep-0567/)
* [contextvars' python implementation](https://github.com/MagicStack/contextvars)
* [immutables](https://github.com/MagicStack/immutables)
* [HAMT](https://en.wikipedia.org/wiki/Hash_array_mapped_trie)
* [pydecimal](https://github.com/python/cpython/blob/master/Lib/_pydecimal.py)
* [CPython context](https://github.com/python/cpython/blob/41cb0baea96a80360971908a0bd79d9d40dd5e44/Python/context.c)
* [asyncio](https://speakerdeck.com/1st1/asyncio-today-and-tomorrow)
* [Python post-Guido](https://lwn.net/Articles/759756/)

## Introduction

* ContextVar 的名字叫做上下文变量，含义在于变量的值是上下文相关的，在不同的上下文中，同一个变量可以具有不同的值。
* threading.local() 是线程上下文变量，在不同的线程中，local对象具有不同的值。一个线程中改变对象的值不会影响其他线程中该对象的值。
* PEP 567 是为了解决 threading.local() 只支持线程上下文，而不支持异步任务中上下文而提出。或者说，在协程环境下面，Python 没有一个安全的变量，能够在协程任务之间保持独立，不受其他协程执行的影响。

~~~Python
"threading.local don't work well with asyncio"
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

```Python
class Context:
    def run(self, callable, *args, **kwargs):
        ...

    def copy(self):
        ...

    def __getitem__(self, var):
        ...

    def __contains__(self, var):
        ...


class ContextVar:
    def get(self):
        ...

    def set(self, value):
        ...

    def reset(self, token):
        ...


def copy_context():
    ...
```

## Implementation

* immutables（持久化数据结构）
* COW
* HAMT
