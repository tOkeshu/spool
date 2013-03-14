from threading import Thread, current_thread
from multiprocessing import Queue


def coroutine(fun):
    def replacement(*args):
        return (fun, args)
    return replacement

coroutine.self = lambda: current_thread().__chan__

def go(spec):
    fun, args = spec
    t = Thread(target=fun, args=args)
    q = Queue()
    t.__setattr__('__chan__', q)
    t.start()
    return q

