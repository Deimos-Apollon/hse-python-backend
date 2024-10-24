from typing import Iterable


def factorial(n: int) -> int:
    if not type(n) is int or n < 0:
        raise ValueError("Invalid number in `factorial`. Must be integer and >= 0")
    factorial = 1
    for i in range(1, n+1):
        factorial *= i
    return factorial


def fibonacci(n: int) -> int:
    if not type(n) is int or n < 0:
        raise ValueError("Invalid number in `fibonacci`. Must be integer and >= 0")
    if n == 0:
        return 0
    prev, curr = 0, 1
    for i in range(1, n):
        prev, curr = curr, prev + curr 
    return curr


def mean(data: Iterable) -> [int, float]:
    try:
        return sum(data) / len(data)
    except TypeError:  
        ValueError("Invalid number sequence in `mean`.")
