#!/usr/bin/env python3
# Copyright (C) 2016 Karl R. Wurst
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301,
# USA

#######################################################################
# Given a CSV file generated from the downloaded XLS from a Doodle poll,
# determines which pair of suggested date/time options cover the largest
# number of unique respondents.

# Call as
# python doodle-poll-analysis.py filename.csv

# where
# filename is a CSV file exported from the XLS file from Doodle

import sys
import itertools

filename = (sys.argv)[1]

f = open(filename)

# get rid of title lines
f.readline()
f.readline()
f.readline()


headers = f.readline().strip().split(',')

# build dictionary with one entry for each date/time
# the entry will be an empty set
dict = {}
for pos in range(1,len(headers)):
    dict[headers[pos]] = set()

# fill the sets with the students who checked off that time
count = 0
for line in f:
    list = line.strip().split(',')
    count = count+1
    for pos in range(1,len(headers)):
        if list[pos] == 'OK':
            dict[headers[pos]].add(list[0])

# get all the sets
dates = dict.items()

# make all possible pairs of date/time combinations
pairs = itertools.combinations(dates, 2)

dateslist = []
# for every date/time pair
# print date/time pair
# print number of student in the union of the two sets
for pair in pairs:
    firstdate = pair[0][0]
    seconddate = pair[1][0]
    firstset = pair[0][1]
    secondset = pair[1][1]
    unique = len(firstset.union(secondset))
    dateslist.append([unique, firstdate, len(firstset), seconddate, len(secondset)])

print(count-1,'Respondents')
print()

for date in sorted(dateslist,reverse=True):
    print(date[1], 'and', date[3])
    print('Unique students:', date[0])
    print('Overlap:', abs(date[2]+date[4]-date[0]))
    print(date[1], date[2], 'students')
    print(date[3], date[4], 'students')
    print()

