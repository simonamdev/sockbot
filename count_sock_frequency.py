import time
import csv
from pprint import pprint


times = []
with open('socks.csv', 'r', newline='') as csvfile:
    sockreader = csv.reader(csvfile, delimiter=',')
    for sock, time_epoch in sockreader:
        # convert to usable data types
        times.append(float(time_epoch))

# convert the epoch seconds to time structs
time_structs = [time.gmtime(datetime) for datetime in times]
day_counts = dict()
previous_stamp = ''
for t in time_structs:
    time_stamp = '{}_{}_{}'.format(t.tm_mday, t.tm_mon, t.tm_year)
    if not time_stamp == previous_stamp:
        day_counts[time_stamp] = 1
    else:
        day_counts[time_stamp] += 1
    previous_stamp = time_stamp
pprint(sorted(day_counts.items(), key=lambda d: d[1]))
