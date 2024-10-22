import re
from collections import Counter


def clean_text(text):
    """Clean the text by removing non-alphabetic characters and converting to lowercase."""
    text = re.sub(r'\W+', ' ', text)
    return text.lower()

def sentence_tokenize(text):
    """Tokenize text into sentences using basic punctuation rules."""
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return [sentence.strip() for sentence in sentences if len(sentence) > 10]  # Ignore very short sentences

def word_tokenize(text):
    """Tokenize text into words."""
    words = re.findall(r'\b\w+\b', text)
    return words

def score_sentences(text):
    """Score sentences based on word frequency and other features."""
    sentences = sentence_tokenize(text)
    words = word_tokenize(text) 
    word_freq = Counter(words)

    sentence_scores = {}
    for sentence in sentences:
        sentence_word_count = word_tokenize(sentence)
        score = sum(word_freq[word] for word in sentence_word_count)
        sentence_scores[sentence] = score

    return sentence_scores