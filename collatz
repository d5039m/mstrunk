__author__ = 'ms71651'
import time
start = time.time()

def collatz(x):

    terms = 1
    while x > 1:
        if x % 2 == 0:
            x = x//2
        else:
            x = 3*x + 1
        terms += 1
    return terms

maxTerms = 0
start = 0
for x in range(1,1000000,2):
    print(x)
    terms = collatz((x))
    if terms > maxTerms:
        maxTerms = terms
        start = x

print(maxTerms)
print(start)
elapsed = (time.time() - start)
print("Ellapsedtime = " + str(elapsed))
