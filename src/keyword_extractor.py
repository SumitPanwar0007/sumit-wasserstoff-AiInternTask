
from sklearn.feature_extraction.text import TfidfVectorizer
import logging


def extract_keywords(text, num_keywords=5):
    """Extracts top keywords using TF-IDF"""
    try:
        # Initialize the TF-IDF vectorizer
        tfidf = TfidfVectorizer(max_features=num_keywords, stop_words='english')
        tfidf_matrix = tfidf.fit_transform([text])
        
        # Get feature names (the keywords) and their TF-IDF scores
        feature_names = tfidf.get_feature_names_out()
        
        return list(feature_names)
    
    except Exception as e:
        logging.error(f"Error extracting keywords: {str(e)}")
        return ["No Keywords Found"]