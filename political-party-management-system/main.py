import psycopg2
from read_input import read_input
from api import man_json
from initialization import create_database
input_file='input.txt'

username = 'init'
password = 'qwerty'
database = 'projekt'


def main():
    lst=read_input(input_file)
    init=lst[0]
    try:
	    my_connection=psycopg2.connect( host='localhost', user = init['open']['login'], password=init['open']['password'], dbname='projekt' )
    except:
        print("status: ERROR")
        return
    create_database(my_connection)
    sz = len(lst)
    for i in range(1,sz):
        man_json(lst[i],my_connection)

if __name__ == '__main__':
    main()
    
