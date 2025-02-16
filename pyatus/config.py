import yaml
import os
from typing import Union

class Config:
    def __init__(
        self, 
        config_file_path: str = "config.yaml",
        reader_folder_path: str = ".",
        reader_source_column: Union[str, int] = 1,
        reader_target_column: Union[str, int] = 2,
        checker_source_lang: str = "en_US",
        checker_target_lang: str = "ja_JP",
        checker_glossary: bool = False,
        checker_glossary_path: str = ".",
        checker_inconsistency_s2t: bool = False,
        checker_inconsistency_t2s: bool = False,
        checker_skip: bool = False,
        checker_identical: bool = False,
        checker_spell: bool = False,
        checker_monolingual: bool = False,
        checker_monolingual_path: str = ".",
        checker_numbers: bool = False,
        checker_unsourced: bool = False,
        checker_unsourced_rev: bool = False,
        checker_length: bool = False,
        writer_output_path: str = "."
    ):
        try:
            with open(config_file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file '{config_file_path}' not found.")
        except UnicodeDecodeError:
            raise UnicodeDecodeError("Configuration file must be encoded in UTF-8.")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {e}")

        try:
            self.reader_folder_path        = data['reader']['folder_path']
            self.reader_source_column      = data['reader']['source_column']
            self.reader_target_column      = data['reader']['target_column']
            self.checker_source_lang       = data['checker']['source_lang']
            self.checker_target_lang       = data['checker']['target_lang']
            self.checker_glossary          = data['checker']['glossary']
            self.checker_glossary_path     = data['checker']['glossary_path']
            self.checker_inconsistency_s2t = data['checker']['inconsistency_s2t']
            self.checker_inconsistency_t2s = data['checker']['inconsistency_t2s']
            self.checker_skip              = data['checker']['skip']
            self.checker_identical         = data['checker']['identical']
            self.checker_spell             = data['checker']['spell']
            self.checker_monolingual       = data['checker']['monolingual']
            self.checker_monolingual_path  = data['checker']['monolingual_path']
            self.checker_numbers           = data['checker']['numbers']
            self.checker_unsourced         = data['checker']['unsourced']
            self.checker_unsourced_rev     = data['checker']['unsourced_rev']
            self.checker_length            = data['checker']['length']
            self.writer_output_path        = data['writer']['output_path']
        except KeyError as e:
            raise KeyError(f"Missing key in configuration file: {e}")

        self.validate_yaml()

    def validate_yaml(self):
        '''
        Validate yaml data
        '''
        # Ensure source_column and target_column are the same type
        if type(self.reader_source_column) != type(self.reader_target_column):
            raise TypeError("source_column and target_column should be of the same type (int or str).")

        # Ensure specified paths exist
        paths_to_check = {
            'reader_folder_path': self.reader_folder_path,
            'checker_glossary_path': self.checker_glossary_path,
            'checker_monolingual_path': self.checker_monolingual_path,
            'writer_output_path': self.writer_output_path
        }
        for key, path in paths_to_check.items():
            if not os.path.exists(path):
                raise FileNotFoundError(f"The specified path for '{key}' does not exist: {path}")

        # Ensure boolean values are properly set
        bool_keys = [
            'checker_glossary', 'checker_inconsistency_s2t', 'checker_inconsistency_t2s', 'checker_skip',
            'checker_identical', 'checker_spell', 'checker_monolingual', 'checker_numbers', 'checker_unsourced',
            'checker_unsourced_rev', 'checker_length'
        ]
        for key in bool_keys:
            if not isinstance(getattr(self, key), bool):
                raise TypeError(f"{key} must be a boolean value (True or False).")
