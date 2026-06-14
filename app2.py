import streamlit as st
from pypdf import PdfReader
import pandas as pd
import plotly.express as px

from skills import skills
from interview_questions import interview_questions
from resume_analyser import analyze_resume
from ai_feedback import get_ai_feedback
from ats_score import calculate_ats_score
from job_role import recommend_roles
from pdf_report import create_report
from resume_category import predict_category

# Page Config
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Title
st.title("📄 AI Resume Analyzer")

st.write(
    "Analyze your resume instantly using AI and improve your chances of getting shortlisted."
)

col1, col2 = st.columns(2)

with col1:
    st.success("✅ Resume Score")
    st.success("✅ ATS Score")
    st.success("✅ Skill Detection")

with col2:
    st.success("✅ AI Feedback")
    st.success("✅ Job Recommendations")
    st.success("✅ PDF Report")

st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs([
    "📄 Analysis",
    "🎤 Interview Questions",
    "🤖 AI Feedback"
])

# Upload Resume
uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if st.button("🚀 Analyze Resume"):
    
    if not uploaded_file:
        st.warning("⬆️ Please upload a PDF resume to start analysis.")

    results = analyze_resume(uploaded_file)

    found_skills = results["found_skills"]
    education_found = results["education_found"]
    projects_found = results["projects_found"]
    github_found = results["github_found"]
    score = results["score"]
    pages = results["pages"]
    text = results["text"]
    ats_score = calculate_ats_score(
            found_skills
    )
    # TAB 1

    with tab1:
        
        if len(text.strip()) == 0:
            st.error("Could not extract text from resume.")
            st.stop()

        st.subheader("📋 Resume Checklist")

        checklist = [
            ("Education", education_found),
            ("Projects", projects_found),
            ("GitHub", github_found)
        ]

        for name, status in checklist:

            if status:
                st.success(f"✅ {name}")
            else:
                st.warning(f"❌ {name}")

        st.subheader("🛠 Detected Skills")

        if found_skills:

            for skill in found_skills:
                st.success(skill)

        else:
            st.warning("No Skills Found")

        st.subheader("📊 Resume Score")

        st.metric(
            "Overall Score",
            f"{score}/100"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Skills Found",
                len(found_skills)
            )

        with col2:
            st.metric(
                "Pages",
                pages
            )

        with col3:
            st.metric(
                "Score",
                score
            )

        # Pie Chart

        if found_skills:

            df = pd.DataFrame({
                "Skill": found_skills,
                "Count": [1] * len(found_skills)
            })

            fig = px.pie(
                df,
                names="Skill",
                values="Count",
                title="Detected Skills"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # Bar Chart

        sections = {
            "Education": 15 if education_found else 0,
            "Projects": 20 if projects_found else 0,
            "GitHub": 15 if github_found else 0,
            "Skills": len(found_skills) * 5
        }

        df_sections = pd.DataFrame({
            "Category": list(sections.keys()),
            "Points": list(sections.values())
        })

        fig = px.bar(
            df_sections,
            x="Category",
            y="Points",
            title="Resume Score Breakdown"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("🔋 Resume Strength")
        
        st.progress(score/100)

        st.metric(
            "Resume Score",
            f"{score}/100"
        )

        ats_score, missing_skills = calculate_ats_score(
            found_skills
        )
        
        st.subheader("🎯 ATS Score")

        st.metric(
            "ATS Score",
            f"{ats_score}%"
        )

        st.progress(
            ats_score / 100
        )
        
        st.subheader("❌ Missing Skills")

        if missing_skills:

            for skill in missing_skills:
                st.warning(skill)

        else:
            st.success("No Missing Skills")
            
        roles = recommend_roles(
            found_skills
        )
        st.subheader("💼 Recommended Job Roles")

        if roles:

            for role in roles:
                st.success(f"✅ {role}")

        else:
            st.warning(
                "No role recommendations available"
            )
            
        feedback = get_ai_feedback(text)
            
        pdf_file = create_report(
            score,
            ats_score,
            found_skills,
            missing_skills,
            roles,
            feedback
        )
        with open(pdf_file, "rb") as file:

            st.download_button(
                label="📥 Download Report",
                data=file,
                file_name="resume_report.pdf",
                mime="application/pdf"
            )
        category = predict_category(
            found_skills
        )

        st.subheader("🎯 Resume Category")
        st.success(category)
    # TAB 2

    with tab2:

        st.subheader("🎤 Interview Questions")

        for skill in found_skills:

            if skill in interview_questions:

                with st.expander(skill):

                    for question in interview_questions[skill]:

                        st.write(f"• {question}")

    # TAB 3

    with tab3:

        st.subheader("🤖 Gemini AI Feedback")

        try:

            with st.spinner("Analyzing Resume..."):

                feedback = get_ai_feedback(text)

            st.success("Analysis Complete")

            st.write(feedback)

        except Exception as e:

            st.error(f"Gemini Error: {e}")