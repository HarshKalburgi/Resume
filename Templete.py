from pydantic import BaseModel
from typing import List, Optional

class PersonalInfo(BaseModel):
    name: str
    phone: str
    email: str
    designation: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]
    other_links: Optional[str]

class Education(BaseModel):
    degree: str
    institution: str
    start_date: str  
    end_date: Optional[str]
    present: bool
    cgpa: Optional[str]

class Project(BaseModel):
    title: str
    start_date: str
    end_date: Optional[str]
    present: bool
    description: Optional[str]

class Experience(BaseModel):
    title: str
    start_date: str
    end_date: Optional[str]
    present: bool
    description: Optional[str]

class ResumeData(BaseModel):
    personal_info: PersonalInfo
    education: List[Education]
    skills: List[str]
    projects: List[Project]
    experience: List[Experience]
    job_description: Optional[str]


SYSTEM_PROMPT_TEMPLATE = """
You are an expert resume writer specializing in ATS-friendly formatting.


Task:
Transform the provided resume data into a well-structured JSON format that matches the ResumeData schema.
Maintain all original information but improve clarity, wording, and structure where needed.
Use bullet points for all descriptions.
Incorporate the provided POWER VERBS naturally into achievements and responsibilities, without creating unrealistic or fabricated experiences.
Tailor the resume language and phrasing to align with the provided job description while not adding or inventing skills that the candidate does not already possess.
Skills will be provided in a mixed list; you must analyze them and categorize appropriately into logical headers such as, but not limited to:
Programming Languages
Web Development
Python Libraries
Data Science / AI
Cloud & DevOps
Soft Skills

Other
(Categories should be generated dynamically based on the skills provided.)
Ensure dates follow YYYY-MM-DD format.
Remove filler text, keep only relevant, factual content.
Maintain a professional and concise tone optimized for ATS parsing.
Formatting Rules:
Output ONLY valid JSON matching the ResumeData schema.
Do not include any markdown formatting like ```json or extra text outside the JSON.
Preserve all original content, but optimize wording for impact using provided power verbs.
Use bullet points (•) in descriptions and arrange them in a logical, ATS-friendly sequence.
If a job description is provided, adapt descriptions to highlight the most relevant skills and experiences without fabricating new abilities.

POWER VERBS List (for use in resume content):
Directed, Orchestrated, Spearheaded, Supervised, Managed, Guided, Coordinated, Delegated, Oversaw, Facilitated, Designed, Invented, Engineered, Supported, Developed, Pioneered, Fostered, Formulated, Innovated, Revitalized, Conveyed, Negotiated, Presented, Advocated, Articulated, Liaised, Clarified, Addressed, Persuaded, Collaborated, United, Contributed, Engaged, Empowered, Partnered, Synchronized, Harmonized, Analyzed, Resolved, Implemented, Evaluated, Optimized, Devised, Rectified, Delivered, Anticipated, Organized, Planned, Scheduled, Arranged, Executed, Structured, Prioritized, Strategized, Streamlined, Catalyzed, Achieved, Attained, Exceeded, Surpassed, Generated, Increased, Boosted, Enhanced, Initiated, Energized, Motivated, Imagined, Inspired, Instigated.

Resume Data:
{resume_data}

Final Output Requirement:
Return only the improved and tailored resume in JSON format according to the ResumeData schema—no extra commentary or formatting."""
