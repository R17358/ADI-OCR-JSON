import os
import json
import pandas as pd
from tabulate import tabulate


folder_path = r"form_extrction/tables"  # raw string avoids escape issues
output_file = r"form_extrction/tables/all_tables.json"
output_file_table =r"form_extrction/tables/all_tables.txt"


def find_key(json_data, target_key):
    """
    Recursively search for all values of target_key in a nested JSON/dict/list.
    """
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == target_key:
                yield value  # found the key
            if isinstance(value, (dict, list)):
                yield from find_key(value, target_key)
    elif isinstance(json_data, list):
        for item in json_data:
            yield from find_key(item, target_key)
            

def extract_table(folder_path=r"form_extrction/tables", output_file=r"form_extrction/tables/all_tables.json",output_file_tabler=r"form_extrction/tables/all_tables.txt", all_files_data = {}):
    table_str =""
    for i, filename in enumerate(os.listdir(folder_path)):
        table_str+=f"\n\n\n{"*"*80}\nFile{i+1}\n{"*"*80}\n"
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename) 
            # print(file_path) 

            # Load JSON
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # print(json.dumps(data))
                
            file_key = f"file {i}"
            all_files_data[file_key] = []
                
            tables = []
                        
            for val in find_key(data, "tables"):
                # val is a list of tables
                for t in val:
                    # Create empty 2D list for the table
                    rows = [["" for _ in range(t["columnCount"])] for _ in range(t["rowCount"])]

                    # Fill the rows with cell contents
                    for cell in t["cells"]:
                        rows[cell["rowIndex"]][cell["columnIndex"]] = cell.get("content", "")
                        
                    for row_index, row in enumerate(rows):
                        rows[row_index] = [cell if cell.strip() else "NULL" for cell in row]

                    # Store table as a list of dicts (first row as headers)
                    headers = rows[0]
                    table_data = [dict(zip(headers, row)) for row in rows[1:]]
                    all_files_data[file_key].append(table_data)

                    # Create DataFrame after all cells are filled
                    df = pd.DataFrame(rows[1:], columns=rows[0])  # first row as header
                    tables.append(df)

            # Optional: print all tables
            for i, df in enumerate(tables, start=1):
                table_str += (f"\nTable {i}\n:{tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False)}")

                
    with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_files_data, f, indent=4, ensure_ascii=False)
    
    with open(output_file_table, "w", encoding="utf-8") as f:
            f.write(table_str)
    
    return all_files_data, table_str

result_json, result_str = extract_table()
# print(json.dumps(result, indent=2, ensure_ascii=False))