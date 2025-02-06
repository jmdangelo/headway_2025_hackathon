import csv
import json
import sys
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

csv.field_size_limit(sys.maxsize)

es = Elasticsearch("http://localhost:9200")

model = SentenceTransformer('paraphrase-MPNet-base-v2')


def embed_data(csv_file_path, batch_size=500, index="zendesk_tickets"):
    # Ensure the index exists with the correct mapping
    es.indices.create(index=index, ignore=400, body={
        "mappings": {
            "properties": {
                "subject": {"type": "text"},
                "conversation": {"type": "text"},
                "embedding": {"type": "dense_vector", "dims": 768}
            }
        }
    })

    bulk_data = []
    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader):
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

            # Prepare bulk request data
            bulk_data.append({
                "index": {"_index": index}
            })
            bulk_data.append({
                "subject": subject,
                "conversation": conversation,
                "embedding": embedding
            })

            # Send bulk request in batches
            if len(bulk_data) >= batch_size * 2:
                es.bulk(index=index, operations=bulk_data)
                bulk_data = []  # Clear after bulk insert

        # Insert remaining data
        if bulk_data:
            es.bulk(index=index, operations=bulk_data)

    print("Zendesk ticket data embedded and stored successfully.")

def embed_sop_data(file_path, index="sop_articles"):
    es.indices.create(index=index, ignore=400, body={
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "url": {"type": "text"},
                "content": {"type": "text"},
                "embedding": {"type": "dense_vector", "dims": 768}
            }
        }
    })
    
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        articles = [row for row in reader]

    for idx, row in enumerate(articles):
        # print(row)
        title = row.get("title", "No Title")
        content = row.get("Text", "")
        url = row.get("URL", "")

        embedding = model.encode(title).tolist()

        # Index each document individually
        es.index(index=index, document={
            "title": title,
            "content": content,
            "url": url,
            "embedding": embedding
        })

    print("SOP article data embedded and stored successfully.")
