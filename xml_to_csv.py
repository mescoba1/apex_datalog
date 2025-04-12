#!/Users/miguel/homebrew/bin/python3

import xml.etree.ElementTree as ET
import csv
import sys

def xml_to_csv(xml_file, csv_file):
    """
    Converts an XML file to a CSV file.

    Args:
        xml_file (str): Path to the input XML file.
        csv_file (str): Path to the output CSV file.
    """

    tree = ET.parse(xml_file)
    root = tree.getroot()

    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Determine column headers based on XML structure
        # (This example assumes a specific structure)
        #hostname = root["hostname"]
        # "datalog" "hostname", "record", "date", "probe", "name", "value"
        headers = ['Date', 'Tmp', 'pH', 'ORP', "Alkx4", "Cax4", "Mgx4"]
        writer.writerow(headers)

        for record in root.findall('./record'):  # Adjust based on your XML structure
            row = []
            row.append(record.find('date').text)
            for probe in record.findall('./probe'):
                probe_name = probe.find('name').text
                if probe_name in headers:
                    probe_value = probe.find('value').text
                    row.append(probe_value)
            writer.writerow(row)

    print(f"XML data successfully converted to CSV: {csv_file}")

# Example usage:
xml_to_csv(sys.argv[1], sys.argv[2]) 