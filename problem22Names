__author__ = 'ms71651'

values = {
    "A":1,
    "B":2,
    "C":3,
    "D":4,
    "E":5,
    "F":6,
    "G":7,
    "H":8,
    "I":9,
    "J":10,
    "K":11,
    "L":12,
    "M":13,
    "N":14,
    "O":15,
    "P":16,
    "Q":17,
    "R":18,
    "S":19,
    "T":20,
    "U":21,
    "V":22,
    "W":23,
    "X":24,
    "Y":25,
    "Z":26
}

file = open("p022_names.txt")
print(file.name)

line = file.readline()
l1 = line.split(",")
print(len(l1))
l1.sort()

totalSum = 0
for x in range(0,len(l1)):
    name = l1[x]
    name = name.replace("\"" ,"")
    sum = 0
    for c in name:
        sum += values[c]

    product = sum * (x+1)
    totalSum += product

print (totalSum)




