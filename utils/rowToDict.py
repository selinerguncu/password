def rowToDict(cur, row):
    d = {}
    for index, description in enumerate(cur.description):
        d[description[0]] = row[index]
    return d
