import os
import pandas as pd
import csv

class Reader:
    def __init__(self, myconfig):
        # read config
        self.folder_path   = myconfig.reader_folder_path
        self.source_column = myconfig.reader_source_column
        self.target_column = myconfig.reader_target_column
        
        # List of segments
        self.segments = []
        
    def read_files(self) -> list:
        '''
        Read CSV and XLSX files in the specified folder including its subfolders.
        Returns a list of Dictionary.
        Segment info is in the following format:

        {
            'file': 'full file path' (str),
            'source': 'source text' (str),
            'target': 'target text' (str),
            'id': 'Column A's value' (str)
        }
        '''
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            #print(file_path)
            if filename.endswith('.csv'):
                print(f"Reading: {file_path}")
                self._read_csv(file_path)
            elif filename.endswith('.xlsx'):
                print(f"Reading: {file_path}")
                self._read_xls(file_path)
        
        return self.segments

    def _read_csv(self, file_path: str) -> list:
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                rows = list(reader)
                total_rows = len(rows)
                
                if total_rows == 0:
                    print(f"Skipping empty file: {file_path}")
                    return
                
                for row in rows:
                    new_segment = {}

                    # get the file path
                    new_segment["file"] = file_path
                    # case: column is specified by integer
                    if type(self.source_column) == int and type(self.target_column) == int:
                        new_segment["source"] = list(row.values())[self.source_column]
                        new_segment["target"] = list(row.values())[self.target_column]
                    # case: column is specified by header string
                    elif type(self.source_column) == str and type(self.target_column) == str:
                        new_segment["source"] = row[self.source_column]
                        new_segment["target"] = row[self.target_column]
                    # get the value of the first column as "id"
                    new_segment["id"] = list(row.values())[0]
                    
                    self.segments.append(new_segment)
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    def _read_xls(self, file_path: str) -> list:
        try:
            df = pd.read_excel(file_path)

            total_rows = len(df)
            
            if total_rows == 0:
                print(f"Skipping empty file: {file_path}")
                return
            
            for index, row in df.iterrows():
                new_segment = {}

                # get the file path
                new_segment["file"] = file_path
                # case: column is specified by integer
                if type(self.source_column) == int and type(self.target_column) == int:
                    new_segment["source"] = list(row)[self.source_column]
                    new_segment["target"] = list(row)[self.target_column]
                # case: column is specified by header string
                elif type(self.source_column) == str and type(self.target_column) == str:
                    new_segment["source"] = row[self.source_column]
                    new_segment["target"] = row[self.target_column]
                # get the value of the first column as "id"
                new_segment["id"] = list(row)[0]
                
                self.segments.append(new_segment)
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
