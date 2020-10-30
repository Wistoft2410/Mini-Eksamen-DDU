from peewee import *

USER = 'nejjyigpsyjcqc'
PASSWORD = 'f7345217f875c8a617f3aff8f2812e35a6f55ef9178bf177a9c1247978b2f223'
HOST = 'ec2-52-208-175-161.eu-west-1.compute.amazonaws.com'
PORT = 5432

DB = PostgresqlDatabase('dae8653ftqev6r', 
                                   user=USER, 
                                   password=PASSWORD, 
                                   host=HOST, 
                                   port=PORT)

if __name__ == '__main__':
    DB.connect()
    DB.create_tables([], safe=True)
    DB.close()
