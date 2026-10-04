def smallest(numbers):
    min=numbers[0]
    for number in numbers:
        if min>number:
            min=number
    return min

numbers=[56,78,11,6,7]
print(smallest(numbers))
