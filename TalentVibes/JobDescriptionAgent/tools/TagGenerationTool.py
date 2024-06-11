# JobDescriptionAgent/tools/TagGenerationTool.py
from pydantic import Field
import spacy
import re
from sentence_transformers import SentenceTransformer, util

from agency_swarm.tools import BaseTool

nlp = spacy.load('en_core_web_sm')
model = SentenceTransformer('all-MiniLM-L6-v2')

class TagGenerationTool(BaseTool):
    job_description: str = Field(..., description="The job description text to be parsed.")

    # Initialization of skills_list
    def __init__(self, **data):
        super().__init__(**data)
        self.skills_list = []  # Initialize an in-memory list of skills

    def is_duplicate(self, new_skill):
        new_skill_embedding = model.encode(new_skill, convert_to_tensor=True)
        for existing_skill in self.skills_list:
            existing_skill_embedding = model.encode(existing_skill, convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(new_skill_embedding, existing_skill_embedding)
            if similarity.item() > 0.8:  # Threshold for similarity
                return True
        return False

    def filter_skills(self, new_skills):
        filtered_skills = []
        for skill in new_skills:
            if not self.is_duplicate(skill):
                filtered_skills.append(skill)
        return filtered_skills

    def run(self):
        doc = nlp(self.job_description)
        
        tags = {
            "Job Title": [],
            "Skills": [],
            "Experience Level": [],
            "Location": [],
            "Industry": [],
            "Education": [],
            "Job Type": [],
            "Certifications": [],
            "Salary Range": [],
            "Language Proficiency": [],
            "Company Size": [],
            "Work Authorization": [],
            "Keywords": [],
            "Job Functions": [],
            "Soft Skills": []
        }

        # Patterns for specific tag extraction
        salary_pattern = re.compile(r"\$\d+(?:,\d{3})*(?:\.\d+)?-\$\d+(?:,\d{3})*(?:\.\d+)?")

        # Named Entity Recognition and other extraction logic
        for ent in doc.ents:
            if ent.label_ in ["ORG"]:
                tags["Company Size"].append(ent.text)
            elif ent.label_ in ["GPE", "LOC"]:
                tags["Location"].append(ent.text)
            elif ent.label_ in ["PERSON", "PRODUCT"]:
                tags["Job Title"].append(ent.text)
            elif ent.label_ in ["DATE"]:
                tags["Experience Level"].append(ent.text)
            elif ent.label_ in ["MONEY"]:
                tags["Salary Range"].append(ent.text)
            elif ent.label_ in ["CARDINAL"]:
                tags["Experience Level"].append(ent.text)
            elif ent.label_ in ["NORP", "FAC"]:
                tags["Industry"].append(ent.text)
            elif ent.label_ in ["LANGUAGE"]:
                tags["Language Proficiency"].append(ent.text)
            else:
                tags["Keywords"].append(ent.text)

        new_skills = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
        filtered_skills = self.filter_skills(new_skills)

        for skill in filtered_skills:
            tags["Skills"].append(skill)

        for chunk in doc.noun_chunks:
            tags["Job Functions"].append(chunk.text)

        # Update the skills list in memory
        self.skills_list.extend(filtered_skills)
        self.skills_list = list(set(self.skills_list))  # Ensure no duplicates

        # Convert tags dictionary to a JSON array format
        json_array = [{"category": category, "tags": tags_list} for category, tags_list in tags.items()]
        
        return json_array
