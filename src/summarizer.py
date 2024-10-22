import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from .text_cleaning import score_sentences


def summarize_text(text, num_sentences=5):
    """Summarize text by extracting the highest-scoring sentences, with a word limit."""
    # Tokenize the input text to determine its word count
    total_word_count = len(word_tokenize(text))
    
    # Set word limit based on the length of the input text
    if total_word_count > 4000:
        max_words = 100
    elif 2000 <= total_word_count <= 4000:
        max_words = 80
    else:
        max_words = 50

    # Score sentences based on their importance
    sentence_scores = score_sentences(text)
    sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)

    
    # Add sentences while keeping total word count under max_words
    summary_sentences = []
    word_count = 0
    for sentence in sorted_sentences:
        sentence_word_count = len(word_tokenize(sentence))

        # If a sentence is longer than the remaining word count, truncate it
        if sentence_word_count > max_words - word_count:
            remaining_words = max_words - word_count
            truncated_sentence = ' '.join(word_tokenize(sentence)[:remaining_words])
            summary_sentences.append(truncated_sentence)
            break
        else:
            summary_sentences.append(sentence)
            word_count += sentence_word_count
            

        # Stop adding sentences if the word limit is reached
        if word_count >= max_words:
            break
    
    return ' '.join(summary_sentences)