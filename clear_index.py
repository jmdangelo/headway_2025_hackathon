import sys
from elasticsearch import Elasticsearch

if len(sys.argv) != 2:
    print("Usage: python clear_index.py <index_name>")
    sys.exit(1)

index = sys.argv[1]

es = Elasticsearch("http://localhost:9200")

if es.indices.exists(index=index):
    es.indices.delete(index=index)
    print(f"Index '{index}' deleted successfully.")
else:
    print(f"Index '{index}' does not exist.")