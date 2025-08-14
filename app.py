import streamlit as st
from datetime import date
from configuration.config_manager import LLMFactory
from pydantic import ValidationError
from Templete import ResumeData, SYSTEM_PROMPT_TEMPLATE

# Load model
model = LLMFactory.get_llm()

st.set_page_config(page_title="AI Resume Builder", layout="wide")
st.title("AI Resume Builder")

# ------------------- Initialize Dynamic Sections -------------------
if "projects" not in st.session_state:
    st.session_state.projects = [{
        "title": "",
        "start_date": date.today(),
        "end_date": date.today(),
        "present": False,
        "description": ""
    }]

if "experiences" not in st.session_state:
    st.session_state.experiences = [{
        "title": "",
        "start_date": date.today(),
        "end_date": date.today(),
        "present": False,
        "description": ""
    }]

# ------------------- Form -------------------
with st.form("resume_form"):
    st.subheader("Personal Information")
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    designation = st.text_input("Designation")
    linkedin = st.text_input("LinkedIn URL")
    github = st.text_input("GitHub URL")
    other_links = st.text_area("Other Links (comma separated)")

    st.subheader("Education")
    degree = st.text_input("Degree")
    institution = st.text_input("Institution")
    edu_start_date = st.date_input("Start Date", date.today(), key="edu_start")
    edu_end_date = st.date_input("End Date", date.today(), key="edu_end")
    edu_present = st.checkbox("Present / Ongoing", key="edu_present")
    cgpa = st.text_input("CGPA")

    st.subheader("Skills")
    all_skills = st.text_area("All Skills (comma separated)")

    # ------------------- Projects -------------------
    st.subheader("Projects")
    for i, project in enumerate(st.session_state.projects):
        st.session_state.projects[i]["title"] = st.text_input(f"Project {i+1} Title", value=project["title"], key=f"proj_title_{i}")
        st.session_state.projects[i]["start_date"] = st.date_input(f"Start Date for Project {i+1}", value=project["start_date"], key=f"proj_start_{i}")
        st.session_state.projects[i]["end_date"] = st.date_input(f"End Date for Project {i+1}", value=project["end_date"], key=f"proj_end_{i}")
        st.session_state.projects[i]["present"] = st.checkbox(f"Present / Ongoing for Project {i+1}", value=project["present"], key=f"proj_present_{i}")
        st.session_state.projects[i]["description"] = st.text_area(f"Description for Project {i+1}", value=project["description"], key=f"proj_desc_{i}")

    proj_col1, proj_col2 = st.columns(2)
    with proj_col1:
        if st.form_submit_button("➕ Add Project"):
            st.session_state.projects.append({"title": "", "start_date": date.today(), "end_date": date.today(), "present": False, "description": ""})
            st.rerun()
    with proj_col2:
        if len(st.session_state.projects) > 1 and st.form_submit_button("❌ Remove Last Project"):
            st.session_state.projects.pop()
            st.rerun()

    # ------------------- Experience -------------------
    st.subheader("Experience / Internships")
    for i, exp in enumerate(st.session_state.experiences):
        st.session_state.experiences[i]["title"] = st.text_input(f"Experience {i+1} Title", value=exp["title"], key=f"exp_title_{i}")
        st.session_state.experiences[i]["start_date"] = st.date_input(f"Start Date for Experience {i+1}", value=exp["start_date"], key=f"exp_start_{i}")
        st.session_state.experiences[i]["end_date"] = st.date_input(f"End Date for Experience {i+1}", value=exp["end_date"], key=f"exp_end_{i}")
        st.session_state.experiences[i]["present"] = st.checkbox(f"Present / Ongoing for Experience {i+1}", value=exp["present"], key=f"exp_present_{i}")
        st.session_state.experiences[i]["description"] = st.text_area(f"Description for Experience {i+1}", value=exp["description"], key=f"exp_desc_{i}")

    exp_col1, exp_col2 = st.columns(2)
    with exp_col1:
        if st.form_submit_button("➕ Add Experience"):
            st.session_state.experiences.append({"title": "", "start_date": date.today(), "end_date": date.today(), "present": False, "description": ""})
            st.rerun()
    with exp_col2:
        if len(st.session_state.experiences) > 1 and st.form_submit_button("❌ Remove Last Experience"):
            st.session_state.experiences.pop()
            st.rerun()

    st.subheader("Job Description")
    job_desc = st.text_area("Paste the Job Description here")

    submitted = st.form_submit_button("Generate Resume")

# ------------------- AI Resume Generation -------------------
if submitted:
    # Convert inputs into a human-readable plain text format
    plain_text_resume_data = f"""
PERSONAL INFORMATION
Name: {name}
Phone: {phone}
Email: {email}
Designation: {designation}
LinkedIn: {linkedin}
GitHub: {github}
Other Links: {other_links}

EDUCATION
Degree: {degree}
Institution: {institution}
Start Date: {edu_start_date}
End Date: {"Present" if edu_present else edu_end_date}
CGPA: {cgpa}

SKILLS
{', '.join([s.strip() for s in all_skills.split(",") if s.strip()])}

PROJECTS
""" + "\n".join(
        [
            f"- {p['title']} ({p['start_date']} to {'Present' if p['present'] else p['end_date']}): {p['description']}"
            for p in st.session_state.projects if p["title"].strip()
        ]
    ) + "\n\nEXPERIENCE\n" + "\n".join(
        [
            f"- {e['title']} ({e['start_date']} to {'Present' if e['present'] else e['end_date']}): {e['description']}"
            for e in st.session_state.experiences if e["title"].strip()
        ]
    ) + f"""

JOB DESCRIPTION
{job_desc}
"""

    st.info("⏳ Generating resume with AI...")

    try:
        # Call the LLM with structured output
        model_with_structure = model.with_structured_output(ResumeData)
        response = model_with_structure.invoke(
            SYSTEM_PROMPT_TEMPLATE.format(resume_data=plain_text_resume_data)
        )

        # Validate and display
        st.success("✅ AI Response Generated Successfully!")
        st.json(response.model_dump())  # ✅ Fixed for Pydantic v2

    except ValidationError as ve:
        st.error(f"Validation Error: {ve}")
    except Exception as e:
        st.error(f"Error: {e}")
