def MySort(list):
    a, b = [], []
    length = len(list[0])
    for i in list:
        if len(i) == length:
            a.append(i)
        else:
            b.append(i)
    if not b:
        return a
    #print(a, b)
    return a + b if len(a[0]) < len(b[0]) else b + a