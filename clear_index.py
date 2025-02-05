from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

index = "zendesk_tickets"
if es.indices.exists(index=index):
    es.indices.delete(index=index)
    print(f"Index '{index}' deleted successfully.")
else:
    print(f"Index '{index}' does not exist.")
