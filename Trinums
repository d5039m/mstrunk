__author__ = 'ms71651'
import math
import time

start = time.time()
def triangle(x):
    return (x * (x + 1))//2

def divisors(x):
    divisors = 0
    for y in range(1, math.ceil(math.sqrt(x))+1,1):
        if x % y == 0:
            divisors += 2
    return divisors

maxdivs = 0
i = 1
while maxdivs < 500:
    tri = triangle(i)
    divs = divisors(tri)
    if divs > maxdivs:
        maxdivs = divs
    print(str(i) + " triangle: "+ str(tri) + " - Divisors: " + str(divs))
    i+=1

elapsed = (time.time() - start)
print("Ellapsedtime = " + str(elapsed))
