import os


#Finding right path for test files folder
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..'))
test_dir = os.path.join(project_root, 'test_files')

# Check if the test directory exists and list its contents
print("Looking in:", project_root)
if not os.path.exists(test_dir):
    raise FileNotFoundError(f"No such directory: {test_dir}")
for name in os.listdir(test_dir):
    if name.split('.')[-1] == 'csv':
        print(f"Found CSV file: {name}")
    else:
        print(f"Found non-CSV file: {name}")