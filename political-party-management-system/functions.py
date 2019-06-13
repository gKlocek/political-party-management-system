def add_member(member,is_leader,password,timestamp,cursor):
    value = '('+str(member)+','+str(is_leader)+',crypt('+"'"+password+"'"+",gen_salt('bf'))," +'to_timestamp('+str(timestamp)+'))'
    cursor.execute('INSERT INTO member(id,is_leader,password,last_action_time) VALUES'+value+';')

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
    # print('validate member'+ str(member))
    if res[0]:
        # print('member exists')
        cursor.execute('SELECT member_validation('+str(member)+','+"'"+password+"'"+');');
        res = cursor.fetchone()
        # print('member validation result: '+str(res[0]))
        if res[0]:
            update_timestamp(member,timestamp,cursor)
            return True
        return False
    else:
        # print('add new member')
        add_member(member,False,password,timestamp,cursor)
        return True
