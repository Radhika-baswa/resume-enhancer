import streamlit as st
from resume_parser import extract_text_from_pdf, extract_text_from_docx
from job_parser import extract_keywords
from keyword_matcher import match_keywords
from suggestions import suggest_action_verbs, generate_impactful_bullet_points

st.set_page_config(page_title="AI Resume Enhancer", layout="centered")

st.title("📄 AI Resume Enhancer")

# Upload resume
resume_file = st.file_uploader("Upload your Resume (PDF/DOCX)", type=['pdf', 'docx'])

# Paste job description directly
job_text_input = st.text_area("📋 Paste Job Description Here:", height=200)

# Analyze button
if st.button("🔍 Analyze Resume"):

    if resume_file and job_text_input.strip():
        # Extract resume text
        if resume_file.name.endswith('.pdf'):
            resume_text = extract_text_from_pdf(resume_file)
        else:
            resume_text = extract_text_from_docx(resume_file)

        # Use pasted job description
        job_text = job_text_input

        # Show previews
        st.subheader("📝 Resume Preview")
        st.text(resume_text[:500] + "...")

        st.subheader("📋 Job Description Preview")
        st.text(job_text[:300] + "...")

        # Process & Analyze
        job_keywords = extract_keywords(job_text)
        missing_keywords = match_keywords(resume_text, job_keywords)
        verb_suggestions = suggest_action_verbs(resume_text)
        resume_lines = [line.strip() for line in resume_text.split('\n') if line.strip()]
        impactful_bullets = generate_impactful_bullet_points(resume_lines)

        # Display Results
        st.subheader("🚨 Missing Keywords")
        st.write(missing_keywords)

        st.subheader("⚡ Suggested Action Verbs")
        st.write(verb_suggestions)

        st.subheader("💡 Improved Bullet Points")
        for bullet in impactful_bullets:
            st.write("•", bullet)

    else:
        st.warning("⚠️ Please upload a resume and paste a job description.")
