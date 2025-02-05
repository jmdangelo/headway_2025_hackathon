import csv
import json
import sys
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

csv.field_size_limit(sys.maxsize)

es = Elasticsearch("http://localhost:9200")

model = SentenceTransformer('paraphrase-MPNet-base-v2')

def embed_data(csv_file_path):
    es.indices.create(index="zendesk_tickets", ignore=400, body={
        "mappings": {
            "properties": {
                "subject": {"type": "text"},
                "conversation": {"type": "text"},
                "embedding": {"type": "dense_vector", "dims": 768}
            }
        }
    })

    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            subject = row.get("SUBJECT", "No Subject")
            comments_json = row.get("COMMENTS", "[]")

            try:
                comments = json.loads(comments_json)
            except json.JSONDecodeError:
                comments = []

            conversation = " ".join([
                f"{comment.get('commenter_type', 'unknown')}: {comment.get('comment_body', '').strip()}"
                for comment in comments
            ])

            embedding = model.encode(conversation).tolist()

            es.index(index="zendesk_tickets", document={
                "subject": subject,
                "conversation": conversation,
                "embedding": embedding
            })

    print("Zendesk ticket data embedded and stored successfully.")

