from threading import Thread, current_thread
import multiprocessing
from select import select as unix_select
from time import sleep

class Channel(object):

    def __init__(self):
        self._in = multiprocessing.Queue()
        self._out = multiprocessing.Queue()

    def incoroutine(self):
        return coroutine.self() is self

    def get(self):
        q = self._in if self.incoroutine() else self._out
        return q.get()

    def put(self, *args):
        q = self._out if self.incoroutine() else self._in
        return q.put(*args)

def go(fun):
    chan = Channel()

    def _fun(*args):
        t = Thread(target=fun, args=args)
        t.__setattr__('__chan__', chan)
        t.start()
        return chan

    return _fun

coroutine = go
coroutine.self = lambda: current_thread().__chan__ if hasattr(current_thread(), '__chan__') else None

