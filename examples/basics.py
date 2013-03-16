from spool import coroutine

def fib(n):
    if n < 2:
        return n
    return fib(n-2) + fib(n-1)

@coroutine
def fibonacci(n):
    chan = coroutine.self()
    chan.put(fib(n))

if __name__ == '__main__':
    chan = fibonacci(10)
    print(fibonacci(10).get())

