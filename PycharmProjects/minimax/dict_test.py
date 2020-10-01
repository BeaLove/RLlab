mydict = {0:(3, 4), 1: (2, 7)}
mytuple = (5, 4)
j = 0
for i in range(0, 10, 2):
    j += 1
    #mydict[i] = j
print(mydict)
print(mydict[0][1])
print(list(mydict.values()))

print(mytuple[0] - mytuple[1])

print(mydict.values()[0][0])
