import sys
import re
from collections import defaultdict

ds_file = sys.argv[1]
dep = sys.argv[2]
arr = sys.argv[3]
bags = sys.argv[4]
is_return = sys.argv[5]

counter = 0
adj_dict = defaultdict(defaultdict(list))

with open(ds_file, "r") as f:
    for line in f:
        counter += 1
        if counter == 1:
            # header = line.split(",")
            continue
        else:
            record = re.match(
                r'([A-Z]{2}\d{3}),'\
                r'([A-Z]{3}),'\
                r'([A-Z]{3}),'\
                r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}),'\
                r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}),'\
                r'(d+\(.\d+)?),'\
                r'(d+\(.\d+)?),'\
                r'(\d+)'
                , line
                )
            # for field in header:
            #     try:
            #         re_match = matcher(field).fullmatch(next(record))
            #     except KeyError:
            #         print("Field names in csv header should be as defined in README")
            #         raise
            assert record != None, "Input data does not follow convention described in README"
            adj_dict[record[2]][record[3]].append([record[1],record[4],record[5],record[6],record[7],record[8]])


            # if field == "flight_no":
            #     curr_flight_no = re_match.group(0)
            # elif field == "origin":
            #     curr_origin = re_match.group(0)
            # elif field == "arrival":
            #     curr_arrival = re_match.group(0)
            # else:
            #     adj_dict[curr_origin][curr_arrival].append()



            

            
        # match_line = re.match(header[0]+flight_no_pattern+r','+header[1]+ori_dest_pattern+r','+(?P<destination>,(?P<departure>,(?P<arrival>,(?P<base_price>\,(?P<bag_price>\d+),(?P<bags_allowed>))')

# def matcher(field_name):
#     switcher = {
#         "flight_no": flight_no_pattern,
#         "origin": ori_dest_pattern,
#         "destination": ori_dest_pattern,
#         "departure": datetime_pattern,
#         "arrival": datetime_pattern,
#         "base_price": price_pattern,
#         "bag_price": price_pattern,
#         "bags_allowed": bags_pattern
#     }

#     return switcher[field_name]