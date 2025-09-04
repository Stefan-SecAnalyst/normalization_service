import json
import jsonschema
import os


# Define the path to Config
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..'))
config_dir = os.path.join(project_root, 'config')

# Validate Json Schema and Sample Config
def load_json_files():
    try:
        with open(os.path.join(config_dir, 'schema.json'), 'r') as schema_file:
            config_schema = json.load(schema_file)
    
    except FileNotFoundError:
        print("Config schema file not found.")
        exit()

    except json.JSONDecodeError as e:
        print("Error decoding JSON from config schema file:", e)
        exit()
    try:
        with open(os.path.join(config_dir, 'normalization_rules.json'), 'r') as config_file:
            config_data = json.load(config_file)

    except FileNotFoundError:
        print("Normalization rules file not found.")

    except json.JSONDecodeError as e:
        print("Error decoding JSON from config schema file:", e)
        exit()

    return config_schema, config_data


def validate_json():
    config_schema, config_data = load_json_files()
    try:
        jsonschema.validate(instance=config_data, schema=config_schema)
        print("JSON data is valid according to the schema.")
    except jsonschema.exceptions.ValidationError as e:
        print("JSON data is invalid:", e)
        exit()
    return config_data
