# Ideas for the final README file
limitations - return flight travel time



# Python weekend entry task -- Bálint Décsi

**Hi! This is my proposed solution for the entry task. In the following, I briefly describe its logic.**

The first step is to create a graph represented by an adjacency list, or more precisely, dictionary. The nodes are the flights (represented as tuples) and they are connected if the second one can be reached in a given airport arriving with the first one and also considering the layover rule; thus the edges are directed. 

Secondly, basicly a depth-first search is performed on the graph with a recursive generator (`plan_route`) repeatedly checking for restrictions (i.e. the already visited airports or the number of bags) and taking into consideration if the current flight is returning or not.

I could imagine improving the script with departure and return dates of the trip because as of now, for large datasets it can take a while combining all possible return trips wit hdeparture trips.

If you have any questions, please don't hesitate to contact me.

### Function description
`balintdecsi_solution.py` has the following parameters:

#### positional arguments:
- `dataset`             path to the dataset that stores the flight data in a csv format
- `departure`           airport to depart from
- `arrival`             airport to arrive to

#### optional arguments:
- `-h`, `--help`        show the help message and exit
- `--bags`              the number of checked bags, up to 10
- `--returns`           optional flag if the trip is not one-way

### Returns
The script creates an output file `balintdecsi_output.json` in the current working directory. The output follows the schema shown in the task description.

### Input dataset format
The input dataset must have a header and otherwise follow the pattern of the provided example files.

### Sample behaviour
Let's assume we run the following:
```bash
python3 -m balintdecsi_solution example/example0.csv RFZ WIW --bags=2 --returns
```
The expected result should be this:
```json
[
	{
		"flights": [
			{
				"flight_no": "ZH214",
				"origin": "RFZ",
				"destination": "WIW",
				"departure": "2021-09-02T05:50:00",
				"arrival": "2021-09-02T10:20:00",
				"base_price": 168.0,
				"bag_price": 12.0,
				"bags_allowed": 2
			},
			{
				"flight_no": "ZH214",
				"origin": "WIW",
				"destination": "RFZ",
				"departure": "2021-09-04T23:20:00",
				"arrival": "2021-09-05T03:50:00",
				"base_price": 168.0,
				"bag_price": 12.0,
				"bags_allowed": 2
			}
		],
		"bags_allowed": 2,
		"bags_count": 2,
		"destination": "RFZ",
		"origin": "RFZ",
		"total_price": 384.0,
		"travel_time": "2 days, 22:00:00"
	},
	{
		"flights": [
			{
				"flight_no": "ZH214",
				"origin": "RFZ",
				"destination": "WIW",
				"departure": "2021-09-02T05:50:00",
				"arrival": "2021-09-02T10:20:00",
				"base_price": 168.0,
				"bag_price": 12.0,
				"bags_allowed": 2
			},
			{
				"flight_no": "ZH214",
				"origin": "WIW",
				"destination": "RFZ",
				"departure": "2021-09-09T23:20:00",
				"arrival": "2021-09-10T03:50:00",
				"base_price": 168.0,
				"bag_price": 12.0,
				"bags_allowed": 2
			}
		],
		"bags_allowed": 2,
		"bags_count": 2,
		"destination": "RFZ",
		"origin": "RFZ",
		"total_price": 384.0,
		"travel_time": "7 days, 22:00:00"
	},
	{
		"flights": [
			{
				"flight_no": "ZH214",
				"origin": "RFZ",
				"destination": "WIW",
				"departure": "2021-09-05T05:50:00",
				"arrival": "2021-09-05T10:20:00",
				"base_price": 168.0,
				"bag_price": 12.0,
				"bags_allowed": 2
			},
			{
				"flight_no": "ZH214",
				"origin": "WIW",
				"destination": "RFZ",
				"departure": "2021-09-09T23:20:00",
				"arrival": "2021-09-10T03:50:00",
				"base_price": 168.0,
				"bag_price": 12.0,
				"bags_allowed": 2
			}
		],
		"bags_allowed": 2,
		"bags_count": 2,
		"destination": "RFZ",
		"origin": "RFZ",
		"total_price": 384.0,
		"travel_time": "4 days, 22:00:00"
	}
]
```