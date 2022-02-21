import argparse
from csv import Sniffer, DictReader
import re
from datetime import datetime as dt, timedelta as td
from copy import deepcopy
from json import dumps


def parse_dataset(filepath):
    """"
    Deserialize the flights data from the raw csv file.

    Arguments:
    filepath -- path to the file containing the data
    """
    all_flights = []
    with open(filepath, newline="") as f:
        sample = "".join([f.readline() for _ in range(22)])
        f.seek(0)
        if Sniffer().has_header(sample):
            f.readline()
        ds_reader = DictReader(
            f,
            fieldnames=["flight_no", "origin", "destination", "departure", "arrival", "base_price", "bag_price", "bags_allowed"])
        for row in ds_reader:
            all_flights.append(
                (row["flight_no"],
                row["origin"], row["destination"],
                dt.fromisoformat(row["departure"]), dt.fromisoformat(row["arrival"]),
                float(row["base_price"]), float(row["bag_price"]),
                int(row["bags_allowed"])))

    return all_flights


def make_adj_dict(sorted_flight_list):
    """
    Make an adjacency dictionary based on elements in a departure time-based sorted list of available flights. (A flight is adjacent to another if its departure airport is the same as the arrival airport of the other and layover rules apply.)

    Arguments:
    sorted_flight_list -- the sorted list containing tuples each representing one flight
    """
    flight_adj_dict = dict()
    for curr_flight in sorted_flight_list:
        flight_adj_dict[curr_flight] = []
        for next_flight in sorted_flight_list[(sorted_flight_list.index(curr_flight) + 1):]:
            if (next_flight[1] == curr_flight[2] and
                    (next_flight[3] > (curr_flight[4] + td(hours=1)) and
                    next_flight[3] < (curr_flight[4] + td(hours=6)))):
                flight_adj_dict[curr_flight].append(next_flight)
                
    return flight_adj_dict


def add_flight(
        bags,
        flight_combination,
        flight_to_add):
    """
    Add a flight with given number of bags to an existing route object.

    Arguments:
    bags -- number of checked bags
    flight_combination -- the route object to update
    flight_to_add -- the flight object to add to the route
    """
    flight_combination["flights"].append(
        {
            "flight_no": flight_to_add[0],
            "origin": flight_to_add[1],
            "destination": flight_to_add[2],
            "departure": flight_to_add[3].isoformat(),
            "arrival": flight_to_add[4].isoformat(),
            "base_price": flight_to_add[5],
            "bag_price": flight_to_add[6],
            "bags_allowed": flight_to_add[7]
        })
    flight_combination["bags_allowed"] = min(flight_to_add[7],flight_combination["bags_allowed"])
    flight_combination["destination"] = flight_to_add[2]
    flight_combination["total_price"] += flight_to_add[5] + flight_to_add[6] * bags
    flight_combination["travel_time"] = str(flight_to_add[4]-dt.fromisoformat(flight_combination["flights"][0]["departure"]))


def plan_route(
        arr,
        bags,
        prev_dest,
        flight_adj_dict,
        flight_adjs,
        flight_combination,
        returns,
        returning):
    """
    Recursive generator that populates all possible routes from the given airport to the given arrival airport using flight data from the given dataset.

    Arguments:
    arr -- airport to arrive to
    bags -- number of checked bags
    prev_dest -- airport to depart from
    flight_adj_dict -- adjacency dictionary that describes graph of all flights of the dataset
    flight_adjs -- adjacency dictionary only with available flights at the given point of the route
    flight_combination -- dictionary with flights previosly taken into account at the given point of the route
    returns -- logical value indicating if this is a departue part of a return trip
    returning -- logical value indicating if this is a returning part of a return trip
    """
    for curr_flight, next_flights in flight_adjs.items():
        if (curr_flight[1] != prev_dest) or (curr_flight[7] < bags):
            continue
        elif not returning:
            if curr_flight[2] in map(lambda x: x["origin"], flight_combination["flights"]):
                continue
        elif returning:
            if curr_flight[2] in map(lambda x: x["origin"], filter(lambda x: x in flight_adj_dict.values(), flight_combination["flights"])):
                continue
        curr_flight_combination = deepcopy(flight_combination)
        add_flight(bags,curr_flight_combination,curr_flight)
        if curr_flight[2] == arr:
            if returns:
                return_flight_adj_dict = make_adj_dict(list(filter(lambda x: x[3] > curr_flight[4], all_flights)))
                yield from plan_route(dep, bags, arr,
                                        return_flight_adj_dict, return_flight_adj_dict,
                                        deepcopy(curr_flight_combination),
                                        False, True)
            else:
                yield curr_flight_combination
        else:
            for next_flight in next_flights:
                yield from plan_route(arr, bags, curr_flight[2],
                                        flight_adj_dict, {k: v for k, v in flight_adj_dict.items() if k == next_flight},
                                        deepcopy(curr_flight_combination),
                                        returns, returning)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Bálint Décsi's solution for the entry task to Kiwi.com Python Weekend in Budapest. For detailed description, please see README.")
    parser.add_argument(
        "dataset",
        action="store",
        nargs=1,
        help="path to the dataset that stores the flight data in a csv format")
    parser.add_argument(
        "departure",
        action="store",
        nargs=1,
        help="airport to depart from")
    parser.add_argument(
        "arrival",
        action="store",
        nargs=1,
        help="airport to arrive to")
    parser.add_argument(
        "--bags",
        action="store",
        nargs=1,
        default=[0],
        type=int,
        choices=[i for i in range(0,11)],
        help="the number of checked bags, up to 10")
    parser.add_argument(
        "--returns",
        action="store_const",
        const=True,
        default=False,
        help="optional flag if the trip is not one-way")

    args = parser.parse_args()

    ds_file = args.dataset[0]
    all_flights = parse_dataset(ds_file)
    all_flights.sort(key = lambda x: x[3])
    dep_airports = set(map(lambda x: x[1], all_flights))
    arr_airports = set(map(lambda x: x[2], all_flights))

    dep = args.departure[0]
    assert dep in dep_airports, "Please enter a departue airport present in the dataset"
    arr = args.arrival[0]
    assert arr in arr_airports, "Please enter an arrival airport present in the dataset"

    bags = args.bags[0]
    returns = args.returns

    all_flights_adj_dict = make_adj_dict(all_flights)

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

    for route in plan_route(
            arr,bags,dep,
            all_flights_adj_dict,all_flights_adj_dict,
            init_flight_combination,
            returns, False):
        route |= {"destination": arr}
        output_flights.append(route)

    print(dumps(sorted(output_flights, key=lambda x: x["total_price"]), indent="\t"))