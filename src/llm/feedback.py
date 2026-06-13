import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def expand_job_role(job_role: str) -> str:
    """
    Use Gemini to expand a job role title into a detailed skill requirements description.
    """
    prompt = f"""
You are a technical recruiter. Generate a detailed job requirements description for the role: "{job_role}"

List the specific technical skills, tools, programming languages, frameworks, and soft skills
typically required for this role. Be specific and realistic.

Format as a plain paragraph of requirements, not bullet points.
Keep it under 150 words.
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Python machine learning deep learning nlp sql docker rest api statistics communication"

def generate_feedback(
    jd_text: str,
    resume_text: str,
    match_score: float,
    gaps: dict
) -> dict:
    """
    Generate personalised resume feedback using Gemini.
    Returns structured feedback with summary, strengths, gaps, and suggestions.
    """

    matched_str = ", ".join(gaps["matched"]) or "None"
    missing_str = ", ".join(gaps["missing"]) or "None"
    extra_str = ", ".join(gaps["extra"]) or "None"

    prompt = f"""
You are an expert career coach and resume consultant.

A candidate has submitted their resume for a job. An AI matching system has
analyzed the fit between the job description and the resume.

JOB DESCRIPTION:
{jd_text}

RESUME:
{resume_text}

MATCHING RESULTS:
- Semantic Match Score: {match_score}%
- Keyword Match: {gaps['match_percentage']}%
- Matched Skills: {matched_str}
- Missing Skills (in JD but not resume): {missing_str}
- Extra Skills (in resume but not JD): {extra_str}

Provide a structured evaluation with exactly these 4 sections:

1. OVERALL ASSESSMENT (2 sentences): Overall fit for this role.
2. STRENGTHS (2-3 bullet points): What the candidate does well for this role.
3. GAPS (2-3 bullet points): Key missing skills or experience the candidate should address.
4. TAILORING TIPS (2-3 bullet points): Specific actionable advice to improve this resume for this job.

Be direct, specific, and constructive. Use professional language.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return {
            "feedback": response.text.strip(),
            "status": "success"
        }
    except Exception as e:
        return {
            "feedback": f"Feedback unavailable: {str(e)}",
            "status": "error"
        }


if __name__ == "__main__":
    sample_jd = """
    We are looking for a Machine Learning Engineer with strong Python skills.
    Experience with PyTorch, MLflow, Docker, and REST APIs required.
    Knowledge of NLP and LLM integration is a plus.
    Must have experience with PostgreSQL and data pipelines.
    """

    sample_resume = """
    Experienced Data Scientist with Python, Scikit-learn, and XGBoost.
    Built NLP pipelines using spaCy. Familiar with Flask, PostgreSQL, and Docker.
    Worked on forecasting and time series projects. Strong communication skills.
    """

    sample_gaps = {
        "matched": ["python", "docker", "nlp", "postgresql"],
        "missing": ["pytorch", "mlflow", "rest api", "machine learning", "llm"],
        "extra": ["flask", "scikit-learn", "spacy", "forecasting", "xgboost"],
        "match_percentage": 44.4
    }

    print("Generating LLM feedback...\n")
    result = generate_feedback(sample_jd, sample_resume, 68.17, sample_gaps)
    print("FEEDBACK:")
    print("-" * 60)
    print(result["feedback"])