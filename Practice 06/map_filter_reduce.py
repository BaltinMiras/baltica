from functools import reduce

nums = [1, 2, 3, 4, 5, 6]

print(list(map(lambda x: x * x, nums)))            # squares
print(list(filter(lambda x: x % 2 == 0, nums)))    # evens
print(reduce(lambda a, b: a * b, nums))            # product = 720
print(reduce(lambda a, b: a + b, nums))            # sum = 21

# Other aggregates
print(len(nums), sum(nums), min(nums), max(nums), sorted(nums, reverse=True))
