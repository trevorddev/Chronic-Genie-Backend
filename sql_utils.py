from django.db import connection


def make_dicts(cursor, row):
    """
    Makes database results to a dictionary.
    :param cursor:
    :param row:
    :return:
    """
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def fetch_all(cur):
    """
    :param cur:
    :return:
    """
    rv = []
    row = cur.fetchone()
    while row is not None:
        rv.append(make_dicts(cur,row))
        row = cur.fetchone()
    if len(rv) == 0:
        return None
    else:
        return rv


def fetch_columnsandrows(cur):
    """
    :param cur:
    :return:
    """
    rv = []
    rows = cur.fetchall()
    columns = cur.description
    result = [{columns[index][0]: column for index, column in enumerate(row)} for row in rows]

    return result



def query_ReturnRow(query, args=(), one=False, returnRowAndColumns = False):
    """
    Args must be sent as a tuple, if you have one argument pass it as (value,)
    :param query:
    :param args:
    :param one:
    :return:
    """
    try:
        with connection.cursor() as cur:
            cur.execute(query, args)
            if returnRowAndColumns == False :
                    rv = fetch_all(cur)
                    result = (rv[0] if rv else None) if one else rv
            else:
                    result = fetch_columnsandrows(cur)
            return result
    except Exception as ex:
        print(str(ex))
        try:
            pass
        except:
            pass
