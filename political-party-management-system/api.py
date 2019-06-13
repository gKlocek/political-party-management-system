from functions import *
from actions import *
from votes import *
from projects import *
from trolls import *
def man_json(js,conn):
    if 'leader' in js:
        add_leader(js,conn)
    if 'support' in js or 'protest' in js:
        add_action(js,conn)
    if 'upvote' in js or 'downvote' in js:
        add_vote(js,conn)
    if 'actions' in js:
        get_actions(js,conn)
    if 'votes' in js:
        get_votes(js,conn)
    if 'projects' in js:
        get_projects(js,conn)
    if 'trolls' in js:
        get_trolls(js,conn)

# { "leader": { "timestamp": 1557473000, "password": "abc", "member": 1}}
# Member(id,is_leader,password,last_action_time);
def add_leader(js,conn):
    cur = conn.cursor()
    add_member(js['leader']['member'],True,js['leader']['password'],js['leader']['timestamp'],cur)
    cur.close()
    conn.commit()

# { "protest": { "timestamp": 1557475700, "password": "123", "member": 3, "action":500, "project":5000, "authority":10000}}
# Action(id,projectid,upvotes,downvotes,type)

#downvote <timestamp> <member> <password> <action>
# votes(member_id,action_id,type)


# actions <timestamp> <member> <password> [ <type> ] [ <project> | <authority> ]
# { "actions": { "timestamp": 1560169050, "member": 1002, "password": "password2", "type": "support" ,"authority": 10000} }

# Project(id,authority)

#def add_vote(js,conn):
