from email.policy import default
import sys
import re
from collections import defaultdict
from datetime import datetime as dt
from datetime import timedelta as td

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
output = dict([])



# return