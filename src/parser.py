import os
import csv
import re
import json
import src.config_utils as config_utils
from src.normalizer import normalize_record



pattern = r"\[(?P<timestamp>[^\]]+)\] (?P<system>[^\s]+) (?P<level>[A-Z]+)\((?P<code>\d+)\): (?P<message>.+)"

def record_normalization(records, loaded_Config):
    print(f"Records object is of {type(records)}")
    normalized_records = []
    rules = loaded_Config["fields"]
    for record in records:
        norm = normalize_record(record, rules)
        print(f"This is the new norm: {norm}")
        normalized_records.append(norm)
    return normalized_records

def read_csv_file(file_path):
    csv_list_dict = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            csv_list_dict.append(row)
    print(csv_list_dict)
    return csv_list_dict

def universal_json_reader(file_path):
    """
    Attempts to read a JSON file as:
    1. JSON array (list of dicts)
    2. JSON object (single dict, wrapped in list)
    3. JSONL (one dict per line)
    Returns: list of dicts
    """
    with open(file_path, 'r') as file:
        try:
            obj = json.load(file)  # Try to parse as standard JSON
            if isinstance(obj, list):
                # Case 1: JSON array
                return obj
            elif isinstance(obj, dict):
                # Case 2: Single JSON object, wrap in a list
                return [obj]
        except json.JSONDecodeError:
            # Not standard JSON (probably JSONL), so try line by line
            file.seek(0)  # Go back to start of file
            records = []
            for line in file:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
            return records  # Case 3: JSONL

def parse_text_file(file_path):
    re.compile(pattern)
    parsed_lines = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            match = re.match(pattern, line)
            if match:
                parsed_lines.append(match.groupdict())
    print(parsed_lines)
    return parsed_lines


def parse_file(file_path, loaded_Config):
    print(f"Parsing files in directory: {file_path}")
    results = {}
    for name in os.listdir(file_path):
        root, ext = os.path.splitext(name)
        print(f"Found file: {name} with extension: {ext}")
        results[root] = parse_file_type(name, file_path, ext, loaded_Config)
    print (results)
    if not results:
        print("No files found in the directory.")
    return results


def parse_file_type(name, file_path,ext, loaded_Config):

    """
    Determines the type of file based on its extension.
    
    Args:
        file_path (str): The path to the file.
        
    Returns:
        str: The type of the file ('text', 'binary', or 'unknown').
    """
    new_file_path = os.path.join(file_path, name)
    
    if ext in ['.csv']:
        print(f"Parsing {ext} as csv file")
        print(f"Reading CSV file: {new_file_path}")
        records = read_csv_file(new_file_path)
        normalized = record_normalization(records, loaded_Config)
        print(f"This is the new .csv file normalized form: {normalized}")
        return 'CSV File Read'
    elif ext in ['.jpg', '.png', '.gif', '.md']:
        print(f"Parsing {ext} as non-usable  file")
        return 'binary'
    elif ext in ['.txt', '.log']:
        print(f"Parsing {ext} as text file")
        records = parse_text_file(new_file_path)
        normalized = record_normalization(records, loaded_Config)
        print(f"This is the new .txt file normalized form: {normalized}")
        return 'Text File Read'
    elif ext in ['.json']:
        print(f"Parsing {ext} as JSON file")
        records = universal_json_reader(new_file_path)
        normalized = record_normalization(records, loaded_Config)
        print(f"This is the .json file normalized form {normalized}")
        return 'json'
    else:
        return 'unknown'

#Finding right path for test files folder
script_dir = os.path.dirname(__file__)              
project_root = os.path.abspath(os.path.join(script_dir, '..'))
test_dir = os.path.join(project_root, 'test_files')

#Call validation
loaded_config = config_utils.validate_json()


# Check if the test directory exists and list its contents
print("Looking in:", project_root)
if not os.path.exists(test_dir):
    raise FileNotFoundError(f"No such directory: {test_dir}")
for name in os.listdir(test_dir):
    root, ext = os.path.splitext(name)


parse_file(test_dir, loaded_config)