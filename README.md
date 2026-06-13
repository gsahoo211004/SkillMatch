# SkillMatch

**SkillMatch** is an AI-powered resume and job fit evaluator built with Streamlit.
Upload a resume PDF and enter a job role or job description to compare extracted skills, compute match scores, and receive career feedback.

## Features

- Upload a PDF resume and extract text from the file.
- Enter a quick job role or paste a full job description.
- Expand short job roles into detailed requirements using Google Gemini.
- Extract skills from resumes and job descriptions using spaCy.
- Compute semantic matching between resume skills and job requirements with SentenceTransformers.
- Generate AI-driven career coach feedback for fit, strengths, gaps, and tailoring tips.

## Built With

- Python 3.12
- Streamlit for the web UI
- spaCy for NLP skill extraction
- sentence-transformers for semantic similarity
- Google Gemini via `google-genai` for LLM expansion and feedback
- PyMuPDF for PDF resume text extraction

## Prerequisites

- Python 3.12 installed
- A terminal or PowerShell session
- `GEMINI_API_KEY` environment variable set for Google Gemini access

## Installation

1. Clone or copy the repository.
2. Install dependencies:

```powershell
cd SkillMatch
pip install --no-cache-dir -r requirements.txt
```

3. If needed, create a `.env` file with your Gemini key:

```text
GEMINI_API_KEY=your_api_key_here
```

## Running Locally

Start the Streamlit app:

```powershell
streamlit run app.py
```

Then open the URL printed in the terminal, typically `http://localhost:8501`.

## Docker

Build the image:

```powershell
docker build -t skillmatch .
```

Run the container:

```powershell
docker run -p 8501:8501 --env GEMINI_API_KEY="your_api_key_here" skillmatch
```

Open `http://localhost:8501` in your browser.

## Usage

1. Upload a resume PDF.
2. Select either `Job Role (quick)` or `Full Job Description (detailed)`.
3. Enter a job title or paste the full job description.
4. Click `Analyse Match`.
5. Review the semantic score, skill breakdown, and AI feedback.

## Project Structure

- `app.py` — Streamlit app entrypoint and UI flow.
- `src/nlp/pdf_reader.py` — PDF text extraction.
- `src/nlp/extractor.py` — Skill extraction using keyword matching and spaCy.
- `src/matching/matcher.py` — Semantic matching and skill gap analysis.
- `src/llm/feedback.py` — Job role expansion and feedback generation via Google Gemini.
- `requirements.txt` — Python dependencies.
- `Dockerfile` — Container image instructions.

## Notes

- The app currently uses a simple keyword-based skill dictionary plus spaCy noun phrase extraction.
- If a Gemini API request fails, the app falls back to a default skill prompt.
- There are no automated tests included in this repository yet.

## Contributing

Feel free to add tests, improve skill matching, or extend the role expansion and feedback prompts.
