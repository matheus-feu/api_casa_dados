import os

import pandas as pd


def create_excel(result, endpoint: str):
    try:
        excel_file_path = os.path.abspath(f"excel/{endpoint}.xlsx")

        if os.path.exists(excel_file_path):
            os.remove(excel_file_path)

        if not result:
            return None

        if endpoint == 'advanced_search':
            if all(isinstance(item, dict) for item in result):
                df = pd.DataFrame(result)
            else:
                raise ValueError("Expected a list of dictionaries")
        else:
            df = pd.DataFrame([result])

        if not df.empty:
            df.to_excel(excel_file_path, index=False)
            return excel_file_path
        else:
            return None

    except Exception as e:
        raise Exception(f"Error: {str(e)}")
