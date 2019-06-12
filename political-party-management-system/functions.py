def add_member(member,is_leader,password,timestamp,cursor):
    value = '('+str(member)+','+str(is_leader)+',crypt('+"'"+password+"'"+",gen_salt('bf'))," +'to_timestamp('+str(timestamp)+'))'
    cursor.execute('INSERT INTO member(id,is_leader,password,last_action_time) VALUES'+value+';')
