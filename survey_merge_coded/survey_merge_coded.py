import argparse
import os
from os import path

from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataCodaIO, TracedDataCodingCSVIO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merges manually cleaned files back into a traced data file.")
    parser.add_argument("user", help="User launching this program", nargs=1)
    parser.add_argument("input", help="Path to JSON input file, which contains a list of TracedData objects", nargs=1)
    parser.add_argument("coding_mode", metavar="coding-mode",
                        help="How to interpret the files in the coding-input-directory. "
                             "Accepted values are 'coda' or 'coding-mode'", nargs=1, choices=["coda", "coding-csv"])
    parser.add_argument("coding_input", metavar="coding-input-directory",
                        help="Directory to read coding files from", nargs=1)
    parser.add_argument("json_output", metavar="json-output",
                        help="Path to a JSON file to write results of cleaning to", nargs=1)

    args = parser.parse_args()
    user = args.user[0]
    input_path = args.input[0]
    coding_mode = args.coding_mode[0]
    coded_input_directory = args.coding_input[0]
    json_output_path = args.json_output[0]

    # Load data from JSON file
    with open(input_path, "r") as f:
        data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    if coding_mode == "coda":
        # Merge manually coded Coda files into the cleaned dataset.
        with open(path.join(coded_input_directory, "gender.csv"), "r") as f:
            data = list(TracedDataCodaIO.import_coda_to_traced_data_iterable(
                user, data, "GENDER_R", "GENDER_R_clean", f, True))

        with open(path.join(coded_input_directory, "age.csv"), "r") as f:
            data = list(TracedDataCodaIO.import_coda_to_traced_data_iterable(
                user, data, "AGE_R", "AGE_R_clean", f, True))

        with open(path.join(coded_input_directory, "location.csv"), "r") as f:
            data = list(TracedDataCodaIO.import_coda_to_traced_data_iterable(
                user, data, "LOCATION_R", "LOCATION_R_clean", f, True))

        with open(path.join(coded_input_directory, "nationality.csv"), "r") as f:
            data = list(TracedDataCodaIO.import_coda_to_traced_data_iterable(
                user, data, "NATIONALITY_R", "NATIONALITY_R_clean", f, True))
    else:
        # Merge manually coded CSV files into the cleaned dataset.
        with open(path.join(coded_input_directory, "gender.csv"), "r") as f:
            data = list(TracedDataCodingCSVIO.import_coding_csv_to_traced_data_iterable(
                user, data, "GENDER_R", "GENDER_R_clean", "GENDER_R", "GENDER_R_clean", f, True))

        with open(path.join(coded_input_directory, "age.csv"), "r") as f:
            data = list(TracedDataCodingCSVIO.import_coding_csv_to_traced_data_iterable(
                user, data, "AGE_R", "AGE_R_clean", "AGE_R", "AGE_R_clean", f, True))

        with open(path.join(coded_input_directory, "location.csv"), "r") as f:
            data = list(TracedDataCodingCSVIO.import_coding_csv_to_traced_data_iterable(
                user, data, "LOCATION_R", "LOCATION_R_clean", "LOCATION_R", "LOCATION_R_clean", f, True))

        with open(path.join(coded_input_directory, "nationality.csv"), "r") as f:
            data = list(TracedDataCodingCSVIO.import_coding_csv_to_traced_data_iterable(
                user, data, "NATIONALITY_R", "NATIONALITY_R_clean", "NATIONALITY_R", "NATIONALITY_R_clean", f, True))

    # Write coded data back out to disk
    if os.path.dirname(json_output_path) is not "" and not os.path.exists(os.path.dirname(json_output_path)):
        os.makedirs(os.path.dirname(json_output_path))
    with open(json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(data, f, pretty_print=True)
