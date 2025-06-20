import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required resources once
nltk.download('punkt')
nltk.download('stopwords')

def extract_keywords(job_description):
    stop_words = set(stopwords.words("english"))
    text = job_description.lower()
    words = word_tokenize(text)
    keywords = [word for word in words if word.isalpha() and word not in stop_words]
    return list(set(keywords))  # return unique keywords
