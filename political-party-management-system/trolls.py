def get_trolls(js,conn):
    cur = conn.cursor()
    cur.execute(
    """
        SELECT id,upvotes,downvotes,is_active(last_action_time::timestamp,to_timestamp("""+str(js['trolls']['timestamp'])+""")::timestamp) FROM
            member WHERE upvotes<downvotes
        ORDER BY downvotes-upvotes
    """
    )
    print('trolls')
    print(cur.fetchall())
    cur.close()
    conn.commit()
