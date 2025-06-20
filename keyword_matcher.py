# keyword_matcher.py
def match_keywords(resume_text, job_keywords):
    resume_words = set(resume_text.lower().split())
    missing = [kw for kw in job_keywords if kw not in resume_words]
    return missing