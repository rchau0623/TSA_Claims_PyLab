#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 18:38:05 2018

@author: ryan
"""

import pylab
import csv
from datetime import datetime
import random

def scrubbydubdub():
    source = 'TSA-Claims.csv'
    target = 'TSA-Claims-output.csv'
    try:
        s = open(source, 'r')
    except Exception as e:
        print('File not found or could not be opened.')
        print(e)
    else:
        lines_written = 0
        t = open(target, 'w')
        author = csv.writer(t,delimiter = ',')
        for line in s:
            row = line.strip().replace('Books,','Books &') .split(',')
            row = row[1:len(row)]
            if len(row) < 2:
                continue
            # Here I add a new column, which is the difference in days between
            # Date Received and Incident Date.
            if lines_written == 0:
                lines_written += 1
                row.insert(2,'Processing Time (Days)')
                author.writerow(row)
                continue
            row[0] = row[0][0:10]
            row[1] = row[1][0:10]
            row.insert(2,difference_date(row[1], row[0])) 
            # Here I am scrubbing my data. For my purposes, I only want to check
            # when the Claim Site is Checked Baggage. I also want to filter out 
            # airport codes ZZZ, ZZX, and - as these are not real airports, Claim
            # Types Personal Injury and Motor Vehicle, as these do not concern
            # baggage. Finally I filtered out rows with a lack of desposition.
            if row[7] == 'Checked Baggage' and not (row[3] == 'ZZZ' or row[3] == 'ZZX' or row[3] == '-' or row[6] == 'Personal Injury' or row[6] == 'Motor Vehicle' or row[10] == '-'):
                lines_written += 1
                row[8] ='\"' + row[8] + '\"'
                row[10] = row[10].strip()
                author.writerow(row)
        s.close()
        t.close()
        print(lines_written, 'lines written')
       
def difference_date(x, y):
    a = datetime.strptime(x, "%m/%d/%Y")
    b = datetime.strptime(y, "%m/%d/%Y")
    delta = b - a
    return delta.days     
    
def pie1():
    source = 'TSA-Claims-output.csv'
    try:
        s = open(source, 'r') 
    except Exception as e:
        print('File not found or could not be opened.')
        print(e)
    else:
        header = True
        y = {}
        for line in s:
            row = line.strip().split(',')
            if header:
                header = False
                continue
            if row[10] not in y:
                y[row[10]] = 1
            else:
                y[row[10]] += 1                
                
        pylab.clf()
        pylab.figure(10,figsize=(6,6))
        pylab.axis('equal') # To make this a circle!
        
        # set up the slices
        labels = []
        for keys in y.keys():
            labels.append(keys + ' - ' + str(y[keys]))
        pylab.pie(y.values(), explode=[0.025]*len(y.keys()), labels=labels,autopct='%1.1f%%')
        pylab.title("Dispositions")
        pylab.show()
    
def pie2():
    source = 'TSA-Claims-output.csv'
    try:
        s = open(source, 'r') 
    except Exception as e:
        print('File not found or could not be opened.')
        print(e)
    else:
        header = True
        y = {}
        for line in s:
            row = line.strip().split(',')
            if header:
                header = False
                continue
            if row[6] not in y:
                y[row[6]] = 1
            else:
                y[row[6]] += 1
                
        z = {}
        z['Other'] = 0
        for key in y.keys():
            if y[key] > 2:
                z[key] = y[key]
            else:
                z['Other'] += 1
                
        pylab.clf()
        pylab.figure(10,figsize=(6,6))
        pylab.axis('equal') # To make this a circle!
        
        # set up the slices
        labels = []
        for keys in z.keys():
            labels.append(keys + ' - ' + str(z[keys]))
        pylab.pie(z.values(), explode=[0.025]*len(z.keys()), labels=labels,autopct='%1.1f%%')
        pylab.title("Claim Types")
        pylab.show()
        
def line1():
    source = 'TSA-Claims-output.csv'
    try:
        s = open(source, 'r') 
    except Exception as e:
        print('File not found or could not be opened.')
        print(e)
    else:
        header = True
        airline_dict = {}
            
        for line in s:
            row = line.strip().split(',')
            if header:
                header = False
                continue
            if row[3] not in airline_dict:
                airline_dict[row[3]] = {'01':0,'02':0,'03':0,'04':0,'05':0,'06':0,'07':0,'08':0,'09':0,'10':0,'11':0,'12':0}
                airline_dict[row[3]][row[0][:2]] = 1
            else:
                airline_dict[row[3]][row[0][:2]] += 1
                    
        airline = input("Please input an airport code (i.e. JFK, LAX, etc.): ")
        while len(airline_dict[airline].keys()) < 1:
            airline = input("Invalid airport code, or airport not in database, please input a valid airport code: ")
        
        values = []
        for key in sorted(airline_dict[airline]):
            values.append(airline_dict[airline][key])
            
        pylab.plot(range(1,13),values)
    
        pylab.xlabel('Months in 2014')
        pylab.ylabel('Total Number of Claims Received\n per Month')
        pylab.title('Total Number of Claims Received at ' + airline + '\n per Month')
        pylab.show()
        
def line2():
    source = 'TSA-Claims-output.csv'
    try:
        s = open(source, 'r') 
    except Exception as e:
        print('File not found or could not be opened.')
        print(e)
    else:
        header = True
        y = {}
        totals = {}
        for line in s:
            row = line.strip().split(',')
            if header:
                header = False
                continue
            date = row[0][:2]
            if  date not in y:
                y[date] = int(row[2])
                totals[date] = 1
            else:
                y[date] += int(row[2])
                totals[date] += 1
        values = []
        for key in sorted(y):
            values.append(y[key]/totals[key])
        pylab.plot(range(1,13),values)
    
        pylab.xlabel('Months in 2014')
        pylab.ylabel('Average Number of Days an \nIncident Occured Before Receival \n(Days) ')
        pylab.title("Average Number of Days an Incident\n Occured Before Receival per Month")
        pylab.show()
     
def line3():
    source = 'TSA-Claims-output.csv'
    try:
        s = open(source, 'r') 
    except Exception as e:
        print('File not found or could not be opened.')
        print(e)
    else:
        header = True
        y = {'01':[],'02':[],'03':[],'04':[],'05':[],'06':[],'07':[],'08':[],'09':[],'10':[],'11':[],'12':[]}
        z = {'01':[],'02':[],'03':[],'04':[],'05':[],'06':[],'07':[],'08':[],'09':[],'10':[],'11':[],'12':[]}
        totals = {}
        other_totals = {}
        for line in s:
            row = line.strip().split(',')
            
            if header:
                header = False
                continue
            
            date = row[0][:2]
            
            if  date not in totals:
                if row[3].strip() not in y[date]:
                    y[date].append(row[3].strip())
                totals[date] = 1
            else:
                if row[3].strip() not in y[date]:
                    y[date].append(row[3].strip())
                totals[date] += 1
                
            if date not in other_totals:
                if row[5].strip() not in z[date]:
                    z[date].append(row[5].strip())
                other_totals[date] = 1
            else:
                if row[5].strip() not in z[date]:
                    z[date].append(row[5].strip())
                other_totals[date] += 1

        values = []
        for key in sorted(y):
            values.append(totals[key]/len(y[key]))
        pylab.plot(range(1,13),values, label='Airports')
        
        other_values = []
        for key in sorted(z):
            other_values.append(other_totals[key]/len(z[key]))
        pylab.plot(range(1,13),other_values, label = 'Airlines')
    
        pylab.xlabel('Months in 2014')
        pylab.ylabel('Average Number of Days an \nIncident Occured Before Receival \n(Days) ')
        pylab.title("Average Number of Days an Incident\n Occured Before Receival per Month\n for Airlines vs Airports")
        pylab.legend(loc='upper right', shadow=True, ncol=1)
        pylab.show()

scrubbydubdub()
pie1()
pie2()
line1()
line2()
line3()










