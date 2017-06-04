from utils.rowToDict import rowToDict

def rowsToDict(cur, rows):
    l = []
    for row in rows:
        l.append(rowToDict(cur, row))

    return l
