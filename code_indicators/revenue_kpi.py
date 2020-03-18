import pandas as pd
import datetime
import csv

def getDuration(dur):
	hours = int(dur[:2])
	mins = int(dur[3:5])
	secs = int(dur[6:])
	return hours*3600 + mins*60 + secs

def isHoliday(date):
	if(date == '2018-12-25'):
		return True
	date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
	week_no = date_obj.weekday()
	if(week_no >= 5):
		return True 
	return False	

route_no = 'SBS-1K'
realtrips_file_path = '/home/nimisha/sem7/bmtc/TicketDataKPI/nimisha/' + route_no + '_realtrips.csv'
realtrips_file = pd.read_csv(realtrips_file_path) 

busses = {}
bus_date = {}

for index, row in realtrips_file.iterrows():
	trip_id = row['trip_id']
	date = trip_id[:10]
	if(isHoliday(date)):
		continue
	vehicle_no = trip_id[11:21]
	duration_seconds = getDuration(row['travel_duration'])
	if vehicle_no not in busses:
		busses[vehicle_no] = [0, 0]
		bus_date[vehicle_no] = set()
	busses[vehicle_no][0] += duration_seconds
	if(date not in bus_date[vehicle_no]):
		busses[vehicle_no][1] += 1
		bus_date[vehicle_no].add(date)

hours_cnt = {}

for key, value in busses.items():
	value[0] /= value[1]
	hours = int(value[0]/3600)
	if(hours not in hours_cnt):
		hours_cnt[hours] = 1
	else:
		hours_cnt[hours] += 1

csv_columns = ['hour', 'no_of_buses']
data = []
for key in sorted(hours_cnt):
	value = hours_cnt[key]
	temp = {}
	temp['hour'] = key
	temp['no_of_buses'] = value
	data.append(temp)

csv_file = route_no + '_revenue_kpi.csv'
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for row in data:
        	writer.writerow(row)
except IOError:
    print("I/O error")