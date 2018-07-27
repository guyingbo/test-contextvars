import contextvars
from decimal import Decimal, getcontext, localcontext
import asyncio


def test_decimal():
    getcontext().prec = 6
    r = Decimal(1) / Decimal(7)
    assert str(r) == "0.142857"


def fractions(precision, x, y):
    with localcontext() as ctx:
        ctx.prec = precision
        yield Decimal(x) / Decimal(y)
        yield Decimal(x) / Decimal(y)


def test_fractions():
    g1 = fractions(precision=2, x=1, y=3)
    g2 = fractions(precision=4, x=2, y=3)
    items = list(zip(g1, g2))
    items = [str(y) for x in items for y in x]
    print("frac2:", items)
    assert items == ["0.33", "0.6667", "0.3333", "0.6667"]


class ContextGenerator:
    def __init__(self, gen):
        self.gen = gen
        self.context = contextvars.copy_context()

    def __next__(self):
        return self.context.run(self.gen.__next__)

    def __iter__(self):
        return self


def fractions2(precision, x, y):
    with localcontext() as ctx:
        ctx.prec = precision
        yield Decimal(x) / Decimal(y)
        yield Decimal(x) / Decimal(y)


def test_fractions2():
    g1 = ContextGenerator(fractions(precision=2, x=1, y=3))
    g2 = ContextGenerator(fractions(precision=4, x=2, y=3))
    items = list(zip(g1, g2))
    items = [str(y) for x in items for y in x]
    print("frac2:", items)
    assert items == ["0.33", "0.6667", "0.33", "0.6667"]


decimal_ctx = contextvars.ContextVar("decimal ctx", default=0)


async def fractions3(precision, x, y):
    print(decimal_ctx.get())
    with localcontext() as ctx:
        print(id(ctx))
        ctx.prec = precision
        r1 = Decimal(x) / Decimal(y)
        await asyncio.sleep(0)
        r2 = Decimal(x) / Decimal(y)
        return (r1, r2)


async def run_fractions3():
    decimal_ctx.set(1)
    t1 = fractions3(precision=2, x=1, y=3)
    t2 = fractions3(precision=4, x=2, y=3)

    g1, g2 = await asyncio.gather(t1, t2)

    items = list(zip(g1, g2))
    items = [str(y) for x in items for y in x]
    print("frac3:", items)
    assert items == ["0.33", "0.6667", "0.33", "0.6667"]


def test_fractions3():
    asyncio.run(run_fractions3())
