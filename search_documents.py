from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

es = Elasticsearch("http://localhost:9200")

model = SentenceTransformer('paraphrase-MPNet-base-v2')

def search_tickets(query, size=100):
    query_vector = model.encode(query).tolist()

    response = es.search(index="zendesk_tickets", body={
        "size": size,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }
    })

    results = []
    for hit in response['hits']['hits']:
        results.append({
            "subject": hit['_source'].get('subject', 'No Subject'),
            "conversation": hit['_source']['conversation']
        })

    return results
