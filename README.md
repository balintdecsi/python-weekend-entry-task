# Ideas for the final README file
limitations - return flight travel time



# Python weekend entry task -- Bálint Décsi

**Hi! This my propsed solution for the entry task.**

### Function description
`balintdecsi_solution.py` has the following parameters:
positional arguments:
- `dataset`             path to the dataset that stores the flight data in a csv format
- `departure`           airport to depart from
- `arrival`             airport to arrive to
optional arguments:
- `-h`, `--help`        show the help message and exit
- `--bags`              the number of checked bags, up to 10
- `--returns`           optional flag if the trip is not one-way

### Returns
The script creates an output file `balintdecsi_output.json` in the working directory. The output follows the schema shown in the task description.

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