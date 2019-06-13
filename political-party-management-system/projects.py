from functions import *
def get_projects(js,conn):
    cur = conn.cursor()
    print('results:')
    if update_and_validate(js['projects']['timestamp'],js['projects']['member'],js['projects']['password'],cur):
        cur.execute('SELECT id,authority FROM project')
        res=str(cur.fetchall())[1:-1]
        if 'authority' in js['projects']:
            authority=str(js['projects']['authority'])
            cur.execute(
            "WITH pom(project,authority) AS (SELECT * FROM (VALUES "+res+") AS t (p,a)) SELECT * FROM pom WHERE authority='"+authority+"';"
            )
            res = cur.fetchone()
        print(res)
    else:
        raise Exception('invalid member');
    cur.close()
    conn.commit()
