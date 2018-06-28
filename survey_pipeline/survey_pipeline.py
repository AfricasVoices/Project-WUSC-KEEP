import argparse
import os
import time
from os import path

from core_data_modules.cleaners import swahili
from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataCodaIO, TracedDataCodingCSVIO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleans a list of TracedData items")
    parser.add_argument("user", help="User launching this program", nargs=1)
    parser.add_argument("input", help="Path to input file, containing a list of TracedData objects as JSON", nargs=1)
    parser.add_argument("json_output", metavar="json-output",
                        help="Path to a JSON file to write results of cleaning to", nargs=1)
    parser.add_argument("coding_output", metavar="coding-output-directory",
                        help="Directory to write Coda and Coding CSV files to", nargs=1)

    args = parser.parse_args()
    user = args.user[0]
    input_path = args.input[0]
    json_output_path = args.json_output[0]
    coded_output_directory = args.coding_output[0]

    coda_output_directory = path.join(coded_output_directory, "coda")
    coding_csv_output_directory = path.join(coded_output_directory, "coding-csv")

    # Load data from JSON file
    with open(input_path, "r") as f:
        data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # Clean survey with Swahili cleaners
    for td in data:
        td.append_data(
            {
                "GENDER_R_clean": swahili.DemographicCleaner.clean_gender(td["GENDER_R"]),
                "AGE_R_clean": swahili.DemographicCleaner.clean_age(td["AGE_R"])
            },
            Metadata(user, Metadata.get_call_location(), time.time())
        )

    # Write json output
    if os.path.dirname(json_output_path) is not "" and not os.path.exists(os.path.dirname(json_output_path)):
        os.makedirs(os.path.dirname(json_output_path))
    with open(json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(data, f, pretty_print=True)

    # Write Coda output
    if not os.path.exists(coda_output_directory):
        os.makedirs(coda_output_directory)

    with open(path.join(coda_output_directory, "gender.csv"), "w") as f:
        TracedDataCodaIO.export_traced_data_iterable_to_coda_with_scheme(
            data, "GENDER_R", "GENDER_R_clean", "Gender", f)

    with open(path.join(coda_output_directory, "age.csv"), "w") as f:
        TracedDataCodaIO.export_traced_data_iterable_to_coda_with_scheme(
            data, "AGE_R", "AGE_R_clean", "Age", f)

    with open(path.join(coda_output_directory, "location.csv"), "w") as f:
        TracedDataCodaIO.export_traced_data_iterable_to_coda(
            data, "LOCATION_R", f)

    with open(path.join(coda_output_directory, "nationality.csv"), "w") as f:
        TracedDataCodaIO.export_traced_data_iterable_to_coda(
            data, "NATIONALITY_R", f)

    # Write Coding CSV output
    if not os.path.exists(coding_csv_output_directory):
        os.makedirs(coding_csv_output_directory)

    with open(path.join(coding_csv_output_directory, "gender.csv"), "w") as f:
        TracedDataCodingCSVIO.export_traced_data_iterable_to_coding_csv_with_scheme(
            data, "GENDER_R", "GENDER_R_clean", f)

    with open(path.join(coding_csv_output_directory, "age.csv"), "w") as f:
        TracedDataCodingCSVIO.export_traced_data_iterable_to_coding_csv_with_scheme(
            data, "AGE_R", "AGE_R_clean", f)

    with open(path.join(coding_csv_output_directory, "location.csv"), "w") as f:
        TracedDataCodingCSVIO.export_traced_data_iterable_to_coding_csv_with_scheme(
            data, "LOCATION_R", "LOCATION_R_clean", f)

    with open(path.join(coding_csv_output_directory, "nationality.csv"), "w") as f:
        TracedDataCodingCSVIO.export_traced_data_iterable_to_coding_csv_with_scheme(
            data, "NATIONALITY_R", "NATIONALITY_R_clean", f)
