def flatten_productions(p):
    if len(p) == 1:
        return p

    if type(p) == tuple:
        return [p]
    elif type(p) == list and p[1][0] == None:
        return [p[0]]

    head = p.pop(0)
    tail = []

    if len(p) > 0:
        tail = flatten_productions(p[0])

    productions = [head] + tail

    return productions
