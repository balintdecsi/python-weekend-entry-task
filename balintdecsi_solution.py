from email.policy import default
import sys
import re
from collections import defaultdict
from datetime import datetime as dt
from datetime import timedelta as td
from xml.dom.xmlbuilder import _DOMInputSourceStringDataType

ds_file = sys.argv[1]
dep = sys.argv[2]
arr = sys.argv[3]
bags = sys.argv[4]
is_return = sys.argv[5]

counter = 0
adj_dict = defaultdict(lambda: defaultdict(list))

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
                r'\n'\
                , line
                )
            assert record != None, "Input data does not follow convention described in README"
            adj_dict[record[2]][record[3]].append([record[1],dt.fromisoformat(record[4]),dt.fromisoformat(record[5]),float(record[6]),float(record[8]),int(record[10])])

# way there
total_flights = []
for dest, flights in adj_dict[dep].items():
    # if dest == arr:
    #     output.append(flights)
    for flight in flights:
        route_flights_init = {
            "flights": [
                {
                "flight_no": flight[0],
                "origin": dep,
                "destination": dest,
                "departure": flight[1].isoformat(),
                "arrival": flight[2].isoformat(),
                "base_price": flight[3],
                "bag_price": flight[4] * bags,
                "bags_allowed": flight[5]
                },
            ],
            "bags_allowed": flight[5],
            "bags_count": bags,
            "destination": dest,
            "origin": dep,
            "total_price": flight[3] + flight[4] * bags,
            "travel_time": str(flight[2]-flight[1])
        }
        total_flights.append(route_planner(route_flights_init,dest,adj_dict))
total_flights = [flight if flight["destination"] == arr else [] for flight in total_flights]

def route_planner(route_flights, prev_dest, upd_adj_dict):
    prev_flight_arr = route_flights["flights"][-1][2]

    if prev_dest == arr:
        return route_flights
    else:
        airport_flights = []
        for next_dest, next_flights in upd_adj_dict[prev_dest].items():
            if next_dest in map(lambda x: x["origin"], route_flights["flights"]):
                continue
            else:
                for next_flight in next_flights:
                    if next_flight[1] < (prev_flight_arr + td(hours=1)) or next_flight[1] > (prev_flight_arr + td(hourse=6)) or next_flight[5] < bags:
                        continue
                    else:
                        route_flights["flights"].append({
                            "flight_no": next_flight[0],
                            "origin": prev_dest,
                            "destination": next_dest,
                            "departure": next_flight[1].isoformat(),
                            "arrival": next_flight[2].isoformat(),
                            "base_price": next_flight[3],
                            "bag_price": next_flight[4] * bags,
                            "bags_allowed": next_flight[5]
                        })
                        route_flights["bags_allowed"] = min(ext_flight[5],route_flights["bags_allowed"])
                        route_flights["destination"] = next_dest
                        route_flights["total_price"] += next_flight[3] * bags
                        route_flights["travel_time"] = str(next_flight[2]-dt.fromisoformat(route_flights["flights"][0]["departure"]))
                        airport_flights.append(route_planner(route_flights, next_dest, upd_adj_dict))
        return airport_flights
