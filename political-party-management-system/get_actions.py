def get_actions(js,conn):
    # print('get_actions for')
    # print(js)
    cur = conn.cursor()
    if update_and_validate(js['actions']['timestamp'],js['actions']['member'],js['actions']['password'],cur):
        # print('validation of member'+str(js['actions']['member'])+' proceed succesfully')
        cur.execute('SELECT action.id, type, project.id,authority,upvotes,downvotes FROM action JOIN project ON action.projectid=project.id')
        res=str(cur.fetchall())[1:-1]
        if 'type' in js['actions']:
            type = str(js['actions']['type'])
            cur.execute(
            "WITH pom(action,type,project,authority,upvotes,downvotes) AS (SELECT * FROM (VALUES "+res+") AS t (a,t,p,au,u,d)) SELECT * FROM pom WHERE type='"+type+"';"
            )
            res=str(cur.fetchall())[1:-1]

        if 'project' in js['actions']:
            project=str(js['actions']['project'])
            cur.execute(
            "WITH pom(action,type,project,authority,upvotes,downvotes) AS (SELECT * FROM (VALUES "+res+") AS t (a,t,p,au,u,d)) SELECT * FROM pom WHERE project='"+project+"';"
            )
            res = cur.fetchone()

        if 'authority' in js['actions']:
            authority=str(js['actions']['authority'])
            cur.execute(
            "WITH pom(action,type,project,authority,upvotes,downvotes) AS (SELECT * FROM (VALUES "+res+") AS t (a,t,p,au,u,d)) SELECT * FROM pom WHERE authority='"+authority+"';"
            )
            res = cur.fetchone()
        print(res)
    else:
        raise Exception('invalid member');
    cur.close()
    conn.commit()
