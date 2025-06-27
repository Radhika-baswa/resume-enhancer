# keyword_matcher.py

import re

def extract_keywords(text):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    stopwords = set([
        "with", "from", "your", "this", "that", "have", "been",
        "more", "than", "will", "they", "their", "using", "also"
    ])
    return set([word for word in words if word not in stopwords])

def compare_keywords(resume_keywords, jd_keywords):
    return list(jd_keywords - resume_keywords)
