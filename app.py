# app.py

import streamlit as st
from resume_utils import extract_text_from_file, get_resume_sections
from keyword_matcher import extract_keywords, compare_keywords
from bullet_rewriter import rephrase_bullet_point
from io import StringIO
import base64

st.set_page_config(page_title="AI Resume Reviewer", layout="wide")
st.title("📄 AI-Powered Resume Reviewer")

st.markdown("Upload your **resume** and (optionally) paste the **job description** to:")
st.markdown("- ✅ Get missing keyword suggestions")
st.markdown("- ✨ Improve weak bullet points")
st.markdown("- 📊 Score your resume sections")
st.markdown("- 📥 Export your enhanced resume")

# Upload Resume File
resume_file = st.file_uploader("📎 Upload Your Resume", type=["pdf", "txt", "docx"])

# Paste Job Description Instead of Upload
job_description_text = st.text_area("🧾 Paste Job Description (Optional)", height=250)

resume_text = ""
enhanced_resume_lines = []

if resume_file:
    resume_text = extract_text_from_file(resume_file)

    # 🔍 Keyword Comparison
    if job_description_text.strip():
        st.subheader("🔍 Keyword Comparison")
        resume_keywords = extract_keywords(resume_text)
        jd_keywords = extract_keywords(job_description_text)
        missing_keywords = compare_keywords(resume_keywords, jd_keywords)

        if missing_keywords:
            st.error(f"⚠️ Missing Keywords ({len(missing_keywords)}):")
            st.write(", ".join(missing_keywords))
            st.markdown("💡 **Tip:** Include these keywords in your experience, projects, or skills section.")
        else:
            st.success("✅ Your resume includes all major keywords from the job description!")

    # ✨ Bullet Point Enhancer
    st.markdown("---")
    st.subheader("✨ Bullet Point Enhancer")

    bullets = [line.strip("•- ").strip() for line in resume_text.split('\n') if line.strip().startswith(("-", "•"))]

    if bullets:
        for i, bullet in enumerate(bullets):
            st.markdown(f"🔹 **Original #{i+1}:** {bullet}")
            new_bullet = rephrase_bullet_point(bullet)
            st.markdown(f"✅ **Improved #{i+1}:** {new_bullet}")
            st.markdown("---")
            enhanced_resume_lines.append(f"- {new_bullet}")
    else:
        st.info("No bullet points found. Make sure your resume has lines starting with '-' or '•'.")

    # 📊 Resume Section Scoring
    st.subheader("📊 Resume Section Scoring")

    sections = get_resume_sections(resume_text)
    scoring_criteria = {
        "Experience": 40,
        "Skills": 25,
        "Projects": 20,
        "Education": 15
    }

    total_score = 0
    for section, weight in scoring_criteria.items():
        if section.lower() in sections:
            st.success(f"✅ {section} section found (+{weight} points)")
            total_score += weight
        else:
            st.warning(f"❌ {section} section not found")

    st.markdown(f"### 🧮 **Final Resume Score: {total_score}/100**")

    # 📥 Download Enhanced Resume
    st.markdown("---")
    st.subheader("📥 Download Enhanced Resume")

    result_text = "\n".join(enhanced_resume_lines) if enhanced_resume_lines else resume_text

    buffer = StringIO()
    buffer.write(result_text)
    buffer.seek(0)

    b64 = base64.b64encode(buffer.read().encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="enhanced_resume.txt">📥 Download Enhanced Resume (.txt)</a>'
    st.markdown(href, unsafe_allow_html=True)

else:
    st.info("Upload your resume to begin.")
