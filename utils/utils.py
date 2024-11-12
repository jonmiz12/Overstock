from datetime import datetime
import json
import os


class Utils:
    TEST_REPORT_DIR: dir() = None
    START_TIME: str = None

    # Converts the page directory into the correspondant locators json file directory
    @staticmethod
    def convert_to_locators_directory(file_path: str) -> str:
        this_file_path = os.path.abspath(file_path)
        locators_path = str(this_file_path.replace("pages", "locators")).replace(".py", ".json")
        return locators_path

    # extract the relevant test data from the relevant json file in test_data folder
    @staticmethod
    def extract_test_data(file_path: str) -> []:
        extracted_path = file_path.split("tests")[-1].replace(".py", "").lstrip(os.sep)
        temp = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        json_path = os.path.join(temp, "test_data", extracted_path + ".json")
        with open(json_path, 'r') as f:
            data = json.load(f)
        array = data["data"]
        return array

    # Creates a test folder in the reports folder sets the START_TIME in the Utils class
    @staticmethod
    def create_test_folder_and_start_time(request):
        Utils.START_TIME = Utils.get_current_datetime()
        test_name = request.node.originalname
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        test_report_dir = os.path.join(project_root, 'reports', test_name)
        os.makedirs(test_report_dir, exist_ok=True)
        Utils.TEST_REPORT_DIR = test_report_dir

    # returns the current date and time as a string
    @staticmethod
    def get_current_datetime() -> str:
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]
        return current_datetime
