import threading
import contextvars

var = contextvars.ContextVar("var")


def sub():
    assert var.get() is None  # The execution context is empty
    # for each new thread.
    var.set("sub")


def test_thread():
    var.set("main")

    thread = threading.Thread(target=sub)
    thread.start()
    thread.join()

    assert var.get() == "main"
