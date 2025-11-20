from pydantic import BaseModel, Field

class JobRequest(BaseModel):
    company_name: str
    address: str
    months: int = Field(ge=1, le=24)
