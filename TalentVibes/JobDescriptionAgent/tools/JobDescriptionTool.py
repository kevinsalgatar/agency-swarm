import requests
from agency_swarm.tools import BaseTool
from pydantic import Field

class JobDescriptionTool(BaseTool):
    company_profile_url: str = Field(..., description="The API endpoint URL to fetch the company profile.")
    job_details_url: str = Field(..., description="The API endpoint URL to fetch the job details.")
    bearer_token: str = Field(..., description="The Bearer token for API authentication.")

    def fetch_data(self, url):
        headers = {'Authorization': f'Bearer {self.bearer_token}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def run(self):
        company_profile = self.fetch_data(self.company_profile_url)
        job_details = self.fetch_data(self.job_details_url)
        
        company_name = company_profile.get('name', 'Company')
        company_description = company_profile.get('description', 'Company description not available.')
        company_culture = company_profile.get('culture', 'Details about company culture not available.')
        company_benefits = company_profile.get('benefits', 'Details about company benefits not available.')
        career_growth = company_profile.get('career_growth', 'Details about career growth opportunities not available.')

        job_title = job_details.get('title', 'Job Title')
        salary = job_details.get('salary', 'Salary not specified')
        employment_type = job_details.get('employment_type', 'Employment type not specified')
        location = job_details.get('location', 'Location not specified')
        tasks = job_details.get('tasks', [])
        responsibilities = job_details.get('responsibilities', [])
        qualifications = job_details.get('qualifications', 'Qualifications not specified.')

        description = f"**Join {company_name} as a {job_title}!**\n\n"
        description += f"**Company Overview:**\n{company_description}\n\n"
        description += f"**Salary:** {salary}\n"
        description += f"**Employment Type:** {employment_type}\n"
        description += f"**Location:** {location}\n\n"
        description += f"**Key Tasks:**\n"
        for task in tasks:
            description += f"- {task}\n"
        description += f"\n**Responsibilities:**\n"
        for responsibility in responsibilities:
            description += f"- {responsibility}\n"
        description += f"\n**Qualifications:**\n{qualifications}\n"
        description += f"\n**Why You'll Love Working Here:**\n"
        description += f"{company_culture}\n\n"
        description += f"**Benefits:**\n"
        description += f"{company_benefits}\n\n"
        description += f"**Career Growth:**\n"
        description += f"{career_growth}\n"
        
        return description
