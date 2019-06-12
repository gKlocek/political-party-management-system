
def man_json(js,conn):
    if 'leader' in js:
        add_leader(js,conn)
    if 'support' in js or 'protest' in js:
        add_action(js,conn)
    # if 'upvote' in js or 'downvote' in js:
    #     vote(js,conn)
    # if 'trolls' in js:
    #     trolls(js,conn)

# { "leader": { "timestamp": 1557473000, "password": "abc", "member": 1}}
# Member(id,is_leader,password,last_action_time);

def add_leader(js,conn):
    value = '('+str(js['leader']['member'])+',true'+',crypt('+"'"+js['leader']['password']+"'"+",gen_salt('bf'))," +'to_timestamp('+str(js['leader']['timestamp'])+'))'
    cur = conn.cursor()
    cur.execute('INSERT INTO member(id,is_leader,password,last_action_time) VALUES'+value)
    cur.close()
    conn.commit()

def add_action(js,conn):
