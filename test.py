import pymysql
from config import *

connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
print('connection successful')

def delete_data(table_name):
    with connection.cursor() as cursor:
        delete_query = f"DELETE FROM {table_name}"
        cursor.execute(delete_query)
        connection.commit()
        print('delete successful')

    connection.close()

def drop_table(table_name):
    with connection.cursor() as cursor:
        drop_query = f"DROP TABLE {table_name};"
        cursor.execute(drop_query)
        print('drop successful')

    connection.close()

def select_all(table_name):
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM {table_name}')
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        print('select successful')

    connection.close()


# delete_data('users')
# select_all('users')
try:
    gfsdsafd
except Exception as ex:
    print(ex)






