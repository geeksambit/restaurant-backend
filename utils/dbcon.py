from django.db import connection

def execute(query):
    cur = connection.cursor()
    result = []
    try:
        cur.execute(query)
        if "insert" in query:
            return cur.lastrowid
        if 'UPDATE' in query:
            if cur.rowcount ==1 :
                return True
            else :
                return False
        columns = tuple( [d[0] for d in cur.description] )
        
        for row in cur:
            result.append(dict(zip(columns, row)))
    except Exception as e:
        print("Exception || {}".format(e))
    finally:
        cur.close()
    return result


