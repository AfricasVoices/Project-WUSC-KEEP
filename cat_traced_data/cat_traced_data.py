import argparse
import os

from core_data_modules.traced_data.io import TracedDataJsonIO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Concatenates two serialised TracedData JSON files togther into"
                                                 "a single file.")
    parser.add_argument("user", help="User launching this program", nargs=1)
    parser.add_argument("json_input_1", metavar="json-input-1",
                        help="Path to input file to concatenate, containing a list of TracedData objects as JSON",
                        nargs=1)
    parser.add_argument("json_input_2", metavar="json-input-2",
                        help="Path to input file to concatenate, containing a list of TracedData objects as JSON",
                        nargs=1)
    parser.add_argument("json_output", metavar="json-output",
                        help="Path to write results of cleaning to", nargs=1)

    args = parser.parse_args()
    user = args.user[0]
    json_input_path_1 = args.json_input_1[0]
    json_input_path_2 = args.json_input_2[0]
    json_output_path = args.json_output[0]

    # Load data from JSON file
    with open(json_input_path_1, "r") as f:
        input_data_1 = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    with open(json_input_path_2, "r") as f:
        input_data_2 = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # Concatenate files
    output_data = list(input_data_1)
    output_data.extend(input_data_2)

    # Write json output
    if os.path.dirname(json_output_path) is not "" and not os.path.exists(os.path.dirname(json_output_path)):
        os.makedirs(os.path.dirname(json_output_path))
    with open(json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(output_data, f, pretty_print=True)
