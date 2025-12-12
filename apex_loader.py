import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import time

# --- Configuration (Set using environment variables in Docker Compose) ---
APEX_HOST = os.environ.get("APEX_HOST", "http://the_sanctuary.local")
START_DATE = os.environ.get("START_DATE", "240101")
DAYS_TO_RETRIEVE = int(os.environ.get("DAYS_TO_RETRIEVE", 1))

# --- InfluxDB Configuration (Matches the 'influxdb' service in docker-compose.yml) ---
INFLUX_URL = "http://influxdb:8086" # Service name in docker-compose is 'influxdb'
INFLUX_TOKEN = os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")
INFLUX_ORG = os.environ.get("DOCKER_INFLUXDB_INIT_ORG")
INFLUX_BUCKET = os.environ.get("DOCKER_INFLUXDB_INIT_BUCKET")
MEASUREMENT_NAME = "apex_probes" 

def fetch_apex_data(host, sdate, days):
    """Fetches the datalog.xml from the Neptune Apex controller."""
    url = f"{host}/cgi-bin/datalog.xml?sdate={sdate}&days={days}"
    print(f"Attempting to fetch data from: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        print("Ensure 'Open XML Access' is enabled on your Apex and the host/IP is correct.")
        return None

def parse_xml_to_dataframe(xml_data):
    # (Same parsing logic as before, just kept for completeness)
    if not xml_data: return None
    root = ET.fromstring(xml_data)
    data = []
    
    # Adjusted parsing logic to match standard Apex datalog.xml structure
    for record in root.findall('record'):
        date_node = record.find('date')
        if date_node is None:
            continue
        timestamp_str = date_node.text
        
        try:
            # Use pandas to parse date flexibly
            timestamp = pd.to_datetime(timestamp_str)
        except ValueError:
            continue
        
        row = {'Timestamp': timestamp}
        
        for probe in record.findall('probe'):
            name = probe.find('name').text
            value = probe.find('value').text
            # Try converting to float, otherwise ignore or store as is (if needed)
            try:
                row[name] = float(value)
            except (ValueError, TypeError):
                pass # Skip non-numeric values for InfluxDB float fields
        
        data.append(row)

    if not data:
        print("No log data found in the XML.")
        return None

    return pd.DataFrame(data).set_index('Timestamp').dropna(axis=1, how='all')

def write_data_to_influxdb(df, url, token, org, bucket, measurement):
    """Writes the DataFrame rows as InfluxDB points."""
    print(f"Connecting to InfluxDB at {url}...")
    try:
        with InfluxDBClient(url=url, token=token, org=org) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            
            points = []
            
            # Iterate through the DataFrame and create InfluxDB Points
            for timestamp, row in df.iterrows():
                # Loop through columns (P1, P2, P3, etc.)
                for probe_name, value in row.items():
                    if value is not None:
                        point = (
                            Point(measurement)
                            .tag("probe_id", probe_name)
                            .field("value", value)
                            .time(timestamp, WritePrecision.NS)
                        )
                        points.append(point)
            
            if points:
                print(f"Writing {len(points)} data points to bucket '{bucket}'...")
                write_api.write(bucket=bucket, org=org, record=points)
                print("Write complete.")
            else:
                print("No valid data points to write.")

    except Exception as e:
        print(f"Error writing to InfluxDB: {e}")
        print("Please check InfluxDB configuration (URL, Token, Org, Bucket).")


# --- Main execution ---
if __name__ == '__main__':
    print("Apex Exporter Service Started...")
          
    xml_content = fetch_apex_data(APEX_HOST, current_sdate, DAYS_TO_RETRIEVE)

    if xml_content:
        df = parse_xml_to_dataframe(xml_content)
                
        if df is not None and not df.empty:
            if not all([INFLUX_TOKEN, INFLUX_ORG, INFLUX_BUCKET]):
                print("ERROR: InfluxDB configuration is incomplete.")
            else:
                write_data_to_influxdb(df, INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG, INFLUX_BUCKET, MEASUREMENT_NAME)