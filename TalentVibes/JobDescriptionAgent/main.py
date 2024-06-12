from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
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
