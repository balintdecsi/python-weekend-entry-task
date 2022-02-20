import sys
import re
from collections import defaultdict
from datetime import datetime as dt
from datetime import timedelta as td
from json import dumps


def make_adj_list(sorted_flight_list):
    flight_adj_dict = defaultdict(list)
    for curr_flight in sorted_flight_list:
        remained_flights = iter(sorted_flight_list[(sorted_flight_list.index(curr_flight)+1):])
        while True:
            try:
                next_flight = next(remained_flights)
            except StopIteration:
                break
            else:
                if next_flight[1] == curr_flight[2] and (next_flight[3] > (curr_flight[4] + td(hours=1)) and next_flight[3] < (curr_flight[4] + td(hours=6))):
                    flight_adj_dict[curr_flight].append(next_flight)
                else:
                    break
    return flight_adj_dict

def add_flight(bags,flight_combination,flight_to_add):
    flight_combination["flights"].append({
    "flight_no": flight_to_add[0],
    "origin": flight_to_add[1],
    "destination": flight_to_add[2],
    "departure": flight_to_add[3].isoformat(),
    "arrival": flight_to_add[4].isoformat(),
    "base_price": flight_to_add[5],
    "bag_price": flight_to_add[6] * bags,
    "bags_allowed": flight_to_add[7]
    })
    flight_combination["bags_allowed"] = min(flight_to_add[7],flight_combination["bags_allowed"])
    flight_combination["destination"] = flight_to_add[2]
    flight_combination["total_price"] += flight_to_add[5] + flight_to_add[6] * bags
    flight_combination["travel_time"] = str(flight_to_add[4]-dt.fromisoformat(flight_combination["flights"][0]["departure"]))
    return flight_combination

def plan_route(arr,bags,prev_dest,flight_adj_dict,flight_combination):
    for curr_flight, next_flights in flight_adj_dict:
        if curr_flight[1] != prev_dest or curr_flight[7] < bags or curr_flight[2] in map(lambda x: x["origin"], flight_combination["flights"]):
            continue
        for next_flight in next_flights:
            flight_combination = add_flight(bags,flight_combination,next_flight)
            if next_flight[2] == arr:
                yield flight_combination
            else:
                yield from plan_route(arr,bags,next_flight[2],flight_adj_dict,flight_combination)

# def route_planner(route_flights, prev_dest, upd_adj_dict):
#     prev_flight_arr = dt.fromisoformat(route_flights["flights"][-1]["arrival"])

#     if prev_dest == arr:
#         return route_flights
#     else:
#         airport_flights = []
#         for next_dest, next_flights in upd_adj_dict[prev_dest].items():
#             if next_dest in map(lambda x: x["origin"], route_flights["flights"]):
#                 continue
#             else:
#                 for next_flight in next_flights:
#                     if next_flight[1] < (prev_flight_arr + td(hours=1)) or next_flight[1] > (prev_flight_arr + td(hours=6)) or next_flight[5] < bags:
#                         continue
#                     else:
#                         route_flights["flights"].append({
#                             "flight_no": next_flight[0],
#                             "origin": prev_dest,
#                             "destination": next_dest,
#                             "departure": next_flight[1].isoformat(),
#                             "arrival": next_flight[2].isoformat(),
#                             "base_price": next_flight[3],
#                             "bag_price": next_flight[4] * bags,
#                             "bags_allowed": next_flight[5]
#                         })
#                         route_flights["bags_allowed"] = min(next_flight[5],route_flights["bags_allowed"])
#                         route_flights["destination"] = next_dest
#                         route_flights["total_price"] += next_flight[3] * bags
#                         route_flights["travel_time"] = str(next_flight[2]-dt.fromisoformat(route_flights["flights"][0]["departure"]))
#                         airport_flights.append(route_planner(route_flights, next_dest, upd_adj_dict))
#         return airport_flights

# def flatten(l):
#     if isinstance(l, list):
#         for v in l:
#             yield from flatten(v)
#     else:
#         yield l

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
for route in plan_route(arr,bags,dep,all_flights_adj_dict,):
    output_flights.append(route)

# way there
# total_flights = []
# for dest, flights in adj_dict[dep].items():
#     # if dest == arr:
#     #     output.append(flights)
#     for flight in flights:
#         route_flights_init = {
#             "flights": [
#                 {
#                 "flight_no": flight[0],
#                 "origin": dep,
#                 "destination": dest,
#                 "departure": flight[1].isoformat(),
#                 "arrival": flight[2].isoformat(),
#                 "base_price": flight[3],
#                 "bag_price": flight[4] * bags,
#                 "bags_allowed": flight[5]
#                 },
#             ],
#             "bags_allowed": flight[5],
#             "bags_count": bags,
#             "destination": dest,
#             "origin": dep,
#             "total_price": flight[3] + flight[4] * bags,
#             "travel_time": str(flight[2]-flight[1])
#         }
#         total_flights.append(route_planner(route_flights_init,dest,adj_dict))
# output_flights = []
# for flight in flatten(total_flights):
#     if flight["destination"] != arr or len(flight) == 0:
#         continue
#     else:
#         output_flights.append(flight)

    # except TypeError:
    #     output_flights.append(flight)
    # finally:
    #     if len(flight) != 0:


print(dumps(sorted(output_flights,key=lambda x:x["total_price"]),indent="\t"))