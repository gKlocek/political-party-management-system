from functions import *

def man_json(js,conn):
    if 'leader' in js:
        add_leader(js,conn)
    if 'support' in js or 'protest' in js:
        add_action(js,conn)
    if 'upvote' in js or 'downvote' in js:
        add_vote(js,conn)
    if 'actions' in js:
        get_actions(js,conn)
    if 'trolls' in js:
        trolls(js,conn)

# { "leader": { "timestamp": 1557473000, "password": "abc", "member": 1}}
# Member(id,is_leader,password,last_action_time);
def add_leader(js,conn):
    cur = conn.cursor()
    add_member(js['leader']['member'],True,js['leader']['password'],js['leader']['timestamp'],cur)
    cur.close()
    conn.commit()

# { "protest": { "timestamp": 1557475700, "password": "123", "member": 3, "action":500, "project":5000, "authority":10000}}
# Action(id,projectid,upvotes,downvotes,type)
def add_action(js,conn):
    cur=conn.cursor()
    type = 'protest'
    if type not in js:
        type = 'support'
    if update_and_validate(js[type]['timestamp'],js[type]['member'],js[type]['password'],cur):
#        print('validation proceed succesfully')
        if 'authority' in js[type]:
            add_project(js[type]['project'],js[type]['authority'],cur)

        value = '('+str(js[type]['action'])+','+str(js[type]['project'])+',0,0,'+"'"+type+"'"+')'
        cur.execute('INSERT INTO action(id,projectid,upvotes,downvotes,type) VALUES'+value+';')
        value = '('+str(js[type]['action'])+','+str(js[type]['member'])+')'
        cur.execute('INSERT INTO Action_has_initiator(action_id,member_id) VALUES'+value+';')
    else:
        conn.rollback()
    cur.close()
    conn.commit()
#downvote <timestamp> <member> <password> <action>
# votes(member_id,action_id,type)
def add_vote(js,conn):
    cur=conn.cursor()
    type = 'upvote'
    if type not in js:
        type='downvote'

    cur.execute('SELECT EXISTS(SELECT * FROM action WHERE id='+str(js[type]['action']) +')')
    res=cur.fetchone()
    if not res[0]:
        raise Exception('voting for non existing action! ');
        cur.close();
        conn.rollback();

    if update_and_validate(js[type]['timestamp'],js[type]['member'],js[type]['password'],cur):
        value = '('+str(js[type]['member'])+','+str(js[type]['action'])+','+"'"+type+"'"+')'
        cur.execute('INSERT INTO votes(member_id,action_id,type) VALUES'+value+';')
    else:
        conn.rollback()
    cur.close()
    conn.commit()


# actions <timestamp> <member> <password> [ <type> ] [ <project> | <authority> ]
# { "actions": { "timestamp": 1560169050, "member": 1002, "password": "password2", "type": "support" ,"authority": 10000} }
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
# Project(id,authority)

#def add_vote(js,conn):
