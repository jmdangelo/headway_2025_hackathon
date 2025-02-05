from embed_documents import embed_data, embed_sop_data
from search_documents import search_tickets
from assist_with_issue import generate_zendesk_assistance, generate_sop_assistance

elasticsearch_index = "zendesk_tickets_large"
sop_index = "sop_data"
if __name__ == "__main__":
    # Embed data from CSV
    csv_file_path = 'files/snowflake_data.csv'
    embed_data(csv_file_path, batch_size=500, index=elasticsearch_index)

    # TODO: Add SOP data to another index
    # sop_csv_file_path = 'files/sop_data.csv'
    # embed_sop_data(sop_csv_file_path, index=sop_index)

    # Search example
    query = input("Enter your search query: ")
    results = search_tickets(query, size=200, index=elasticsearch_index)

    related_zendesk_tickets = []
    for hit in results:
        related_zendesk_tickets.append({
            "subject": hit['_source'].get('subject', 'No Subject'),
            "conversation": hit['_source']['conversation']
        })

    # Get AI assistance
    ai_response = generate_zendesk_assistance(query, results)

    # TODO: query against SOP index with ai response
    # sop_results = search_tickets(ai_response, size=200, index=sop_index)

    # Ask AI for final response
    # ai_response = generate_sop_assistance(ai_response[0].text, sop_results)

    # Display results
    print("AI Assistance Response:")
    print(ai_response)
