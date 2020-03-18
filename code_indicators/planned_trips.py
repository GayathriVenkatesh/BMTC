import pandas as pd 
import csv

route_no = 'SBS-1K'
real_trips_file_path = '/home/nimisha/sem7/bmtc/TicketDataKPI/nimisha/' + route_no + '_realtrips.csv'
real_trips_file = pd.read_csv(real_trips_file_path)

form_four_file_path = '/home/nimisha/sem7/bmtc/TicketDataKPI/nimisha/11_10_form_four_Jan, 2019.xlsx'
form_four_file = pd.read_excel(form_four_file_path)
form_four_file = form_four_file[form_four_file['org_name'].isin(['Depot-06', 'Depot-25', 'Depot-28', 'Depot-41'])] #actual data present for only these depos

up_actual = [0 for i in range(24)]
dn_actual = [0 for i in range(24)]
days = set()

up_source = 0
up_dest = 0
dn_source = 0
dn_dest = 0

# date = '2018-12-05' # for a particular date
date = 'all' # in case of taking average

for index, row in real_trips_file.iterrows():
	trip_id_len = len(row['trip_id'])
	direction = row['trip_id'][trip_id_len - 2: ]
	if(row['trip_id'][:10] != date and date != 'all'):
		continue
	days.add(row['trip_id'][:10])
	if(direction == 'up'):
		up_actual[row['trip_start_hour_of_day']] += 1
		if(up_source == 0):
			up_source = row['from_bus_stop_id']
			up_dest = row['to_bus_stop_id']
	else:
		dn_actual[row['trip_start_hour_of_day']] += 1
		if(dn_source == 0):
			dn_source = row['from_bus_stop_id']
			dn_dest = row['to_bus_stop_id']

num_days = len(days)
print(num_days)
for i in range(24):
	up_actual[i] = round((up_actual[i]/num_days), 2)
	dn_actual[i] = round((dn_actual[i]/num_days), 2)

up_planned = [0 for i in range(24)]
dn_planned = [0 for i in range(24)]

route_trips = form_four_file[form_four_file['route_number'] == route_no]
for index, row in route_trips.iterrows():
	hour = int(row['start_time'][:2])
	if(row['route_direction'] == 'UP'):
		if(row['start_point'] == up_source and row['end_point'] == up_dest):
			up_planned[hour] += 1
	else:
		if(row['start_point'] == dn_source and row['end_point'] == dn_dest):
			dn_planned[hour] += 1

csv_columns = ['hour_of_day', 'no_planned_trips', 'no_actual_trips']
csv_file = route_no + '_trip_kpi.csv'

data = []
for i in range(24):
	row = {}
	row['hour_of_day'] = i
	row['no_actual_trips'] = up_actual[i] + dn_actual[i]
	row['no_planned_trips'] = up_planned[i] + dn_planned[i]
	data.append(row)

try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for row in data:
        	writer.writerow(row)
except IOError:
    print("I/O error")
