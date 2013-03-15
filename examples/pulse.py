from spool import coroutine
from time import sleep

@coroutine
def pulse(n):
    chan = coroutine.self()
    while chan.alive():
        chan.put('ping')
        sleep(n)

if __name__ == '__main__':
    chan = pulse(1)
    for x in xrange(10):
        print(chan.get())
    chan.close()

