import argparse
import os
import time
from os import path

from core_data_modules.cleaners import swahili, DigitCleaner
from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataCodaIO, TracedDataCodingCSVIO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleans a Swahili survey and exports results to Coda.")
    parser.add_argument("user", help="User launching this program", nargs=1)
    parser.add_argument("input", help="Path to input file, containing a list of TracedData objects as JSON", nargs=1)
    parser.add_argument("language", help="Language which the survey responses are in. Used to determine which "
                                         "cleaners to apply.",
                        choices=["arabic", "english", "swahili", "turkana"], nargs=1)
    parser.add_argument("json_output", metavar="json-output",
                        help="Path to a JSON file to write results of cleaning to", nargs=1)
    parser.add_argument("coding_output_mode", metavar="coding-output-mode",
                        help="File format to export data to for coding."
                             "Accepted values are 'coda' or 'coding-mode'", nargs=1, choices=["coda", "coding-csv"])
    parser.add_argument("coding_output_directory", metavar="coding-output-directory",
                        help="Directory to write Coda and Coding CSV files to", nargs=1)

    args = parser.parse_args()
    user = args.user[0]
    input_path = args.input[0]
    language = args.language[0]
    json_output_path = args.json_output[0]
    coding_mode = args.coding_output_mode[0]
    coded_output_directory = args.coding_output_directory[0]

    # Load data from JSON file
    with open(input_path, "r") as f:
        data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # Clean survey with Swahili cleaners
    if language == "swahili":
        for td in data:
            td.append_data(
                {
                    "GENDER_R_clean": swahili.DemographicCleaner.clean_gender(td["GENDER_R"]),
                    "AGE_R_clean": swahili.DemographicCleaner.clean_age(td["AGE_R"])
                },
                Metadata(user, Metadata.get_call_location(), time.time())
            )
    else:
        for td in data:
            td.append_data(
                {
                    "AGE_R_clean": DigitCleaner.clean_number_digits(td["AGE_R"])
                },
                Metadata(user, Metadata.get_call_location(), time.time())
            )

    # Write json output
    if os.path.dirname(json_output_path) is not "" and not os.path.exists(os.path.dirname(json_output_path)):
        os.makedirs(os.path.dirname(json_output_path))
    with open(json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(data, f, pretty_print=True)

    if coding_mode == "coda":
        # Write Coda output
        if not os.path.exists(coded_output_directory):
            os.makedirs(coded_output_directory)

        with open(path.join(coded_output_directory, "gender.csv"), "w") as f:
            TracedDataCodaIO.export_traced_data_iterable_to_coda_with_scheme(
                data, "GENDER_R", "GENDER_R_clean", "Gender", f)

        with open(path.join(coded_output_directory, "age.csv"), "w") as f:
            TracedDataCodaIO.export_traced_data_iterable_to_coda_with_scheme(
                data, "AGE_R", "AGE_R_clean", "Age", f)

        # ATA uses LOCATION/NATIONALITY whereas BIBLIA uses LOCATION 1/LOCATION 2
        if len(data) > 0 and "LOCATION_R" in data[0]:
            with open(path.join(coded_output_directory, "location.csv"), "w") as f:
                TracedDataCodaIO.export_traced_data_iterable_to_coda(
                    data, "LOCATION_R", f)
            with open(path.join(coded_output_directory, "nationality.csv"), "w") as f:
                TracedDataCodaIO.export_traced_data_iterable_to_coda(
                    data, "NATIONALITY_R", f)
        else:
            with open(path.join(coded_output_directory, "location 1.csv"), "w") as f:
                TracedDataCodaIO.export_traced_data_iterable_to_coda(
                    data, "LOCATION 1_R", f)
            with open(path.join(coded_output_directory, "location 2.csv"), "w") as f:
                TracedDataCodaIO.export_traced_data_iterable_to_coda(
                    data, "LOCATION 2_R", f)
    else:
        # Write Coding CSV output
        if not os.path.exists(coded_output_directory):
            os.makedirs(coded_output_directory)

        with open(path.join(coded_output_directory, "gender.csv"), "w") as f:
            TracedDataCodingCSVIO.export_traced_data_iterable_to_coding_csv_with_scheme(
                data, "GENDER_R", "GENDER_R_clean", f)

        with open(path.join(coded_output_directory, "age.csv"), "w") as f:
            TracedDataCodingCSVIO.export_traced_data_iterable_to_coding_csv_with_scheme(
                data, "AGE_R", "AGE_R_clean", f)

        # ATA uses LOCATION/NATIONALITY whereas BIBLIA uses LOCATION 1/LOCATION 2
        if len(data) > 0 and "LOCATION_R" in data[0]:
            with open(path.join(coded_output_directory, "location.csv"), "w") as f:
                TracedDataCodingCSVIO.export_traced_data_iterable_to_coding_csv_with_scheme(
                    data, "LOCATION_R", "LOCATION_R_clean", f)
            with open(path.join(coded_output_directory, "nationality.csv"), "w") as f:
                TracedDataCodingCSVIO.export_traced_data_iterable_to_coding_csv_with_scheme(
                    data, "NATIONALITY_R", "NATIONALITY_R_clean", f)
        else:
            with open(path.join(coded_output_directory, "location 1.csv"), "w") as f:
                TracedDataCodingCSVIO.export_traced_data_iterable_to_coding_csv_with_scheme(
                    data, "LOCATION 1_R", "LOCATION 1_R_clean", f)
            with open(path.join(coded_output_directory, "location 2.csv"), "w") as f:
                TracedDataCodingCSVIO.export_traced_data_iterable_to_coding_csv_with_scheme(
                    data, "LOCATION 2_R", "LOCATION 2_R_clean", f)
