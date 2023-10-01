import requests

PROJECT_ID = "<project_name>"

payload = {
    "source_conn": {
        "source_type": "MSSQL",
        "host": "35.225.164.168",
        "port": 1433,
        "user": "striim1219",
        "password": "fortran21",
        "database": "adventure-works-2019"
    },
    "target_conn": {
        "source_type": "Postgres",
        "host": "127.0.0.1",
        "port": 15432,
        "user": "postgres",
        "password": "q13%Huu-/jG*=8ln",
        "database": "postgres"
    },
    "type": "Schema",
    "schema_name": "dbo",
    "table_name": "departments",
    "target_schema_name": "public",
    "target_table_name": "departments",
    "grouped_columns": [],
    "aggregates": [
        {
            "source_column": None,
            "target_column": None,
            "field_alias": "count",
            "type": "count"
        }
    ],
    "threshold": 0.0,
    "result_handler": None,
    "labels": [
        ["label_1_name", "label_1_value"],
        ["label_2_name", "label_2_value"]
    ],
    "format": "table"
}

url = "http://35.188.117.143:9082/"
res = requests.post(url=url, json=payload)
print(res.content.decode())
