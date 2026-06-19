import week_2.day_8.practices.fibo as fibo
# from fibo import fib, fib2
# from fibo import *
# import fibo as fib

fibo.fib(1000)

print(fibo.fib2(100))

print(fibo.__name__)

fib = fibo.fib
fib(500)


from week_2.day_8.practices.fibo import fib as fibonacci
fibonacci(500)