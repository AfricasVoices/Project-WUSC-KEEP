import argparse
import os

from core_data_modules.cleaners import Cleaners, swahili
from core_data_modules.traced_data.io import TracedDataJsonIO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleans a list of TracedData items")
    parser.add_argument("user", help="User launching this program", nargs=1)
    parser.add_argument("input", help="Path to input file, containing a list of TracedData objects as JSON", nargs=1)
    parser.add_argument("json_output", metavar="json-output",
                        help="Path to write results of cleaning to", nargs=1)

    args = parser.parse_args()
    user = args.user[0]
    input_path = args.input[0]
    json_output_path = args.json_output[0]

    # Load data from JSON file
    with open(input_path, "r") as f:
        data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # Clean survey
    Cleaners.clean_traced_data_iterable(user, data, [
        {"raw": "GENDER_R", "cleaners": swahili.DemographicCleaner.clean_gender},
        {"raw": "AGE_R", "cleaners": swahili.DemographicCleaner.clean_age}
    ])

    # Write json output
    if os.path.dirname(json_output_path) is not "" and not os.path.exists(os.path.dirname(json_output_path)):
        os.makedirs(os.path.dirname(json_output_path))
    with open(json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(data, f, pretty_print=True)
