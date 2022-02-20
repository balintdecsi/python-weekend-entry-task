import sys
import re
from collections import defaultdict
from datetime import datetime as dt
from datetime import timedelta as td
from copy import deepcopy
from json import dumps


def make_adj_list(sorted_flight_list):
    flight_adj_dict = dict()
    for curr_flight in sorted_flight_list:
        flight_adj_dict[curr_flight] = []
        for next_flight in sorted_flight_list[(sorted_flight_list.index(curr_flight)+1):]:
            if next_flight[1] == curr_flight[2] and (next_flight[3] > (curr_flight[4] + td(hours=1)) and next_flight[3] < (curr_flight[4] + td(hours=6))):
                flight_adj_dict[curr_flight].append(next_flight)
    return flight_adj_dict

def add_flight(bags,output_flight_combination,flight_to_add):
    # output_flight_combination = flight_combination.copy()
    output_flight_combination["flights"].append({
    "flight_no": flight_to_add[0],
    "origin": flight_to_add[1],
    "destination": flight_to_add[2],
    "departure": flight_to_add[3].isoformat(),
    "arrival": flight_to_add[4].isoformat(),
    "base_price": flight_to_add[5],
    "bag_price": flight_to_add[6] * bags,
    "bags_allowed": flight_to_add[7]
    })
    output_flight_combination["bags_allowed"] = min(flight_to_add[7],output_flight_combination["bags_allowed"])
    output_flight_combination["destination"] = flight_to_add[2]
    output_flight_combination["total_price"] += flight_to_add[5] + flight_to_add[6] * bags
    output_flight_combination["travel_time"] = str(flight_to_add[4]-dt.fromisoformat(output_flight_combination["flights"][0]["departure"]))

def plan_route(arr,bags,prev_dest,flight_adj_dict,flight_adjs,flight_combination):
    for curr_flight, next_flights in flight_adjs.items():
        if curr_flight[1] != prev_dest or curr_flight[7] < bags or curr_flight[2] in map(lambda x: x["origin"], flight_combination["flights"]):
            continue
        else:
            curr_flight_combination = deepcopy(flight_combination)
            add_flight(bags,curr_flight_combination,curr_flight)
            if curr_flight[2] == arr:
                yield curr_flight_combination
            else:
                for next_flight in next_flights:
                    next_flight_combination = deepcopy(curr_flight_combination)
                    # add_flight(bags,next_flight_combination,curr_flight)
                    yield from plan_route(arr,bags,curr_flight[2],flight_adj_dict,{k:v for k,v in flight_adj_dict.items() if k == next_flight},next_flight_combination)

ds_file = sys.argv[1]
dep = sys.argv[2]
arr = sys.argv[3]
bags = int(sys.argv[4])
is_return = sys.argv[5]


counter = 0
all_flights = []

with open(ds_file, "r") as f:
    for line in f:
        counter += 1
        if counter == 1:
            assert re.fullmatch(r'[a-z_]+(,[a-z_]+){7}\n', line) != None, "Does not have header or header does not follow convention described in README"
            continue
        else:
            record = re.fullmatch(
                r'([A-Z]{2}\d{3}),'\
                r'([A-Z]{3}),'\
                r'([A-Z]{3}),'\
                r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}),'\
                r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}),'\
                r'(\d+(\.\d+)?),'\
                r'(\d+(\.\d+)?),'\
                r'(\d+)'\
                r'(\n)?'\
                , line
                )
            assert record != None, "Input data does not follow convention described in README"
            all_flights.append((record[1],record[2],record[3],dt.fromisoformat(record[4]),dt.fromisoformat(record[5]),float(record[6]),float(record[8]),int(record[10])))

all_flights.sort(key=lambda x:x[3])
print(set(map(lambda x:x[1],all_flights)))
all_flights_adj_dict = make_adj_list(all_flights)
output_flights = []
init_flight_combination = {
    "flights": [],
    "bags_allowed": 1000,
    "bags_count": bags,
    "destination": dep,
    "origin": dep,
    "total_price": 0,
    "travel_time": ""
}
for route in plan_route(arr,bags,dep,all_flights_adj_dict,all_flights_adj_dict,init_flight_combination):
    output_flights.append(route)

print(dumps(sorted(output_flights,key=lambda x:x["total_price"]),indent="\t"))