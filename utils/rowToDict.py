def rowToDict(cur, row):
    d = {}
    if row == None:
        return d

    for index, description in enumerate(cur.description):
        # print description[0], row[index]
        d[description[0]] = row[index]

    return d
