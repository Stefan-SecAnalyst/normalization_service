Project Purpose

The Normalization Service is a modular Python tool for parsing, normalizing, and exporting security log data from various formats (CSV, TXT/LOG, JSON/JSONL). It transforms diverse input fields into a consistent schema using config-driven rules, preparing the data for analytics or downstream use.

Project Folder Structure
normalization_service/
│
├── src/               # Main code modules
│
├── config/            # Normalization rules and schema files
│
├── output/            # Where normalized files are saved
│
├── tests/             # Test files (TBD or in-progress)
│
├── requirements.txt   # Project dependencies
├── README.md          # Project documentation
├── .gitignore         # Files/folders to ignore in git
└── LICENSE            # Project license (if present)

src/
1. parser.py

Purpose:
Main pipeline for parsing input files, detecting file type, applying normalization, and saving output. Orchestrates the whole process.

Key Functions:

parse_file_type(name, file_path, ext, loaded_config)
Detects file type and selects the correct parsing/normalization approach for each input file.

parse_file(input_dir, loaded_config)
Iterates through all files in the input directory, calling parse_file_type on each.

file_output(output_path, records, name)
Handles writing normalized output to file, including safe overwrite/copy logic.

prompt_options()
Prompts user for action (overwrite, copy) if output file already exists.

Important Variables:

output_dir
Destination folder for normalized output files.

results
Dict holding all normalized records keyed by input file.

2. normalizer.py

Purpose:
Contains the core logic for transforming (“normalizing”) raw input records to match the consistent, config-driven schema.

Key Functions:

normalize_record(record, rules)
Central function: loops over desired output fields, applies field mapping, normalization functions, and rules.

datetime_normalizer(value, rule)
Converts date/time strings to a desired format.

uppercase_normalizer(value)
Transforms string to uppercase.

lowercase_normalizer(value)
Transforms string to lowercase.

code_normalizer(value, rule)
Validates and normalizes integer code fields (e.g., error codes), enforces min/max.

message_normalizer(rule, value)
Masks message field if certain keywords are present.

Important Variables:

field_map
Dict mapping normalized field names to all possible input keys/aliases for robust field detection.

3. config_utils.py

Purpose:
Handles loading of normalization config and schema files from JSON.

Key Functions:

load_config(config_path)
Loads and returns normalization config dict from a JSON file.

load_schema(schema_path)
Loads and returns a schema dict from a JSON file.

4. csv_utils.py

Purpose:
Specialized helper functions for parsing CSV files and converting them to a list of dicts.

Key Functions:

read_csv_file(file_path)
Reads a CSV file and returns a list of dictionaries for each row.

5. json_utils.py

Purpose:
Specialized helper functions for reading and parsing JSON files (object, array, or JSONL).

Key Functions:

universal_json_reader(file_path)
Reads and parses a JSON file, supporting both arrays and object-per-line formats.

6. text_utils.py

Purpose:
Handles parsing of plain text log files using regex, converting each line into a structured dictionary.

Key Functions:

parse_text_file(file_path)
Reads a TXT/LOG file and extracts structured fields per line using regex.

7. cli.py

Purpose:
Command-line entrypoint for the entire pipeline. Parses arguments, loads config, and runs the main normalization workflow.

Key Functions:

main()
Entry function for CLI use—parses CLI arguments and triggers parsing/normalization.

Important Variables:

args
Stores CLI arguments (--config, --input, etc.)

config/

normalization_rules.json
Defines field-level normalization instructions (types, formats, allowed values, masking, etc.)

schema.json
(If present) Defines the expected structure for validation.

output/

All normalized files are written here.
E.g., sample1_normalized.json

tests/

(To do) Add test files for normalization logic, file type detection, and config loading.

requirements.txt

Lists all Python dependencies required to run the project.

.gitignore

Specifies files/folders to be excluded from version control (e.g., output/, venv/, __pycache__/).