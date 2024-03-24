import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

PASSWORD = os.getenv('PASSWORD')
USER = os.getenv('USER')
HOST = os.getenv('HOST')

def grava_dados_postgres(moradia, sg_moradia):

    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port="5432",
                                      database="postgres")
        cursor = connection.cursor()
        postgreSQL_select_Query = "INSERT INTO despesas (date_time, date, moradia, sg_moradia) VALUES (now(), now(), %s, %s);"
        cursor.execute(postgreSQL_select_Query, [moradia, sg_moradia])
        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return


