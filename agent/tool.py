from typing import List, Optional, Union
import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "sensor_data.xlsx")


def filter_records(
        filter_type: str,
        filter_value: str,
        previous_results: Optional[List[dict]] = None
    ) -> List[dict]:
    

    if previous_results is None:
        df = pd.read_excel(DATA_PATH)
        previous_results = df.to_dict(orient="records")


        

    if filter_type == "value_range":
        min_value = filter_value.get("min") if filter_value.get("min") is not None else float('-inf')
        max_value = filter_value.get("max") if filter_value.get("max") is not None else float('inf')

        return [record for record in previous_results if min_value <= record["value"] <= max_value]
    else:
        return [record for record in previous_results if  record[filter_type] == filter_value]
