
def man_json(js,conn):
    if 'leader' in js:
        add_leader(js,conn)
    if 'support' in js or 'protest' in js:
        add_action(js,conn)
    if 'upvote' in js or 'downvote' in js:
        add_vote(js,conn)
    if 'trolls' in js:
         trolls(js,conn)

# { "leader": { "timestamp": 1557473000, "password": "abc", "member": 1}}
# Member(id,is_leader,password,last_action_time);
def add_leader(js,conn):
    cur = conn.cursor()
    add_member(js['leader']['member'],true,js['leader']['password'],js['leader']['timestamp'],cur)
    cur.close()
    conn.commit()

def add_member(member,is_leader,password,timestamp,cursor):
    value = '('+str(member)+str(is_leader)+',crypt('+"'"+password+"'"+",gen_salt('bf'))," +'to_timestamp('+str(timestamp)+'))'
    cur.execute('INSERT INTO member(id,is_leader,password,last_action_time) VALUES'+value+';')

# { "protest": { "timestamp": 1557475700, "password": "123", "member": 3, "action":500, "project":5000, "authority":10000}}
# Action(id,projectid,memberid,upvotes,downvotes,type)
def add_action(js,conn):
    cur=conn.cursor()
    type = 'support'
    if type not in js:
        type = 'protest'
    if update_add_validate(js[type]['timestamp'],js[type]['member'],js[type]['password'],cur):
        if 'authority' in js:
            add_project(js[type]['project'],js[type]['authority'],cur)

        value = '('+str(js[type]['action'])+','+str(js[type]['project'])+',0,0,'+type+')'
        cur.execute('INSERT INTO action(id,projectid,upvotes,downvotes,type) VALUES'+value+';')
        cur.commit()
    cur.close()

# Project(id,authority)
def add_project(project,authority,cur):
    value = '('+project+','+authority+')'
    cur.execute('INSERT INTO project(id,authority) VALUES'+value+';')

def update_timestamp(member,timestamp,cursor):
    cursor.execute('UPDATE member SET timestamp= to_timestamp('+str(timestamp)+') WHERE id='+str(member)+';')

def update_add_validate(timestamp,member,password,cursor):
    cursor.execute('SELECT EXISTS( SELECT * FROM member WHERE id ='+str(member)+');');
    res = cursor.fetchone()
    print(res)
    if res:
        cursor.execute('SELECT member_validation('+str(member)+','+password');');
        if cursor.fetchone()
            return True
        return False
    else
        add_member(member,False,password,timestamp,cursor)
        return True

#def add_vote(js,conn):
