import csv, operator
import datetime, calendar
from string import replace
def Sort_Tuple(tup):
    tup.sort(key = lambda x: x[0].split('-')[2])
    return tup


with open('out.csv', 'wb') as f: # output csv file
    writer = csv.writer(f)
    with open('tripocc_SBS-1K.csv','rb') as csvfile: # input csv file
        reader = csv.DictReader(csvfile, delimiter=',')
        array=[]
        dates=[]
        stops=[]
        csvfile.seek(0)

        for row in reader:
            dates.append(row['trip_date'].split('_')[0])
            stops.append(row['busstop'].split('_')[1])
            array.append(row['busstop'].split('_')[0])  #direc
            array.append(row['trip_date'].split('_')[0]) #date

            array.append(row['occ_time'].split()[1]) #time
            array.append(row['busstop'].split('_')[1]) #stop

    lst=[]
    for i in range(0, len(array)-3, 4):
        lst.append((array[i],array[i+1],array[i+2],array[i+3]))
    lst.sort(key = operator.itemgetter(3, 1, 2))

    f.write("%s,%s,%s,%s,%s\n"%("Trip Direction","Date","Time", "Hour","Stop"))
    for i in lst:
        f.write("%s,%s,%s,%s,%s\n"%(i[0],i[1],i[2],i[2].split(":")[0],i[3]))


dates = set(dates)
f.close()
print len(stops)
for stop in set(stops):
    buses={}
    busesDown={}
    with open('out.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        count={k:[] for k in dates}
        countDown = {k:[] for k in dates}
        for row in reader:
            print stop,row['Stop']
            if row['Stop']==stop:
                if row['Trip Direction']=='up':
                    count[row['Date']].append(row["Hour"])
                else:
                    countDown[row['Date']].append(row['Hour'])

        print countDown


        for i in count:
            temp=[]
            j=count[i]
            for k in range(5,23):
                k=str(k)
                if len(k)==1:
                    k="0"+k
                temp.append((k, count[i].count(k)))
            buses[i]=temp

        for i in countDown:
            tempdown=[]
            j=countDown[i]
            for k in range(5,23):
                k=str(k)
                if len(k)==1:
                    k="0"+k
                tempdown.append((k, countDown[i].count(k)))
            busesDown[i]=tempdown
    	print buses


    final=[]
    filename = stop+'up.csv'
    with open(filename,'wb') as f:
        writer = csv.writer(f)
        f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%("Date","Day", "05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22"))
        for i in buses:
            if i=='nan' : i = '2018-12-01'
            final.append((i,buses[i][0][1], buses[i][1][1], buses[i][2][1], buses[i][3][1], buses[i][4][1], buses[i][5][1], buses[i][6][1], buses[i][7][1], buses[i][8][1], buses[i][9][1], buses[i][10][1], buses[i][11][1], buses[i][12][1], buses[i][13][1], buses[i][14][1], buses[i][15][1], buses[i][16][1], buses[i][17][1]))

        final = Sort_Tuple(final)

        for i in final:
            born = datetime.datetime.strptime(i[0], '%Y-%m-%d').weekday()
            f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(i[0], calendar.day_name[born], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[13], i[14], i[15], i[16], i[17], i[18]))
    f.close()

    final=[]
    with open(stop+'down.csv','wb') as f:
        writer = csv.writer(f)
        f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%("Date", "Day", "05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22"))
        print len(busesDown)
        for i in busesDown:
            if i=='nan': i='2018-12-01'
            print len(busesDown[i])
            final.append((i,busesDown[i][0][1], busesDown[i][1][1], busesDown[i][2][1], busesDown[i][3][1], busesDown[i][4][1], busesDown[i][5][1], busesDown[i][6][1], busesDown[i][7][1], busesDown[i][8][1], busesDown[i][9][1], busesDown[i][10][1], busesDown[i][11][1], busesDown[i][12][1], busesDown[i][13][1], busesDown[i][14][1], busesDown[i][15][1], busesDown[i][16][1], busesDown[i][17][1]))
        print "final", final
        final = Sort_Tuple(final)

        for i in final:
            born = datetime.datetime.strptime(i[0], '%Y-%m-%d').weekday()
            f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(i[0], calendar.day_name[born], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[13], i[14], i[15], i[16], i[17], i[18]))
