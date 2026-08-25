import os

from google import genai
from google.genai import types

from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()


# ==================================================
# PYDANTIC SCHEMAS
# ==================================================

class SkillAnalysis(BaseModel):
    skill: str
    status: str
    importance: str


class WeakBullet(BaseModel):
    original: str
    problem: str
    improved: str


class ResumeAnalysis(BaseModel):

    candidate_name: str

    professional_summary: str

    technical_skills: list[str]

    soft_skills: list[str]

    education: list[str]

    projects: list[str]

    experience: list[str]

    certifications: list[str]

    strengths: list[str]

    weaknesses: list[str]

    missing_keywords: list[str]

    skill_analysis: list[SkillAnalysis]

    weak_bullets: list[WeakBullet]

    ats_score: int

    job_match_score: int

    improvement_plan: list[str]


# ==================================================
# GEMINI CLIENT
# ==================================================

def get_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found. "
            "Please configure it in your .env file."
        )

    return genai.Client(api_key=api_key)


# ==================================================
# RESUME ANALYSIS
# ==================================================

def analyze_resume(resume_text, job_description):

    client = get_client()

    prompt = f"""
You are an expert ATS recruiter, technical recruiter,
and resume optimization specialist.

Analyze the candidate's resume against the target
job description.

IMPORTANT RULES:

1. Do not invent experience.
2. Do not invent skills.
3. Do not invent education.
4. Do not invent certifications.
5. Only use information present in the resume.
6. Identify important missing keywords.
7. Evaluate ATS compatibility.
8. Evaluate job compatibility.
9. Identify weak resume bullet points.
10. Suggest improvements without creating fake achievements.

========================
RESUME
========================

{resume_text}

========================
TARGET JOB DESCRIPTION
========================

{job_description}

========================
REQUIRED ANALYSIS
========================

Analyze:

- candidate name
- professional summary
- technical skills
- soft skills
- education
- projects
- experience
- certifications
- strengths
- weaknesses
- missing keywords
- skill-by-skill comparison
- weak bullet points
- ATS score from 0-100
- job match score from 0-100
- improvement plan

ATS SCORE:

90-100 = Excellent
80-89 = Very Good
70-79 = Good
60-69 = Needs Improvement
Below 60 = Poor

Return structured JSON matching the provided schema.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ResumeAnalysis,
        ),
    )

    return ResumeAnalysis.model_validate_json(
        response.text
    )