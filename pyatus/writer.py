import os
import pandas as pd
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class Writer:
    def __init__(self, myconfig):
        try:
            self.output_path = myconfig.writer_output_path
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)
        except AttributeError:
            logging.error("Invalid configuration: 'writer_output_path' not found.")
            raise
        except Exception as e:
            logging.error(f"Error initializing Writer: {e}")
            raise

    def _write_xls(self, output_path, errors):
        if not isinstance(errors, list):
            logging.error("Invalid input: 'errors' should be a list.")
            return

        today = datetime.date.today().strftime('%Y%m%d')
        output_file = os.path.join(output_path, f'{today}_report.xlsx')

        print(f"Generating report: {output_file}.")
        
        columns = ["ID", "File", "Source", "Target", "Category", "Message", "Match"]
        
        try:
            data = [
                [
                    str(error.get('segment', {}).get('id', 'N/A')),
                    error.get('segment', {}).get('file', 'N/A'),
                    error.get('segment', {}).get('source', 'N/A'),
                    error.get('segment', {}).get('target', 'N/A'),
                    error.get('category', 'N/A'),
                    error.get('message', 'N/A'),
                    error.get('match', 'N/A')
                ]
                for error in errors if isinstance(error, dict)
            ]
        except Exception as e:
            logging.error(f"Error processing errors list: {e}")
            return

        if not data:
            logging.warning("No valid error data to write.")
            return

        total_rows = len(data) + 1
        df = pd.DataFrame(data, columns=columns)

        try:
            with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='pyatus report', index=False)
                
                workbook = writer.book
                worksheet = writer.sheets['pyatus report']
                
                cell_format = workbook.add_format({
                    'font_name': 'Arial',
                    'font_size': 11,
                    'bg_color': '#FFFFFF',
                    'border': 1,
                    'border_color': '#4F4F4F',
                    'align': 'left',
                    'valign': 'top'
                })
                
                header_format = workbook.add_format({
                    'font_name': 'Arial',
                    'font_size': 11,
                    'bold': True,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                
                worksheet.conditional_format(f'A1:G{total_rows}', {'type': 'no_errors', 'format': cell_format})
                worksheet.set_row(0, None, header_format)
                worksheet.set_column('A:G', 15)
        except Exception as e:
            logging.error(f"Error writing Excel file: {e}")

    def generate_report(self, errors):
        try:
            self._write_xls(self.output_path, errors)
        except Exception as e:
            logging.error(f"Error generating report: {e}")
