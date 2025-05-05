import pandas as pd
import csv

class item:
     def __init__(self, station, times, number):
          self.station = station
          self.times = times
          self.number = number



def clean_consolidate(name):  #this function makes sure that there is one name per station/cleans the whitespace
        name = name.strip('"/"')
        if(name.lower().startswith("arrive ")):
             name = name[7:]
        if(name.lower().startswith("leave ")):
             name = name[6:]

        station_key = {"montclair state": "MONTCLAIR STATE UNIVERSITY",
                       "world trade":"WORLD TRADE CENTER",
                       "world financial": "WORLD FINANCIAL CENTER",
                       "summit": "SUMMIT",
                       "airport": "NEWARK INTERNATIONAL AIRPORT",
                       "newark broad": "NEWARK BROAD STREET",
                       "trenton": "TRENTON",
                       "30th": "PHILADELPHIA 30TH STREET"}
        
        for key in station_key:
            if key in name.lower():
                 name = station_key[key]

        return name.upper() if name else None


def clean_times(station_times): #cleans the station times
    cleanarr = []
    for time in station_times:
            clean = ''.join(t for t in time if t.isdigit() or t == ".")
            cleanarr.append(clean)
    return cleanarr



train_numbers = []
train_amorpm = []
stations_dictionary = []
train_data_list = []
train_dict = []



file = open("njtransitdata.csv")
line = file.readline()
j=0
trains  = False

while line:
    line = line.strip()
    if(line.lower().startswith("via") or "Q,Q" in line or line =="" or "Departing from" in line or "STATIONS" in line #getting rid of unwanted lines
    ):
        line = file.readline()
        continue
    if(line.lower().startswith('""')):
        line = line[3:]

    row = line.split(",") #splitting the line by commas

    if all(part.strip().isdigit() for part in row): #separating train numbers
        train_numbers = row[0:]
        train_dict.append(train_numbers)
        line = file.readline()
        continue
    elif("TRAINS" in line):
        train_numbers = row[1:]
        train_dict.append(train_numbers)
        line = file.readline()
        trains = True
        continue

    if("A.M." in line or "P.M." in line): #Finding if its AM or PM 
        train_amorpm = row[0:]
        line = file.readline()
        continue

    station_name = clean_consolidate(row[0]) #finding station name
    if(station_name not in stations_dictionary): #adding to dictionary if its not already in it
        stations_dictionary.append(station_name)
    if(station_name == None):
        continue
    if(trains):
        station_times = row[2:]
        trains = False
    else:
         station_times = row[1:]
    cleantimes = clean_times(station_times)
    i = 0

    while i<len(train_numbers): #creating triplets

        new_item = item(station_name, cleantimes[i] + " " + train_amorpm[i],train_numbers[i])
        i= i+1
        train_data_list.append(new_item)
    
    line = file.readline()
    j+=1


data_frame_rows = []


for triplet in train_data_list: #making rows for the data frame
    if triplet.times == " A.M." or triplet.times == " P.M.":
        triplet.times = None
    data_frame_rows.append({
         "Station": triplet.station,
         "Train Number": triplet.number,
         "Time": triplet.times
    })

df = pd.DataFrame(data_frame_rows)     #creating data frame and organizing it
df_organized = df.pivot_table(index="Station", columns="Train Number", values = "Time", aggfunc='first') 
df_organized = df_organized.sort_index()
df_organized.to_csv("Mahima_Muddu_NJT_Station_Record.csv")



with open('Mahima_Muddu_NJT_Station_Record.csv', 'a') as f: #finding number of trains stopped at each station
    for station in stations_dictionary:
        k = 0
        for triplet in train_data_list:
            if triplet.station == station:
                if not triplet.times == None:
                    k+=1
        f.write(f"{station}: {k} stopping trains\n")
        
     

