import json
import boto3
import psycopg2
import requests
from datetime import datetime

REDSHIFT_DB = "your_redshift_db"
REDSHIFT_USER = "your_username"
REDSHIFT_PASSWORD = "your_password"
REDSHIFT_HOST = "your-cluster-name.region.redshift.amazonaws.com"
REDSHIFT_PORT = 5439

POWERBI_ENDPOINT = "https://api.powerbi.com/beta/your-streaming-dataset-url"

def lambda_handler(event, context):
    try:
        conn = psycopg2.connect(
            dbname=REDSHIFT_DB,
            user=REDSHIFT_USER,
            password=REDSHIFT_PASSWORD,
            host=REDSHIFT_HOST,
            port=REDSHIFT_PORT
        )

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM your_glue_schema.vehicle_data ORDER BY timestamp DESC LIMIT 10;")
        rows = cursor.fetchall()

        # Format for Power BI Streaming API
        for row in rows:
            data = {
                "id": row[0],
                "deviceID": row[1],
                "timestamp": row[2].isoformat(),
                "latitude": row[3],
                "longitude": row[4],
                "speed": row[6]
            }

            r = requests.post(POWERBI_ENDPOINT, data=json.dumps([data]), headers={"Content-Type": "application/json"})
            print(f"Posted: {data} | Status: {r.status_code}")

        cursor.close()
        conn.close()
        return {"statusCode": 200, "body": "Success"}

    except Exception as e:
        print("Error:", str(e))
        return {"statusCode": 500, "body": str(e)}
