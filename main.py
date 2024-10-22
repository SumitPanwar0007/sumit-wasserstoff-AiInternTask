import nltk
from src.pdf_parser import process_multiple_pdfs_for_summary_and_keywords
from src.mongodb_connection import MongoDBClient

# Download necessary NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def main():
    # Create MongoDB client
    mongo_client = MongoDBClient()
    # Example workflow
    folder_path = r'D:\AI_ML\RAG\pdf'
    
    # Process all PDFs in the folder for summarization and keyword extraction
    all_pdf_results = process_multiple_pdfs_for_summary_and_keywords(folder_path)

    # Print results for each PDF
    print(f"Processing results for {len(all_pdf_results)} PDFs.")  # Debug statement
    for pdf_name, result in all_pdf_results.items():
        print(f"Processing: {pdf_name}")  # Debug statement
        if "error" in result:
            print(f"Error processing {pdf_name}: {result['error']}")
        else:
            print(f"Summary for {pdf_name}:\n{result['summary']}\n")
            print(f"Keywords for {pdf_name}: {', '.join(result['keywords'])}\n")
            print("="*80 + "\n")

            # Save summary to MongoDB
            pdf_id = mongo_client.store_metadata(pdf_name, folder_path)
            if pdf_id:  # Only update if insertion was successful
                mongo_client.update_with_summary_and_keywords(pdf_id, result['summary'], result['keywords'])
            else:
                print(f"Failed to store metadata for {pdf_name}")
            

if __name__ == "__main__":
    main()
