from flask import Flask, request, jsonify
import os
from src.pdf_parser import process_multiple_pdfs_for_summary_and_keywords
from src.mongodb_connection import MongoDBClient
import logging
app = Flask(__name__)

# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Flask server is running!"}), 200

@app.route('/process_pdfs', methods=['POST'])
def process_pdfs():
    logging.debug("Received request to process PDFs")
    folder_path = request.json.get('folder_path', './pdf')
    logging.debug(f"Folder path received: {folder_path}")

    if not os.path.exists(folder_path):
        return jsonify({"error": "Folder path does not exist"}), 400
    
    all_results = {}  # To collect results for all PDF
    
    try:
        all_pdf_results = process_multiple_pdfs_for_summary_and_keywords(folder_path, max_workers=4)
    
    # Store results in MongoDB
        mongo_client = MongoDBClient()
        for pdf_name, result in all_pdf_results.items():
            if "error" in result:
                logging.error(f"Error processing {pdf_name}: {result['error']}")
                continue
            pdf_id = mongo_client.store_metadata(pdf_name, folder_path)
            if pdf_id:  # Only update if insertion was successful
                mongo_client.update_with_summary_and_keywords(pdf_id, result['summary'], result['keywords'])
                all_results[pdf_name] = result  # Store successful results
            else:
                logging.error(f"Failed to store metadata for {pdf_name}")
                all_results[pdf_name] = {"error": "Failed to store metadata"}
            # mongo_client.update_with_summary_and_keywords(pdf_id, result['summary'], result['keywords'])
        return jsonify(all_pdf_results),200
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
