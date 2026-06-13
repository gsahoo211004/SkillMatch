from sentence_transformers import SentenceTransformer, util
import torch

# Load SBERT model — this runs locally, no API needed
model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_match_score(jd_skills: list[str], resume_skills: list[str]) -> float:
    """
    Compute semantic similarity between JD skills and resume skills.
    Returns a score from 0 to 100.
    """
    if not jd_skills or not resume_skills:
        return 0.0

    # Convert skill lists to single strings for embedding
    jd_text = " ".join(jd_skills)
    resume_text = " ".join(resume_skills)

    # Generate embeddings
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)

    # Compute cosine similarity
    similarity = util.cos_sim(jd_embedding, resume_embedding)
    score = float(similarity[0][0]) * 100

    return round(score, 2)


def get_skill_gaps(jd_skills: list[str], resume_skills: list[str]) -> dict:
    """
    Compare JD skills vs resume skills.
    Returns matched, missing, and extra skills.
    """
    jd_set = set(jd_skills)
    resume_set = set(resume_skills)

    matched = sorted(jd_set & resume_set)
    missing = sorted(jd_set - resume_set)
    extra = sorted(resume_set - jd_set)

    return {
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "match_percentage": round(len(matched) / len(jd_set) * 100, 1) if jd_set else 0
    }


if __name__ == "__main__":
    jd_skills = ["python", "docker", "mlflow", "nlp", "llm", "pytorch",
                 "postgresql", "rest api", "machine learning"]
    resume_skills = ["python", "docker", "spacy", "nlp", "scikit-learn",
                     "postgresql", "flask", "forecasting", "xgboost"]

    print("Computing match score...")
    score = compute_match_score(jd_skills, resume_skills)
    print(f"Semantic Match Score: {score}%")

    print("\nSkill Gap Analysis:")
    gaps = get_skill_gaps(jd_skills, resume_skills)
    print(f"  Matched  ({len(gaps['matched'])}): {gaps['matched']}")
    print(f"  Missing  ({len(gaps['missing'])}): {gaps['missing']}")
    print(f"  Extra    ({len(gaps['extra'])}): {gaps['extra']}")
    print(f"  Keyword Match: {gaps['match_percentage']}%")