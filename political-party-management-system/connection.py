#!/usr/bin/python

hostname = 'localhost'
username = 'init'
password = 'qwerty'
database = 'projekt'

# Simple routine to run a query on a database and print the results:
def doQuery( conn ) :
    cur = conn.cursor()
    cur.execute('CREATE TABLE Member (id int PRIMARY KEY,is_leader bool,password text,last_action_time timestamp)')
    cur.execute( "SELECT firstname, lastname FROM employee" )
    for firstname, lastname in cur.fetchall() :
        print(firstname, lastname)


print("Using psycopg2...")
import psycopg2
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
doQuery( myConnection )
myConnection.close()

print("Using PyGreSQL ...")
import pgdb
myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
doQuery( myConnection )
myConnection.close()
