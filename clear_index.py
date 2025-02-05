from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

if es.indices.exists(index="zendesk_tickets"):
    es.indices.delete(index="zendesk_tickets")
    print("Index 'zendesk_tickets' deleted successfully.")
else:
    print("Index 'zendesk_tickets' does not exist.")
