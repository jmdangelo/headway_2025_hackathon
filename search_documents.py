from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

es = Elasticsearch("http://localhost:9200")

model = SentenceTransformer('paraphrase-MPNet-base-v2')

def search_tickets(query, size=100, index="zendesk_tickets"):
    query_vector = model.encode(query).tolist()

    response = es.search(index=index, body={
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

    return response['hits']['hits']
