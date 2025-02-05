import csv
import json

input_csv = 'files/snowflake_data.csv'
output_json = 'files/processed_data.json'

processed_data = []

with open(input_csv, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        subject = row.get("SUBJECT", "No Subject")
        comments_json = row.get("COMMENTS", "[]")

        try:
            comments = json.loads(comments_json)
        except json.JSONDecodeError:
            comments = []

        conversation = [
            f"{comment.get('commenter_type', 'unknown')}: {comment.get('comment_body', '').strip()}"
            for comment in comments
        ]

        processed_data.append({
            "subject": subject,
            "conversation": conversation
        })

with open(output_json, mode='w', encoding='utf-8') as jsonfile:
    json.dump(processed_data, jsonfile, indent=4)

print(f"Processed data saved to {output_json}")