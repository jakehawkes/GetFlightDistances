#! wa_getanswer

import wolframalpha
from pprint import pprint
import pickle

wa_client = wolframalpha.Client('7Q63U9-5PQ2E7LKY6')
# http://api.wolframalpha.com/v2/query?input=distance+from+calgary+to+minneapolis&appid=7Q63U9-5PQ2E7LKY6


iata_codes = {"YYC": "Calgary",
			  "DFW": "Dallas",
			  "MSP": "Minneapolis",
			  "DEN": "Denver",
			  "OMA": "Omaha",
			  "SLC": "Salt Lake City",
			  "ORD": "Chicago",
			  "BOS": "Boston",
			  "SFO": "San Francisco",
			  "IND": "Indianapolis",
			  "DTW": "Detroit",
			  "YYJ": "Victoria BC",
			  "YVR": "Vancouver",
			  "YYZ": "Toronto",
			  "YOW": "Ottawa",
			  "BDL": "Hartford",
			  "YQB": "Quebec City",
			  "YUL": "Montreal",
			  "YQU": "Grande Prairie Alberta",
			  "YZF": "Yellowknife",
			  "YQV": "Norman Wells, Canada",
			  "YEV": "Inuvik, Canada",
			  "CMH": "Columbus",
			  "CCS": "Caracas",
			  "MAR": "Maracaibo",
			  "MUN": "Maturin",
			  "TUL": "Tulsa",
			  "FRA": "Frankfurt",
			  "CAI": "Cairo",
			  "MRD": "Merida",
			  "ANK": "Ankara",
			  "MAI": "Maimi",
			  "UIO": "Quito",
			  "PER": "Perth",
			  "MEL": "Melbourne",
			  "SIN": "Sinagapore",
			  "LAX": "Los Angeles",
			  "CIN": "Cincinati",
			  "ZUR": "Zurich",
			  "SVQ": "Seville",
			  "MAD": "Madrid",
			  "AMS": "Amsterdam",
			  "KTA": "Karratha, Western Australia",
			  "KWI": "Kuwait",
			  "DXB": "Dubai",
			  "LHR": "London Heathrow",
			  "BRU": "Brussels",
			  "BHM": "Birmingham",
			  "PHL": "Philidelphia",
			  "STN": "Stansted UK",
			  "IAD": "Washington Dulles",
			  "MKE": "Milwaukee",
			  "SYR": "Syracuse",
			  "JFK": "New York",
			  }

print "Loading in previous data"
try:
	with open("flight_legs.db", "rb") as handle:
		legs = pickle.load(handle)
except Exception as error:
	print "No database file found. Starting from scratch"
	legs = {}

trips = []
total_distance = 0

print "Reading flight data"
f = open('flights')
for line in f:
	parts = line.split(":")
	if len(parts) == 3:
		trips.append(parts[1].strip())

f.close()

print "Analysing trip legs"
for trip in trips:
	parts = trip.split("-")
	for x in range(0, len(parts) -1):
		leg = parts[x] + "-" + parts[x+1]
		if not leg in legs:
			legs[leg] = 0.0	

# print legs.keys().sorted()
pprint(legs)

print "Retrieving leg distance from Wolfram Alpha"
for leg in legs:
	if legs[leg] != '':
		print "Already have data for " + leg
		continue
	else:
		print "Looking up " + leg

	cities = leg.split("-")
	lookup = "distance between " + iata_codes[cities[0]] + " and " + iata_codes[cities[1]]
	res = wa_client.query(lookup)
	distance = next(res.results).text.split()[0]
	legs[leg] = distance

	with open("flight_legs.db", "wb") as handle:
		pickle.dump(legs, handle, protocol=pickle.HIGHEST_PROTOCOL)

	total_distance = total_distance + float(distance)

	print lookup + " = " + distance

print "Calculating total trip lengths"
for trip in trips:
	parts = trip.split("-")
	trip_length = 0

	for x in range(0, len(parts) -1):
		leg = parts[x] + "-" + parts[x+1]
		trip_length = trip_length + float(legs[leg])

	print trip + " = " + str(trip_length)
	total_distance = total_distance + trip_length

print "Total Distance Flown = " + str(total_distance) 
