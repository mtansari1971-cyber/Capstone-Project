import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from resume_parser import extract_text_from_file
from gemini_engine import analyze_resume
from analysis_utils import (
    create_skill_dataframe,
    create_bullet_dataframe
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume Critic",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 600;
        margin-top: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🤖 AI Resume Critic")

    st.write(
        """
        AI-powered Resume & Job Match Analyzer.

        Upload your resume and provide a target
        job description to receive an AI-powered
        analysis.
        """
    )

    st.divider()

    st.subheader("✨ Features")

    st.write("📄 Resume PDF/DOCX analysis")
    st.write("🎯 ATS compatibility score")
    st.write("💼 Job match score")
    st.write("🔍 Missing keyword detection")
    st.write("🧠 Skill analysis")
    st.write("⚠️ Weakness detection")
    st.write("✍️ Bullet improvement")
    st.write("🚀 Improvement recommendations")
    st.write("📥 Downloadable report")

    st.divider()

    st.caption(
        "Powered by Python, Streamlit and Gemini"
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🤖 AI Resume Critic</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Analyze your resume against a target job description
    and discover how to improve your chances of getting shortlisted.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# INPUT SECTION
# ============================================================

st.header("📄 Resume & Job Description")


input_col1, input_col2 = st.columns(
    [1, 1],
    gap="large"
)


# ------------------------------------------------------------
# RESUME UPLOAD
# ------------------------------------------------------------

with input_col1:

    st.subheader("📄 Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"],
        help="Supported formats: PDF and DOCX"
    )

    if uploaded_file:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )


# ------------------------------------------------------------
# JOB DESCRIPTION
# ------------------------------------------------------------

with input_col2:

    st.subheader("💼 Target Job Description")

    job_description = st.text_area(
        "Paste the job description here",
        height=250,
        placeholder=(
            "Example:\n\n"
            "We are looking for a Machine Learning Engineer...\n"
            "Required skills: Python, SQL, Machine Learning..."
        )
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.divider()

analyze_button = st.button(
    "🚀 Analyze Resume",
    type="primary",
    use_container_width=True
)


# ============================================================
# INPUT VALIDATION + ANALYSIS
# ============================================================

if analyze_button:

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if uploaded_file is None:

        st.error(
            "❌ Please upload your resume first."
        )

        st.stop()


    if not job_description.strip():

        st.error(
            "❌ Please enter a job description."
        )

        st.stop()


    # --------------------------------------------------------
    # ANALYSIS
    # --------------------------------------------------------

    with st.spinner(
        "🤖 AI is analyzing your resume..."
    ):

        try:

            # Extract resume text
            resume_text = extract_text_from_file(
                uploaded_file
            )


            if not resume_text.strip():

                st.error(
                    "❌ Could not extract text from the resume."
                )

                st.stop()


            # Send resume + JD to Gemini
            analysis = analyze_resume(
                resume_text,
                job_description
            )


            # Save analysis in session state
            st.session_state["analysis"] = analysis


            st.success(
                "✅ Resume analysis completed successfully!"
            )


        except Exception as e:

            st.error(
                f"❌ An error occurred during analysis:\n\n{e}"
            )

            st.stop()


# ============================================================
# DISPLAY PREVIOUS ANALYSIS
# ============================================================

analysis = st.session_state.get(
    "analysis",
    None
)


if analysis is None:

    st.info(
        "👆 Upload a resume, enter a job description, "
        "and click **Analyze Resume** to begin."
    )

    st.stop()


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_score_label(score):

    if score >= 90:
        return "Excellent"

    elif score >= 80:
        return "Very Good"

    elif score >= 70:
        return "Good"

    elif score >= 60:
        return "Needs Improvement"

    else:
        return "Poor"


# ============================================================
# MAIN RESULTS
# ============================================================

st.divider()

st.header("📊 Resume Performance")


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🎯 ATS Score",
        f"{analysis.ats_score}/100"
    )

    st.caption(
        get_score_label(
            analysis.ats_score
        )
    )


with col2:

    st.metric(
        "💼 Job Match",
        f"{analysis.job_match_score}/100"
    )

    st.caption(
        get_score_label(
            analysis.job_match_score
        )
    )


with col3:

    st.metric(
        "🔍 Missing Keywords",
        len(analysis.missing_keywords)
    )


with col4:

    st.metric(
        "✍️ Weak Bullets",
        len(analysis.weak_bullets)
    )


# ============================================================
# RESUME HEALTH
# ============================================================

st.subheader("❤️ Resume Health")


st.write(
    f"ATS Compatibility — {analysis.ats_score}%"
)

st.progress(
    min(
        max(
            analysis.ats_score / 100,
            0
        ),
        1
    )
)


st.write(
    f"Job Compatibility — {analysis.job_match_score}%"
)

st.progress(
    min(
        max(
            analysis.job_match_score / 100,
            0
        ),
        1
    )
)


# ============================================================
# SCORE CHART
# ============================================================

st.header("📈 Score Breakdown")


score_df = pd.DataFrame(
    {
        "Metric": [
            "ATS Score",
            "Job Match"
        ],

        "Score": [
            analysis.ats_score,
            analysis.job_match_score
        ]
    }
)


fig = go.Figure()


fig.add_trace(
    go.Bar(
        x=score_df["Metric"],
        y=score_df["Score"],
        text=score_df["Score"],
        textposition="auto"
    )
)


fig.update_layout(

    title="Resume Performance",

    yaxis=dict(
        title="Score",
        range=[0, 100]
    ),

    xaxis=dict(
        title="Evaluation"
    ),

    height=450
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# RESUME OVERVIEW
# ============================================================

st.header("👤 Resume Overview")


overview_col1, overview_col2 = st.columns(2)


with overview_col1:

    st.subheader("Candidate")

    st.write(
        getattr(
            analysis,
            "candidate_name",
            "Not identified"
        )
    )


with overview_col2:

    st.subheader("Overall Assessment")

    st.write(
        getattr(
            analysis,
            "professional_summary",
            "No summary available."
        )
    )


# ============================================================
# STRENGTHS & WEAKNESSES
# ============================================================

st.header("🔎 Resume Analysis")


strength_col, weakness_col = st.columns(2)


with strength_col:

    st.subheader("✅ Strengths")

    strengths = getattr(
        analysis,
        "strengths",
        []
    )

    if strengths:

        for strength in strengths:

            st.success(
                f"✓ {strength}"
            )

    else:

        st.info(
            "No major strengths identified."
        )


with weakness_col:

    st.subheader("⚠️ Weaknesses")

    weaknesses = getattr(
        analysis,
        "weaknesses",
        []
    )

    if weaknesses:

        for weakness in weaknesses:

            st.warning(
                f"⚠ {weakness}"
            )

    else:

        st.success(
            "No major weaknesses identified."
        )


# ============================================================
# MISSING KEYWORDS
# ============================================================

st.header("🔍 Missing Keywords")


missing_keywords = getattr(
    analysis,
    "missing_keywords",
    []
)


if missing_keywords:

    keyword_columns = st.columns(3)


    for i, keyword in enumerate(
        missing_keywords
    ):

        with keyword_columns[
            i % 3
        ]:

            st.error(
                f"❌ {keyword}"
            )

else:

    st.success(
        "🎉 No major missing keywords detected!"
    )


# ============================================================
# SKILL ANALYSIS
# ============================================================

st.header("🧠 Skill Analysis")


st.write(
    """
    This table compares important skills identified
    from the target job with the skills found in the resume.
    """
)


try:

    skill_df = create_skill_dataframe(
        analysis.skill_analysis
    )

except Exception:

    skill_df = pd.DataFrame()


if not skill_df.empty:

    st.dataframe(
        skill_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No skill analysis was returned."
    )


# ============================================================
# WEAK BULLET ANALYSIS
# ============================================================

st.header("✍️ Resume Bullet Improvements")


st.write(
    """
    AI identifies weak resume bullet points and
    provides suggestions for making them clearer,
    stronger and more impactful.
    """
)


try:

    bullet_df = create_bullet_dataframe(
        analysis.weak_bullets
    )

except Exception:

    bullet_df = pd.DataFrame()


if not bullet_df.empty:

    st.dataframe(
        bullet_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "🎉 No weak bullet points were identified."
    )


# ============================================================
# IMPROVEMENT PLAN
# ============================================================

st.header("🚀 Personalized Improvement Plan")


improvement_plan = getattr(
    analysis,
    "improvement_plan",
    []
)


if improvement_plan:

    for i, recommendation in enumerate(
        improvement_plan,
        start=1
    ):

        st.write(
            f"### {i}. {recommendation}"
        )

else:

    st.info(
        "No improvement recommendations available."
    )


# ============================================================
# RESUME DETAILS
# ============================================================

st.header("📚 Resume Details")


# ------------------------------------------------------------
# EDUCATION
# ------------------------------------------------------------

with st.expander("🎓 Education"):

    education = getattr(
        analysis,
        "education",
        []
    )

    if education:

        for item in education:

            st.write(
                f"• {item}"
            )

    else:

        st.info(
            "No education information found."
        )


# ------------------------------------------------------------
# EXPERIENCE
# ------------------------------------------------------------

with st.expander("💼 Experience"):

    experience = getattr(
        analysis,
        "experience",
        []
    )

    if experience:

        for item in experience:

            st.write(
                f"• {item}"
            )

    else:

        st.info(
            "No experience information found."
        )


# ------------------------------------------------------------
# PROJECTS
# ------------------------------------------------------------

with st.expander("🛠️ Projects"):

    projects = getattr(
        analysis,
        "projects",
        []
    )

    if projects:

        for item in projects:

            st.write(
                f"• {item}"
            )

    else:

        st.info(
            "No projects found."
        )


# ------------------------------------------------------------
# CERTIFICATIONS
# ------------------------------------------------------------

with st.expander("🏆 Certifications"):

    certifications = getattr(
        analysis,
        "certifications",
        []
    )

    if certifications:

        for item in certifications:

            st.write(
                f"• {item}"
            )

    else:

        st.info(
            "No certifications found."
        )


# ============================================================
# DOWNLOAD REPORT
# ============================================================

st.header("📥 Download Report")


def list_to_text(items):

    if not items:

        return "None"

    return "\n".join(
        f"- {item}"
        for item in items
    )


report = f"""
==================================================
             AI RESUME CRITIC REPORT
==================================================

CANDIDATE
---------
{getattr(analysis, "candidate_name", "Not identified")}


ATS SCORE
---------
{analysis.ats_score}/100


JOB MATCH SCORE
---------------
{analysis.job_match_score}/100


PROFESSIONAL SUMMARY
--------------------
{getattr(analysis, "professional_summary", "Not available")}


STRENGTHS
---------
{list_to_text(analysis.strengths)}


WEAKNESSES
----------
{list_to_text(analysis.weaknesses)}


MISSING KEYWORDS
----------------
{list_to_text(analysis.missing_keywords)}


IMPROVEMENT PLAN
----------------
{list_to_text(analysis.improvement_plan)}


==================================================
Generated by AI Resume Critic
==================================================
"""


st.download_button(

    label="📥 Download Analysis Report",

    data=report,

    file_name="AI_Resume_Critic_Report.txt",

    mime="text/plain",

    use_container_width=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🤖 AI Resume Critic | Built with Python, Streamlit and Gemini"
)