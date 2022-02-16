from ast import arg
import sys
import re

ds_file = sys.argv[1]
dep = sys.argv[2]
arr = sys.argv[3]
bags = sys.argv[4]
is_return = sys.argv[5]

counter = 0
flight_no_pattern = r'[A-Z]{2}\d{3})'
ori_dest_pattern = r'[A-Z]{3})'
datetime_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})'
base_price_pattern = r'd+\.\d+)'



with open(ds_file, "r") as f:
    for line in f:
        counter += 1
        if counter == 1:
            header = line.split(",")
            header = list(map(lambda x:r'(?P<'+x+r'>',header))
            continue
        else:
            match_line = re.match(header[0]+flight_no_pattern+r','+header[1]+ori_dest_pattern+r','+(?P<destination>,(?P<departure>,(?P<arrival>,(?P<base_price>\,(?P<bag_price>\d+),(?P<bags_allowed>))')