# apex_datalog
Export and Visualize Neptune Apex XML Datalog with Grafana

## Overview
This application provides a complete monitoring stack for Neptune Apex Aquarium Controllers. It automates the extraction of historical aquarium data, stores it efficiently, and provides modern visualization tools.

**Key Features:**
*   **Automated ETL**: A Python script exports the Apex XML datalog daily (default: 11:59 PM) and parses the sensor data.
*   **Time-Series Storage**: Data is stored in InfluxDB, allowing for long-term retention and efficient querying.
*   **Visualization**: A pre-configured Grafana dashboard visualizes key metrics like Temperature, pH, ORP, Salinity, and Amp usage.
*   **Containerized**: The entire stack (Python loader, InfluxDB, Grafana) is deployed via Docker Compose.

## Dependencies
Before running this application, ensure you have the following:
*   **Neptune Apex Controller**: Connected to your local network.
*   **Docker & Docker Compose**: Installed on the host machine (e.g., Raspberry Pi, Linux Server, Desktop).
*   **Network Access**: The host machine must be able to reach the Apex controller's IP address.

## Installation
0. Find Apex IP Address via Ping
```
$ ping the_sanctuary.local # <YOUR_APEX_NAME>
PING the_sanctuary.local (192.168.1.131): 56 data bytes
64 bytes from 192.168.1.131: icmp_seq=0 ttl=64 time=0.735 ms
64 bytes from 192.168.1.131: icmp_seq=1 ttl=64 time=0.690 ms
```
1. Replace `docker-compose.yml` fields with your own
```
      DOCKER_INFLUXDB_INIT_USERNAME: admin # TODO: change
      DOCKER_INFLUXDB_INIT_PASSWORD: your_admin_password # TODO: change
      DOCKER_INFLUXDB_INIT_ORG: Ugreen_Apex
      DOCKER_INFLUXDB_INIT_BUCKET: apex_datalog
      DOCKER_INFLUXDB_INIT_ADMIN_TOKEN: your_long_secure_token 
      ...
      # Python Script Configuration (Matches variables in apex_loader.py)
      APEX_HOST: http://the_sanctuary.local # <--- CHANGE THIS TO YOUR APEX IP
      ...
      # InfluxDB Connection (Uses same values as the influxdb service above)
      DOCKER_INFLUXDB_INIT_ORG: Ugreen_Apex
      DOCKER_INFLUXDB_INIT_BUCKET: apex_datalog
      DOCKER_INFLUXDB_INIT_ADMIN_TOKEN: your_long_secure_token
      ...      
      - GF_SECURITY_ADMIN_USER=admin # TODO: change
      - GF_SECURITY_ADMIN_PASSWORD=your_admin_password # TODO: change
```
2. Move files to you machine of choice
- Preferably to docker folder
3. Build and Run Docker Images
- The docker containers will run on your machines in an isolated environment
- Keep note of what this machines IP Address is, will be used later `<MACHINE_IP>`.
```
docker compose up -d --build
```

## Dashboards
1. InfluxDB
- This webapp will store the datalogs pulled from Apex
```
http://<MACHINE_IP>:8086/
```
2. Grafana
- This webapp will visualize the datalogs stored in InfluxDB
```
http://<MACHINE_IP>:3000/
```

### Grafana Dashboard
You can find a grafana dashboard template to use in `grafana/dashboard.json` and import to Grafana to get something that should look like this:
![Dashboard](grafana/dashboard.png)
