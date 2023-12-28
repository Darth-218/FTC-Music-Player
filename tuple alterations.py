d1 = {1:'a', 2:'b', 3:'c'}
d2 = {2:'x', 1:'y', 4:'z'}

for i in d1.keys():
    for j in d2.keys():
        if i == j:
            print(i)