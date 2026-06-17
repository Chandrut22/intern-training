import fibo
# from fibo import fib, fib2
# from fibo import *
# import fibo as fib

fibo.fib(1000)

print(fibo.fib2(100))

print(fibo.__name__)

fib = fibo.fib
fib(500)


from fibo import fib as fibonacci
fibonacci(500)