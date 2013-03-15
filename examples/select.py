from spool import coroutine, select
from time import sleep

@coroutine
def pulse(n):
    chan = coroutine.self()
    while chan.alive():
        chan.put('ping from %s' % chan)
        sleep(n)

if __name__ == '__main__':
    chan1 = pulse(1)
    chan2 = pulse(2)

    print(chan1, chan2)

    i = 0
    for source in select(chan1, chan2):
        print(source.get())

        if i == 10:
            break
        i += 1

    chan1.close()
    chan2.close()

