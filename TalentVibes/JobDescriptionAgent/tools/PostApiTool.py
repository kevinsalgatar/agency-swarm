from agency_swarm.tools import BaseTool
from pydantic import Field
import requests

class PostApiTool(BaseTool):
    job_description: str = Field(..., description="The job description text to be posted.")
    tags: dict = Field(..., description="The tags associated with the job description.")
    api_endpoint: str = Field(..., description="The API endpoint URL to post the job description and tags.")
    bearer_token: str = Field(..., description="The Bearer token for API authentication.")

    def run(self):
        headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'job_description': self.job_description,
            'tags': self.tags
        }
        response = requests.post(self.api_endpoint, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
