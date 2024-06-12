from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from tools.FetchJobDetailsTool import FetchJobDetailsTool
from tools.FetchCompanyDataTool import FetchCompanyDataTool
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

class CompanyResponse(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    about: Optional[str] = None
    location: Optional[str] = None
    companyUrl: Optional[str] = None
    companyLogoUrl: Optional[str] = None
    companyBannerUrl: Optional[str] = None
    galleries: Optional[List[str]] = None

class Role(BaseModel):
    id: int
    name: str

class WorkingHour(BaseModel):
    id: int
    name: str

class ExperienceLevel(BaseModel):
    id: int
    name: str

class Currency(BaseModel):
    id: int
    name: str
    code: str

class PayPeriod(BaseModel):
    id: int
    name: str
    description: str

class WorkLocation(BaseModel):
    id: int
    name: str
    description: str

class JobData(BaseModel):
    id: int
    userId: int
    title: str
    industryTypeId: Optional[int] = None
    countryId: Optional[int] = None
    cityId: Optional[int] = None
    roleId: int
    workingHourId: int
    companyId: int
    currencyId: int
    minimumPay: int
    maximumPay: int
    payPeriodId: int
    workLocationId: int
    experienceLevelId: int
    roleDetails: str
    isActive: bool
    createdAt: str
    updatedAt: Optional[str] = None
    deletedAt: Optional[str] = None
    jobBoards: List[int]
    industryTypeName: Optional[str] = None
    clientName: Optional[str] = None
    archived: bool
    location: Optional[str] = None
    department: Optional[str] = None
    industryType: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    role: Role
    workingHour: WorkingHour
    experienceLevel: ExperienceLevel
    currency: Currency
    payPeriod: PayPeriod
    workLocation: WorkLocation

class JobResponse(BaseModel):
    data: JobData
    status: int

class JobDetailsRequest(BaseModel):
    job_details_url: str
    bearer_token: str
@app.get("/fetch-company-data", response_model=CompanyResponse)
async def fetch_company_data(company_url: str = Query(...), bearer_token: str = Query(...)):
    logging.info(f"Received request with company_url: {company_url} and bearer_token: {bearer_token}")

    fetch_tool = FetchCompanyDataTool(company_url=company_url, bearer_token=bearer_token)
    result = fetch_tool.run()
    
    logging.info(f"Fetched data: {result}")

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    try:
        # Extract the nested 'data' field
        data = result.get("data", {})

        # Log the extracted data for debugging purposes
        logging.info(f"Extracted data: {data}")

        company_response = CompanyResponse(
            id=data.get("id"),
            name=data.get("name"),
            about=data.get("about"),
            location=data.get("location"),
            companyUrl=data.get("companyUrl"),
            companyLogoUrl=data.get("companyLogoUrl"),
            companyBannerUrl=data.get("companyBannerUrl"),
            galleries=data.get("galleries", [])
        )
        return company_response
    except KeyError as e:
        logging.error(f"Missing key in response data: {e}")
        raise HTTPException(status_code=500, detail=f"Missing key in response data: {e}")
    except TypeError as e:
        logging.error(f"Type error in response data: {e}")
        raise HTTPException(status_code=500, detail=f"Type error in response data: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

@app.get("/fetch-job-details", response_model=JobResponse)
async def fetch_job_details(job_details_url: str = Query(...), bearer_token: str = Query(...)):
    logging.info(f"Received request with job_details_url: {job_details_url} and bearer_token: {bearer_token}")

    fetch_tool = FetchJobDetailsTool(job_url=job_details_url, bearer_token=bearer_token)
    result = fetch_tool.run()
    
    logging.info(f"Fetched data: {result}")

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    try:
        job_response = JobResponse(data=result.get("data"), status=result.get("status", 200))
        return job_response
    except KeyError as e:
        logging.error(f"Missing key in response data: {e}")
        raise HTTPException(status_code=500, detail=f"Missing key in response data: {e}")
    except TypeError as e:
        logging.error(f"Type error in response data: {e}")
        raise HTTPException(status_code=500, detail=f"Type error in response data: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")