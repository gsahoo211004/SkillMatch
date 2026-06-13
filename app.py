import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(__file__))

from src.nlp.pdf_reader import extract_text_from_bytes
from src.nlp.extractor import extract_skills
from src.matching.matcher import compute_match_score, get_skill_gaps
from src.llm.feedback import generate_feedback, expand_job_role

st.set_page_config(
    page_title="SkillMatch",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 SkillMatch — AI Resume vs Job Fit Evaluator")
st.markdown("Upload your resume and enter a job role or description to get an AI-powered match analysis.")

st.divider()

# Input section
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload Your Resume")
    uploaded_pdf = st.file_uploader(
        "Upload your resume as a PDF:",
        type=["pdf"]
    )
    if uploaded_pdf:
        st.success(f"Uploaded: {uploaded_pdf.name}")

with col2:
    st.subheader("💼 Job Details")
    input_type = st.radio(
        "Input type:",
        ["Job Role (quick)", "Full Job Description (detailed)"],
        horizontal=True
    )

    if input_type == "Job Role (quick)":
        job_input = st.text_input(
            "Enter job role:",
            placeholder="e.g. Applied AI Intern, Data Scientist, ML Engineer"
        )
        job_description = ""
    else:
        job_description = st.text_area(
            "Paste the full job description:",
            height=250,
            placeholder="Copy and paste the full job description from LinkedIn, Naukri, etc."
        )
        job_input = "Custom JD"

# Analyse button
st.divider()
if st.button("🔍 Analyse Match", type="primary"):
    if not uploaded_pdf:
        st.error("Please upload your resume PDF.")
    elif input_type == "Job Role (quick)" and not job_input:
        st.error("Please enter a job role.")
    elif input_type == "Full Job Description (detailed)" and not job_description:
        st.error("Please paste a job description.")
    else:
        # Stage 1: Extract resume text from PDF
        with st.spinner("Stage 1/4 — Reading your resume PDF..."):
            pdf_bytes = uploaded_pdf.read()
            resume_text = extract_text_from_bytes(pdf_bytes)

        if resume_text.startswith("Error"):
            st.error(resume_text)
        else:
            with st.expander("View extracted resume text"):
                st.text(resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text)

            # Stage 2: Expand job role if needed + extract skills
            with st.spinner("Stage 2/4 — Extracting skills..."):
                if input_type == "Job Role (quick)" and job_input:
                    with st.spinner(f"Expanding '{job_input}' into skill requirements using AI..."):
                        job_description = expand_job_role(job_input)
                    with st.expander("View expanded job description"):
                        st.write(job_description)

                jd_skills = extract_skills(job_description)["matched_skills"]
                resume_skills = extract_skills(resume_text)["matched_skills"]

            # Stage 3: Compute match
            with st.spinner("Stage 3/4 — Computing semantic match score..."):
                semantic_score = compute_match_score(jd_skills, resume_skills)
                gaps = get_skill_gaps(jd_skills, resume_skills)

            # Stage 4: LLM feedback
            with st.spinner("Stage 4/4 — Generating AI career coach feedback..."):
                result = generate_feedback(
                    job_description, resume_text, semantic_score, gaps
                )

            st.success("Analysis complete!")
            st.divider()

            # Match score
            st.subheader("📊 Match Score")
            c1, c2, c3 = st.columns(3)
            c1.metric("Semantic Match", f"{semantic_score}%")
            c2.metric("Keyword Match", f"{gaps['match_percentage']}%")
            c3.metric("Skills Matched", f"{len(gaps['matched'])}/{len(gaps['matched']) + len(gaps['missing'])}")
            st.progress(int(min(semantic_score, 100)))

            st.divider()

            # Skill breakdown
            st.subheader("🔍 Skill Breakdown")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("✅ **Matched Skills**")
                if gaps["matched"]:
                    for skill in gaps["matched"]:
                        st.markdown(f"- {skill}")
                else:
                    st.markdown("_None found_")

            with col2:
                st.markdown("❌ **Missing Skills**")
                if gaps["missing"]:
                    for skill in gaps["missing"]:
                        st.markdown(f"- {skill}")
                else:
                    st.markdown("_None missing — great fit!_")

            with col3:
                st.markdown("➕ **Extra Skills**")
                if gaps["extra"]:
                    for skill in gaps["extra"]:
                        st.markdown(f"- {skill}")
                else:
                    st.markdown("_None_")

            st.divider()

            # LLM Feedback
            st.subheader("🤖 AI Career Coach Feedback")
            st.markdown(result["feedback"])