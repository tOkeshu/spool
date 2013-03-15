from threading import Thread, current_thread
import multiprocessing
from select import select as unix_select
from time import sleep

def alive(source):
    try:
        source.fileno()
        return True
    except:
        return False


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

    def fileno(self):
        q = self._in if self.incoroutine() else self._out
        return q._reader.fileno()

    def close(self):
        self._in.close()
        self._out.close()


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


def select(*sources):
    sources = filter(alive, sources)
    while sources:
        readables, writables, exceptions = unix_select(sources, [], [])
        for source in readables:
            yield source
        sources = filter(alive, sources)

