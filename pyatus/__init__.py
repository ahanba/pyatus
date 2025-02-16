from pyatus.config import Config
from pyatus.reader import Reader
from pyatus.checker import Checker
from pyatus.writer import Writer

class Pyatus():
    def __init__(self, config_file: str = "config.yaml"):
        self.config = Config(config_file)

    def read_files(self):
        '''
        Read all CSV and XLSX files in the specified folder including its subfolders.
        '''
        reader = Reader(self.config)
        segments = reader.read_files()
        return segments

    def run_checker(self):
        '''
        Run all checks where True.
        '''
        segments = self.read_files()
        checker = Checker(self.config, segments)
        errors = checker.detect_errors()
        return errors

    def generate_report(self):
        '''
        Generate XLSX error report in the specified folder.
        '''
        writer = Writer(self.config)
        errors = self.run_checker()
        writer.generate_report(errors)

