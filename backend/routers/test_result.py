from fastapi import APIRouter

# Import the model so it gets registered in SQLModel.metadata
from models.test_result import TestResult  # noqa: F401

router = APIRouter(
    prefix="/testresult",
    tags=["testresults"],
)

# Endpoints will be implemented later
