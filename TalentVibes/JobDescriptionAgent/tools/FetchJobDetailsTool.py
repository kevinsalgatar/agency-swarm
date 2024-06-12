from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import logging
from typing import Dict

class FetchJobDetailsTool(BaseTool):
    """
    Tool to fetch job details from the source API.
    The tool sends a GET request to the job details API and returns the processed response data.
    """
    job_url: str = Field(..., description="The URL of the job details API.")
    bearer_token: str = Field(..., description="The bearer token for authorization.")

    def run(self) -> Dict:
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method sends a GET request to the job details API and processes the response.
        """
        # Prepare headers for the request
        headers = {
            "Authorization": f"Bearer {self.bearer_token}"
        }
        
        logging.info(f"Making request to {self.job_url} with bearer token.")

        try:
            # Make the GET request to the job details API
            response = requests.get(self.job_url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the JSON response
            response_data = response.json()

            logging.info(f"Received response: {response_data}")

            # Handle any potential errors in the response
            if "detail" in response_data:
                return {"error": response_data["detail"]}
            
            # Return the processed data
            return response_data
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception: {e}")
            return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    tool = FetchJobDetailsTool(job_url="https://dev-api.talentvibes.io/api/job/admin/107", bearer_token="your_bearer_token")
    result = tool.run()
    print(result)
