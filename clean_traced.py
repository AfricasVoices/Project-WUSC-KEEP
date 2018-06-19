import argparse
import os

from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataTheInterfaceIO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleans a list of TracedData items")
    parser.add_argument("user", help="User launching this program", nargs=1)
    parser.add_argument("input", help="Path to input file, containing a list of TracedData objects as JSON", nargs=1)
    parser.add_argument("json_output", metavar="json-output",
                        help="Path to write results of automatic coding to", nargs=1)
    parser.add_argument("interface_output", metavar="interface-output",
                        help="Directory to write The Interface files to", nargs=1)
    # parser.add_argument("coda_output", metavar="coda-output", help="Path to write Coda file to", nargs=1)

    args = parser.parse_args()
    user = args.user[0]
    input_path = args.input[0]
    json_output_path = args.json_output[0]
    interface_output_directory = args.interface_output[0]

    # Load data from JSON file
    with open(input_path, "r") as f:
        data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # Clean survey
    # Cleaners.clean_traced_data_iterable(user, data, [
    #     {"raw": "GENDER_R", "cleaners": swahili.DemographicCleaner.clean_gender},
    #     {"raw": "AGE_R", "cleaners": swahili.DemographicCleaner.clean_age}
    # ])

    # Filter out messages which are only 1 character long
    data = list(filter(lambda td: len(td["Message"]) > 1, data))

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

    # Write Coda output
    # if os.path.dirname(coda_output_path) is not "" and not os.path.exists(os.path.dirname(coda_output_path)):
    #     os.makedirs(os.path.dirname(coda_output_path))
    # with open(coda_output_path, "w") as f:
    #     TracedDataCodaIO.export_traced_data_iterable_to_coda(
    #         data, gender_col, f, exclude_coded_with_key=gender_col_clean)
