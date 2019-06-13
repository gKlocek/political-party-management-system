from functions import *
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
# votes <timestamp> <member> <password> [ <action> | <project> ]
# <member> <upvotes> <downvotes>
def get_votes(js,conn):
    cur = conn.cursor()
    if update_and_validate(js['votes']['timestamp'],js['votes']['member'],js['votes']['password'],cur):
        if 'action' in js['votes']:
            cur.execute(
            """
            SELECT
            member_id,
            count(votes.type) filter (where votes.type='upvote'),
            count(votes.type) filter (where votes.type='downvote') FROM
                votes WHERE action_id="""+str(js['votes']['action'])+"""
            GROUP BY member_id
            ORDER BY member_id;"""
            )
            res=str(cur.fetchall())
        else:

            if 'project' in js['votes']:
                cur.execute(
                """
                SELECT
                member_id,
                count(votes.type) filter (where votes.type='upvote'),
                count(votes.type) filter (where votes.type='downvote') FROM
                    votes JOIN action ON action.id=votes.action_id
                WHERE projectid="""+str(js['votes']['project'])+ """
                GROUP BY member_id
                ORDER BY member_id;"""
                )
                res=str(cur.fetchall())
            else:
                cur.execute('SELECT id,upvotes,downvotes FROM member ORDER BY id')
                res=str(cur.fetchall())
        print(res)
    else:
        raise Exception('invalid member');
    cur.close()
    conn.commit()
