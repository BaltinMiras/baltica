# 1. Squares up to N
def squares_upto(n):
    for i in range(n + 1):
        yield i * i

# 2. Even numbers 0..n, comma separated
def evens(n):
    for i in range(0, n + 1, 2):
        yield i

# 3. Divisible by 3 and 4 in 0..n
def div_3_and_4(n):
    for i in range(n + 1):
        if i % 12 == 0:
            yield i

# 4. Squares from a to b
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

# 5. Countdown n..0
def countdown(n):
    while n >= 0:
        yield n
        n -= 1


if __name__ == "__main__":
    print(list(squares_upto(5)))

    n = int(input("n: "))
    print(",".join(str(x) for x in evens(n)))

    print(list(div_3_and_4(n)))

    for v in squares(3, 6):
        print(v)

    print(list(countdown(5)))
