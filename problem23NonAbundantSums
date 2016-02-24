__author__ = 'ms71651'
import math
import time


abundantNumbers = []

start = time.time()
def getDivisors(x):
    divisors = []
    for i in range(1, int(math.sqrt(x))+1):
        if x % i == 0:
            divisors.append(i)
            if i != 1 and i*i != x:
                divisors.append(x // i)
    return divisors



for x in range(1,28124):
    divisors = getDivisors(x)
    sumDiv = sum(divisors)
    if sumDiv > x:
        abundantNumbers.append(x)
print(abundantNumbers)
print(len(abundantNumbers))

sums = set()
for x in abundantNumbers:
    for y in abundantNumbers:
        test = x + y
        if test < 28123:
            sums.add(test)

print(len(sums))


cantSum = []
for x in range(1,28123):
    print(x)
    if x not in sums:
        cantSum.append(x)

print(cantSum)
print(len(cantSum))
print(sum(cantSum))
