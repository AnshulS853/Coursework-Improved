def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# cur.row_factory = dict_factory
# #Add this line to change the row factory in your cursor