Spool
=====

Spool is a microframework to write asynchronous code with Python.

Getting started
---------------

Spool provides you 3 primitives:

  - a `go` function
  - a `coroutine` decorator
  - a `select` function

The `go` function is used to decorate other functions in your code:

::

    from spool import go

    def fib(n):
        if n < 2:
            return n
        return fib(n-2) + fib(n-1)

    go(fib)(10) # calculate fib(10) in the background



When a function is decorated via the `go` function, his code is run in
another thread.  It's handy to launch computation in the
background. In the case of fibonacci computation, it's not very useful
because we certainly want the result.

To do that we can write the following wrapper:

::

    from spool import go, coroutine

    def fib(n):
        if n < 2:
            return n
        return fib(n-2) + fib(n-1)

    def fibonacci(n):
        chan = coroutine.self()
        chan.put(fib(n))

    chan = go(fibonacci)(10)
    chan.get() # the result of fib(10)


Each decorated function have access to a channel used to communicate
with other threads. To retrieve the channel of the current thread, you
can use `coroutine.self()`.

A channel have 4 methods, `get`, `put`, `close` and `alive`.

A channel is attached to a thread and is bidirectional. For instance
if you `put` something in it while being inside the thread, you can
retrieve the object outside the thread via `get`. If you `put` an
object while being outside the thread, you can retrieve it from inside
the thread via `get`.

Channels use `multiprocessing.Queue` and thus are thread safe.

The `coroutine` decorator allow you to easily transform a function
into a factory of threaded functions.

For instance with the fibonacci wrapper we can write:

::

    from spool import coroutine

    def fib(n):
        if n < 2:
            return n
        return fib(n-2) + fib(n-1)

    @coroutine
    def fibonacci(n):
        chan = coroutine.self()
        chan.put(fib(n))

    chan = fibonacci(10)
    chan.get() # the result of fib(10)


Now each time the fibonacci function is called, we launch a thread to
run its code. Each call create a different thread and a corresponding
channel.

Sometimes you want to passively wait for multiple channels, that's the
purpose of the `select` function.

The `select` function allow you to listen for multiple channels and get notified when one have something for you:

::

    from spool import coroutine, select

    @coroutine
    def pulse(n):
        chan = coroutine.self()
        while chan.alive():
            chan.put('ping from %s' % chan)
            sleep(n)

    pulse1 = pulse(1)
    pulse2 = pulse(2)
    for source in select(pulse1, pulse2):
        if source is pulse1:
            print(pulse1.get()) # got a pulse from pulse1
        elif source is pulse2:
            print(pulse2.get()) # got a pulse from pulse2


Here we have a pulse coroutine that sleeps for a given number of
seconds.  We create two threaded version of the pulse, one at 1
second, the other one at 2 seconds. Then we passively wait for one of
them to put something in their channel. As soon as something is
available the select function returns and we can check which pulse has
been triggered.

License
-------

Spool is released under the `GNU General Public License v3` or later.

.. `Gnu General Public License v3`: http://www.gnu.org/licenses/gpl.html

