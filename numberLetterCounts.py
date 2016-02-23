__author__ = 'ms71651'


num2words = {1 : "one",2: "two",3:"three",4:"four",5:"five", 6:"six",7:"seven", 8:"eight", 9:"nine",10:"ten",11:"eleven",
12:"twelve",13:"thirteen",14:"fourteen",15:"fifteen",16:"sixteen",17:"seventeen",18:"eighteen",19:"nineteen"}

numTens = ["twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety"]
"hundred"
"thousand"

print(divmod(121,100))

def getString(x):

    if x == 1000:
        return "onethousand"
    if x < 20:
        return num2words[x]
    #units
    elif x < 100:
        tup = divmod(x, 10)
        tens = tup[0]
        units = tup[1]
        word = numTens[tens-2]
        if units > 0:
            word += num2words[units]
        return word

    elif x < 1000:
        tup = divmod(x,100)
        hundreds = tup[0]
        word = num2words[hundreds] + "hundred"
        remainder = tup[1]
        if remainder == 0:
            return word
        else:
            word += "and"
            tup2 = divmod(remainder, 10)
            tens = tup2[0]
            if remainder < 20:
                word += num2words[remainder]
                return word
            else:
                word += numTens[tens-2]
                units = tup2[1]
                if units > 0:
                     word +=  num2words[units]
                return word


totalWords =""
for x in range (1,1001):
    word = getString(x)
    totalWords += word
    print(word)

print(len(totalWords))
