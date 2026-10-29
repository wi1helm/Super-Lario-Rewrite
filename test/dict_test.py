
dict = {"nub": (2,0),
        "hej": (4,5),
        "food": (2,4)}

for key in dict:
    print(key)
    print(dict[key])
    fx, fy = dict[key]
    fx *= 2
    fy *= 2
    dict[key] = (fx,fy)

print(dict)
