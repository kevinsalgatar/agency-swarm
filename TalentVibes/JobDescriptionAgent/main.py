from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from tools.JobDescriptionTool import JobDescriptionTool
from tools.TagGenerationTool import TagGenerationTool
from tools.PostApiTool import PostApiTool
import logging

app = FastAPI()

# In-memory storage for job descriptions and tags
database = {
    "job_descriptions": [],
    "tags": []
}

# Pydantic models for request and response
class JobDescriptionRequest(BaseModel):
    company_profile_url: str
    job_details_url: str
    bearer_token: str

class JobDescriptionResponse(BaseModel):
    description: str
    tags: List[Dict[str, List[str]]]

class TagGenerationRequest(BaseModel):
    job_description: str

class TagGenerationResponse(BaseModel):
    tags: List[Dict[str, List[str]]]

class PostJobRequest(BaseModel):
    job_description: str
    tags: List[Dict[str, List[str]]]
    api_endpoint: str
    bearer_token: str

class PostJobResponse(BaseModel):
    result: dict

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get ("/")
def root():
    return {"message": "Hello, please visit /docs to see the API documentation."}

@app.post("/generate-job-description/", response_model=JobDescriptionResponse)
def generate_job_description(request: JobDescriptionRequest):
    try:
        logger.info("Generating job description...")
        
        # Generate job description
        job_description_tool = JobDescriptionTool(
            company_profile_url=request.company_profile_url,
            job_details_url=request.job_details_url,
            bearer_token=request.bearer_token
        )
        job_description = job_description_tool.run()
        logger.info(f"Job description generated: {job_description}")
        
        # Generate tags
        tag_tool = TagGenerationTool(job_description=job_description)
        tags = tag_tool.run()
        logger.info(f"Tags generated: {tags}")
        
        # Store in in-memory database
        database["job_descriptions"].append(job_description)
        database["tags"].append(tags)
        
        return JobDescriptionResponse(description=job_description, tags=tags)
    except Exception as e:
        logger.error(f"Error generating job description: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/post-job/", response_model=PostJobResponse)
def post_job(request: PostJobRequest):
    try:
        logger.info("Posting job...")
        
        # Post job description and tags
        post_tool = PostApiTool(
            job_description=request.job_description,
            tags=request.tags,
            api_endpoint=request.api_endpoint,
            bearer_token=request.bearer_token
        )
        result = post_tool.run()
        logger.info(f"Job posted with result: {result}")
        
        return PostJobResponse(result=result)
    except Exception as e:
        logger.error(f"Error posting job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs/", response_model=List[JobDescriptionResponse])
def get_jobs():
    try:
        logger.info("Fetching all jobs...")
        
        jobs = []
        for desc, tags in zip(database["job_descriptions"], database["tags"]):
            jobs.append(JobDescriptionResponse(description=desc, tags=tags))
        
        logger.info(f"Jobs fetched: {jobs}")
        return jobs
    except Exception as e:
        logger.error(f"Error fetching jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/job-descriptions/", response_model=List[str])
def get_job_descriptions():
    try:
        logger.info("Fetching job descriptions...")
        
        job_descriptions = database["job_descriptions"]
        logger.info(f"Job descriptions fetched: {job_descriptions}")
        
        return job_descriptions
    except Exception as e:
        logger.error(f"Error fetching job descriptions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tags/", response_model=List[Dict[str, List[str]]])
def get_tags():
    try:
        logger.info("Fetching tags...")
        
        tags = database["tags"]
        logger.info(f"Tags fetched: {tags}")
        
        return tags
    except Exception as e:
        logger.error(f"Error fetching tags: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
