from datetime import datetime
import json
import os


class Utils:
    TEST_REPORT_DIR: dir() = None
    START_TIME: str = None

    @staticmethod
    def extract_json(file_name: str) -> []:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        with open(file_path, 'r') as f:
            data = json.load(f)
        array = data["queries"]
        return array

    @staticmethod
    def create_test_folder_and_start_time(request):
        Utils.START_TIME = Utils.get_current_datetime()
        test_name = request.node.originalname
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        test_report_dir = os.path.join(project_root, 'reports', test_name)
        os.makedirs(test_report_dir, exist_ok=True)
        Utils.TEST_REPORT_DIR = test_report_dir

    @staticmethod
    def get_current_datetime() -> str:
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]
        return current_datetime
