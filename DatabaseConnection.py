import psycopg2

connection = psycopg2.connect(host="192.168.0.175", port="5432", database="Power_BI", user="wschultz", password="2433006Ws")

select_query = "SELECT dbo.\"usp_SEL_Application_Last_Update\"('Power BI Desktop')"
update_query = "select dbo.\"usp_UPD_Application_Update_Date\"('Power BI Desktop', '01/01/2003')"

cursor = connection.cursor()

cursor.execute(select_query)
records = cursor.fetchall()

for record in records:
    previous_update_date = record[0]

print(previous_update_date)

try:
    cursor.execute(update_query)
    connection.commit()

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)

if(connection):
    cursor.close()
    connection.close()
