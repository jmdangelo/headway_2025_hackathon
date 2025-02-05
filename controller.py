from embed_documents import embed_data
from search_documents import search_tickets
from assist_with_issue import generate_assistance

if __name__ == "__main__":
    # Embed data from CSV
    # csv_file_path = 'files/snowflake_data.csv'
    # embed_data(csv_file_path)

    # Search example
    query = input("Enter your search query: ")
    results = search_tickets(query)

    # Get AI assistance
    ai_response = generate_assistance(query, results)

    # Display results
    print("AI Assistance Response:")
    print(ai_response)
