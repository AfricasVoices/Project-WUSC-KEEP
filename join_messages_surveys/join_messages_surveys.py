import argparse
import os
import time

from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataCSVIO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Joins radio show answers with survey answers on respondents' "
                                                 "phone ids.")
    parser.add_argument("user", help="User launching this program")
    parser.add_argument("json_input_path", metavar="json-input-path",
                        help="Path to the input messages JSON file, containing a list of serialized TracedData objects")
    parser.add_argument("demog_input_path", metavar="demog-input-path",
                        help="Path to the demog JSON file, containing a list of serialized TracedData objects")
    parser.add_argument("json_output_path", metavar="json-output-path",
                        help="Path to a JSON file to write processed messages to")
    parser.add_argument("csv_output_path", metavar="csv-output-path",
                        help="Path to a CSV file to write the joined dataset to")

    args = parser.parse_args()
    user = args.user
    json_input_path = args.json_input_path
    demog_input_path = args.demog_input_path
    json_output_path = args.json_output_path
    csv_output_path = args.csv_output_path

    message_keys = [
        "avf_phone_id",
        "Date",
        "Message"
    ]

    demog_keys = [
        "AGE_R_clean",
        "GENDER_R_clean",
        "LOCATION_R_clean",
        "NATIONALITY_R_clean",
        "LOCATION 1_R_clean",
        "LOCATION 2_R_clean"
    ]

    def load_survey_dict(file_path):
        """
        Loads a survey from a TracedData JSON file into a dict indexed by avf_phone_id

        :param file_path: Path to survey file to load
        :type file_path: str
        :return: Dictionary mapping contact id ('avf_phone_id') to the survey TracedData for that contact.
        :rtype: dict of str -> TracedData
        """
        with open(file_path, "r") as f:
            return {td["avf_phone_id"]: td for td in TracedDataJsonIO.import_json_to_traced_data_iterable(f)}

    # Load messages
    with open(json_input_path, "r") as f:
        data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # Load surveys
    demog_table = load_survey_dict(demog_input_path)

    # Left join messages and demographic surveys on avf_phone_id
    # TODO: Refactor join step into CoreDataModules once satisfied with the implementation.
    # TODO: Note that this approach does not preserve the history of demographic data in the final TracedData
    for td in data:
        if td["avf_phone_id"] in demog_table:
            demog_td = demog_table[td["avf_phone_id"]]

            td.append_data(
                {k: demog_td.get(k) for k in demog_keys if demog_td.get(k) is not None},
                Metadata(user, Metadata.get_call_location(), time.time())
            )

    # Write json output
    if os.path.dirname(json_output_path) is not "" and not os.path.exists(os.path.dirname(json_output_path)):
        os.makedirs(os.path.dirname(json_output_path))
    with open(json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(data, f, pretty_print=True)

    # Output to CSV for analysis
    export_keys = list(message_keys)
    export_keys.extend(demog_keys)

    if os.path.dirname(csv_output_path) is not "" and not os.path.exists(os.path.dirname(csv_output_path)):
        os.makedirs(os.path.dirname(csv_output_path))
    with open(csv_output_path, "w") as f:
        TracedDataCSVIO.export_traced_data_iterable_to_csv(data, f, headers=export_keys)
