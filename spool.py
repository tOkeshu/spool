from collections import namedtuple
from threading import Thread, current_thread
from multiprocessing import Queue

Coroutine = namedtuple('Coroutine', ['fun', 'args'])

def coroutine(fun):
    def replacement(*args):
        return Coroutine(fun, args)
    return replacement

coroutine.self = lambda: current_thread().__chan__

def go(spec):
    fun, args = spec
    chan = Queue()

    t = Thread(target=fun, args=args)
    t.__setattr__('__chan__', chan)
    t.start()

    return chan

