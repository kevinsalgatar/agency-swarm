from agency_swarm.tools import BaseTool
from pydantic import Field
import re
from collections import Counter

class GenerateKeywordTagsTool(BaseTool):
    """
    Generate an array of keyword tags from the job descriptions.
    """
    job_description: str = Field(..., description="The job description from which to generate keyword tags.")

    def run(self):
        """
        Generate keyword tags from the job description.
        """
        words = re.findall(r'\w+', self.job_description.lower())
        common_words = Counter(words).most_common(10)
        keywords = [word for word, count in common_words if len(word) > 3]
        
        return keywords
