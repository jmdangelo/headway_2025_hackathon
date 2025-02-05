import csv
import sys

csv.field_size_limit(sys.maxsize)

csv_file_path = 'files/snowflake_data.csv'

unique_ticket_ids = set()

with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        ticket_id = row.get("ZENDESK_TICKET_ID")
        if ticket_id:
            unique_ticket_ids.add(ticket_id)

print(f"Total unique ZENDESK_TICKET_IDs in file: {len(unique_ticket_ids)}")