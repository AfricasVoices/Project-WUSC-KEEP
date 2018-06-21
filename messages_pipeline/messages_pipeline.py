import argparse
import os

from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataTheInterfaceIO
from dateutil.parser import isoparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleans a list of TracedData items")
    parser.add_argument("user", help="User launching this program", nargs=1)
    parser.add_argument("input", help="Path to input file, containing a list of TracedData objects as JSON", nargs=1)
    parser.add_argument("json_output", metavar="json-output",
                        help="Path to write results of cleaning to", nargs=1)
    parser.add_argument("interface_output", metavar="interface-output",
                        help="Directory to write The Interface files to", nargs=1)

    args = parser.parse_args()
    user = args.user[0]
    input_path = args.input[0]
    json_output_path = args.json_output[0]
    interface_output_directory = args.interface_output[0]

    # Time range of messages to keep. Messages outside of this range will be dropped.
    # Inclusive lower-bound, exclusive upper-bound
    earliest_time_string = "2018-06-12T20:00:00+03:00"
    latest_time_string = "2018-06-13T00:00:00+03:00"

    # Load data from JSON file
    with open(input_path, "r") as f:
        data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # Filter out messages which are only 1 character long
    data = list(filter(lambda td: len(td["Message"]) > 1, data))

    # Filter out messages received outwith the desired time range
    earliest_time = isoparse(earliest_time_string)
    latest_time = isoparse(latest_time_string)
    data = list(filter(lambda td: earliest_time <= isoparse(td["Date"]) < latest_time, data))

    # Write json output
    if os.path.dirname(json_output_path) is not "" and not os.path.exists(os.path.dirname(json_output_path)):
        os.makedirs(os.path.dirname(json_output_path))
    with open(json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(data, f, pretty_print=True)

    # Write interface output
    if not os.path.exists(interface_output_directory):
        os.makedirs(interface_output_directory)
    TracedDataTheInterfaceIO.export_traced_data_iterable_to_the_interface(
        data, interface_output_directory, "avf_phone_id", "Message", "Date")
