import streamlit as st
import os
from datetime import date
from configuration.config_manager import LLMFactory
from Templete import SYSTEM_PROMPT_TEMPLATE
from conveter import Converter

# Create .tmp directory if it doesn't exist
os.makedirs('.tmp', exist_ok=True)

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
    # Prepare the resume data in a clean format for the LLM
    resume_data = {
        "personal_information": {
            "name": name,
            "phone": phone,
            "email": email,
            "designation": designation,
            "linkedin": linkedin,
            "github": github,
            "other_links": [link.strip() for link in other_links.split(",") if link.strip()]
        },
        "education": {
            "degree": degree,
            "institution": institution,
            "start_date": edu_start_date.strftime("%Y-%m-%d") if edu_start_date else "",
            "end_date": "Present" if edu_present else (edu_end_date.strftime("%Y-%m-%d") if edu_end_date else ""),
            "cgpa": cgpa
        },
        "skills": [s.strip() for s in all_skills.split(",") if s.strip()],
        "projects": [
            {
                "title": p["title"],
                "start_date": p["start_date"].strftime("%Y-%m-%d") if p["start_date"] else "",
                "end_date": "Present" if p["present"] else (p["end_date"].strftime("%Y-%m-%d") if p["end_date"] else ""),
                "description": p["description"]
            }
            for p in st.session_state.projects if p["title"].strip()
        ],
        "experience": [
            {
                "title": e["title"],
                "start_date": e["start_date"].strftime("%Y-%m-%d") if e["start_date"] else "",
                "end_date": "Present" if e["present"] else (e["end_date"].strftime("%Y-%m-%d") if e["end_date"] else ""),
                "description": e["description"]
            }
            for e in st.session_state.experiences if e["title"].strip()
        ],
        "job_description": job_desc
    }
    
    st.info("⏳ Generating resume with AI...")
    
    try:
        # Format the resume data as a clean string for the LLM
        formatted_resume = ""
        
        # Personal Information
        personal = resume_data["personal_information"]
        formatted_resume += f"PERSONAL INFORMATION\nName: {personal['name']}\n"
        if personal['phone']:
            formatted_resume += f"Phone: {personal['phone']}\n"
        if personal['email']:
            formatted_resume += f"Email: {personal['email']}\n"
        if personal['designation']:
            formatted_resume += f"Designation: {personal['designation']}\n"
        if personal['linkedin']:
            formatted_resume += f"LinkedIn: {personal['linkedin']}\n"
        if personal['github']:
            formatted_resume += f"GitHub: {personal['github']}\n"
        if personal['other_links']:
            formatted_resume += f"Other Links: {', '.join(personal['other_links'])}\n"
        
        # Education
        edu = resume_data["education"]
        formatted_resume += "\nEDUCATION\n"
        if edu['degree'] or edu['institution']:
            if edu['degree']:
                formatted_resume += f"Degree: {edu['degree']}\n"
            if edu['institution']:
                formatted_resume += f"Institution: {edu['institution']}\n"
            if edu['start_date']:
                formatted_resume += f"Period: {edu['start_date']} to {edu['end_date']}\n"
            if edu['cgpa']:
                formatted_resume += f"CGPA: {edu['cgpa']}\n"
        # Skills
        if resume_data["skills"]:
            formatted_resume += "\nSKILLS\n"
            formatted_resume += ", ".join(resume_data["skills"]) + "\n"
        
        # Projects
        if resume_data["projects"]:
            formatted_resume += "\nPROJECTS\n"
            for proj in resume_data["projects"]:
                formatted_resume += f"\n{proj['title']}\n"
                if proj['start_date']:
                    formatted_resume += f"{proj['start_date']} to {proj['end_date']}\n"
                if proj['description']:
                    formatted_resume += f"{proj['description']}\n"
        
        # Experience
        if resume_data["experience"]:
            formatted_resume += "\nEXPERIENCE\n"
            for exp in resume_data["experience"]:
                formatted_resume += f"\n{exp['title']}\n"
                if exp['start_date']:
                    formatted_resume += f"{exp['start_date']} to {exp['end_date']}\n"
                if exp['description']:
                    formatted_resume += f"{exp['description']}\n"
        
        # Job Description
        if resume_data["job_description"]:
            formatted_resume += "\nJOB DESCRIPTION\n"
            formatted_resume += f"{resume_data['job_description']}\n"
        
        # Call the LLM with the formatted resume data
        response = model.invoke(
            SYSTEM_PROMPT_TEMPLATE.format(resume_data=formatted_resume)
        )
        
        # Convert AIMessage to string if needed
        response_content = response.content if hasattr(response, 'content') else str(response)
        
        # Save the AI-generated resume to a file
        output_file = os.path.join('.tmp', f"{name.replace(' ', '_')}_resume.md" if name else 'resume.md')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response_content)
        
        st.success(f"✅ AI-generated resume saved successfully to {output_file}!")
        
        # Save the AI-generated resume to a file
        output_md_file = os.path.join('.tmp', f"{name.replace(' ', '_')}_resume.md" if name else 'resume.md')
        with open(output_md_file, 'w', encoding='utf-8') as f:
            f.write(response_content)

        st.success(f"✅ AI-generated resume saved successfully to {output_md_file}!")

        # ------------------- Generate PDF -------------------
        try:
            output_pdf_file = output_md_file.replace(".md", ".pdf")
            Converter.md_to_pdf(output_md_file, output_pdf_file)
            st.success(f"📄 PDF successfully generated at {output_pdf_file}!")

            # Optionally let the user download it
            with open(output_pdf_file, "rb") as pdf_file:
                st.download_button(
                    label="⬇️ Download Resume as PDF",
                    data=pdf_file,
                    file_name=os.path.basename(output_pdf_file),
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"❌ Failed to generate PDF: {str(e)}")
            st.exception(e)

        # ------------------- Display the generated resume -------------------
        st.markdown("## Generated Resume Preview")
        st.markdown(response_content, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred while generating the resume: {str(e)}")
        st.exception(e)
