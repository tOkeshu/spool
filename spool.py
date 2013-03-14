from threading import Thread
from multiprocessing import Queue

def coroutine(fun):
    def replacement(*args):
        return (fun, args)
    return replacement

def go(spec):
    fun, args = spec
    Thread(target=fun, args=args).start()

