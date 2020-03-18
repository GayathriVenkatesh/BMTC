import pandas as pd 
import csv

route_no = 'SBS-1K'
occ_file_path = '/home/nimisha/sem7/bmtc/TicketDataKPI/nimisha/SBS-1K_occ.xlsx'
route_file_path = '/home/nimisha/sem7/bmtc/TicketDataKPI/nimisha/route.csv'

occ_file = pd.read_excel(occ_file_path)
route_file = pd.read_csv(route_file_path)

route_rows = route_file[route_file['route_number'] == route_no]
route_row_up = route_rows[route_rows['route_direction'] == 'UP']
route_row_down = route_rows[route_rows['route_direction'] == 'DOWN']

trips = {}
min_duration = 40*60 # in seconds
max_duration = 4*3600 # in seconds

def getTrips(dir, source_id, destination_id, source_name, destination_name):
	for index, row in occ_file.iterrows():
		key = row['trip_date'] + '_' + str(row['trip_no'])
		busstop = row['busstop']
		direction = busstop[:2]
		key += '_' + direction
		stop_name = busstop[3:]
		if(direction == dir):
			if(key not in trips):
				value_dict = {}
				value_dict['from_bus_stop_id'] = source_id
				value_dict['to_bus_stop_id'] = destination_id
				value_dict['observed_trip_start_time'] = None
				value_dict['observed_trip_end_time'] = None
				value_dict['travel_duration'] = None
				value_dict['computed_speed'] = None
				value_dict['whether_boardings_observed'] = 'No'
				value_dict['trip_start_hour_of_day'] = None
				trips[key] = value_dict
			if(stop_name == source_name):
				value_dict['observed_trip_start_time'] = row['occ_time']
			elif(stop_name == destination_name):
				value_dict['observed_trip_end_time'] = row['occ_time']
			if(value_dict['whether_boardings_observed'] == 'No' and row['board'] > 0):
				value_dict['whether_boardings_observed'] = 'Yes'

def getDuration(dur):
	hours = int(dur[:2])
	mins = int(dur[3:5])
	secs = int(dur[6:])
	return hours*3600 + mins*60 + secs

def isTripValid(trip):
	if(trip['whether_boardings_observed'] == 'No'):
		return False
	if(trip['observed_trip_start_time'] >= trip['observed_trip_end_time']):
		return False
	duration = getDuration(trip['travel_duration'])
	if(duration < min_duration or duration > max_duration):
		return False
	return True

up_source_id = route_row_up['source_id'].values[0]
up_source_name = route_row_up['source_name'].values[0]
up_destination_id = route_row_up['destination_id'].values[0]
up_destination_name = route_row_up['destination_name'].values[0]

down_source_id = route_row_down['source_id'].values[0]
down_source_name = route_row_down['source_name'].values[0]
down_destination_id = route_row_down['destination_id'].values[0]
down_destination_name = route_row_down['destination_name'].values[0]

getTrips('up', up_source_id, up_destination_id, up_source_name, up_destination_name)
getTrips('dn', down_source_id, down_destination_id, down_source_name, down_destination_name)

for key, value in trips.items():
	value['travel_duration'] = value['observed_trip_end_time'] - value['observed_trip_start_time']
	value['trip_start_hour_of_day'] = value['observed_trip_start_time'].hour 
	duration_hr = value['travel_duration'].components.hours
	duration_min = value['travel_duration'].components.minutes
	value['travel_duration'] = str(value['travel_duration'])[7: ] #removing day component
	if(duration_hr + (duration_min/60) != 0):
		value['computed_speed'] = round(22/(duration_hr + (duration_min/60)), 2)

data = []
for k, v in trips.items():
	v['trip_id'] = k
	if(isTripValid(v)):
		data.append(v)

csv_columns = ['trip_id', 'from_bus_stop_id', 'to_bus_stop_id', 'observed_trip_start_time', 'observed_trip_end_time', 'travel_duration', 'computed_speed', 'whether_boardings_observed', 'trip_start_hour_of_day']
csv_file = route_no + '_realtrips.csv'
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for row in data:
        	writer.writerow(row)
except IOError:
    print("I/O error")