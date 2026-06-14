import streamlit as st
from pypdf import PdfReader
import re
import plotly.express as px
import pandas as pd
import google.generativeai as genai
genai.configure(api_key="YOURKEY")
model = genai.GenerativeModel("gemini-2.5-flash")
    

# Page Configuration    
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Sidebar
tab1, tab2, tab3 = st.tabs([
    "📄 Analysis",
    "🎤 Interview Questions",
    "🤖 AI Feedback"
])

# Title
st.title("AI Resume Analyzer")
st.write("Welcome to AI Resume Analyzer & Interview Assistant")

# Upload Resume
uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

# Skills Database
skills = [
    "Python",
    "Java",
    "C",
    "C++",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Node.js",
    "Machine Learning",
    "Data Science",
    "Linux"
]  

#interview Questions
interview_questions = {

    "Python": [
        "What is the difference between a list and a tuple?",
        "What is OOP in Python?",
        "What are Python decorators?"
    ],

    "JavaScript": [
        "What is the difference between var, let, and const?",
        "What is a closure?",
        "What is the DOM?"
    ],

    "SQL": [
        "What is a primary key?",
        "What is a foreign key?",
        "Difference between WHERE and HAVING?"
    ],

    "HTML": [
        "What is semantic HTML?",
        "Difference between div and span?"
    ],

    "CSS": [
        "What is Flexbox?",
        "Difference between relative and absolute positioning?"
    ],

    "Git": [
        "What is Git?",
        "Difference between git pull and git fetch?"
    ],

    "Linux": [
        "What is Linux?",
        "What is the purpose of chmod?"
    ]
}

with tab1:
    if uploaded_file:    
        #strengths
    strengths = []
    #improvement
    improvements = []
    #score for resume
    score = 0
    st.success("Resume Uploaded Successfully!")
    st.info(f"📄 File Name: {uploaded_file.name}")
    
    if st.button("Analyze Resume"):

        # Read PDF
        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted
                
        with tab3:
            prompt = f"""
        You are an expert resume reviewer.
        Analyze the following resume.
        Give:
        1. Resume strengths
        2. Resume weaknesses
        3. Skills improvement suggestions
        4. Overall rating out of 10
        Keep the entire response under 100 words.
        Resume:
        {text}
        """
            with st.spinner("Analyzing Resume with Gemini AI..."):
                response = model.generate_content(prompt)

            st.subheader("🤖 Gemini AI Feedback")
            st.success("Analysis Complete!")
            st.write(response.text)


        # Convert to lowercase
        text_lower = text.lower()

        # Remove ALL whitespace
        cleaned_text = re.sub(r"\s+", "", text_lower)
        
        education_found = "education" in cleaned_text
        projects_found = "project" in cleaned_text or "projects" in cleaned_text
        email_found = "@" in text
        
        
        # Debug
        st.subheader("Debug Information")
        st.write("Characters Extracted:", len(text))
        st.write("Pages:", len(reader.pages))

        # Skill Detection
        found_skills = []

        for skill in skills:
            skill_clean = skill.lower().replace(" ", "")
            if skill_clean in cleaned_text:
                found_skills.append(skill)

        # Display Skills
        st.subheader("Detected Skills")

        if found_skills:
            for skill in found_skills:
                st.success(f"✅ {skill}")
            st.write("Total Skills Found:", len(found_skills))
        else:
            st.warning("No Skills Found")
            
            
        # Resume Sections
        st.subheader("Resume Sections")

        if "education" in cleaned_text:
            st.success("✅ Education Section Found")
            score += 15
        else:
            st.warning("❌ Education Section Missing")

        if "project" in cleaned_text or "projects" in cleaned_text:
            st.success("✅ Projects Section Found")
            score += 20
        else:
            st.warning("❌ Projects Section Missing")

        if "@" in text:
            st.success("✅ Email Found")
        else:
            st.warning("❌ Email Missing")
        if "github" in cleaned_text:
            score += 15
        
        skill_count = len(found_skills)
        
        if skill_count >= 8:
            score += 40
        elif skill_count >= 5:
            score += 30
        elif skill_count >= 3:
            score += 20
        elif skill_count >= 1:
            score += 10
            
        #display score
        st.subheader("Resume Score")
        
        st.metric(
            label="Overall Score",
            value=f"{score}/100"
        )
        
        st.subheader("Suggestions")
        
        if len(found_skills) < 5:
            st.warning("Add more technical skills")
        if "project" not in cleaned_text:
            st.warning("Add projects section")
        if "github" not in cleaned_text:
            st.warning("Add GitHub profile")
        if "linkedin" not in cleaned_text:
            st.warning("Add LinkedIn profile")
            
        with tab2:
            st.subheader("Interview Questions")
            for skill in found_skills:
                    if skill in interview_questions:
                        with st.expander(f"{skill} Questions"):
                            for question in interview_questions[skill]:
                                st.write(f"• {question}")
                            
        st.subheader("🤖 AI Resume Feedback")
        
        if len(found_skills) >= 5:
                strengths.append("Strong technical skill set")
        if "project" in cleaned_text:
                strengths.append("Projects section is present")
        if "github" in cleaned_text:
                strengths.append("GitHub profile included")
        if "linkedin" in cleaned_text:
                strengths.append("LinkedIn profile included")
                
        st.write("### Strengths")

        for strength in strengths:
            st.success(strength)
        if len(found_skills) < 5:
            improvements.append("Add more technical skills")
        if "certificate" not in cleaned_text and "certification" not in cleaned_text:
            improvements.append("Add certifications")
        if "achievement" not in cleaned_text:
            improvements.append("Add achievements section")
        if "internship" not in cleaned_text:
            improvements.append("Add internships or practical experience")
            
        st.write("### Areas for Improvement")

        for improvement in improvements:
            st.warning(improvement)

        st.write("### Overall Assessment")
        
        if score >= 80:
                st.success("Excellent resume for a student profile.")
        elif score >= 60:
                st.info("Good resume with room for improvement.")
        else:
                st.warning("Resume needs significant improvement.")
                
        co11,co12,co13 = st.columns(3)
        
        with co11:
            st.metric("Resume Score", score)
        with co12:
            st.metric("Skills Found", len(found_skills))
        with co13:
            st.metric("Pages", len(reader.pages))
        
        df = pd.DataFrame({
            "Skills": found_skills,
            "Value": [1]*len(found_skills)
        })
        
        fig = px.pie(
            df,
            names= "Skills",
            values="Value",
            title="Detected Skills"
        )
        
        st.plotly_chart(fig)
        
        sections = {
            "Skills": len(found_skills) * 5,
            "Education": 15 if education_found else 0,
            "Projects": 20 if projects_found else 0,
            "GitHub": 15 if "github" in cleaned_text else 0
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

        st.plotly_chart(fig)
        
        st.subheader("Resume Strength")

        st.progress(score / 100)
        
        st.write(df.columns)
        
        st.info(
            f"""
Resume Score: {score}/100

Skills Found: {len(found_skills)}

Projects: {'Yes' if projects_found else 'No'}

Education: {'Yes' if education_found else 'No'}
"""
)
        