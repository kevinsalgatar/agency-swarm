from agency_swarm.tools import BaseTool
from pydantic import Field
from typing import Dict
import logging

class GenerateJobDescriptionTool(BaseTool):
    """
    Tool to generate an attractive job description based on company and job details.
    The tool formats the input data into a compelling job description.
    """
    company_details: Dict = Field(..., description="The details of the company.")
    job_details: Dict = Field(..., description="The details of the job.")

    def run(self) -> str:
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method formats the company and job details into an attractive job description.
        """
        try:
            # Extract relevant details from the input data
            company_name = self.company_details.get("name", "Company Name")
            company_description = self.company_details.get("description", "Company Description")
            job_title = self.job_details.get("title", "Job Title")
            job_location = self.job_details.get("location", "Job Location")
            job_requirements = self.job_details.get("requirements", "Job Requirements")
            job_responsibilities = self.job_details.get("responsibilities", "Job Responsibilities")
            
            logging.info("Generating job description based on provided company and job details.")

            # Format the job description
            job_description = f"""
            **{job_title} at {company_name}**

            **Location:** {job_location}

            **Company Overview:**
            {company_description}

            **Job Responsibilities:**
            {job_responsibilities}

            **Job Requirements:**
            {job_requirements}

            **Why Join Us?**
            Join {company_name} and be part of a dynamic team that values {self.company_details.get("values", "our values and culture")}.
            """

            logging.info("Job description generated successfully.")

            return job_description.strip()

        except Exception as e:
            logging.error(f"Error generating job description: {e}")
            return f"Error generating job description: {str(e)}"

# Example usage
if __name__ == "__main__":
    company_details = {
        "name": "TalentVibes",
        "description": "TalentVibes is a leading company in talent management solutions.",
        "values": "innovation, integrity, and teamwork"
    }
    job_details = {
        "title": "Software Engineer",
        "location": "Remote",
        "requirements": "Experience with Python and REST APIs. Knowledge of cloud services.",
        "responsibilities": "Develop and maintain web applications. Collaborate with cross-functional teams."
    }
    tool = GenerateJobDescriptionTool(company_details=company_details, job_details=job_details)
    result = tool.run()
    print(result)
