import boto3
import json
from botocore.exceptions import ClientError

# Load schema and config
def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

schema = load_json('../configs/glue_schema.json')
config = load_json('../configs/glue_config.json')

# Convert schema for Glue format
glue_columns = [{"Name": col["Name"], "Type": col["Type"]} for col in schema]

# Glue client
glue = boto3.client('glue', region_name=config['region'])

# === 1. Check/Create Database ===
try:
    glue.get_database(Name=config["database_name"])
    print(f"Database '{config['database_name']}' already exists.")
except glue.exceptions.EntityNotFoundException:
    glue.create_database(DatabaseInput={"Name": config["database_name"]})
    print(f"Database '{config['database_name']}' created.")

# === 2. Check Table Existence ===
table_input = {
    "Name": config["table_name"],
    "StorageDescriptor": {
        "Columns": glue_columns,
        "Location": config["s3_input_path"],
        "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
        "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
        "SerdeInfo": {
            "SerializationLibrary": "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe",
            "Parameters": {
                "field.delim": ","
            }
        }
    },
    "TableType": "EXTERNAL_TABLE",
    "Parameters": {
        "classification": config["classification"],
        "has_encrypted_data": "false"
    }
}

try:
    glue.get_table(DatabaseName=config["database_name"], Name=config["table_name"])
    print(f"Table '{config['table_name']}' exists — updating it.")
    glue.update_table(DatabaseName=config["database_name"], TableInput=table_input)
except glue.exceptions.EntityNotFoundException:
    glue.create_table(DatabaseName=config["database_name"], TableInput=table_input)
    print(f"Table '{config['table_name']}' created.")

print("Glue table is ready for Athena.")
