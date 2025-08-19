import os
import csv


def read_csv_file(file_path):
    csv_dict = {}
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row['system_name']
            csv_dict[key] = row
    print(csv_dict)
    return csv_dict



def parse_file(file_path):
    print(f"Parsing files in directory: {file_path}")
    results = {}
    for name in os.listdir(file_path):
        root, ext = os.path.splitext(name)
        print(f"Found file: {name} with extension: {ext}")
        results[root] = parse_file_type(name, file_path, ext)
    print (results)
    if not results:
        print("No files found in the directory.")
    return results


def parse_file_type(name, file_path,ext):

    """
    Determines the type of file based on its extension.
    
    Args:
        file_path (str): The path to the file.
        
    Returns:
        str: The type of the file ('text', 'binary', or 'unknown').
    """
    if ext in ['.csv']:
        print(f"Parsing {ext} as csv file")
        new_file_path = os.path.join(file_path, name)
        print(f"Reading CSV file: {new_file_path}")
        read_csv_file(new_file_path)
        return 'text'
    elif ext in ['.jpg', '.png', '.gif']:
        print(f"Parsing {ext} as binary file")
        return 'binary'
    elif ext in ['.txt','.md']:
        print(f"Parsing {ext} as text file")
        return 'text'
    elif ext in ['.json']:
        print(f"Parsing {ext} as JSON file")
        return 'json'
    else:
        return 'unknown'

#Finding right path for test files folder
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..'))
test_dir = os.path.join(project_root, 'test_files')

# Check if the test directory exists and list its contents
print("Looking in:", project_root)
if not os.path.exists(test_dir):
    raise FileNotFoundError(f"No such directory: {test_dir}")
for name in os.listdir(test_dir):
    root, ext = os.path.splitext(name)


parse_file(test_dir)