from embed_documents import embed_data, embed_sop_data
from search_documents import search_tickets
from assist_with_issue import generate_zendesk_assistance, generate_sop_assistance
import sys

zendesk_index = "zendesk_tickets_large_clean"
sop_index = "sop_data"
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if 'index_zendesk' in sys.argv:
            # Embed Zendesk data from CSV
            print("Embedding Zendesk ticket data...")
            csv_file_path = 'files/snowflake_data.csv'
            embed_data(csv_file_path, batch_size=2000, index=zendesk_index)
        if 'index_sop' in sys.argv:
            # Embed SOP data from CSV
            print("Embedding SOP data...")
            sop_csv_file_path = 'files/sop_data.csv'
            embed_sop_data(sop_csv_file_path, index=sop_index)

    # Search example
    query = input("Enter your search query: ")
    results = search_tickets(query, size=150, index=zendesk_index)
    related_zendesk_tickets = []
    for hit in results:
        related_zendesk_tickets.append({
            "subject": hit['_source'].get('subject', 'No Subject'),
            "conversation": hit['_source']['conversation']
        })
    print(f"Related Zendesk Tickets: {related_zendesk_tickets}")

    # Get AI assistance
    ai_response = generate_zendesk_assistance(query, related_zendesk_tickets)

    print(f"First AI Assistance Response: {ai_response[0].text}")

    # TODO: query against SOP index with ai response
    sop_results = search_tickets(ai_response[0].text, size=45, index=sop_index)
    related_sop_titles = []
    for hit in sop_results:
        related_sop_titles.append({
            "title": hit['_source'].get('title', 'No Title')
        })

    print(f"Related SOP Articles: {related_sop_titles}")

    # Ask AI for final response
    final_ai_response = generate_sop_assistance(ai_response[0].text, related_sop_titles)

    # Display results
    print("final AI Assistance Response:")
    print(final_ai_response[0].text)
