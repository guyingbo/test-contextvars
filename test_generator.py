import contextvars

var1 = contextvars.ContextVar("var1")
var2 = contextvars.ContextVar("var2")


def gen():
    var1.set("gen")
    assert var1.get() == "gen"
    assert var2.get() == "main"
    yield 1

    # Modification to var1 in main() is shielded by
    # gen()'s local modification.
    assert var1.get() == "gen"

    # But modifications to var2 are visible
    assert var2.get() == "main modified"
    yield 2


class ContextGenerator:
    def __init__(self, gen):
        self.gen = gen
        self.context = contextvars.copy_context()

    def __next__(self):
        return self.context.run(self.gen.__next__)

    def __iter__(self):
        return self


def failed_example():
    g = gen()
    # g = ContextGenerator(gen())

    var1.set("main")
    var2.set("main")
    next(g)

    # Modification of var1 in gen() is not visible.
    assert var1.get() == "main"

    var1.set("main modified")
    var2.set("main modified")
    next(g)
