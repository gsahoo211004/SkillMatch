import spacy

nlp = spacy.load("en_core_web_sm")

# Common tech skills dictionary for matching
KNOWN_SKILLS = [
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c", "r", "sql",
    "scala", "go", "rust", "kotlin", "swift",
    # ML / AI
    "machine learning", "deep learning", "nlp", "computer vision",
    "neural networks", "transformers", "bert", "gpt", "llm", "genai",
    "reinforcement learning", "time series", "forecasting",
    # Frameworks
    "pytorch", "tensorflow", "keras", "scikit-learn", "xgboost",
    "hugging face", "langchain", "spacy", "nltk",
    # Data Engineering
    "spark", "hadoop", "airflow", "kafka", "etl", "data pipeline",
    "bigquery", "snowflake", "dbt", "databricks",
    # MLOps
    "mlflow", "docker", "kubernetes", "ci/cd", "github actions",
    "evidently", "wandb", "aws", "gcp", "azure",
    # Databases
    "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
    # Backend
    "flask", "django", "fastapi", "rest api", "graphql", "nodejs",
    # Data Science
    "pandas", "numpy", "matplotlib", "streamlit", "power bi", "tableau",
    "statistics", "a/b testing", "hypothesis testing",
    # Soft skills
    "communication", "teamwork", "leadership", "problem solving",
]


def extract_skills(text: str) -> list[str]:
    """
    Extract skills from text using keyword matching + spaCy NLP.
    Returns a list of found skills.
    """
    text_lower = text.lower()
    found_skills = []

    for skill in KNOWN_SKILLS:
        if skill in text_lower:
            found_skills.append(skill)

    # Also extract noun phrases using spaCy for unlisted skills
    doc = nlp(text_lower)
    noun_phrases = [chunk.text.strip() for chunk in doc.noun_chunks
                    if len(chunk.text.strip()) > 2]

    return {
        "matched_skills": found_skills,
        "noun_phrases": list(set(noun_phrases))
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
    Worked on forecasting and time series projects.
    """

    print("JD Skills:")
    jd_skills = extract_skills(sample_jd)
    print(f"  Matched: {jd_skills['matched_skills']}")

    print("\nResume Skills:")
    resume_skills = extract_skills(sample_resume)
    print(f"  Matched: {resume_skills['matched_skills']}")