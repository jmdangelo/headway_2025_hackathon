from embed_documents import embed_data
from search_documents import search_tickets
from assist_with_issue import generate_assistance

elasticsearch_index = "zendesk_tickets_large"
if __name__ == "__main__":
    # Embed data from CSV
    csv_file_path = 'files/snowflake_data.csv'
    embed_data(csv_file_path, batch_size=500, index=elasticsearch_index)

    # Search example
    query = input("Enter your search query: ")
    results = search_tickets(query, size=200, index=elasticsearch_index)

    # Get AI assistance
    ai_response = generate_assistance(query, results)

    # Display results
    print("AI Assistance Response:")
    print(ai_response)
