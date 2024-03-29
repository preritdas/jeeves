"""Protected API access to a userless Jeeves base agent."""
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from jeeves.agency import generate_base_agent_response
from keys import KEYS


router = APIRouter()


class IncorrectPasswordError(Exception):
    """
    Raised when the password is incorrect. Not implemented as a JSON error response
    is given back to the requestor. 
    """

    def __init__(self, failed_pwd: str) -> None:
        super().__init__(f"Password {failed_pwd} is incorrect.")


class BaseAgentJob(BaseModel):
    """Protected payload for a base model job."""
    password: str
    query: str


class BaseAgentResponse(BaseModel):
    """Protected response for a base model job."""
    response: str


@router.post("/run")
async def base_agent(job: BaseAgentJob) -> BaseAgentResponse:
    """Run a base agent job."""
    # Check the password
    if job.password != KEYS.General.base_agent_password:
        raise HTTPException(
            status_code=401, 
            detail=f"Incorrect password: {job.password}."
        )

    return BaseAgentResponse(response=generate_base_agent_response(job.query))
