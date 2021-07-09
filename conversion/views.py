from django.http import HttpResponse
from django.views import View
import pymongo
# Create your views here.
# from conversion.models import DataTable
from psycopg2 import sql, connect


class dashboard(View):
    def get(self, request):
        col_cursor = ''
        table_name = "conversion_datatable"
        user_name = 'postgres'
        host = 'localhost'
        password = '1234'
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["conversionDB"]
        mycol = mydb["convertedData"]
        db_name = "newwebsite"
        try:
            # declare a new PostgreSQL connection object
            conn = connect(
                dbname=db_name,
                user=user_name,
                host=host,
                password=password
            )
            # print the connection if successful
            print("psycopg2 connection:", conn)
            col_cursor = conn.cursor()

        except Exception as err:
            print("psycopg2 connect() ERROR:", err)
            conn = None
            return HttpResponse('Error Database URL is incorrect')
        # declare an empty list for the column names
        columns = []
        if conn != None:
            # pass a PostgreSQL string for the table name to the function
            columns = get_columns_names(table_name, col_cursor)
            print("columns:", columns)
        raw_query = "Select * from {}".format(table_name)
        col_cursor.execute(raw_query)
        data_in_db = []
        data_all = col_cursor.fetchall()
        col_cursor.close()
        for tup in data_all:
            data_in_db += [tup]
        # close the cursor object to prevent memory leaks
        col_cursor.close()
        data_to_add = []
        for i in range(len(data_in_db)):
            data_to_add.append({
                columns[0]: data_in_db[i][0],
                columns[1]: data_in_db[i][1],
                columns[2]: data_in_db[i][2],
                columns[3]: data_in_db[i][3]
            })
        for i in data_to_add:
            x = mycol.insert_one(i)
        return HttpResponse('inserted')


def get_columns_names(table, col_cursor):
    columns = []
    col_names_str = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE "
    col_names_str += "table_name = '{}';".format(table)
    print("\ncol_names_str:", col_names_str)

    try:
        sql_object = sql.SQL(col_names_str).format(sql.Identifier(table))
        col_cursor.execute(sql_object)
        col_names = (col_cursor.fetchall())
        # iterate list of tuples and grab first element
        for tup in col_names:
            # append the col name string to the list
            columns += [tup[0]]
    except Exception as err:
        print("get_columns_names ERROR:", err)

    # return the list of column names
    return columns
