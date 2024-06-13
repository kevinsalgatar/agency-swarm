from agency_swarm.tools import BaseTool
from pydantic import Field
from typing import Dict, Any
import logging

class GenerateJobDescriptionTool(BaseTool):
    """
    Tool to generate an attractive job description based on company and job details.
    The tool formats the input data into a compelling job description.
    """
    company_details: Dict[str, Any] = Field(..., description="The details of the company.")
    job_details: Dict[str, Any] = Field(..., description="The details of the job.")

    def run(self) -> str:
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method formats the company and job details into an attractive job description.
        """
        try:
            # Ensure all required fields are present
            if not all(key in self.company_details for key in ["name", "description", "values"]):
                raise ValueError("Missing required company details.")
            if not all(key in self.job_details for key in ["title", "location", "requirements", "responsibilities"]):
                raise ValueError("Missing required job details.")
            
            # Extract relevant details from the input data
            company_name = self.company_details["name"]
            company_description = self.company_details["description"]
            company_values = self.company_details["values"]
            job_title = self.job_details["title"]
            job_location = self.job_details["location"]
            job_requirements = self.job_details["requirements"]
            job_responsibilities = self.job_details["responsibilities"]
            
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
            Join {company_name} and be part of a dynamic team that values {company_values}.
            """

            logging.info("Job description generated successfully.")

            return job_description.strip()

        except ValueError as e:
            logging.error(f"Validation error: {e}")
            return f"Validation error: {str(e)}"
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
