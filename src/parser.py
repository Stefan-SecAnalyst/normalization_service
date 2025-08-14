import os



def parse_file(file_path):
    results = {}
    for name in os.listdir(file_path):
        root, ext = os.path.splitext(name)
        print(f"Found file: {name} with extension: {ext}")
        results[root] = parse_file_type(ext)
    print (results)
    if not results:
        print("No files found in the directory.")
    return results


def parse_file_type(ext):

    """
    Determines the type of file based on its extension.
    
    Args:
        file_path (str): The path to the file.
        
    Returns:
        str: The type of the file ('text', 'binary', or 'unknown').
    """
    if ext in ['.txt', '.csv', '.md']:
        print(f"Parsing {ext} as text file")
        return 'text'
    elif ext in ['.jpg', '.png', '.gif']:
        print(f"Parsing {ext} as binary file")
        return 'binary'
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