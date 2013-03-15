from threading import Thread, current_thread
from multiprocessing import Queue

def go(fun):
    chan = Queue()

    def _fun(*args):
        t = Thread(target=fun, args=args)
        t.__setattr__('__chan__', chan)
        t.start()
        return chan

    return _fun

coroutine = go
coroutine.self = lambda: current_thread().__chan__ if hasattr(current_thread(), '__chan__') else None

