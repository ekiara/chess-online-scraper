import json
import os
import sys

if len(sys.argv) != 4:
    print(
        "Please provide an input file and output file in the following format: "
        "python `script.py <input-file> <output-file> <key-name>`"
    )
    sys.exit(1)

INPUT_FILENAME = sys.argv[1]
OUTPUT_FILENAME = sys.argv[2]
KEY_NAME = sys.argv[3]

if not os.path.exists(INPUT_FILENAME):
    print(f"Input filename {INPUT_FILENAME} does not exist.")
    sys.exit(1)

if os.path.exists(OUTPUT_FILENAME):
    print(
        f"Output filename {OUTPUT_FILENAME} already exists. "
        "Please provide an alternative output filename."
    )
    sys.exit(1)

with open(INPUT_FILENAME, "r") as f:
    data = json.load(f)

records = len(data)
print(f"Total records: {records}")

values = [obj[KEY_NAME] for obj in data if obj[KEY_NAME] != ""]

with open(OUTPUT_FILENAME, "w") as f:
    f.write("\n".join(values))
