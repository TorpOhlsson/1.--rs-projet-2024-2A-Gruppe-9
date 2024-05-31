import mysql.connector
import calendar
from datetime import datetime

mydb = mysql.connector.connect(
    	host="XXXXX",
        user="XXXXX",
        password="XXXXX",
        database="XXXXX"
)

date_now = datetime.now()
this_day = int(date_now.strftime("%d"))
this_month = int(date_now.strftime("%m"))
this_year = int(date_now.strftime("%Y"))

remove_list = []

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM logs")
rows = mycursor.fetchall()

for row in rows:

	keep = False

	get_time = row[8]
	split_time = get_time.split("-") 
	
	remove_timestrap = split_time[2].split(" ") 
	split_time[2] = remove_timestrap[0]

	if int(split_time[0]) == this_day and int(split_time[1]) == this_month and int(split_time[2]) == this_year:
		keep = True

	yeaster_day = this_day - 1
	yeaster_month = this_month
	yeaster_year = this_year

	if yeaster_day == 0 and yeaster_month != 1:
		yeaster_month = yeaster_month - 1
		yeaster_day = calendar.monthrange(this_year, yeaster_month)[1]
	
	if yeaster_day == 0 and yeaster_month == 1:
		yeaster_month = 12
		yeaster_year = yeaster_year - 1
		yeaster_day = 31

	if int(split_time[0]) == yeaster_day and int(split_time[1]) == yeaster_month and int(split_time[2]) == yeaster_year:
		keep = True

	if keep == False:
		remove_list.append(row[0])

counter = 0

for item in remove_list:
	counter = counter + 1
	vars = [item]
	mycursor.execute("DELETE FROM logs WHERE id=%s AND status='fine'",vars)
	mydb.commit()

print(str(counter) + " deleted from database")
    