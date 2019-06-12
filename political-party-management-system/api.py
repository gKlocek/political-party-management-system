
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
    add_member(js['leader']['member'],True,js['leader']['password'],js['leader']['timestamp'],cur)
    cur.close()
    conn.commit()

# { "protest": { "timestamp": 1557475700, "password": "123", "member": 3, "action":500, "project":5000, "authority":10000}}
# Action(id,projectid,memberid,upvotes,downvotes,type)
def add_action(js,conn):
    cur=conn.cursor()
    type = 'protest'
    if type not in js:
        type = 'support'
    if update_and_validate(js[type]['timestamp'],js[type]['member'],js[type]['password'],cur):
#        print('validation proceed succesfully')
        if 'authority' in js[type]:
#            print('there is authority sratatatatatatat')
            add_project(js[type]['project'],js[type]['authority'],cur)

        value = '('+str(js[type]['action'])+','+str(js[type]['project'])+',0,0,'+"'"+type+"'"+')'
        cur.execute('INSERT INTO action(id,projectid,upvotes,downvotes,type) VALUES'+value+';')
    else:
        conn.rollback()
    cur.close()
    conn.commit()


# Project(id,authority)
def add_project(project,authority,cur):
    value = '('+str(project)+','+str(authority)+')'
    cur.execute('INSERT INTO project(id,authority) VALUES'+value+';')

def update_timestamp(member,timestamp,cursor):
    cursor.execute('UPDATE member SET last_action_time= to_timestamp('+str(timestamp)+') WHERE id='+str(member)+';')

def update_and_validate(timestamp,member,password,cursor):
    # print('updating and validating values: ')
    # print(str(timestamp)+','+str(member)+','+password)
    cursor.execute('SELECT EXISTS( SELECT * FROM member WHERE id ='+str(member)+');');
    res = cursor.fetchone()
    if res[0]:
    #    print('member exists')
        cursor.execute('SELECT member_validation('+str(member)+','+"'"+password+"'"+');');
        res = cursor.fetchone()
#        print('member validation result: '+str(res[0]))
        if res[0]:
            update_timestamp(member,timestamp,cursor)
            return True
        return False
    else:
        add_member(member,False,password,timestamp,cursor)
        return True

#def add_vote(js,conn):
